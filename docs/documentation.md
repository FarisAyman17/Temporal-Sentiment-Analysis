# Temporal Sentiment Analysis for YouTube Highlights

---

# Title Page & Authors

## Temporal Sentiment Analysis for YouTube Highlights

### Authors

- Faris Ayman – 202210206


### Supervised by

Husam Barham

### Course

20252 – Graduation Project

### Semester

second Semester, 2025/2026

### Submission Date

[8\6\2026]

---

# Table of Contents

1. [Abstract](#abstract)
2. [Acknowledgment](#acknowledgment)
3. [Business Intelligence Project Description and Objectives](#business-intelligence-project-description-and-objectives)
4. [Data Research and Acquiring Effort](#data-research-and-acquiring-effort)
5. [Data Description and Understanding](#data-description-and-understanding)
6. [Data Primary Cleaning and Transformation](#data-primary-cleaning-and-transformation)
7. [Data Visualization and Insights](#data-visualization-and-insights)
8. [Dashboard Design & Business Insights](#dashboard-design--business-insights)
9. [Advanced Analytics and AI Modeling](#advanced-analytics-and-ai-modeling)
10. [Tools Research and Selection Effort](#tools-research-and-selection-effort)
11. [Project Deployment Effort – Use Case](#project-deployment-effort--use-case)
12. [Results](#results)
13. [Limitations](#limitations)
14. [Future Work](#future-work)
15. [References](#references)
16. [Code Setup and Dependencies](#code-setup-and-dependencies)

---

# Abstract

The rapid growth of online video content has generated massive volumes of audience feedback in the form of comments, reactions, and discussions. While platforms such as YouTube provide traditional engagement metrics including views, likes, and watch time, they often fail to reveal which exact moments within a video captured audience attention and generated strong emotional responses. This project addresses this limitation by developing a Business Intelligence and Artificial Intelligence solution capable of identifying significant moments in YouTube videos through timestamp-based comment analysis.

The proposed system collects YouTube comments using the YouTube Data API v3, extracts timestamp references through pattern matching techniques, and performs sentiment analysis using a transformer-based Natural Language Processing model. Timestamp comments are grouped into temporal segments, enriched with engagement indicators such as likes and replies, and analyzed using a custom highlight-ranking algorithm. The processed data is presented through an interactive Streamlit dashboard designed to support exploratory analysis and decision making.

The results demonstrate that timestamp comments can serve as valuable indicators of audience attention and engagement. By combining sentiment analysis, engagement metrics, and temporal analytics, the system successfully identifies video highlights, measures audience reactions, and transforms unstructured social media data into actionable business insights. The developed solution provides value for content creators, digital marketers, media analysts, and researchers seeking a deeper understanding of audience behavior.

---

# Acknowledgment

We would like to express our sincere gratitude to our supervisor, **[Supervisor Name]**, for the continuous guidance, encouragement, and valuable feedback provided throughout the development of this graduation project.

We also extend our appreciation to the faculty members of the Computer Information Systems Department for the knowledge and support they provided during our academic journey. Their contributions have played a significant role in the successful completion of this work.

Finally, we would like to acknowledge Google for providing access to the YouTube Data API and the open-source community whose tools, libraries, and machine learning models made the implementation of this project possible.

---

# Business Intelligence Project Description and Objectives

## Project Description

Temporal Sentiment Analysis for YouTube Highlights is a Business Intelligence and Artificial Intelligence solution designed to analyze audience reactions and automatically identify the most engaging moments within YouTube videos.

The system leverages timestamp references embedded within audience comments to determine which moments viewers consider important, memorable, entertaining, educational, or controversial. These timestamp references are combined with sentiment analysis and engagement metrics to generate meaningful insights about audience behavior.

Unlike traditional analytics platforms that focus primarily on aggregate metrics such as views and watch time, this project provides moment-level intelligence by identifying the exact segments that generate audience attention and emotional reactions.

---

## Industry Domain

This project operates within several domains:

- Digital Media Analytics
- Social Media Intelligence
- Content Creation and Management
- Digital Marketing
- Business Intelligence
- Audience Behavior Analysis

---

## Business Problem

Content creators and organizations frequently receive thousands of comments on popular videos. Manually analyzing these comments presents several challenges:

- Significant time and effort are required.
- Important audience feedback can be overlooked.
- It is difficult to identify which moments generated the strongest reactions.
- Emotional responses are not easily measurable.
- Traditional analytics tools provide limited insight into moment-level engagement.

As a result, creators often struggle to understand which parts of their content resonate most strongly with viewers.

---

## Proposed Solution

The proposed solution automatically:

1. Collects comments from YouTube videos.
2. Detects timestamp references within comments.
3. Performs sentiment analysis on timestamp-related comments.
4. Measures engagement through likes and replies.
5. Groups reactions into temporal segments.
6. Calculates highlight scores for each segment.
7. Visualizes insights through an interactive dashboard.

---

## Project Objectives

The primary objectives of this project are:

### Objective 1: Timestamp Detection

Automatically extract timestamp references from audience comments.

### Objective 2: Audience Sentiment Analysis

Determine whether audience reactions are positive, neutral, or negative.

### Objective 3: Highlight Discovery

Identify the most engaging moments within a video.

### Objective 4: Engagement Measurement

Measure audience interaction through likes and replies.

### Objective 5: Business Intelligence Dashboard

Provide decision-makers with clear and interactive visualizations.

### Objective 6: Audience Behavior Understanding

Generate insights that help creators understand audience interests, preferences, and reactions.

---

## Expected Business Value

The developed system provides value for multiple stakeholders.

### Content Creators

- Discover video highlights automatically.
- Understand audience preferences.
- Improve future content strategy.

### Marketing Teams

- Identify highly engaging moments.
- Measure audience reactions to campaigns.

### Researchers

- Study collective audience behavior.
- Analyze sentiment patterns across content.

### Media Organizations

- Monitor public reaction to published content.
- Evaluate audience satisfaction and engagement.

---

## Success Criteria

The project is considered successful if it can:

- Accurately extract timestamp references.
- Correctly classify audience sentiment.
- Identify meaningful video highlights.
- Provide intuitive visualizations.
- Generate actionable Business Intelligence insights.

---


## Success Criteria

The project is considered successful if it can:

- Accurately extract timestamp references.
- Correctly classify audience sentiment.
- Identify meaningful video highlights.
- Provide intuitive visualizations.
- Generate actionable Business Intelligence insights.

---



