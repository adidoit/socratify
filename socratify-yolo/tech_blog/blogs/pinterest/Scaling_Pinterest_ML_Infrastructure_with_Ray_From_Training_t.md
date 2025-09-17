---
title: "Scaling Pinterest ML Infrastructure with Ray: From Training to End-to-End ML Pipelines | by Pinterest Engineering | Pinterest Engineering Blog"
author: "Unknown"
url: "https://medium.com/pinterest-engineering/scaling-pinterest-ml-infrastructure-with-ray-from-training-to-end-to-end-ml-pipelines-4038b9e837a0?source=rss----4c5a5f6279b6---4"
date: "2025-09-15"
---

# Scaling Pinterest ML Infrastructure with Ray: From Training to End-to-End ML Pipelines

[![Pinterest Engineering](https://miro.medium.com/v2/resize:fill:64:64/1*iAV-apeVpCJ1h6Znt1AzCg.jpeg)](/@Pinterest_Engineering?source=post_page---byline--4038b9e837a0---------------------------------------)

[Pinterest Engineering](/@Pinterest_Engineering?source=post_page---byline--4038b9e837a0---------------------------------------)

8 min read

·

Jun 24, 2025

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fpinterest-engineering%2F4038b9e837a0&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fpinterest-engineering%2Fscaling-pinterest-ml-infrastructure-with-ray-from-training-to-end-to-end-ml-pipelines-4038b9e837a0&user=Pinterest+Engineering&userId=ef81ef829bcb&source=---header_actions--4038b9e837a0---------------------clap_footer------------------)

\--

2

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2F4038b9e837a0&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fpinterest-engineering%2Fscaling-pinterest-ml-infrastructure-with-ray-from-training-to-end-to-end-ml-pipelines-4038b9e837a0&source=---header_actions--4038b9e837a0---------------------bookmark_footer------------------)

Listen

Share

Andrew Yu Staff Software Engineer / Jiahuan Liu Staff Software Engineer / Qingxian Lai Staff Software Engineer / Kritarth Anand Staff Software Engineer

## 1\. Introduction: Expanding Ray Beyond Training & Inference

At Pinterest, ML engineers continuously strive to optimize feature development, sampling strategies, and label experimentation. However, the traditional ML infrastructure was constrained by slow data pipelines, costly feature iterations, and inefficient compute usage.

While Ray has already transformed our training/batch inference workflows, we saw an opportunity to extend its capabilities to the entire ML infrastructure stack. This blog details how we expanded Ray’s role beyond training to feature development, sampling, and label modeling — ultimately making ML iteration at Pinterest faster, more efficient, and more scalable**.**

“Provide reliable and**efficient data platforms**and services at planet-scale to**accelerate innovation**and sustain our business” — ML foundation mission statement

## 2\. Challenges in Scaling ML Infrastructure

Before integrating Ray across our broader ML stack, we faced several key challenges:

### 2.1. Feature Development Bottlenecks

* Adding new features or testing algorithmic variations required days-long backfill jobs.
* Feature joins across multiple datasets were costly and slow due to Spark-based workflows.
* Experimenting with features at scale was limited by CPU and memory bottlenecks. Spark jobs are tedious to fine tune.

### 2.2. Inefficient Sampling Experiment

* Sampling was performed using dedicated Spark jobs, requiring intermediate storage and additional compute.
* The process lacked fine-tuning capabilities within the training loop.

### 2.3. Slow Labeling Experimentation

* Experimenting with different reward functions (a labeling technique)****involved high-latency batch workflows.
* Reward signal updates needed repeated full-dataset recomputations, inflating infrastructure costs.

To solve these challenges, we introduced a Ray-native ML infrastructure stack, focusing on four major improvements.

## 3\. Expanding Ray’s Role: Key Technical Innovations

To extend Ray’s role across our ML infrastructure, we introduced:

### 3.1. Building a Ray Data Native Pipeline API for ML Data Transformations

**Goal:**Develop functionalities to enable feature development, sampling, and label transformations natively in Ray, eliminating the need for Spark backfills.

**How:**

