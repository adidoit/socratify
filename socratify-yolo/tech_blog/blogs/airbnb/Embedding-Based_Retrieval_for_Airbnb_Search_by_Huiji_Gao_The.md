---
title: "Embedding-Based Retrieval for Airbnb Search | by Huiji Gao | The Airbnb Tech Blog"
author: "Unknown"
url: "https://medium.com/airbnb-engineering/embedding-based-retrieval-for-airbnb-search-aabebfc85839?source=rss----53c7c27702d5---4"
date: "2025-09-15"
---

#**Embedding-Based Retrieval for Airbnb Search**

[![Huiji Gao](https://miro.medium.com/v2/resize:fill:64:64/1*QJBw9p2GFxG32ybruPxGMQ.jpeg)](/@huiji.gao?source=post_page---byline--aabebfc85839---------------------------------------)

[Huiji Gao](/@huiji.gao?source=post_page---byline--aabebfc85839---------------------------------------)

7 min read

·

Mar 19, 2025

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2Faabebfc85839&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fembedding-based-retrieval-for-airbnb-search-aabebfc85839&user=Huiji+Gao&userId=a369b17211d6&source=---header_actions--aabebfc85839---------------------clap_footer------------------)

\--

10

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Faabebfc85839&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fembedding-based-retrieval-for-airbnb-search-aabebfc85839&source=---header_actions--aabebfc85839---------------------bookmark_footer------------------)

Listen

Share

Press enter or click to view image in full size

Our journey in applying embedding-based retrieval techniques to build an accurate and scalable candidate retrieval system for Airbnb Homes search

