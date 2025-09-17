---
title: "Improving platform resilience at Cloudflare through automation"
author: "Unknown"
url: "https://blog.cloudflare.com/improving-platform-resilience-at-cloudflare/"
date: "2025-09-15"
---

# Improving platform resilience at Cloudflare through automation

2024-10-09

* [![Opeyemi Onikute](https://blog.cloudflare.com/cdn-cgi/image/format=auto,dpr=3,width=64,height=64,gravity=face,fit=crop,zoom=0.5/https://cf-assets.www.cloudflare.com/zkvhlag99gkb/4JlqK0q5EMuONqQsWp1lMe/862893cec0f15fc80cafb9b0c092e56c/opeyemi.jpeg)](/author/opeyemi/)

[Opeyemi Onikute](/author/opeyemi/)

8 min read

![](https://cf-assets.www.cloudflare.com/zkvhlag99gkb/7FvFSEX52ZrPRMJrE9SmhX/ff490b045cfdc52e117a8c8749b3b3b8/BLOG-2498_1.png)

Failure is an expected state in production systems, and no predictable failure of either software or hardware components should result in a negative experience for users. The exact failure mode may vary, but certain remediation steps must be taken after detection. A common example is when an error occurs on a server, rendering it unfit for production workloads, and requiring action to recover.

When operating at Cloudflare’s scale, it is important to ensure that our platform is able to recover from faults seamlessly. It can be tempting to rely on the expertise of world-class engineers to remediate these faults, but this would be manual, repetitive, unlikely to produce enduring value, and not scaling. In one word: toil; not a viable solution at our scale and rate of growth.

In this post we discuss how we built the foundations to enable a more scalable future, and what problems it has immediately allowed us to solve.

## Growing pains

The Cloudflare [_Site Reliability Engineering (SRE)_](https://en.wikipedia.org/wiki/Site_reliability_engineering) team builds and manages the platform that helps product teams deliver our extensive suite of offerings to customers. One important component of this platform is the collection of servers that power critical products such as Durable Objects, Workers, and DDoS mitigation. We also build and maintain foundational software services that power our product offerings, such as configuration management, provisioning, and IP address allocation systems.

As part of tactical operations work, we are often required to respond to failures in any of these components to minimize impact to users. Impact can vary from lack of access to a specific product feature, to total unavailability. The level of response required is determined by the priority, which is usually a reflection of the severity of impact on users. Lower-priority failures are more common — a server may run too hot, or experience an unrecoverable hardware error. Higher-priority failures are rare and are typically resolved via a well-defined incident response process, requiring collaboration with multiple other teams.

The commonality of lower-priority failures makes it obvious when the response required, as defined in runbooks, is “toilsome”. To reduce this toil, we had previously implemented a plethora of solutions to automate runbook actions such as manually-invoked shell scripts, cron jobs, and ad-hoc software services. These had grown organically over time and provided solutions on a case-by-case basis, which led to duplication of work, tight coupling, and lack of context awareness across the solutions.

We also care about how long it takes to resolve any potential impact on users. A resolution process which involves the manual invocation of a script relies on human action, increasing the Mean-Time-To-Resolve (MTTR) and leaving room for human error. This risks increasing the amount of errors we serve to users and degrading trust.

These problems proved that we needed a way to automatically heal these platform components. This especially applies to our servers, for which failure can cause impact across multiple product offerings. While we have [_mechanisms to automatically steer traffic away_](https://blog.cloudflare.com/unimog-cloudflares-edge-load-balancer) from these degraded servers, in some rare cases the breakage is sudden enough to be visible.

## Solving the problem

To provide a more reliable platform, we needed a new component that provides a common ground for remediation efforts. This would remove duplication of work, provide unified context-awareness and increase development speed, which ultimately saves hours of engineering time and effort.

A good solution would not allow only the SRE team to auto-remediate, it would empower the entire company. The key to adding self-healing capability was a generic interface for all teams to self-service and quickly remediate failures at various levels: machine, service, network, or dependencies.

A good way to think about auto-remediation is in terms of workflows. A workflow is a sequence of steps to get to a desired outcome. This is not dissimilar to a manual shell script which executes what a human would otherwise do via runbook instructions. Because of this logical fit with workflows and durable execution, we decided to adopt an open-source platform called [_Temporal_](https://github.com/temporalio/temporal).

The concept of durable execution is useful to gracefully manage infrastructure failures such as network outages and transient failures in external service endpoints. This capability meant we only needed to build a way to schedule “workflow” tasks and have the code provide reliability guarantees by default, using Temporal. This allowed us to focus on building out the orchestration system to support the control and flow of workflow execution in our data centers.

[_Temporal’s documentation_](https://learn.temporal.io/getting_started/go/first_program_in_go/) provides a good introduction to writing Temporal workflows.

## Building an Automatic Remediation System

Below, we describe how our automatic remediation system works. It is essentially a way to schedule tasks across our global network with built-in reliability guarantees. With this system, teams can serve their customers more reliably. An unexpected failure mode can be recognized and immediately mitigated, while the root cause can be determined later via a more detailed analysis.

### Step one: we need a coordinator

After our initial testing of Temporal, it was now possible to write workflows. But we needed a way to schedule workflow tasks from other internal services. The coordinator was built to serve this purpose, and became the primary mechanism for the authorisation and scheduling of workflows.

The most important roles of the coordinator are authorisation, workflow task routing, and safety constraints enforcement. Each consumer is authorized via [_mTLS authentication_](https://www.cloudflare.com/learning/access-management/what-is-mutual-tls/), and the coordinator uses an ACL to determine whether to permit the execution of a workflow. An ACL configuration looks like the following example.

    server_config {
        enable_tls = true
        [...]
        route_rule {
          name  = "global_get"
          method = "GET"
          route_patterns = ["/*"]
          uris = ["spiffe://example.com/worker-admin"]
        }
        route_rule {
          name = "global_post"
          method = "POST"
          route_patterns = ["/*"]
          uris = ["spiffe://example.com/worker-admin"]
          allow_public = true
        }
        route_rule {
          name = "public_access"
          method = "GET"
          route_patterns = ["/metrics"]
          uris = []
          allow_public = true
          skip_log_match = true
        }
    }

Each workflow specifies two key characteristics: where to run the tasks and the safety constraints, using an [_HCL_](https://github.com/hashicorp/hcl) configuration file. Example constraints could be whether to run on only a specific node type (such as a database), or if multiple parallel executions are allowed: if a task has been triggered too many times, that is a sign of a wider problem that might require human intervention. The coordinator uses the Temporal [_Visibility API_](https://docs.temporal.io/visibility) to determine the current state of the executions in the Temporal cluster.

An example of a configuration file is shown below:

    task_queue_target = "<target>"
    
    # The following entries will ensure that
    # 1. This workflow is not run at the same time in a 15m window.
    # 2. This workflow will not run more than once an hour.
    # 3. This workflow will not run more than 3 times in one day.
    #
    constraint {
        kind = "concurency"
        value = "1"
        period = "15m"
    }
    
    constraint {
        kind = "maxExecution"
        value = "1"
        period = "1h"
    }
    
    constraint {
        kind = "maxExecution"
        value = "3"
        period = "24h"
        is_global = true
    }

### Step two: Task Routing is amazing

An unforeseen benefit of using a central Temporal cluster was the discovery of Task Routing. This feature allows us to schedule a Workflow/Activity on any server that has a running Temporal Worker, and further segment by the type of server, its location, etc. For this reason, we have three primary task queues — the general queue in which tasks can be executed by any worker in the datacenter, the node type queue in which tasks can only be executed by a specific node type in the datacenter, and the individual node queue where we target a specific node for task execution.

We rely on this heavily to ensure the speed and efficiency of automated remediation. Certain tasks can be run in datacenters with known low latency to an external resource, or a node type with better performance than others (due to differences in the underlying hardware). This reduces the amount of failure and latency we see overall in task executions. Sometimes we are also constrained by certain types of tasks that can only run on a certain node type, such as a database.

Task Routing also means that we can configure certain task queues to have a higher priority for execution, although this is not a feature we have needed so far. A drawback of task routing is that every Workflow/Activity needs to be registered to the target task queue, which is a common gotcha. Thankfully, it is possible to catch this failure condition with proper testing.

### Step three: when/how to self-heal?

None of this would be relevant if we didn’t put it to good use. A primary design goal for the platform was to ensure we had easy, quick ways to trigger workflows on the most important failure conditions. The next step was to determine what the best sources to trigger the actions were. The answer to this was simple: we could trigger workflows from anywhere as long as they are properly authorized and detect the failure conditions accurately.

Example triggers are an alerting system, a log tailer, a health check daemon, or an authorized engineer via a chatbot. Such flexibility allows a high level of reuse, and permits to invest more in workflow quality and reliability.

As part of the solution, we built a daemon that is able to poll a signal source for any unwanted condition and trigger a configured workflow. We have initially found [_Prometheus_](https://blog.cloudflare.com/how-cloudflare-runs-prometheus-at-scale) useful as a source because it contains both service-level and hardware/system-level metrics. We are also exploring more event-based trigger mechanisms, which could eliminate the need to use precious system resources to poll for metrics.

We already had internal services that are able to detect widespread failure conditions for our customers, but were only able to page a human. With the adoption of auto-remediation, these systems are now able to react automatically. This ability to create an automatic feedback loop with our customers is the cornerstone of these self-healing capabilities, and we continue to work on stronger signals, faster reaction times, and better prevention of future occurrences.

The most exciting part, however, is the future possibility. Every customer cares about any negative impact from Cloudflare. With this platform we can onboard several services (especially those that are foundational for the critical path) and ensure we react quickly to any failure conditions, even before there is any visible impact.

### Step four: packaging and deployment

The whole system is written in [_golang_](https://go.dev/), and a single binary can implement each role. We distribute it as an apt package or a container for maximum ease of deployment.

We deploy a Temporal-based worker to every server we intend to run tasks on, and a daemon in datacenters where we intend to automatically trigger workflows based on the local conditions. The coordinator is more nuanced since we rely on task routing and can trigger from a central coordinator, but we have also found value in running coordinators locally in the datacenters. This is especially useful in datacenters with less capacity or degraded performance, removing the need for a round-trip to schedule the workflows.

### Step five: test, test, test

Temporal provides native mechanisms to test an entire workflow, via a [_comprehensive test suite_](https://docs.temporal.io/develop/go/testing-suite) that supports end-to-end, integration, and unit testing, which we used extensively to prevent regressions while developing. We also ensured proper test coverage for all the critical platform components, especially the coordinator.

Despite the ease of written tests, we quickly discovered that they were not enough. After writing workflows, engineers need an environment as close as possible to the target conditions. This is why we configured our staging environments to support quick and efficient testing. These environments receive the latest changes and point to a different (staging) Temporal cluster, which enables experimentation and easy validation of changes.

After a workflow is validated in the staging environment, we can then do a full release to production. It seems obvious, but catching simple configuration errors before releasing has saved us many hours in development/change-related-task time.

## Deploying to production

As you can guess from the title of this post, we put this in production to automatically react to server-specific errors and unrecoverable failures. To this end, we have a set of services that are able to detect single-server failure conditions based on analyzed traffic data. After deployment, we have successfully mitigated potential impact by taking any errant single sources of failure out of production.

We have also created a set of workflows to reduce internal toil and improve efficiency. These workflows can automatically test pull requests on target machines, wipe and reset servers after experiments are concluded, and take away manual processes that cost many hours in toil.

Building a system that is maintained by several SRE teams has allowed us to iterate faster, and rapidly tackle long-standing problems. We have set ambitious goals regarding toil elimination and are on course to achieve them, which will allow us to scale faster by eliminating the human bottleneck.

## Looking to the future

Our immediate plans are to leverage this system to provide a more reliable platform for our customers and drastically reduce operational toil, freeing up engineering resources to tackle larger-scale problems. We also intend to leverage more Temporal features such as [_Workflow Versioning_](https://docs.temporal.io/develop/go/versioning), which will simplify the process of making changes to workflows by ensuring that triggered workflows run expected versions.

We are also interested in how others are solving problems using durable execution platforms such as Temporal, and general strategies to eliminate toil. If you would like to discuss this further, feel free to reach out on the [_Cloudflare Community_](https://community.cloudflare.com) and start a conversation!

If you’re interested in contributing to projects that help build a better Internet, [_our engineering teams are hiring_](https://www.cloudflare.com/en-gb/careers/jobs/?department=Engineering&location=default).

Cloudflare's connectivity cloud protects [entire corporate networks](https://www.cloudflare.com/network-services/), helps customers build [Internet-scale applications efficiently](https://workers.cloudflare.com/), accelerates any [website or Internet application](https://www.cloudflare.com/performance/accelerate-internet-applications/), [wards off DDoS attacks](https://www.cloudflare.com/ddos/), keeps [hackers at bay](https://www.cloudflare.com/application-security/), and can help you on [your journey to Zero Trust](https://www.cloudflare.com/products/zero-trust/).

Visit [1.1.1.1](https://one.one.one.one/) from any device to get started with our free app that makes your Internet faster and safer.

To learn more about our mission to help build a better Internet, [start here](https://www.cloudflare.com/learning/what-is-cloudflare/). If you're looking for a new career direction, check out [our open positions](https://www.cloudflare.com/careers).

[Discuss on Hacker News](https://news.ycombinator.com/submitlink?u=https://blog.cloudflare.com/improving-platform-resilience-at-cloudflare "Discuss on Hacker News")

[Edge](/tag/edge/)[Engineering](/tag/engineering/)[Serverless](/tag/serverless/)[Developer Platform](/tag/developer-platform/)[Developers](/tag/developers/)[Go](/tag/go/)[Reliability](/tag/reliability/)[Speed & Reliability](/tag/speed-and-reliability/)