* We developed a Ray Data native transformation API for ML workflows.
* This API allows on-the-fly feature transformation inside the training pipeline, reducing preprocessing time.
* User code and data transformation are abstracted so they can be easily moved to any other data processing systems.

**Design:**

***Code Consolidation:**Consolidated common code across teams, e.g. the dataset readers for Iceberg and Parquet.
***Enhanced Functionalities**: Implemented Iceberg Bucket Joins and Bucket Writes in Ray, which will be discussed in the following sections.
***Cross-Platform Abstraction**: Abstracted data transformations can be run in serving systems or any other ML data processing framework such as Spark, PyTorch, Huggingface, etc.

Press enter or click to view image in full size

**Impact:**

* Main building block to extend Ray to E2E ML infra
* Lower maintain and onboarding cost to minimum

### 3.2. Efficient Data Joining with Iceberg Bucket Joins

**Goal:**Enable fast, efficient feature joins across different sources without precomputing large tables.

**How:**

* Implemented Iceberg bucket joins in Ray to dynamically join datasets at run time.
* This allows efficient merging of features and labels from multiple sources without offline preprocessing.

## System Components

Press enter or click to view image in full size

1.**File Resolver**: Maps files between main and side tables based on partitioning information. It understands bucket patterns and creates efficient matching between corresponding partitions, handling cases where tables have different bucket counts.
2.**Bucket Join Datasource**: Acts as a Ray datasource that creates read tasks for each partition. Each read task processes a complete partition by loading all relevant files from main and side tables for that partition.
3.**Joiner Implementations**: Multiple join strategies are available:
• TWO_STEP_CONCAT: Creates small index tables for efficiency, then performs data alignment.
• PANDAS: Uses pandas for flexibility but higher memory usage.
• CUSTOM: For customized joining.
4.**Partition Mapping System**: Handles different naming conventions between tables using a mapping dictionary, translating partition keys like “user_id” to “userId” across tables.

## Design Tradeoffs

1.**Memory vs. Computation Speed
• Tradeoff**: Each partition is processed as a complete unit, which increases memory usage but reduces computation overhead.
•**Decision**: Pinterest optimized for speed by processing entire partitions, delivering up to 10x faster iteration times while carefully sizing worker resources to prevent out-of-memory errors, particularly when using memory-intensive join methods.
2.**Flexibility vs. Overhead
• Tradeoff**: Supporting multiple join methods adds complexity but allows optimization for different data patterns.
**• Decision**: Pinterest implemented a flexible system with TWO_STEP_CONCAT as the default method, enabling teams to select the most appropriate strategy for their specific workloads and data characteristics, ultimately improving performance across diverse use cases.
3.**Data Movement vs. Storage Requirements
• Tradeoff**: Bucket joins leverage existing data partitioning, reducing data movement but requiring consistent bucketing across tables.
**• Decision**: Pinterest required tables to share compatible bucketing schemas with the same semantic partition keys (allowing different names through mapping), eliminating large-scale data movement while establishing standardized data organization patterns across their ML infrastructure.

**Impact:
**Eliminated the need for expensive pre-joining of data, allowing ML engineers to experiment with new features in hours rather than waiting days for traditional pipelines to complete.

## 3.3. Data Persistence for Efficient Iteration

**Goal:**The ability to write****transformed data that can be efficiently read by subsequent experimentations and production retrains.

**How:**

* Introduced Iceberg write mechanisms in Ray to store the transformed features as new features.
* Instead of recomputing feature transformations for every training iteration, Ray caches the features and reuses them when applicable.
* Once the feature transformation is ready to launch, the Ray-based data pipeline will be reused to set up production serving and training data generation.

**Design:**

Press enter or click to view image in full size

This design addresses two common challenges in ML development:

* After making modeling changes for the new features, it still requires many rounds of subsequent hyperparameter tuning to maximize the model improvement.
* New features need to be added to production training data after they are ready to launch. At Pinterest, this is through a [logging pipeline](/pinterest-engineering/training-foundation-improvements-for-closeup-recommendation-ranker-67d90603426e) that involves 5+ systems.

With the new design, the process of developing new features from ideation to launching will become:

