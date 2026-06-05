import re
import pandas as pd
from googleapiclient.discovery import build
from transformers import pipeline

import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

classifier = pipeline(
    "text-classification",
    model="cardiffnlp/twitter-roberta-base-sentiment-latest"
)

def run_analysis(video_id):

    youtube = build(
        "youtube",
        "v3",
        developerKey=API_KEY
    )

    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )
    response = request.execute()

    while request:
        for item in response["items"]:
            comment_data = item["snippet"]["topLevelComment"]["snippet"]
            replies = item["snippet"]["totalReplyCount"]
            formatted_date = pd.to_datetime(comment_data["publishedAt"]).strftime("%m/%d/%Y")

            comments.append([
                comment_data["textOriginal"],
                comment_data["likeCount"],
                replies,
                formatted_date
            ])

        request = youtube.commentThreads().list_next(request, response)
        if request:
            response = request.execute()

    df_raw = pd.DataFrame(comments, columns=["comment","likes","replies","date"])

    def extract_timestamp(comment):
        pattern = r'(?<!\d)(\d{1,2}:\d{2}(?::\d{2})?)(?!\d)'
        match = re.search(pattern, comment)
        if match:
            timestamp = match.group(1)
            for w in ["am","pm","mst","est","utc"]:
                if timestamp + " " + w in comment.lower():
                    return None
            return timestamp
        return None

    df_raw["timestamp"] = df_raw["comment"].apply(extract_timestamp)
    df_extracted = df_raw.dropna(subset=["timestamp"]).copy()

    def timestamp_to_seconds(t):
        p = t.split(":")
        if len(p)==2:
            return int(p[0])*60+int(p[1])
        if len(p)==3:
            return int(p[0])*3600+int(p[1])*60+int(p[2])
        return 0

    df_extracted["seconds"] = df_extracted["timestamp"].apply(timestamp_to_seconds)

    def clean_comment(t):
        t = t.lower()
        t = re.sub(r'http\S+','',t)
        t = re.sub(r'\b\d{1,2}:\d{2}(?::\d{2})?\b','',t)
        t = re.sub(r'\s+',' ',t).strip()
        return t

    df_cleaned = df_extracted.copy()
    df_cleaned["clean_comment"] = df_cleaned["comment"].apply(clean_comment)
    df_cleaned = df_cleaned[df_cleaned["clean_comment"].str.len()>2]
    df_cleaned = df_cleaned.drop_duplicates(subset=["clean_comment"])
    df_cleaned = df_cleaned[df_cleaned["clean_comment"].str.len()<500]
    df_cleaned = df_cleaned[df_cleaned["clean_comment"].str.split().str.len()>=2]

    df_cleaned["weight"] = df_cleaned["likes"]*2 + df_cleaned["replies"]*3
    df_cleaned = df_cleaned.sort_values(by="weight",ascending=False)

    def predict_sentiment(t):
        r = classifier(t,truncation=True,max_length=512)[0]
        return pd.Series([r["label"].lower(),r["score"]])

    df_model = df_cleaned.copy()
    df_model[["label","confidence"]] = df_model["clean_comment"].apply(predict_sentiment)
    df_model["confidence"] = df_model["confidence"].round(2)

    sentiment_map = {"positive":1,"neutral":0,"negative":-1}
    df_model["sentiment_score"] = df_model["label"].map(sentiment_map)
    df_model["segment"] = (df_model["seconds"]//30).astype(int)

    timestamp_counts = df_model["timestamp"].value_counts().head(10)

    peak_data = df_model.groupby("segment").agg({
        "comment":"count",
        "likes":"sum",
        "replies":"sum",
        "sentiment_score":"mean"
    }).reset_index()

    peak_data.columns = ["segment","comment_count","total_likes","total_replies","avg_sentiment"]
    peak_data["start_second"] = peak_data["segment"]*30
    peak_data["end_second"] = peak_data["start_second"]+29

    def time(s):
        return f"{s//60:02d}:{s%60:02d}"

    peak_data["time_range"] = peak_data["start_second"].apply(time)+" - "+peak_data["end_second"].apply(time)

    peak_data["peak_score"] = (
        peak_data["comment_count"]*3 +
        peak_data["total_likes"]*2 +
        peak_data["total_replies"]*3 +
        abs(peak_data["avg_sentiment"])*10
    )

    peak_data = peak_data.sort_values(by="peak_score",ascending=False)
    peak_data["avg_sentiment"] = peak_data["avg_sentiment"].round(2)
    peak_data["peak_score"] = peak_data["peak_score"].round().astype(int)

    return df_raw,df_cleaned,df_model,peak_data,timestamp_counts