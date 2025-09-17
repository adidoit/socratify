---
title: "Open Source and In-House: How Uber Optimizes LLM Training"
author: "Unknown"
url: "https://www.uber.com/blog/open-source-and-in-house-how-uber-optimizes-llm-training/"
published_date: "None"
downloaded_date: "2025-09-15T09:38:47.509070"
---

Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
Stay up to date with the latest from Uber Engineering
[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)[Follow us on LinkedIn](https://p.uber.com/eng-linkedin-banner)
X
![Featured image for Open Source and In-House: How Uber Optimizes LLM Training](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/10/head-image-17310452085533-1024x465.png)
Share
  * [Facebook](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fopen-source-and-in-house-how-uber-optimizes-llm-training%2F&t=Open+Source+and+In-House%3A+How+Uber+Optimizes+LLM+Training)
  * [X social](https://twitter.com/share?text=Open+Source+and+In-House%3A+How+Uber+Optimizes+LLM+Training&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fopen-source-and-in-house-how-uber-optimizes-llm-training%2F)
  * [Linkedin](https://www.linkedin.com/shareArticle/?mini=true&url=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fopen-source-and-in-house-how-uber-optimizes-llm-training%2F)
  * [Envelope](mailto:?subject=Open+Source+and+In-House%3A+How+Uber+Optimizes+LLM+Training&body=https%3A%2F%2Fuber.com%2Fen-CA%2Fblog%2Fopen-source-and-in-house-how-uber-optimizes-llm-training%2F)
  * Link

# Introduction
Generative AI powered by LLMs (Large Language Models) has a wide range of applications at Uber, like Uber Eats recommendations and search, customer support chatbots, code development, and SQL query generation. 
To support these applications, Uber leverages open-source models like Meta® Llama 2 and Mistral AI Mixtral®, and closed-source models from OpenAI, Google, and other third-party providers. As a leading company in mobility and delivery, Uber also has considerable domain-specific knowledge that can improve LLM performance for these applications. ‌One way Uber incorporates this domain-specific knowledge is through RAG (Retrieval Augmented Generation). 
Uber also explores ways to adapt LLMs to Uber’s knowledge base through continuous pre-training and instruction fine-tuning. For example, for Uber Eats, we found that a model finetuned on Uber’s knowledge of items, dishes, and restaurants could improve the accuracy of item tagging, search queries, and user preference understanding compared to open-source model results. Even further, these finetuned models can achieve similar performance to GPT-4 models while allowing for much more traffic at Uber’s scale. 
AI community support and open-source libraries like [transformers](https://huggingface.co/docs/transformers/index), Microsoft DeepSpeed®, and [PyTorch FSDP](https://pytorch.org/blog/introducing-pytorch-fully-sharded-data-parallel-api/) empower Uber to rapidly build infrastructure to efficiently train and evaluate LLMs. Emerging open-source initiatives like[ ](https://github.com/facebookresearch/llama-recipes)Meta® Llama 3 [llama-recipes](https://github.com/facebookresearch/llama-recipes), Microsoft [LoRA](https://github.com/microsoft/LoRA)®, [QLoRA](https://github.com/artidoro/qlora)™, and Hugging Face [PEFT](https://github.com/huggingface/peft)™ simplify the fine-tuning lifecycle for LLMs and reduce engineering efforts. Tools like [Ray](https://github.com/ray-project/ray)® and [vLLM](https://github.com/vllm-project/vllm)™ maximize the throughput of large-scale pre-training, fine-tuning, offline batch prediction, and online serving capabilities for open-source LLMs.
The novel in-house LLM training approach described in this blog ensures Uber’s flexibility and speed in prototyping and developing Generative AI-driven services. We use SOTA (state-of-the-art) open-source models for faster, cheaper, and more secure and scalable experimentation. Optimized in-house LLM training helps Uber maintain cutting-edge technology innovations and passes on the benefits to people who use the Uber app.
* * *
## Infrastructure Stack
A critical component of LLM training at Uber is the thoroughly tested infrastructure stack that enables rapid experimentation. 
### Layer 0: Hardware
Uber’s in-house LLM workflows are scheduled on 2 kinds of computing instances: (1) NVIDIA® A100 GPU instances in Uber’s on-prem clusters and (2) NVIDIA H100 GPU instances on Google Cloud. Each Uber on-prem A100 host is equipped with 4 A100 GPUs, 600 GB memory, and 3 TB SSD. On Google Cloud, each host is a 3-highgpu-8g machine type, with 8 H100 GPUs, 1872GB CPU memory, and 6TB SSD. These machines are managed as part of the [Crane](https://www.uber.com/en-MX/blog/crane-ubers-next-gen-infrastructure-stack/) infrastructure stack.
### Layer 1: Orchestration
Computing resources are managed by Kubernetes® and Ray. Kubernetes is used to schedule training workloads and manage hardware requirements. Ray, along with the KubeRay operator, is used for distributing the workload to the workers. 
### Layer 2: Federation
The end-to-end flow of resource management is depicted in Figure 1 below. Our multiple Kubernetes clusters are managed by a federation layer, which schedules workloads based on resource availability. Training jobs are modeled as a Job with multiple Tasks. The JobSpec defines the goal state of the Job and includes information like the instance SKUs, clusters, compute/storage resources, and post-Docker-launch commands to set up tokens and environment variables. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/10/fig1k8s-17291800154604-1024x799.png)Figure 1: Resource scheduling for LLM workflows.
* * *
## Training Stack
We fully embraced open source when building our LLM training stack. Specifically, we integrated PyTorch, Ray, Hugging Face, DeepSpeed, and NCLL to enable training LLMs with the Michelangelo platform. 
  * PyTorch is our chosen deep learning framework because most SOTA open-source LLMs and techniques are implemented in PyTorch. 
  * Ray Train provides a thin API to perform distributed training using PyTorch on Ray clusters. 
  * Hugging Face Transformers provide APIs and tools to download and train SOTA transformer-based models. 
  * DeepSpeed is a deep learning optimization software suite that enables unprecedented scale and speed for deep learning training and inference.

As shown in Figure 2 below, Ray is at the top of the LLM training stack for coordinating tasks. NCCL is at the bottom level for GPU communication.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/10/fig2-17291323864935-1024x535.png)Figure 2: Uber LLM training software stack.
* * *
## Distributed Training Pipeline
To support our in-house implementation, we built an LLM distributed training pipeline that includes host communication, data preparation, distributed model training, and model checkpoint management. Here is how it works:  

  1. **Multi-host and multi-GPU communication**. To start, a TorchTrainer in Ray Train creates multiple workers in the form of Ray Actors, handles in-bound communication (used by Ray Object Store), and initializes a PyTorch distributed process group (used by Deepspeed) on GPUs across all hosts.
  2. **Data preparation**. The LLM training framework supports remote data sources on Uber HDFS, Uber Terrablob, and Hugging Face public datasets.
  3. **Model training**. Tokenization converts input text into integers that will be fed into the models. For distributed training, each GPU worker initializes a Hugging Face Transformers Trainer object using the DeepSpeed ZeRO stage 1/2/3 options. 
  4. **Saving results.** Metrics associated with the training experiment are saved on the Uber Comet server. The main training process on the Ray head node pushes training model weights and associated configuration files to Terrablob storage. 

![Image](https://lh7-rt.googleusercontent.com/docsz/AD_4nXdT3F2A2DQU9CZxNSsCKbIAIB7ZfHvNFKT2W7E2DRlpzCxmyD0NIwbwy0CfOCs2dnPJdQyHLuH5Ia7Dt5QSgICSuNmz9igsWp_TabDWQ8XCJs1GWbMBRohsvSv9qg-J19oJyuLqixlDKAlRZrfZyhzu3l_3?key=F9WnaYLpB5WvGJfBHoMLXQ)Figure 3: Uber LLM distributed training pipeline.
* * *
## Training Results
Our exploration involved demonstrating that the in-house Michelangelo platform has the capability and scalability to train any open-source LLM with throughput optimization. 
### Training on State-Of-The-Art LLMs
We found that the Michelangelo platform can support the largest open-source LLMs while training under different settings, including full-parameter fine tuning and parameter-efficient fine tuning with LoRA and QLoRA. 
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/10/figure-4-17291324832411-1024x505.png)Figure 4: Training loss of Llama 2 models with and without (Q)LoRA.
Figure 4 (above) shows the training loss curve for Llama 2 13B and Llama 2 70B with and without LoRA. We found that, even if LoRA and QLoRA use far fewer GPUs and train much faster with fewer GPUs, the loss decreases much less than the full parameter training. Therefore, it’s important to improve the throughput/Model Flops Utilization (MFU) for full parameter fine-tuning of LLMs.
###   
Throughput/MFU Optimization
Scaling the transformer architecture is heavily bottlenecked by the model’s self-attention mechanism, which has quadratic time and memory complexity. To achieve better training throughput, we’ve explored several industry recommended efforts to optimize GPU memory usage: CPU offload and flash attention.
The first training throughput optimization we explored was using DeepSpeed ZeRO-stage-3 CPU Optimizer Offload, which led to at least 34% GPU memory reduction with the same batch size when training Llama 2 70B. This allowed us to increase the batch size by 3-4 times but still keep the same forward and backward speed, so the training throughput increased by 2-3 times.
The second training throughput optimization explored was following Hugging Face’s suggestion to use flash attention. Flash attention is an attention algorithm used to reduce quadratic complexity and scale transformer-based models more efficiently, enabling faster training. With flash attention, we could save 50% of GPU memory with the same batch size. If we maximized the usage of GPU memory, then we could double the batch size while keeping compatible forward and backward speed.
To study training efficiency, we used Hardware Model Flops Utilization ([MFU](https://arxiv.org/pdf/2204.02311.pdf)). MFU is the ratio of the observed throughput to the theoretical maximum throughput if the benchmarked hardware setup was operating at peak FLOPS with no memory or communication overhead.
In our benchmark, we used [Deepspeed Flops Profiler](https://deepspeed.readthedocs.io/en/latest/flops-profiler.html) to obtain the expected FLOPS number. FLOPS per GPU was calculated as: forward and backward FLOPS per GPU/iteration latency. Then we divided it by the device’s ​​peak theoretical performance and obtained our final MFU metric. ‌In all our experiments, we maximized the batch size under different optimization settings so that GPU memory was fully utilized. We did this with the training arguments, setting _gradient_accumulation_steps = 1_ so that _macro_batch_size = micro_batch_size x num_gpus x 1_.
Here’s what we found: 
  * **Throughput** : Both flash attention and CPU offload saved GPU memory, enabling us to increase batch size 2 to 7 times during Llama 2 70B training with maximum GPU memory usage (70GB-80GB) on 32 GPUs (8 hosts on A100, 4 hosts on H100). This led to significant throughput increases. 
  * **MFU** : MFU on H100 was lower than on A100, and GPU utilization wasn’t full with maximum GPU memory usage. This might indicate that for Llama 2 70B training, we have memory-bound GPU instead of compute-bound. That’s also why CPU offload could help the most to improve MFU, as plotted in Figure 5 below. 
  * **Compute or Memory Bound** : The story is slightly different for Llama 2 7B on 4 A100/H100 on a single host, where we may have compute-bound GPU instead of memory-bound GPU. We saw that the MFU of training Llama 2 7B was higher than training Llama 2 70B, and CPU offload was not helpful to improve MFU. Flash attention could help the most, as shown in Figure 6 below. 
  * **Network:** In our experiment, the network usage was around 10GB/second on H100 and 3GB/second on A100 for Llama 2 70B model training. This is small compared to the infra theoretical value, indicating that the network is yet to be a bottleneck compared to GPU compute and memory. 

![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/10/figure-5-17291325919540-1024x634.png)Figure 5: Model Flops Utilization of training Llama 2 70B.
![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/10/figure-6-17291326224707-1024x635.png)Figure 6: Model Flops Utilization of training Llama 2 7B.
### LLM Scorer
To evaluate the raw or finetuned models, we also implemented an offline LLM scorer to predict on large datasets. We used Ray to create a cluster on Kubernetes with multiple instances and each instance with multiple GPUs. This way, we could distribute the data and score in parallel. On each instance, we used inference servers such as [vLLM](https://github.com/vllm-project/vllm).
In our implementation, we used Ray jobs as the operational foundation. Each Ray job allocates a specified number of CPU and GPU resources, downloads models, and partitions datasets by rank. The Ray `ActorPool` aggregates the outputs from different Ray Actors. Figure 7 below shows the implementation of this LLM scorer. 
![Image](https://lh7-rt.googleusercontent.com/docsz/AD_4nXcptqsUis4TPQFJP9-OfxrU60nUal734joeKAohIc3jWOMuOU30fC58yufglGf4nzT3KI8VggrcxoASoFb8aSmOQKMXOk5ccrXsIhpQAr_-Pomo-INJ-MUMOMIYkgqKv9u2Q7Dwg3laKTYJ750mU3w45i8?key=F9WnaYLpB5WvGJfBHoMLXQ)Figure 7: Distributed LLM scorer with Ray and vLLM.
Figure 8 below summarizes the performance of batch prediction for Mixtral 8x7b models using 2 A100 and H100 GPUs, where the input token size is 4K and the maximum output tokens are 700. We observed that output tokens per second increased linearly for batch sizes up to 64 on both GPU types. Notably, the H100 achieved a throughput 3 times higher than the A100. This benchmark helps teams make production decisions and plan resource requirements. 
![Image](https://lh7-rt.googleusercontent.com/docsz/AD_4nXfpULj9Ck6J4EpGtKKPx8e4f_q925QVj3CisQlmWVKLzr1NiTnTpsSSxOj_NfaZZ8eQWuxxBRM0Grb280IbiDTkdRqaK5RSg3moI346umhtDDnHFqVOhPflkhI0Bk0pIbI272dXCbLHt0zw0iKOafuN-l4?key=F9WnaYLpB5WvGJfBHoMLXQ)Figure 8: Throughput for Mixtral-8x7b on 2 x A100/H100.
* * *
# Conclusion
As more and larger open-source models get published, like Llama 3 450B, we’ll improve our LLM training infrastructure to support fine-tuning them. Using these finetuned models will help us improve things like Uber Eats recommendations and search.
Thinking about the broader industry, our journey exploring in-house LLM training has brought us these insights:
  1. **Embracing open source is the key****to catching up with generative AI trends.** In a short time, we’ve seen and benefitted from the fast-growing open-source community Hugging Face and the rapid adoption of DeepSpeed. Open-source model structures like Falcon, Llama, and Mixtral are published one-after-another every few months. With open-source solutions, we can train SOTA LLMs and achieve the industry standard MFU to maximize GPU usage. 
  2. **Having long-time-tested and extensible cluster management is critical to catching the latest trends quickly.** Our well-established Ray and Kubernetes stack makes it easy to integrate new open-source solutions into our production environment. 

* * *
## Acknowledgements
This major step for GenAI at Uber couldn’t have happened without the many teams at Uber who contributed to it: Michelangelo, Applied AI, Dev Platform, and Platform Core Service.
_Apache ®, Apache Kafka, Kafka, Apache Spark, Spark, and the star logo are either registered trademarks or trademarks of the Apache Software Foundation in the United States and/or other countries. No endorsement by The Apache Software Foundation is implied by the use of these marks._
_Deepspeed ® and its logo, LoRA_® _and its logo_ _are registered trademarks of Microsoft ® in the United States and other countries. No endorsement by Microsoft is implied by the use of these marks._
_Kubernetes ® and its logo are registered trademarks of The Linux Foundation® in the United States and other countries. No endorsement by The Linux Foundation is implied by the use of these marks._
_Llama 2 ®, Llama 3® and their logos are registered trademarks of Meta® in the United States and other countries. No endorsement by Meta is implied by the use of these marks._
_Mixtral ® and its logo are registered trademarks of Mistral AI® in the United States and other countries. No endorsement by Mistral AI is implied by the use of these marks._
_NVIDIA ® and the NVIDIA logo are trademarks and/or registered trademarks of NVIDIA Corporation in the U.S. and other countries. No endorsement by NVIDIA is implied by the use of these marks._
_PyTorch, the PyTorch logo and any related marks are trademarks of The Linux Foundation._
_Transformers ® and its logo are registered trademarks of Hugging Face® in the United States and other countries. No endorsement by Hugging Face is implied by the use of these marks._
* * *
![Bo Ling](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2023/07/Bo_TTE_EngBlog.jpeg)
Bo Ling
Bo Ling is a Staff Software Engineer on Uber’s AI Platform team. He works on NLP, Large language models and recommendation systems. He is the leading engineer on embedding models and LLM in the team.
![Jiapei Huang](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/10/jh-pic-17291342709091-e1729134346331.jpg)
Jiapei Huang
Jiapei Huang is a Software Engineer working on Deep Learning training infrastructure at Uber Michelangelo team. He has end-to-end experience of AI infra and unblocked multiple business-critical scenarios like LLM, time series modeling, etc.
![Baojun Liu](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/10/image-10-16-24-at-11.38am-17291331161100.jpeg)
Baojun Liu
Baojun Liu is a Software Engineer working on online and offline serving, software and hardware co-development for AI Infra at Uber Michelangelo team. Prior to that, he was a deep learning framework architect working on DL compiler intermediate representation, software stack development for heterogeneous architecture, and its enabling for serving and training.
![Chongxiao Cao](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/10/image-10-16-24-at-11.39am-17291332209224.jpeg)
Chongxiao Cao
Chongxiao Cao is a Senior Software Engineer at Uber, leading the development of the deep learning training infrastructure on Michelangelo, including scaling up data throughput, accelerating training speed, increasing model size, and optimizing resource utilization. He also serves as a leading contributor to the Horovod distributed deep learning framework and Petastorm data loading library.
![Anant Vyas](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/03/anantpic-17436334916283.png)
Anant Vyas
Anant Vyas is a Senior Staff Engineer and the Tech Lead of AI Infrastructure at Uber. His focus is on maximizing the performance and reliability of their extensive computing resources for training and serving.
![Peng Zhang](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/10/image-10-16-24-at-11.39am-2-17291334226500-e1729133442218.jpeg)
Peng Zhang
Peng Zhang is an Engineering Manager on the AI Platform team at Uber. He supports the teams dedicated to developing modeling and training frameworks, managing GPU-based clusters, and enhancing ML infrastructure for training classical, deep learning, and generative AI models.
* * *
Posted by Bo Ling, Jiapei Huang, Baojun Liu, Chongxiao Cao, Anant Vyas, Peng Zhang 
Category:
[Engineering](/en-CA/blog/engineering/)
[Uber AI](/en-CA/blog/engineering/ai/)
* * *
### Related articles
[![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/09/cover-photo-clock-gears-17575284883091-1024x680.jpg)Engineering, Backend, Data / MLOpen-Sourcing Starlark Worker: Define Cadence Workflows with StarlarkSeptember 11 / Global](/en-CA/blog/starlark/)
[![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/09/cover-photo-17569388153419-1024x683.jpg)Engineering, Data / MLBuilding Uber’s Data Lake: Batch Data Replication Using HiveSyncSeptember 4 / Global](/en-CA/blog/building-ubers-data-lake-batch-data-replication-using-hivesync/)
[![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/08/cover-photo-2-17563345896014-1024x629.jpg)Engineering, BackendControlling the Rollout of Large-Scale Monorepo ChangesAugust 28 / Global](/en-CA/blog/controlling-the-rollout-of-large-scale-monorepo-changes/)
[![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/08/cover-1-17561626024808-1024x683.jpg)Engineering, BackendHow Uber Serves over 150 Million Reads per Second from Integrated Cache with Stronger Consistency GuaranteesAugust 26 / Global](/en-CA/blog/how-uber-serves-over-150-million-reads/)
[![Image](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/08/cover-photo-17557274589976.jpg)Engineering, BackendLightweight Office Infrastructure: Transitioning from Backbone to SD-WANAugust 21 / Global](/en-CA/blog/lightweight-office-infrastructure/)
## Most popular
[![Post thumbnail](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/06/cropped-17508030478819-1024x512.png)EarnJune 30 / CanadaHelping you stay informed about risks to your account status](/en-CA/blog/new-reports-experience/)[![Post thumbnail](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/cover-17514078235579-1024x683.jpg)Engineering, Data / ML, Uber AIJuly 2 / GlobalReinforcement Learning for Modeling Marketplace Balance](/en-CA/blog/reinforcement-learning-for-modeling-marketplace-balance/)[![Post thumbnail](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2025/07/41577658914f37d9ff4d8o-17525304449657-1024x499.jpg)Engineering, BackendJuly 15 / GlobalHow Uber Processes Early Chargeback Signals](/en-CA/blog/how-uber-processes-early-chargeback-signals/)[![Post thumbnail](https://blog.uber-cdn.com/cdn-cgi/image/width=2160,quality=80,onerror=redirect,format=auto/wp-content/uploads/2024/02/UberIM_009076-1024x684.jpg)TransitJuly 15 / GlobalYour guide to NJ TRANSIT’s Access Link Riders’ Choice Pilot 2.0](/en-CA/blog/your-guide-to-access-link-riders-choice-pilot-2-0/)
[View more stories](/en-CA/blog/engineering/)
## Select your preferred language
[English](/en-CA/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)
## [Sign up to drive](https://www.uber.com/signup/drive)
## [Sign up to ride](https://get.uber.com/sign-up)
  * ### Products
    * [EarnResources for driving and delivering with Uber](/en-CA/blog/earn/)
    * [RideExperiences and information for people on the move](/en-CA/blog/ride/)
    * [EatOrdering meals for delivery is just the beginning with Uber Eats](/en-CA/blog/eat/)
    * [MerchantsPutting stores within reach of a world of customers](/en-CA/blog/merchants/)
    * [BusinessTransforming the way companies move and feed their people](/en-CA/blog/business/)
    * [FreightTaking shipping logistics in a new direction](/en-CA/blog/freight/)
    * [Higher EducationEnhancing campus transportation](/en-CA/blog/higher-education/)
    * [TransitExpanding the reach of public transportation](/en-CA/blog/transit/)
  * ### Company
    * [CareersExplore how Uber employees from around the globe are helping us drive the world forward at work and beyond](/en-CA/blog/careers/)
    * [EngineeringThe technology behind Uber Engineering](/en-CA/blog/engineering/)
    * [NewsroomUber news and updates in your country](https://uber.com/newsroom)
    * [Uber.comProduct, how-to, and policy content—and more](https://uber.com)

EN
## Select your preferred language
[English](/en-CA/blog/open-source-and-in-house-how-uber-optimizes-llm-training/)
## [Sign up to drive](https://www.uber.com/signup/drive)
## [Sign up to ride](https://get.uber.com/sign-up)