* Development: Define the feature and implement a Ray-based data pipeline to generate it on-the-fly inside training jobs.
* Hyperparameter tuning: Store the new feature in S3 for persistence. All the subsequent training jobs will reuse the feature without having to recompute it. We added an Iceberg Bucket Write mechanism so the data can be read by Iceberg Bucket Joins efficiently.
* Production serving: Add configurations to commit the persisted new features to Galaxy, an in-house feature storage and serving system at Pinterest.
* Production retrain: Set up training data generation by reusing the feature transformation pipeline with a few lines of extra configurations. Add the new features to periodic retraining.

**Impact:**

Enable faster experimentation and hyperparameter tuning by avoiding redundant computation. Reduce the engineering efforts of end-to-end launching new features to production.

## 3.4. Ray Data Optimizations for Large Workloads

**Goal:**Accelerate large-scale ML workloads by optimizing Ray’s data processing capabilities.

**How:**

* Optimized Ray’s underlying data structure for faster access and processing.
* Introduced UDF & feature conversion level optimization for large datasets using Ray Data.

(This will be covered in detail in a future blog post, but we mention it here as an enabler of our approach.)

We have put significant effort to optimize data processing, and achieved 2–3X speedup across different pipelines. The optimization can be categorized into three categories: Ray Data, Feature Conversion and UDF efficiency.

1. Ray Data:

**a. Removing block slicing:**Ray internally enables block slicing by setting the target_max_block_size attribute of DataContext to avoid excessively large blocks. This incurs significant CPU and memory overhead.

**b. Remove combine_chunks:**The combine_chunks function within the batcher can cause unnecessary data copying. This function was originally a workaround to prevent slowness on following operations, as a single continuous chunk can perform better than discrete chunks. Chunk combination will be performed only when necessary in our pipeline, and many operations are optimized for single chunks, so we can operate on the list of chunks without combining them.

Press enter or click to view image in full size

2\. Feature conversion

**a. Deduplication by Request ID,**Within a given batch of training data, certain features will share the same value due to their common origin. This data duplication presents an opportunity for optimization. The primary trade-off lies in balancing the computational cost of deduplication against the potential savings in conversion time, network transfer, and GPU memory utilization.

Press enter or click to view image in full size

b. Redundant data copying and operations during pyarrow conversion can be avoided by implementing optimization on feature conversion, such as by avoiding null filling and reorder operations. These optimizations will be covered in a later blog post that focuses on optimization techniques.

3\. UDF Efficiency
The efficiency of UDFs, such as filtering or aggregation transformations, is essential for overall pipeline performance, regardless of the data loader used. Slow UDFs can create bottlenecks due to the bucket mechanism.

a. Combining UDFs/Filters:
Consolidating filters into a single UDF minimizes data copying and enhances efficiency.

b. Numba JIT Optimization:
Numba employs Just-In-Time (JIT) compilation to translate segments of Python code into optimized machine code during runtime, significantly accelerating numerical computations and overall execution speed.

The combination optimization achieved significantly speed up on training and data transformation pipeline, on our homefeed ranking model training pipeline we are able to achieve 90% of roofline throughput**.**

## 4\. The New Ray-Powered ML Workflow at Pinterest

With these improvements, we now have a**fully Ray-powered ML workflow**that extends beyond training:

Press enter or click to view image in full size

This transformation reduces ML iteration times by 10X while significantly cutting infrastructure costs.

## 5\. Next Steps & Future Work

While we have made significant improvements, there’s still room for further expansion of Ray’s capabilities:

1.**Enhancing Ray Data Optimization for best performance.**(coming in a future blog post).
2.**Extending caching to support even more ML workflows**.
3.**Extending to unleash LLM use cases**: Expand LLM use cases to power recommendation systems with generative models, particularly through model experimentation on user sequence infrastructure.

## 6\. Conclusion: Why Ray is the Future of ML Infrastructure

By extending Ray’s role beyond training into feature engineering, sampling, and labeling, we’ve unlocked a more scalable, efficient, and cost-effective ML infrastructure.

At Pinterest, Ray now powers end-to-end ML workflows, reducing iteration time, improving compute efficiency, and lowering infrastructure costs.
