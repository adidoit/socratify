---
title: "Incident Report: June 6th, 2025"
author: "Unknown"
url: "https://blog.railway.com/p/incident-report-june-6-2025"
date: "2025-09-15"
---

![Avatar of Jake Cooper](https://s3-us-west-2.amazonaws.com/public.notion-static.com/535761c1-ecdb-4bed-b7c5-91f7eeb44bd4/Screen_Shot_2021-06-08_at_11.08.11_AM.png)Jake Cooper

Jun 6, 2025

We recently experienced an outage that affected our GitHub Login and Backend API

When outages occur, it is Railway’s policy to document them.

## [Impact](/p/incident-report-june-6-2025#impact)

This outage impacted the dashboard and the login/authentication functionality. While it did not affect overall deployments (or webhook based builds), users who attempted to access the dashboard during this period may have seen slow requests and in some situations outright timeouts, prompting them to re-authenticate

Upon clicking re-authenticate via GitHub, sessions were cleared and users were fully logged out. During this time, GitHub rate limits were in affect, preventing new logins (while previously logged in sessions remained valid)

## [Incident Timeline](/p/incident-report-june-6-2025#incident-timeline)

[Incident on our Status Page](https://status.railway.com/cma4dbm5h004zt60jp9f8sr0s)

* [4:31pm UTC] We were notified of imminent connection exhaustion on our primary database, resulting in request delays
* [4:34pm UTC] We identified high CPU usage in our pooling layer, following a periodic pattern every 5 minutes
* [5:08pm UTC] Incident called after users were unable to login to GitHub
* [6:49pm UTC] Logins restored
* [6:58pm UTC] Incident resolved
* [7:41pm UTC] Incident re-opened upon reports of further failed logins
* [9:00pm UTC] Partial recovery started
* [9:16pm UTC] Full recovery completed
* [9:57pm UTC] Incident closed after extended monitoring

## [What Happened?](/p/incident-report-june-6-2025#what-happened)

Railway has been scaling rapidly over the past 6 months. Due to this new influx of users, pressure was applied to our primary database.

We were notified of this pressure at 8:31am PST and performed the runbook action to scale out our systems.

Should full connection exhaustion occur, Railway has circuit breakers designed to prevent further degradation.

When our backend circuit breakers triggered, aggressive websocket reconnect logic initiated on every connected client at once, further overwhelming an already stressed database.

Websocket handshakes were not configured under our WAF policy, and, as a result, hundreds of thousands of users bypassed our firewall rules, resulting in millions of requests to our backend, preventing it from renegotiating connections.

When the frontend is unable to reconnect, it serves the default login page.

As we served this default page to any user who saw timed out request, this not only invalidated their session (preventing them from logging in), but it also created a massive amount of traffic to GitHub’s OAuth endpoints, causing GitHub to trigger a secondary rate limit on Railway’s OAuth app.

We rolled out changes to reduce the exponential backoff from clients. However, due to the nature of client server architecture, unless the user refreshed the page, they would still have the aggressive websocket retry.

This week, we renegotiated our contract with our upstream WAF vendor. However, in upgrading our account, they failed to add the required permission to modify or add new WAF rules. As a result, during this incident, we could not mitigate the attack vector.

If the backend was restored, the flood of requests from stale clients caused further degradation to all other users.

If the circuit breaker were tripped, the page serving the GitHub Login, which sent traffic to GitHub causing them to rate limit us.

In lieu of degrading the experience for all, we opted to slowly roll out our own login OAuth rate limiting on top of GitHub’s to re-login any logged out clients to offgas the session renegotiation.

## [Preventative Measures](/p/incident-report-june-6-2025#preventative-measures)

So far we’ve rolled out:

* GitHub Login Bottleneck and Rate limit queues
* Websocket reconnect logic backoff on our frontend
* Modified rate limiting rules to handle errant websocket reconnect logic
* Real-time logic now utilizes our read replica instead of the primary

Within the next 24 hours we will be rolling out:

* WAF rules API testing to notify us of provider configuration failures
* Serving the login buttons only if the backend is ready to service them

* * *

Railway is committed to providing the best-in-class cloud experience. Any downtime is unacceptable for us. We apologize for any inconvenience caused by this, and we are going to work towards eliminating the entire class of issues contributing to this incident.
