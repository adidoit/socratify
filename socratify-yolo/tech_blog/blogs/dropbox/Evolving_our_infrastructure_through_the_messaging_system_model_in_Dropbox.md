---
title: "Evolving our infrastructure through the messaging system model in Dropbox"
author: "dropbox"
url: "https://dropbox.tech/infrastructure/infrastructure-messaging-system-model-async-platform-evolution"
system_score: 72
date: "2025-09-15"
---

[Dropbox.Tech](https://dropbox.tech/)

  * Topics
    * [Application](https://dropbox.tech/application)
    * [Front End](https://dropbox.tech/frontend)
    * [Infrastructure](https://dropbox.tech/infrastructure)
    * [Machine Learning](https://dropbox.tech/machine-learning)
    * [Mobile](https://dropbox.tech/mobile)
    * [Security](https://dropbox.tech/security)
    * [Culture](https://dropbox.tech/culture)
  * [Developers](https://dropbox.tech/developers)
  * [Jobs](http://dropbox.com/jobs)
  * [Dash](https://dash.dropbox.com/?utm=blogs)

![](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-all/resources/button_dark-mode-new.svg) ![](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-all/resources/button_search-new.svg)

// Press enter to search 

![](/cms/content/dam/dropbox/tech-blog/en-us/2025/async-platform-evolution/headers/1x/Infrastructure-Async-Evolution-1440x305-light@2x.png/_jcr_content/renditions/Infrastructure-Async-Evolution-1440x305-light@2x.webp) ![](/cms/content/dam/dropbox/tech-blog/en-us/2025/async-platform-evolution/headers/1x/Infrastructure-Async-Evolution-1440x305-dark@2x.png/_jcr_content/renditions/Infrastructure-Async-Evolution-1440x305-dark@2x.webp)

# Evolving our infrastructure through the messaging system model in Dropbox

// By Dmitry Kopytkov and Deepak Gupta • Jan 21, 2025

  1. Challenges and limitations in our asynchronous infrastructure
  2. Rethinking our approach
  3. The five layers of the messaging system model
  4. Conclusion



The asynchronous platform at Dropbox integrates a suite of services that enable tasks and workflows to function independently without having to wait on one another. This is pretty important to our work as developers: It empowers any service within Dropbox to initiate and schedule tasks, seamlessly supporting over 400 product use cases—including [Dropbox Dash](https://www.dash.dropbox.com/) and our other AI innovations—and efficiently routing more than 30 million tasks _every minute_. It also handles [change data capture (CDC)](https://www.confluent.io/learn/change-data-capture/) use cases, where changes in our underlying storage system, including the FileSystem, are relayed to various product lambdas and processes. In short, it helps us ensure impactful and efficient business operations.

This implementation was essential to our growth from where we were a couple of years ago. Back then, the asynchronous platform struggled with scalability and reliability, frequently falling short of the demands of our expanding product portfolio. For product engineers, the platform posed additional hurdles due to limited developer productivity tools, making it cumbersome to build and iterate on asynchronous workflows. Today’s transformation into a robust and scalable system marks a dramatic shift from those early challenges—it enables innovation at a desired pace.

In this blog, we’ll introduce an open **messaging system model (MSM)** , which played a key role in evolving our platform. It helped us build a unified event-driven system capable of orchestrating a wide range of asynchronous tasks and meeting future needs, especially as we focus on AI. Inspired by the [Open Systems Interconnection (OSI) model](https://en.wikipedia.org/wiki/OSI_model), the MSM divides our platform into five logical layers. This standardization simplifies layers such as frontend interfaces, lambda functions, event schedulers, and event routers, allowing them to work across various use cases with different delivery guarantees and data sources, including those related to CDC.

Let’s get into it.

![](https://cdn.prod.website-files.com/65dcd70b48edc3a7b446950e/670692ee7692f74d4834e4f4_Frame%201400006055.svg) Dropbox Dash: Find anything. Protect everything.

Find, organize, and protect your work with Dropbox Dash. Now with advanced search for video and images—plus generative AI capabilities across even more connected apps.

[See what's new →](https://dash.dropbox.com/?utm=blogs)

## Challenges and limitations in our asynchronous infrastructure

Beginning in 2021, our infrastructure comprised multiple asynchronous systems, each tailored to specific product or process requirements. These systems facilitated diverse functions—such as streaming events for Dropbox file uploads and edits—as well as supporting domains like security, abuse prevention, machine learning, and search indexing. Additionally, Dropbox integrated CDC functionality, enabling any modification within the underlying storage systems to generate an event, subsequently activating the async infrastructure. Despite occasional functional overlaps, these systems were developed, operated, and maintained separately, leading to inconsistencies in development speed, reliability, and operational ease.

Key issues and limitations with these systems were as follows:

**Developer efficiency  
**The complexity of the current systems required product engineers to undertake a steep learning curve and assume responsibility for operational tasks such as capacity planning, release processes, and support, leading to reduced development speed and productivity.

**Reliability  
**These systems had varied [service-level objectives (SLOs)](https://en.wikipedia.org/wiki/Service-level_objective) for availability, latency, processing, and recovery, which resulted in inconsistent and unreliable performance. Additionally, systems were not multi-homed, and this created significant reliability risk for multiple business use cases in the event of data center failure.

**Operability  
**The variety of systems led to higher operational costs due to their complexity, requiring additional development effort for maintenance and support. The asynchronous components in our technology stack relied on a mix of external queuing solutions, such as Kafka, Redis, and Amazon SQS, creating an infrastructure that was challenging to manage and operate.

**System scalability  
**At the beginning of 2021, our system was processing over 30 billion requests daily to dispatch jobs to lambda functions. (Lambda is a serverless cloud service that runs your code automatically in response to events, without requiring you to manage any servers.) However, meeting the defined SLOs became increasingly challenging. Certain critical components, such as the delayed event scheduler, had already maxed out their throughput capacity. Consequently, we had to implement rigorous screening protocols for each new use case before onboarding in order to ensure it adhered to the system's capacity limitations and wouldn't jeopardize its performance.

**Lambda infrastructure  
**The lambda-based architecture utilized on the consumer side was complex and diverged from the Dropbox [service-oriented architecture (SOA)](https://dropbox.tech/infrastructure/meet-bandaid-the-dropbox-service-proxy) guidelines and established best practices. Consequently, diagnosing and investigating issues on the consumption side became highly challenging, as it didn't integrate seamlessly with the Dropbox infrastructure and recommended methodologies. This lack of alignment resulted in several adverse effects, notably:

  * **Release consistency _:_** The release procedures across these systems lacked uniformity and robust safety measures, introducing deployment and update risks.
  * **Compute efficiency _:_** The compute clusters supporting these systems operated below peak efficiency, resulting in suboptimal resource utilization.
  * **No autoscaling:** The absence of autoscaling for lambda infrastructure, stemming from its deviation from the Dropbox SOA guidelines, resulted in poor integration with our autoscaling infrastructure. As a result, there was a reliance on customer or platform-owner intervention to manually augment capacity when the base capacity proved inadequate to manage the workload.



**Extensibility  
**Extensibility posed a significant challenge for these systems, characterized by a deficiency in flexibility and scalability to adapt to emerging product demands. The current solutions were ill-equipped to seamlessly integrate new workflows, and any attempts to expand them would introduce unnecessary complexities in implementation. With the introduction of Cypress, our new filesystem architecture, the existing system faced limitations in expanding our CDC pipeline to distribute Cypress events to multiple subscribers within Dropbox.

In all, these challenges underscored the need for a more unified and consistent approach to our asynchronous infrastructure, emphasizing the importance of addressing developer velocity, reliability, operability, efficiency, and extensibility to better support the company's evolving product landscape.

## Rethinking our approach

The existing async systems already supported over 400 business use cases. The large number of existing use cases meant we didn’t have the flexibility to construct an entirely new system from scratch, as the migration would have been very time consuming. Instead, we decided to adopt a phased approach, with incremental steps to rebuild existing systems that mitigate risks associated with migrating existing production flows to a new infrastructure. Returning to the drawing board, we outlined three primary goals for the new platform, envisioning a gradual and incremental build-up of capabilities:

**Development velocity**

  * Simplify the asynchronous interface to streamline platform adoption for product engineers. This allows them to focus on creating innovative product features rather than investing time in understanding the complex asynchronous landscape and determining the most suitable system for their use case.
  * Decrease the operational burden on product engineers by implementing release practices that identify code regressions during deployment and automatically initiate rollbacks if a new release breaches predefined thresholds.
  * Enable automatic compute scaling when a lambda function encounters a backlog of events to process, ensuring that the current base capacity is augmented if deemed insufficient.



**Robust and extensible async foundation**

  * Unify common elements and patterns across existing async systems within Dropbox and simplify the interface.
  * Support new use cases with minimal modifications and avoid the need to build entire new systems by providing extensible components and flexible APIs.



**Cost and operational efficiency**

  * Streamline the foundational infrastructure by phasing out redundant systems (where applicable) and cut down on operational costs.
  * Transition lambda infrastructure to the Dropbox SOA stack to increase compute efficiency and enable functionalities such as autoscaling, multihoming, and improved out-of-the-box monitoring capabilities.



The overarching key performance indicator (KPI) that we aimed to improve over time was the "time to launch" for product engineers to deploy a new use case into production. As platform owners, our primary KPI of interest was the "oncall time" expended on a weekly basis.

##  The five layers of the messaging system model

The initial step in the refinement of the async system involved deconstructing it into its fundamental layers. We undertook this process to achieve the aforementioned objectives. Subsequently, a systematic approach was devised, beginning with the dissection of the async system into its core elements, followed by the formulation of a bottom-up strategy for its progressive enhancement.

From a macroscopic standpoint, the asynchronous system can be mapped to an MSM consisting of three primary layers, analogous to the seven layers of the OSI model in network transmission frameworks. These three primary layers are:

  * **Customer layer:** This component, also known as the “frontend layer,” encompasses the various pathways through which users interact and interface with the async system. It encapsulates the mechanisms by which users communicate with and integrate into the async environment.
  * **Orchestration layer:** This layer is intrinsic to the async system and encompasses the entirety of the tasks required for the scheduling and transmission of async operations to the compute layer (also known as the “execution layer”). It serves as the intermediary stage between the customer layer and the compute layer, and it’s responsible for ensuring that various components and services interact seamlessly to fulfill complex workflows and business logic requirements.
  * **Compute layer:** This layer is the execution hub of the async system, where the actual processing and execution of async tasks take place. It is responsible for the seamless execution of asynchronous operations, thereby ensuring the efficient functioning of the system as a whole.



![](/cms/content/dam/dropbox/tech-blog/en-us/2025/async-platform-evolution/diagrams/0125-Infrastructure-Async-Evolution.png/_jcr_content/renditions/0125-Infrastructure-Async-Evolution.webp)

A 10,000-foot view of the async system

The three layers mentioned above can then be _further_ broken down into five, more specific layers—frontend, scheduler, flow control, delivery, and execution—with each new layer serving an important role within the above three buckets. (Some overlap occurs between the customer and orchestration layers). These five layers of the MSM are illustrated in the diagram below.

![](/cms/content/dam/dropbox/tech-blog/en-us/2025/async-platform-evolution/diagrams/0125-Infrastructure-Async-Evolution-2.png/_jcr_content/renditions/0125-Infrastructure-Async-Evolution-2.webp)

An illustration of the five components of the Messaging System Model (MSM)

Now, let's take a closer look at each of these five layers.

### Frontend

In the architecture of an asynchronous system, the frontend layer assumes the critical role of serving as the primary interface for user interaction with the system. It represents the user-facing aspect of the asynchronous environment, orchestrating seamless communication and integration with the system's core functionalities. Users are categorized into two distinct groups: first, there are the regular product engineers who utilize programmatic methods to invoke a publish remote procedure call (RPC) and enqueue events, destined to be consumed by one or more subscribers. The second category encompasses systems such as databases or event sources, which necessitate the enqueuing of changes to diverse objects, entities, or files, thereby propelling both internal and external business workflows forward.

A pivotal responsibility of the frontend layer is the management of the schema registry and the rigorous validation of every event schema traversing the system. This stringent schema validation process ensures that published events conform to the predefined contract established with subscribers. Additionally, the frontend layer is tasked with the intricate conversion of disparate message formats, including JSON, Proto, and Avro, among others, into a standardized message format—typically protocol buffers—compatible with the internal asynchronous implementation.

Furthermore, the frontend component is entrusted with guaranteeing the durability of all events published to the asynchronous system, thereby safeguarding the integrity and reliability of the system's data flow. 

### Scheduler

The scheduler is the core engine within an async system and plays a crucial role in coordinating and dispatching disparate events for various consumers that subscribe to these events. This layer plays various roles. For example, for a CDC use case, this will call external data source APIs to get relevant range for the payloads that will be delivered to the subscribers. For a use case where events need delayed execution, the scheduler would store these events separately so they can be trigger at desired timestamp with a process keeping tabs on these events and publishing them to subscribers at those desired scheduled timestamps. 

Scheduler also has the responsibility to maintain the order of execution of the events and ensures task delivery to subscribers based on this order.

### Flow control

Flow control plays a pivotal role in the orchestration layer, managing the distribution of tasks to subscribers based on several factors, such as subscriber availability, task priority, and potential throttling events. For instance, in a CDC scenario, the orchestration layer dynamically adjusts the rate of queries dispatched to subscribers. This adaptation occurs when the orchestration layer detects that a subscriber is unable to handle the job throughput effectively or when the source, backing CDC, signals the scheduler client to reduce the pace.

State management, another function of this layer, encompasses the maintenance of data structures responsible for tracking ongoing events and their respective statuses (such as pending, running, or complete). Additionally, it incorporates mechanisms to retry tasks in case of transient failures, ensuring robustness and reliability in task execution.

### Delivery

The execution layer of the messaging system model can be broken down into two main parts. The first is the delivery layer, which is the process of directing the event to the right place or service. The second, the event execution, we’ll get to in a bit.

Routing is the final layer in an asynchronous system, responsible for directing the message out of the system and into the domain where a designated process or lambda function will handle the event. This process or lambda function may be hosted within the same virtual private cloud (VPC) as the messaging infrastructure or may be a part of public clouds like AWS, Azure, etc. In a push-based model, the routing layer is one of the most critical components, similar to the “last mile delivery” in an e-commerce delivery system.

Routing enables many critical functions, including:

  * Message filtering based on subscriber preferences
  * Delivery retries for transient failures
  * Continuously monitoring the health of a subscriber’s event execution hosts, and then routing events only to those that are healthy
  * Dispatching event execution status to the orchestration layer for state machine management
  * Event delivery concurrency management



### Execution

The event execution is the second layer of the primary compute bucket. It’s when the actual task happens, and it’s usually done by a lambda function (i.e., serverless code), or a remote process—potentially even another system or service—that handles the event. In short, the compute layer involves first _routing_ the event and then actually _processing_ it.

Lambda infrastructure refers to the underlying framework responsible for executing events. When an event is triggered, a process is initiated within this infrastructure, which subsequently returns either a success or retriable failure status post-execution. If no status is returned, or if an error occurs, the default assumption is a retriable failure. In this interaction, the router acts as the client, operating under a push model.

Ideally, the executing process operates across multiple cloud environments to enhance reliability. The router has the capability to push events to various clouds based on the locality preference configured by the lambda/process owner. For example, some users may opt to configure their processes to be active in specific clouds to ensure proximity to backend storage dependencies, thereby minimizing cross-data center latency.

Lambda infrastructure should also include autoscaling as part of its features. At Dropbox, our lambda infrastructure [is backed by Atlas](https://dropbox.tech/infrastructure/atlas--our-journey-from-a-python-monolith-to-a-managed-platform), which offers autoscaling capabilities. Additionally, Atlas supports release-time hooks, enabling validation and rollback of code changes if they would potentially degrade service uptime or impact any features negatively.

## Conclusion

Engaging with customers and understanding their requirements and pain points is vital when evolving or reconstructing a major platform component. This approach was instrumental in shaping the blueprint for MSM. By applying first principles, we deconstructed the problem into its smallest components and envisioned a system that delivers the flexibility and extensibility required for the platform. This solid foundation enabled us to rebuild from the ground up with clarity and purpose, ensuring the platform meets current demands while remaining adaptable to future challenges.

This blog has only scratched the surface of the asynchronous platform we’ve built over the past few years, and we’re constantly looking for new ways to improve our infrastructure. We’re excited to, in the future, dive deeper into other critical design decisions that help us build a more efficient and useful Dropbox!

~ ~ ~

_If building innovative products, experiences, and infrastructure excites you, come build the future with us! Visit_[ __dropbox.com/jobs__](https://dropbox.com/jobs) _to see our open roles, and follow @LifeInsideDropbox on_[ __Instagram__](https://www.instagram.com/lifeinsidedropbox/?hl=en) _and_[ __Facebook__](https://www.facebook.com/lifeinsidedropbox/) _to see what it's like to create a more enlightened way of working._

* * *

// Tags   


  * [ Infrastructure ](https://dropbox.tech/infrastructure)
  * [models](https://dropbox.tech/tag-results.models)
  * [Developer](https://dropbox.tech/tag-results.developer)
  * [AI](https://dropbox.tech/tag-results.ai)
  * [Lambda](https://dropbox.tech/tag-results.lambda)
  * [Dash](https://dropbox.tech/tag-results.dash)



// Copy link   


Link copied

![Copy link](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/copy.svg)

  * Link copied

![Copy link](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/copy.svg)
  * [ ![Share on Twitter](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/twitter.svg) ](https://twitter.com/intent/tweet/?text=Evolving%20our%20infrastructure%20through%20the%20messaging%20system%20model%20in%20Dropbox&url=https://dropbox.tech/infrastructure/infrastructure-messaging-system-model-async-platform-evolution)
  * [ ![Share on Facebook](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/facebook.svg) ](https://facebook.com/sharer/sharer.php?u=https://dropbox.tech/infrastructure/infrastructure-messaging-system-model-async-platform-evolution)
  * [ ![Share on Linkedin](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/linkedin.svg) ](https://www.linkedin.com/shareArticle?mini=true&url=https://dropbox.tech/infrastructure/infrastructure-messaging-system-model-async-platform-evolution&title=Evolving%20our%20infrastructure%20through%20the%20messaging%20system%20model%20in%20Dropbox&source=https://dropbox.tech/infrastructure/infrastructure-messaging-system-model-async-platform-evolution)



[ ![Dropbox](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-all/resources/logo_dropbox.svg) ](https://dropbox.com)

  * [ About us ](https://www.dropbox.com/about)
  * [ X ](https://twitter.com/Dropbox)
  * [ Dropbox Dash ](https://dash.dropbox.com/)
  * [ LinkedIn ](https://www.linkedin.com/company/dropbox)
  * [ Jobs ](https://www.dropbox.com/jobs)
  * [ Instagram ](https://www.instagram.com/dropbox)
  * [ Privacy and terms ](https://www.dropbox.com/terms)
  * [ RSS feed ](https://dropbox.tech/feed)
  * [ AI principles ](https://www.dropbox.com/ai-principles)
  * [ Engineering Career Framework ](https://dropbox.tech/culture/our-updated-engineering-career-framework)
  * [ Cookies and CCPA preferences ](https://dropbox.tech/#manage-cookies)
  * [ Blog ](https://blog.dropbox.com/)


