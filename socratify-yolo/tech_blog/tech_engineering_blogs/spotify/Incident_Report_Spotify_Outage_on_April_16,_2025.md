---
title: "Incident Report: Spotify Outage on April 16, 2025"
author: "Unknown"
url: "https://engineering.atspotify.com/2025/5/incident-report-spotify-outage-on-april-16-2025/"
published_date: "Unknown"
downloaded_date: "2025-09-15T10:17:21.072857"
company: "spotify"
---

# Incident Report: Spotify Outage on April 16, 2025
![Feature Image](/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fp762jor363g1%2Fattachment_0dc2fa8d257ba108e0e23876295600bf%2Fba4b5a83829eeab9a308a8f1d100cb3e%2Fattachment_0dc2fa8d257ba108e0e23876295600bf.png&w=1920&q=75)
On April 16, Spotify experienced an outage that affected users worldwide. Here is what happened and what we are going to do about it.
## Context
We use [Envoy Proxy](https://www.envoyproxy.io/) for our networking perimeter systems. The perimeter is the first piece of our software that receives users (your!) network traffic. It then distributes that traffic to other services. We use cloud regions to distribute that traffic sensibly across the globe.
To enhance Envoy's capabilities, we develop and integrate our own custom filters. A specific example is our filter for [rate limiting](https://en.wikipedia.org/wiki/Rate_limiting), which we discussed in detail during our [recent talk at EnvoyCon 2025](https://www.youtube.com/watch?v=Bof1ZAk1Ca8).
## What happened?
On April 16 2025, between 12:20 and 15:45 UTC, we experienced an outage, affecting the majority of our users worldwide. During the incident most traffic was disrupted, except to our Asia Pacific region due to timezone differences. The graph below shows the amount of successful requests on our perimeter, the purple line is the unaffected Asia Pacific region.
![attachment_5ef29b7880669d51adf755312fe1f5e3](//images.ctfassets.net/p762jor363g1/attachment_5ef29b7880669d51adf755312fe1f5e3/148b740ce3d8a045886e1071efcab36c/attachment_5ef29b7880669d51adf755312fe1f5e3.jpg)
_Graph showing the amount of successful requests on our perimeter_
## What caused this outage?
On the day of the incident we changed the order of our [Envoy filters](https://github.com/envoyproxy/envoy/blob/main/source/docs/async_http_filters.md). This change was deemed low risk and as such we applied it to all regions at the same time. Changing the order triggered a bug in one of our filters which in turn caused Envoy to crash. Unlike typical isolated crashes, this crash happened simultaneously on all Envoy instances.
The immediate restart of all Envoy instances, combined with client side application retry logic, created an unprecedented load spike for the perimeter. The sudden surge in traffic then exposed a misconfiguration. Envoy instances were continuously cycled by Kubernetes as the [Envoy max heap size](https://www.envoyproxy.io/docs/envoy/latest/configuration/operations/overload_manager/overload_manager) was set higher than the allowed [memory limit](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#requests-and-limits). As soon as any new Envoy instance started up it received a very large amount of traffic, which in turn caused it to use more than the allowed Kubernetes memory limit. Kubernetes then automatically shut down the instance and the cycle repeated.
Lower traffic in our Asia Pacific region at the time of the incident, due to the difference in timezone and time of day, meant the regional Envoy memory usage never reached the kubernetes limit, which is why this region was unaffected.
The outage was mitigated by increasing the total perimeter server capacity which in turn allowed the Envoy servers to drop under the Kubernetes memory limits. This in turn stopped the continuous cycling of servers.
## Timeline
12:18 UTC - Envoy filter order changed and all Envoy instances crash
12:20 UTC - Alarms are triggered indicating a significant drop of incoming traffic
12:28 UTC - Situation escalated, no traffic worldwide except for the Asia Pacific region
14:20 UTC - Traffic fully recovered in the European regions
15:10 UTC - Traffic fully recovered in the US regions
15:40 UTC - All traffic patterns back to normal
## Where do we go from here?
We recognize the impact such outages can have, and we’re committed to learning from it. Here are the steps we’re taking to improve our systems and prevent similar issues in the future;
* We have fixed the bug causing Envoy to crash
* We have fixed the configuration mismatch between Envoy heap size and Kubernetes memory limits
* We will improve how we roll out configuration changes to our perimeter
* We will improve our monitoring capabilities to be able to catch these issues sooner
As we have in the past, we will continue to provide transparency on similar occasions so as to hold ourselves accountable and support ongoing improvements to our services.
Tags: [backend](/tag/backend), [Mobile](/tag/mobile)