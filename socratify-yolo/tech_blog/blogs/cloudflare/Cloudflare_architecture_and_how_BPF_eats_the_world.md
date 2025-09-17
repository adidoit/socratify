---
title: "Cloudflare architecture and how BPF eats the world"
company: "cloudflare"
url: "https://blog.cloudflare.com/cloudflare-architecture-and-how-bpf-eats-the-world/"
content_length: 14832
type: "manual_premium_harvest"
premium: true
curated: true
date: "2025-09-15"
---

# Cloudflare architecture and how BPF eats the world

2019-05-18

  * [![Marek Majkowski](https://blog.cloudflare.com/cdn-cgi/image/format=auto,dpr=3,width=64,height=64,gravity=face,fit=crop,zoom=0.5/https://cf-assets.www.cloudflare.com/zkvhlag99gkb/1JuU5qavgwVeqR8BAUrd6U/3a0d0445d41c9a3c42011046efe9c37b/marek-majkowski.jpeg)](/author/marek-majkowski/)

[Marek Majkowski](/author/marek-majkowski/)




7 min read

This post is also available in [简体中文](/zh-cn/cloudflare-architecture-and-how-bpf-eats-the-world), [Deutsch](/de-de/cloudflare-architecture-and-how-bpf-eats-the-world), [Español](/es-es/cloudflare-architecture-and-how-bpf-eats-the-world) and [Français](/fr-fr/cloudflare-architecture-and-how-bpf-eats-the-world).

![](https://cf-assets.www.cloudflare.com/zkvhlag99gkb/3U9o2wDqtM0igvB2yasO3s/5f9173ea6599de3db0c7823da7391990/cloudflare-architecture-and-how-bpf-eats-the-world.jpg)

Recently at [Netdev 0x13](https://www.netdevconf.org/0x13/schedule.html), the Conference on Linux Networking in Prague, I gave [a short talk titled "Linux at Cloudflare"](https://netdevconf.org/0x13/session.html?panel-industry-perspectives). The [talk](https://speakerdeck.com/majek04/linux-at-cloudflare) ended up being mostly about BPF. It seems, no matter the question - BPF is the answer.

Here is a transcript of a slightly adjusted version of that talk.

* * *

At Cloudflare we run Linux on our servers. We operate two categories of data centers: large "Core" data centers, processing logs, analyzing attacks, computing analytics, and the "Edge" server fleet, delivering customer content from 180 locations across the world.

In this talk, we will focus on the "Edge" servers. It's here where we use the newest Linux features, optimize for performance and care deeply about DoS resilience.

* * *

Our edge service is special due to our network configuration - we are extensively using anycast routing. Anycast means that the same set of IP addresses are announced by all our data centers.

This design has great advantages. First, it guarantees the optimal speed for end users. No matter where you are located, you will always reach the closest data center. Then, anycast helps us to spread out DoS traffic. During attacks each of the locations receives a small fraction of the total traffic, making it easier to ingest and filter out unwanted traffic.

* * *

Anycast allows us to keep the networking setup uniform across all edge data centers. We applied the same design inside our data centers - our software stack is uniform across the edge servers. All software pieces are running on all the servers.

In principle, every machine can handle every task - and we run many diverse and demanding tasks. We have a full HTTP stack, the magical [Cloudflare Workers](https://www.cloudflare.com/developer-platform/workers/), two sets of DNS servers - authoritative and resolver, and many other publicly facing applications like [Spectrum](https://www.cloudflare.com/application-services/products/cloudflare-spectrum/) and [Warp](https://www.cloudflare.com/learning/dns/what-is-1.1.1.1/).

Even though every server has all the software running, requests typically cross many machines on their journey through the stack. For example, an HTTP request might be handled by a different machine during each of the 5 stages of the processing.

* * *

Let me walk you through the early stages of inbound packet processing:

(1) First, the packets hit our router. The router does ECMP, and forwards packets onto our Linux servers. We use ECMP to spread each target IP across many, at least 16, machines. This is used as a rudimentary load balancing technique.

(2) On the servers we ingest packets with XDP eBPF. In XDP we perform two stages. First, we run volumetric [DoS mitigations](https://www.cloudflare.com/learning/ddos/ddos-mitigation/), dropping packets belonging to very large layer 3 attacks.

(3) Then, still in XDP, we perform layer 4 [load balancing](https://www.cloudflare.com/learning/performance/what-is-load-balancing/). All the non-attack packets are redirected across the machines. This is used to work around the ECMP problems, gives us fine-granularity load balancing and allows us to gracefully take servers out of service.

(4) Following the redirection the packets reach a designated machine. At this point they are ingested by the normal Linux networking stack, go through the usual iptables firewall, and are dispatched to an appropriate network socket.

(5) Finally packets are received by an application. For example HTTP connections are handled by a "protocol" server, responsible for performing TLS encryption and processing HTTP, HTTP/2 and QUIC protocols.

It's in these early phases of request processing where we use the coolest new Linux features. We can group useful modern functionalities into three categories:

  * DoS handling

  * Load balancing

  * Socket dispatch




* * *

Let's discuss DoS handling in more detail. As mentioned earlier, the first step after ECMP routing is Linux's XDP stack where, among other things, we run DoS mitigations.

Historically our mitigations for volumetric attacks were expressed in classic BPF and iptables-style grammar. Recently we adapted them to execute in the XDP eBPF context, which turned out to be surprisingly hard. Read on about our adventures:

  * [L4Drop: XDP DDoS Mitigations](/l4drop-xdp-ebpf-based-ddos-mitigations/)

  * [xdpcap: XDP Packet Capture](/xdpcap/)

  * [XDP based DoS mitigation](https://netdevconf.org/0x13/session.html?talk-XDP-based-DDoS-mitigation) talk by Arthur Fabre

  * [XDP in practice: integrating XDP into our DDoS mitigation pipeline](https://netdevconf.org/2.1/papers/Gilberto_Bertin_XDP_in_practice.pdf) (PDF)




During this project we encountered a number of eBPF/XDP limitations. One of them was the lack of concurrency primitives. It was very hard to implement things like race-free token buckets. Later we found that [Facebook engineer Julia Kartseva](http://vger.kernel.org/lpc-bpf2018.html#session-9) had the same issues. In February this problem has been addressed with the introduction of `bpf_spin_lock` helper.

* * *

While our modern volumetric DoS defenses are done in XDP layer, we still rely on `iptables` for application layer 7 mitigations. Here, a higher level firewall’s features are useful: connlimit, hashlimits and ipsets. We also use the `xt_bpf` iptables module to run cBPF in iptables to match on packet payloads. We talked about this in the past:

  * [Lessons from defending the indefensible](https://speakerdeck.com/majek04/lessons-from-defending-the-indefensible) (PPT)

  * [Introducing the BPF tools](/introducing-the-bpf-tools/)




* * *

After XDP and iptables, we have one final kernel side DoS defense layer.

Consider a situation when our UDP mitigations fail. In such case we might be left with a flood of packets hitting our application UDP socket. This might overflow the socket causing packet loss. This is problematic - both good and bad packets will be dropped indiscriminately. For applications like DNS it's catastrophic. In the past to reduce the harm, we ran one UDP socket per IP address. An unmitigated flood was bad, but at least it didn't affect the traffic to other server IP addresses.

Nowadays that architecture is no longer suitable. We are running more than 30,000 DNS IP's and running that number of UDP sockets is not optimal. Our modern solution is to run a single UDP socket with a complex eBPF socket filter on it - using the `SO_ATTACH_BPF` socket option. We talked about running eBPF on network sockets in past blog posts:

  * [eBPF, Sockets, Hop Distance and manually writing eBPF assembly](/epbf_sockets_hop_distance/)

  * [SOCKMAP - TCP splicing of the future](/sockmap-tcp-splicing-of-the-future/)




The mentioned eBPF rate limits the packets. It keeps the state - packet counts - in an eBPF map. We can be sure that a single flooded IP won't affect other traffic. This works well, though during work on this project we found a rather worrying bug in the eBPF verifier:

  * [eBPF can't count?!](/ebpf-cant-count/)




I guess running eBPF on a UDP socket is not a common thing to do.

* * *

Apart from the DoS, in XDP we also run a layer 4 load balancer layer. This is a new project, and we haven't talked much about it yet. Without getting into many details: in certain situations we need to perform a socket lookup from XDP.

The problem is relatively simple - our code needs to look up the "socket" kernel structure for a 5-tuple extracted from a packet. This is generally easy - there is a `bpf_sk_lookup` helper available for this. Unsurprisingly, there were some complications. One problem was the inability to verify if a received ACK packet was a valid part of a three-way handshake when SYN-cookies are enabled. My colleague Lorenz Bauer is working on adding support for this corner case.

* * *

After DoS and the load balancing layers, the packets are passed onto the usual Linux TCP / UDP stack. Here we do a socket dispatch - for example packets going to port 53 are passed onto a socket belonging to our DNS server.

We do our best to use vanilla Linux features, but things get complex when you use thousands of IP addresses on the servers.

Convincing Linux to route packets correctly is relatively easy with [the "AnyIP" trick](/how-we-built-spectrum). Ensuring packets are dispatched to the right application is another matter. Unfortunately, standard Linux socket dispatch logic is not flexible enough for our needs. For popular ports like TCP/80 we want to share the port between multiple applications, each handling it on a different IP range. Linux doesn't support this out of the box. You can call `bind()` either on a specific IP address or all IP's (with 0.0.0.0).

* * *

In order to fix this, we developed a custom kernel patch which adds [a `SO_BINDTOPREFIX` socket option](http://patchwork.ozlabs.org/patch/602916/). As the name suggests - it allows us to call `bind()` on a selected IP prefix. This solves the problem of multiple applications sharing popular ports like 53 or 80.

Then we run into another problem. For our Spectrum product we need to listen on all 65535 ports. Running so many listen sockets is not a good idea (see [our old war story blog](/revenge-listening-sockets/)), so we had to find another way. After some experiments we learned to utilize an obscure iptables module - TPROXY - for this purpose. Read about it here:

  * [Abusing Linux's firewall: the hack that allowed us to build Spectrum](/how-we-built-spectrum/)




This setup is working, but we don't like the extra firewall rules. We are working on solving this problem correctly - actually extending the socket dispatch logic. You guessed it - we want to extend socket dispatch logic by utilizing eBPF. Expect some patches from us.

* * *

Then there is a way to use eBPF to improve applications. Recently we got excited about doing TCP splicing with SOCKMAP:

  * [SOCKMAP - TCP splicing of the future](/sockmap-tcp-splicing-of-the-future/)




This technique has a great potential for improving tail latency across many pieces of our software stack. The current SOCKMAP implementation is not quite ready for prime time yet, but the potential is vast.

Similarly, the new [TCP-BPF aka BPF_SOCK_OPS](https://netdevconf.org/2.2/papers/brakmo-tcpbpf-talk.pdf) hooks provide a great way of inspecting performance parameters of TCP flows. This functionality is super useful for our performance team.

* * *

Some Linux features didn't age well and we need to work around them. For example, we are hitting limitations of networking metrics. Don't get me wrong - the networking metrics are awesome, but sadly they are not granular enough. Things like `TcpExtListenDrops` and `TcpExtListenOverflows` are reported as global counters, while we need to know it on a per-application basis.

Our solution is to use eBPF probes to extract the numbers directly from the kernel. My colleague Ivan Babrou wrote a Prometheus metrics exporter called "ebpf_exporter" to facilitate this. Read on:

  * [Introducing ebpf_exporter](/introducing-ebpf_exporter/)

  * <https://github.com/cloudflare/ebpf_exporter>




With "ebpf_exporter" we can generate all manner of detailed metrics. It is very powerful and saved us on many occasions.

* * *

In this talk we discussed 6 layers of BPFs running on our edge servers:

  * Volumetric DoS mitigations are running on XDP eBPF

  * Iptables `xt_bpf` cBPF for application-layer attacks

  * `SO_ATTACH_BPF` for rate limits on UDP sockets

  * Load balancer, running on XDP

  * eBPFs running application helpers like SOCKMAP for TCP socket splicing, and TCP-BPF for TCP measurements

  * "ebpf_exporter" for granular metrics




And we're just getting started! Soon we will be doing more with eBPF based socket dispatch, eBPF running on [Linux TC (Traffic Control)](https://linux.die.net/man/8/tc) layer and more integration with cgroup eBPF hooks. Then, our SRE team is maintaining ever-growing list of [BCC scripts](https://github.com/iovisor/bcc) useful for debugging.

It feels like Linux stopped developing new API's and all the new features are implemented as eBPF hooks and helpers. This is fine and it has strong advantages. It's easier and safer to upgrade eBPF program than having to recompile a kernel module. Some things like TCP-BPF, exposing high-volume performance tracing data, would probably be impossible without eBPF.

Some say "software is eating the world", I would say that: "BPF is eating the software".

Cloudflare's connectivity cloud protects [entire corporate networks](https://www.cloudflare.com/network-services/), helps customers build [Internet-scale applications efficiently](https://workers.cloudflare.com/), accelerates any [website or Internet application](https://www.cloudflare.com/performance/accelerate-internet-applications/), [wards off DDoS attacks](https://www.cloudflare.com/ddos/), keeps [hackers at bay](https://www.cloudflare.com/application-security/), and can help you on [your journey to Zero Trust](https://www.cloudflare.com/products/zero-trust/).  
  
Visit [1.1.1.1](https://one.one.one.one/) from any device to get started with our free app that makes your Internet faster and safer.  
  
To learn more about our mission to help build a better Internet, [start here](https://www.cloudflare.com/learning/what-is-cloudflare/). If you're looking for a new career direction, check out [our open positions](https://www.cloudflare.com/careers).

[Discuss on Hacker News](https://news.ycombinator.com/submitlink?u=https://blog.cloudflare.com/cloudflare-architecture-and-how-bpf-eats-the-world "Discuss on Hacker News")

[eBPF](/tag/ebpf/)[Linux](/tag/linux/)[Programming](/tag/programming/)[Developers](/tag/developers/)[Anycast](/tag/anycast/)[TCP](/tag/tcp/)
