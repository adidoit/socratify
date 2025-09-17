---
title: "Distributed Systems & Parallel Computing"
company: "google"
url: "https://research.google/research-areas/distributed-systems-and-parallel-computing/"
focus_area: "distributed systems, search, ML infrastructure"
system_score: 25
type: "expansion_systems"
date: "2025-09-15"
---

  1. [Home](/)
  2. [Research areas](/research-areas/)



# Distributed Systems and Parallel Computing

No matter how powerful individual computers become, there are still reasons to harness the power of multiple computational units, often spread across large geographic areas. Sometimes this is motivated by the need to collect data from widely dispersed locations (e.g., web pages from servers, or sensors for weather or traffic). Other times it is motivated by the need to perform enormous computations that simply cannot be done by a single CPU.

From our company’s beginning, Google has had to deal with both issues in our pursuit of organizing the world’s information and making it universally accessible and useful. We continue to face many exciting distributed systems and parallel computing challenges in areas such as concurrency control, fault tolerance, algorithmic efficiency, and communication. Some of our research involves answering fundamental theoretical questions, while other researchers and engineers are engaged in the construction of systems to operate at the largest possible scale, thanks to our [hybrid research model](https://cacm.acm.org/magazines/2012/7/151226-googles-hybrid-approach-to-research/fulltext).

### Recent Publications

[ See More ](https://research.google/pubs/?category=distributed-systems-and-parallel-computing)

[ How we use GenAI in SRE ](https://research.google/pubs/how-we-use-genai-in-sre/)

[ Ramón Medrano Llamas ](/people/ramonmedranollamas/)

CommitConf, Madrid (2024) 

Preview Preview abstract  Google services are powered by the largest network of computers in the world. Site Reliability Engineers (SRE) make sure that the whole stack is cool: datacenters are safe, well provisioned; we have fallback mechanisms, and data integrity; to make sure we design our stack properly, using the right storage, replication and software trade-offs. Generative AI is a great tool to make us super-effective: having access to tools to generate our most toily configurations, to classify risks and events, to manage large swaths of machines with agents or to automate complex workflows cheaply. This talk will cover the journey that SRE started years ago to become a truly AI-First discipline and the latest advancements in tooling, practices and workflows. [ View details ](https://research.google/pubs/how-we-use-genai-in-sre/)

[ BigLake: BigQuery’s Evolution toward a Multi-Cloud Lakehouse ](https://research.google/pubs/biglake-bigquerys-evolution-toward-a-multi-cloud-lakehouse/)

Justin Levandoski 

Garrett Casto 

Mingge Deng 

Rushabh Desai 

[ Pavan Edara ](/people/pavanedara/)

Thibaud Hottelier 

Amir Hormati 

Anoop Johnson 

Jeff Johnson 

Dawid Kurzyniec 

[ Sam McVeety ](/people/sammcveety/)

Prem Ramanathan 

Gaurav Saxena 

Vidya Shanmugam 

Yuri Volobuev 

SIGMOD (2024) 

Preview Preview abstract  BigQuery’s cloud-native disaggregated architecture has allowed Google Cloud to evolve the system to meet several customer needs across the analytics and AI/ML workload spectrum. A key customer requirement for BigQuery centers around the unification of data lake and enterprise data warehousing workloads. This approach combines: (1) the need for core data management primitives, e.g., security, governance, common runtime metadata, performance acceleration, ACID transactions, provided by an enterprise data warehouses coupled with (2) harnessing the flexibility of the open source format and analytics ecosystem along with new workload types such as AI/ML over unstructured data on object storage. In addition, there is a strong requirement to support BigQuery as a multi-cloud offering given cloud customers are opting for a multi-cloud footprint by default. This paper describes BigLake, an evolution of BigQuery toward a multi-cloud lakehouse to address these customer requirements in novel ways. We describe three main innovations in this space. We first present BigLake tables, making open-source table formats (e.g., Apache Parquet, Iceberg) first class citizens, providing fine-grained governance enforcement and performance acceleration over these formats to BigQuery and other open-source analytics engines. Next, we cover the design and implementation of BigLake Object tables that allow BigQuery to integrate AI/ML for inferencing and processing over unstructured data. Finally, we present Omni, a platform for deploying BigQuery on non-GCP clouds, focusing on the infrastructure and operational innovations we made to provide an enterprise lakehouse product regardless of the cloud provider hosting the data. [ View details ](https://research.google/pubs/biglake-bigquerys-evolution-toward-a-multi-cloud-lakehouse/)

[ Federated Variational Inference: Towards Improved Personalization and Generalization ](https://research.google/pubs/federated-variational-inference-towards-improved-personalization-and-generalization/)

Elahe Vedadi 

Josh Dillon 

Philip Mansfield 

Karan Singhal 

Arash Afkanpour 

Warren Morningstar 

AAAI Federated Learning on the Edge Symposium (2024) 

Preview Preview abstract  Conventional federated learning algorithms train a single global model by leveraging all participating clients' data. However, due to heterogeneity in client generative distributions and predictive models, these approaches may not appropriately approximate the predictive process, converge to an optimal state, or generalize to new clients. We study personalization and generalization in stateless cross-device federated learning setups assuming heterogeneity in client data distributions and predictive models. We first propose a hierarchical generative model and formalize it using Bayesian Inference. We then approximate this process using Variational Inference to train our model efficiently. We call this algorithm Federated Variational Inference (FedVI). We use PAC-Bayes analysis to provide generalization bounds for FedVI. We evaluate our model on FEMNIST and CIFAR-100 image classification and show that FedVI beats the state-of-the-art on both tasks. [ View details ](https://research.google/pubs/federated-variational-inference-towards-improved-personalization-and-generalization/)

[ Vortex: A Stream-oriented Storage Engine For Big Data Analytics ](https://research.google/pubs/vortex-a-stream-oriented-storage-engine-for-big-data-analytics/)

[ Pavan Edara ](/people/pavanedara/)

Jonathan Forbes 

Bigang Li 

SIGMOD (2024) 

Preview Preview abstract  Vortex is an exabyte scale structured storage system built for streaming and batch analytics. It supports high-throughput batch and stream ingestion. For the user, it supports both batch-oriented and stream-based processing on the ingested data. [ View details ](https://research.google/pubs/vortex-a-stream-oriented-storage-engine-for-big-data-analytics/)

[ Thesios: Synthesizing Accurate Counterfactual I/O Traces from I/O Samples ](https://research.google/pubs/thesios-synthesizing-accurate-counterfactual-io-traces-from-io-samples/)

Mangpo Phothilimthana 

[ Saurabh Kadekodi ](/people/saurabhkadekodi/)

Soroush Ghodrati 

Selene Moon 

[ Martin Maas ](/people/martinmaas/)

ASPLOS 2024, Association for Computing Machinery 

Preview Preview abstract  Representative modeling of I/O activity is crucial when designing large-scale distributed storage systems. Particularly important use cases are counterfactual “what-if” analyses that assess the impact of anticipated or hypothetical new storage policies or hardware prior to deployment. We propose Thesios, a methodology to accurately synthesize such hypothetical full-resolution I/O traces by carefully combining down-sampled I/O traces collected from multiple disks attached to multiple storage servers. Applying this approach to real-world traces that a real ready routinely sampled at Google, we show that our synthesized traces achieve 95–99.5% accuracy in read/write request numbers, 90–97% accuracy in utilization, and 80–99.8% accuracy in read latency compared to metrics collected from actual disks. We demonstrate how The-sios enables diverse counterfactual I/O trace synthesis and analyses of hypothetical policy, hardware, and server changes through four case studies: (1) studying the effects of changing disk’s utilization, fullness, and capacity, (2) evaluating new data placement policy, (3) analyzing the impact on power and performance of deploying disks with reduced rotations-per-minute (RPM), and (4) understanding the impact of increased buffer cache size on a storage server. Without Thesios, such counterfactual analyses would require costly and potentially risky A/B experiments in production. [ View details ](https://research.google/pubs/thesios-synthesizing-accurate-counterfactual-io-traces-from-io-samples/)

[ Load is not what you should balance: Introducing Prequal ](https://research.google/pubs/load-is-not-what-you-should-balance-introducing-prequal/)

Bartek Wydrowski 

Bobby Kleinberg 

Steve Rumble 

[ Aaron Archer ](/people/aaronarcher/)

(2024) 

Preview Preview abstract  We present Prequal (\emph{Probing to Reduce Queuing and Latency}), a load balancer for distributed multi-tenant systems. Prequal aims to minimize real-time request latency in the presence of heterogeneous server capacities and non-uniform, time-varying antagonist load. It actively probes server load to leverage the \emph{power of $d$ choices} paradigm, extending it with asynchronous and reusable probes. Cutting against received wisdom, Prequal does not balance CPU load, but instead selects servers according to estimated latency and active requests-in-flight (RIF). We explore its major design features on a testbed system and evaluate it on YouTube, where it has been deployed for more than two years. Prequal has dramatically decreased tail latency, error rates, and resource use, enabling YouTube and other production systems at Google to run at much higher utilization. [ View details ](https://research.google/pubs/load-is-not-what-you-should-balance-introducing-prequal/)

## Some of our teams

  * [ Algorithms & optimization  ](/teams/algorithms-optimization/)
  * [ Athena  ](/teams/athena/)
  * [ Graph mining  ](/teams/graph-mining/)
  * [ Network infrastructure  ](/teams/network-infrastructure/)
  * [ System performance  ](/teams/system-performance/)



## Join us

We're always looking for more talented, passionate people.

[ See opportunities ](https://research.google/careers/)

![Careers](https://storage.googleapis.com/gweb-research2023-media/images/Careers.original.jpg)
