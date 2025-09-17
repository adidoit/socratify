---
title: "Load Testing with Impulse at Airbnb | by Chenhao Yang | The Airbnb Tech Blog"
author: "Unknown"
url: "https://medium.com/airbnb-engineering/load-testing-with-impulse-at-airbnb-f466874d03d2?source=rss----53c7c27702d5---4"
date: "2025-09-15"
---

# Load Testing with Impulse at Airbnb

[![Chenhao Yang](https://miro.medium.com/v2/resize:fill:64:64/0*gj-Rpi1dOmxDue6y.jpg)](/@chenhao.yang?source=post_page---byline--f466874d03d2---------------------------------------)

[Chenhao Yang](/@chenhao.yang?source=post_page---byline--f466874d03d2---------------------------------------)

8 min read

·

Jun 9, 2025

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fairbnb-engineering%2Ff466874d03d2&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fload-testing-with-impulse-at-airbnb-f466874d03d2&user=Chenhao+Yang&userId=19684187c790&source=---header_actions--f466874d03d2---------------------clap_footer------------------)

\--

2

[](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Ff466874d03d2&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fairbnb-engineering%2Fload-testing-with-impulse-at-airbnb-f466874d03d2&source=---header_actions--f466874d03d2---------------------bookmark_footer------------------)

Listen

Share

Comprehensive Load Testing with Load Generator, Dependency Mocker, Traffic Collector, and More

Press enter or click to view image in full size

Authors: [Chenhao Yang](https://www.linkedin.com/in/chenhao-yang-9799b022/), [Haoyue Wang](https://www.linkedin.com/in/haoyue-wang-a722509a/), [Xiaoya Wei](https://www.linkedin.com/in/xiaoyawei/), [Zay Guan](https://www.linkedin.com/in/zhijie-guan/), [Yaolin Chen](https://www.linkedin.com/in/yaolin-chen-591a31339/) and [Fei Yuan](https://www.linkedin.com/in/fei-yuan/)

System-level load testing is crucial for reliability and efficiency. It identifies bottlenecks, evaluates capacity for peak traffic, establishes performance baselines, and detects errors. At a company of Airbnb’s size and complexity, we’ve learned that load testing needs to be robust, flexible, and decentralized. This requires the right set of tools to enable engineering teams to do self-service load tests that integrate seamlessly with CI.

Impulse is one of our internal load-testing-as-a-service frameworks. It provides tools that can generate synthetic loads, mock dependencies, and collect traffic data from production environments. In this blog post, we’ll share how Impulse is architected to minimize manual effort, seamlessly integrate with our observability stack, and empower teams to proactively address potential issues.

## Architecture

Impulse is a comprehensive load testing framework that allows service owners to conduct context-aware load tests, mock dependencies, and collect traffic data to ensure the system’s performance under various conditions. It includes the following components:

1.**Load generator**to generate context-aware requests on the fly, for testing different scenarios with synthetic or collected traffic.
2.**Dependency mocker**to mock the downstream responses with latency, so that the load testing on the service under test (SUT) doesn’t need to involve certain dependent services. This is especially crucial when the dependencies are vendor services that don’t support load testing, or if the team wants to regression load test their service during day-to-day deployment without affecting downstreams.
3.**Traffic collector**to collect both the upstream and downstream traffic from the production environment, and then apply the resulting data to the test environment.
4.**Testing API generator**to wrap asynchronous workflows into synchronous API calls for load testing.

Press enter or click to view image in full size

Figure 1: The Impulse framework and its four main components

Each of these four tools are independent, allowing service owners the flexibility to select one or more components for their load testing needs.

### Load generator

Press enter or click to view image in full size

Figure 2: Containerized load generator

_Context aware_

When load testing, requests made to the SUT often require some information from the previous response or need to be sent in a specific order. For example, if an update API needs to provide an _entity_id_ to update, we must ensure the entity already exists in the testing environment context.

Our load generator tool allows users to write arbitrary testing logic in Java or Kotlin and launch containers to run these tests at scale against the SUT. Why write code instead of DSL/configuration logic?

* Flexibility: Programming languages are more expressive than DSL and can better support complex contextual scenarios.
* Reusability: The same testing code can be used in other tests, e.g., integration tests.
* Developer proficiency: Low/no learning curve to onboard, don’t need to learn how to write testing logic.
* Developer experience: IDE support, testing, debugging, etc.

Here is an example of synthetic context-aware test case:

    class HelloWorldLoadGenerator : LoadGenerator {  
       override suspend fun run() {  
           val createdEntity = sutApiClient.create(CreateRequest(name="foo", ...)).data  
      
           // request with id from previous response (context)  
           val updateResponse = sutApiClient.update(UpdateRequest(id=createdEntity.id, name="bar"))  
             
           // ... other operations  
             
           // clean up  
           sutApiClient.delete(DeleteRequest(id=createdEntity.id))  
       }  
    }

_Decentralized_

The load generator is decentralized and containerized, which means each time a load test is triggered, a set of new containers will be created to run the test. This design has several benefits:

* Isolation: Load testing runs between different services are isolated from each other, eliminating any interference.
* Scalability: The number of containers can be scaled up or down according to the traffic requirements.
* Cost efficiency: The containers are short-lived, as they only exist during the load testing run.

What’s more, as our services are cloud based, a subtle point is that the Impulse framework will evenly distribute the workers among all our data centers, and the load will be emitted evenly from all the workers. Impulse’s load generator ensures the overall trigger per second (TPS) is as configured. Based on this, we can better leverage the locality settings in load balancers, which can better mimic the real traffic distribution in production.

_Execution_

The load generator is designed to be executed in the CI/CD pipeline, which means we can trigger load testing automatically. Developers can configure the testing spec in multiple phases, e.g., a warm up phase, a steady state phase, a peak phase, etc. Each phase can be configured with:

* Test cases to run
* TPS (trigger per second) of each test case
* Test duration

### Dependency mocker

Press enter or click to view image in full size

Figure 3: Dependency mocker

Impulse is a decentralized framework where each service has its own dependency mocker. This can eliminate interference between services and reduce communication costs. Each dependency mocker is an out-of-process service, which means the SUT behaves just as it does in production. We run the mockers in separate instances to avoid any impact on the performance of the SUT. The mock servers are all short lived — they only start before tests run and shut down afterwards to save costs and maintenance effort. The response latency and exceptions are configurable and the number of mocker instances can be adjusted on demand to support large amounts of traffic.

Other noteworthy features:

* You can selectively stub some of the dependencies. Currently, stubbing is supported for HTTP JSON, Airbnb Thrift, and Airbnb GraphQL dependencies.
* The dependency mockers support use cases beyond load testing. For instance, integration tests often rely on other services or third-party API calls, which may not guarantee a stable testing environment or might only support ideal scenarios. Dependency mockers can address this by offering predefined responses or exceptions to fully test those flows.

Impulse supports two options for generating mock responses:

1. Synthetic response: The response is generated by user logic, as in integration testing; the difference is that the response comes from a remote (out-of-process) server with simulated latency.
\- Similar to the load generator, the logic is written in Java/Kotlin code and contains request matching and response generation.
\- Latency can be simulated using p95/p99 metrics.
2. Replay response: The response is replayed from the production downstream recording, supported by the traffic collector component.

Here is an example of a synthetic response with latency in Kotlin:

    downstreamsMocking.every(  
          thriftRequest<FooRequest>().having { it.message == "hello" }  
        ).returns { request ->  
          ThriftDownstream.Response.thriftEncoded(  
            HttpStatus.OK,  
            FooResponse.builder.reply("${request.message} world").build()  
          )  
        }.with {  
          delay = latencyFromP95(p95=500.miliseconds, min=200.miliseconds, max=2000.miliseconds)  
        }

### Traffic collector

Press enter or click to view image in full size

Figure 4: Traffic collector

The traffic collector component is designed to capture both upstream and downstream traffic, along with the relationships between them. This approach allows Impulse to accurately replay production traffic during load testing, avoiding inconsistencies in downstream data or behavior. By replicating downstream responses — including production-like latency and errors — via the dependency mocker, the system ensures high-fidelity load testing. As a result, services in the testing environment behave identically to those in production, enabling more realistic and reliable performance evaluations.

### Testing API generator

We rely heavily on event-driven, asynchronous workflows that are critical to our business operations. These include processing events from a message queue (MQ) and executing delayed jobs. Most of the MQ events/jobs are emitted from synchronous flows (e.g., API calls), so theoretically they can be covered by API load testing. However, the real world is more complex. These asynchronous flows often involve long chains of event and job emissions originating from various sources, making it difficult to replicate and test them accurately using only API-based methods.

To address this, the testing API generator component creates HTTP APIs during the CI stage according to the event or job schema. These APIs act as wrappers around the underlying asynchronous flows and are registered exclusively in the testing environment. This setup enables load testing tools — such as load generators — to send traffic to these synthetic APIs, allowing asynchronous flows to be exercised as if they were synchronous. As a result, it’s possible to perform targeted, realistic load testing on asynchronous logic that would otherwise be hard to simulate.

Figure 5: Testing API generator for async flows

The goal of the testing API generator is to help developers identify performance bottlenecks and potential issues in their async flow implementations and under high traffic conditions. It does this by enabling direct load testing of async flows without involving middleware components like MQs. The rationale is that developers typically aim to evaluate the behavior of their own logic, not the middleware, which is usually already well-tested. By bypassing these components, this approach simplifies the load testing process and empowers developers to independently manage and execute their own tests.

### Integration with other testing frameworks

Airbnb emphasizes product quality, utilizing versatile testing frameworks that cover integration and API tests across development, staging, and production environments, and integrate smoothly into CI/CD pipelines. The modular design of Impulse facilitates its integration with these frameworks, offering systematic service testing.

Press enter or click to view image in full size

Figure 6: How Impulse interfaces with other internal testing frameworks

## Conclusion

In this blog post, we shared how Impulse and its four core components help developers perform self-service load testing at Airbnb. As of this writing, Impulse has been implemented in several customer support backend services and is currently under review with different teams across the company who are planning to leverage Impulse to conduct load testing.

We’ve received a lot of good feedback in the process. For example: “ _Impulse helps us to identify and address potential issues in our service. During testing, it detected an ApiClientThreadToolExhaustionException caused by thread pool pressure. Additionally, it alerted us about occasional timeout errors in client API calls during service deployments. Impulse helped us identify high memory usage in the main service container, enabling us to fine-tune the memory allocation and optimize our service’s resource usage. Highly recommend utilizing Impulse as an integral part of the development and testing processes._ ”

## Acknowledgments

Thanks to Jeremy Werner, Yashar Mehdad, Raj Rajagopal, Claire Cheng, Tim L., Wei Ji, Jay Wu, Brian Wallace for support on the Impulse project.

Does this type of work interest you? Check out our open roles [here](https://careers.airbnb.com/).