Authors: [Mustafa (Moose) Abdool](https://www.linkedin.com/in/mustafa-moose-abdool-8aab037a/), [Soumyadip Banerjee](https://www.linkedin.com/in/soumyadip-banerjee-75991b42/), [Karen Ouyang](https://www.linkedin.com/in/kouyang1/), [Do-Kyum Kim](https://www.linkedin.com/in/do-kyum-kim-9a810417/), [Moutupsi Paul](https://www.linkedin.com/in/moutupsi-paul/), [Xiaowei Liu](https://www.linkedin.com/in/xiaowei-liu-60415841/), [Bin Xu](https://www.linkedin.com/in/bin-xu-96253aa5/), [Tracy Yu](https://www.linkedin.com/in/tracy-xiaoxi-yu/), [Hui Gao](https://www.linkedin.com/in/hui-gao-275a924/), [Yangbo Zhu](https://www.linkedin.com/in/yangbo-zhu/), [Huiji Gao](https://www.linkedin.com/in/huiji-gao/), [Liwei He](https://www.linkedin.com/in/liweihe/), [Sanjeev Katariya](https://www.linkedin.com/in/sanjeevkatariya/)

## Introduction

Search plays a crucial role in helping Airbnb guests find the perfect stay. The goal of Airbnb Search is to surface the most relevant listings for each user’s query — but with millions of available homes, that’s no easy task. It’s especially difficult when searches include large geographic areas (like California or France) or high-demand destinations (like Paris or London). Recent innovations — such as _flexible date search_ , which allows guests to explore stays without fixed check-in and check-out dates — have added yet another layer of complexity to ranking and finding the right results.

To tackle these challenges, we need a system that can retrieve relevant homes while also being scalable enough (in terms of latency and compute) to handle queries with a large candidate count. In this blog post, we share our journey in building Airbnb’s first-ever Embedding-Based Retrieval (EBR) search system. The goal of this system is to narrow down the initial set of eligible homes into a smaller pool, which can then be scored by more compute-intensive machine learning models later in the search ranking process.

Press enter or click to view image in full size

**Figure 1:**The general stages and scale for the various types of ranking models used in Airbnb Search

We’ll explore three key challenges in building this EBR system: (1) constructing training data, (2) designing the model architecture, and (3) developing an online serving strategy using Approximate Nearest Neighbor (ANN) solutions.

## Training Data Construction

The first step in building our EBR system was training a machine learning model to map both homes and de-identified search queries into numerical vectors. To achieve this, we built a training data pipeline (Figure 3) that leveraged contrastive learning — a strategy that involves identifying pairs of positive- and negative-labeled homes for a given query. During training, the model learns to map a query, a positive home, and a negative home into a numerical vector, such that the similarity between the query and the positive home is much higher than the similarity between the query and the negative home.

To construct these pairs, we devised a sampling method based on user trips. This was an important design decision, since users on Airbnb generally undergo a multi-stage search journey. Data shows that before making a final booking, users tend to perform multiple searches and take various actions — such as clicking into a home’s details, reading reviews, or adding a home to a wishlist. As such, it was crucial to develop a strategy that captures this entire multi-stage journey and accounts for the diverse types of listings a user might explore.

Diving deeper, we first grouped all historical queries of users who made bookings, using key query parameters such as location, number of guests, and length of stay — our definition of a “trip.” For each trip, we analyzed all searches performed by the user, with the final booked listing as the positive label. To construct (positive, negative) pairs, we paired this booked listing with other homes the user had seen but not booked. Negative labels were selected from homes the user encountered in search results, along with those they had interacted with more intentfully — such as by wishlisting — but ultimately did not book. This choice of negative labels was key: Randomly sampling homes made the problem too easy and resulted in poor model performance.

Press enter or click to view image in full size

**Figure 2:**Example of constructing (positive, negative) pairs for a given user journey. The booked home is always treated as a positive. Negatives are selected from homes that appeared in the search result (and were potentially interacted with) but that the user did not end up booking.

**Figure 3:**Example of overall data pipeline used to construct training data for the EBR model.

## Model Architecture

The model architecture followed a traditional two-tower network design. One tower (the _listing tower_) processes features about the home listing itself — such as historical engagement, amenities, and guest capacity. The other tower (the _query tower_) processes features related to the search query — such as the geographic search location, number of guests, and length of stay. Together, these towers generate the embeddings for home listings and search queries, respectively.

A key design decision here was choosing features such that the listing tower could be computed offline on a daily basis. This enabled us to pre-compute the home embeddings in a daily batch job, significantly reducing online latency, since only the query tower had to be evaluated in real-time for incoming search requests.

Press enter or click to view image in full size

**Figure 4:**Two-tower architecture as used in the EBR model. Note that the listing tower is computed offline daily for all homes.

## Online Serving

The final step in building our EBR system was choosing the infrastructure for online serving. We explored a number of approximate nearest neighbor (ANN) solutions and narrowed them down to two main candidates: inverted file index (IVF) and hierarchical navigable small worlds (HNSW). While HNSW performed slightly better in terms of evaluation metrics — using recall as our main evaluation metric — we ultimately found that IVF offered the best trade-off between speed and performance.

The core reason for this is the high volume of real-time updates per second for Airbnb home listings, as pricing and availability data is frequently updated. This caused the memory footprint of the HNSW index to grow too large. In addition, most Airbnb searches include filters, especially geographic filters. We found that parallel retrieval with HNSW alongside filters resulted in poor latency performance.

In contrast, the IVF solution, where listings are clustered beforehand, only required storing cluster centroids and cluster assignments within our search index. At serving time, we simply retrieve listings from the top clusters by treating the cluster assignments as a standard search filter, making integration with our existing search system quite straightforward.

**Figure 5:**Overall serving flow using IVF. Homes are clustered beforehand and, during online serving, homes are retrieved from the closest clusters to the query embedding.

In this approach, our choice of similarity function in the EBR model itself ended up having interesting implications. We explored both dot product and Euclidean distance; while both performed similarly from a model perspective, using Euclidean distance produced much more balanced clusters on average. This was a key insight, as the quality of IVF retrieval is highly sensitive to cluster size uniformity: If one cluster had too many homes, it would greatly reduce the discriminative power of our retrieval system.

We hypothesize that this imbalance arises with dot product similarity because it inherently only considers the direction of feature vectors while ignoring their magnitudes — whereas many of our underlying features are based on historical counts, making magnitude an important factor.

Press enter or click to view image in full size

**Figure 6:**Example of the distribution of cluster sizes when using dot product vs. Euclidean distance as a similarity measure. We found that Euclidean distance produced much more balanced cluster sizes.

## Results

The EBR system described in this post was fully launched in both Search and Email Marketing production and led to a statistically-significant gain in overall bookings when A/B tested. Notably, the bookings lift from this new retrieval system was on par with some of the largest machine learning improvements to our search ranking in the past two years.

The key improvement over the baseline was that our EBR system effectively incorporated query context, allowing homes to be ranked more accurately during retrieval. This ultimately helped us display more relevant results to users, especially for queries with a high number of eligible results.

## Acknowledgments

We would like to especially thank the entire Search and Knowledge Infrastructure & ML Infrastructure org (led by [Yi Li](https://www.linkedin.com/in/yi-li-755a6b24/)) and Marketing Technology org (led by [Michael Kinoti](https://www.linkedin.com/in/michael-kinoti-7a309215/)) for their great collaborations throughout this project!
