---
title: "Incident Report: April 30th, 2025"
author: "Unknown"
url: "https://blog.railway.com/p/incident-report-april-30-2025"
date: "2025-09-15"
---

![Avatar of Ray Chen](https://s3-us-west-2.amazonaws.com/public.notion-static.com/0af3e5d8-66da-4bc1-a79c-d86752bb5af0/F5A4688F-502D-444E-B007-A01215C4F415.jpg)Ray Chen
Apr 30, 2025
We recently experienced an outage that affected our API backend.
When a Major Outage occurs, it is Railway’s policy to share the public details of what happened.
## [Impact](/p/incident-report-april-30-2025#impact)
This outage impacted our API backend. You may have experienced connection errors if you were using the Railway dashboard ([https://railway.com](https://railway.com/)), the CLI, or Railway’s Public GraphQL API during this period. GitHub-based deployments were also temporarily delayed.
All running deployments and platform-level networking features remained online throughout this period.
## [Incident Timeline](/p/incident-report-april-30-2025#incident-timeline)
[Incident on our Status Page](https://status.railway.com/cma4dbm5h004zt60jp9f8sr0s)
* Around 19:50 UTC: We noticed user reports that the Railway dashboard was not loading. Our health check monitors were also failing
* 20:00 UTC: We called an incident declaring the dashboard to be Partially Degraded. Investigations into the underlying cause started immediately
* 20:36 UTC: We identified some potential issues with recent configuration changes and rolled them back
* 20:36 UTC to 22:11 UTC: We continued our efforts, focusing on full service restoration
* 21:48 UTC: We noticed wider impact than initially anticipated, and upgraded the incident to a Major Outage
* 22:20 UTC: We started seeing full recovery and resolved the incident
* 22:24 UTC: Our health check monitors started failing again
* 22:49 UTC to 23:23 UTC: We started rolling back additional configuration changes
* 23:23 UTC: We started seeing signs of full recovery and continued monitoring user reports and metrics
* 23:40 UTC: Incident resolved and full recovery confirmed
## [What Happened?](/p/incident-report-april-30-2025#what-happened)
Railway’s dashboard, CLI, and Public GraphQL API relies on our API backend. For example:
* When you visit [https://railway.com/dashboard](https://railway.com/dashboard), we load data from our API backend;
* When you run a command (e.g.`railway up`) from the CLI, we issue requests to our API backend;
* When you merge a PR on GitHub, our API backend processes webhooks from GitHub to know when to re-deploy your service with its latest changes.
In the past 3 months, we have been receiving increased amount of reports regarding dashboard latency issues, along with a few other latency-related errors.
During this period, Railway’s rate of signups grew by over 5X. The load on our API backend increased significantly as a result of this growth. To address this, we started an initiative to reduce dashboard latency across the board — this is among our top priorities for Q2’2025.
As part of this work, we made various configuration changes to our API backend’s infrastructure that runs on Kubernetes. We discovered a few issues after investigating the high latency reports:
* We were relying on a service mesh for internal proxy-ing to various other services, even adjacent ones such as our database connection pooler, which has been historically flaky in our experience
* We have many unoptimized SQL queries that were causing unnecessary load on our database
To address the above, we shipped various configuration changes in the past week. The changes we rolled out unfortunately caused this outage.
Our Kubernetes pods were repeatedly crashing with database connection errors some time after they successfully start up. This resulted in a loop where pods come up healthy and start serving traffic before eventually crashing after a few minutes — this is what happened between 22:20 UTC and 22:24 UTC where we thought the incident was resolved, but it actually was not.
Because we modified our healthcheck, it passed without being healthy. The new healthchecks did not account for Postgres liveness, which meant we marked unhealthy instances as healthy, and overloaded our Postgres instance.
After a few unsuccessful attempts at recovery, we decided to fully revert all changes that were made. Despite a full code revert, no recovery was observed.
The database connection issues were traced down to pgbouncer pods (our Postgres connection pooler) that were reporting themselves to be healthy, but was unable to serve any traffic through the service mesh, because the service mesh failed to inject its routing information causing DNS resolution to fail.
Recovery took longer than it should have because we did not know about the service mesh’s behaviour on DNS propagation to pods, and we were rolling back configuration changes selectively.
Even after a full revert, we had to cycle all pods because the service mesh pushed DNS updates that broke other pods’ routing.
At 23:23 UTC, we confirmed the issue was fixed and subsequently resolved the incident at 23:40 UTC after 17 minutes of cautiously monitoring user reports and metrics.
## [Preventative Measures](/p/incident-report-april-30-2025#preventative-measures)
We’re going to continue working on the dashboard latency issues while exercising caution.
To prevent this from happening again, we have made a few changes in how we rollout configuration changes:
* All configuration changes will be appropriately staggered (according to their risk) instead of being rolled out all at once in a short interval
* Each configuration change we rollout will now have a rollback plan, and will be optimized for faster rollbacks in case something goes awry
* If something appears to be off, we will revert full configuration changes immediately instead of selectively
We have also removed the service mesh entirely from our API backend, and we’re going to fully remove it from all critical paths. A service mesh is ultimately a highly dangerous single point of failure that can and should be replaced with simple load balancers.
* * *
Railway is committed to providing the best-in-class cloud experience. Any downtime is unacceptable for us. We apologize for any inconvenience caused by this, and we are going to work towards eliminating the entire class of issues contributing to this incident.
