---
title: "Introducing DNS Resolver, 1.1.1.1 (not a joke)"
company: "cloudflare"
url: "https://blog.cloudflare.com/dns-resolver-1-1-1-1/"
type: "system_architecture"
date: "2025-09-15"
---

# Introducing DNS Resolver, 1.1.1.1 (not a joke)

2018-04-01

  * [![Ólafur Guðmundsson](https://blog.cloudflare.com/cdn-cgi/image/format=auto,dpr=3,width=64,height=64,gravity=face,fit=crop,zoom=0.5/https://cf-assets.www.cloudflare.com/zkvhlag99gkb/1Q0Z4uWqwV6Vc2zYTEzXXu/aba8f4a8aad6fba686bfc01780cf76d7/olafur-gudmundsson.jpg)](/author/olafur-gudmundsson/)

[Ólafur Guðmundsson](/author/olafur-gudmundsson/)




7 min read

This post is also available in [简体中文](/zh-cn/dns-resolver-1-1-1-1), [Deutsch](/de-de/dns-resolver-1-1-1-1), [日本語](/ja-jp/dns-resolver-1-1-1-1), [Español](/es-es/dns-resolver-1-1-1-1) and [Français](/fr-fr/dns-resolver-1-1-1-1).

![](https://cf-assets.www.cloudflare.com/zkvhlag99gkb/4qgaJIg5CKfBvs2TAbyw8o/51cd533853ce1267691d626e9796d7df/dns-resolver-1-1-1-1.png)

Cloudflare’s mission is to help build a better Internet and today we are releasing our DNS resolver, [1.1.1.1](https://1.1.1.1/) \- a recursive DNS service. With this offering, we’re fixing the foundation of the Internet by building a faster, more secure and privacy-centric public DNS resolver. The DNS resolver, 1.1.1.1, is available publicly for everyone to use - it is the first consumer-focused service Cloudflare has ever released.

We’re using the following IPv4 addresses for our resolver: **1.1.1.1** and **1.0.0.1**. Easy to remember. These addresses have been provided to Cloudflare by APNIC for both joint research and this service. You can read more about their work via the [APNIC blog](https://labs.apnic.net/?p=1127).

DNS resolver, 1.1.1.1, is served by Cloudflare’s Global Anycast [Network](https://www.cloudflare.com/network/).

### Background: A quick refresher on the role of the resolver in DNS

Our friends at [DNSimple](https://dnsimple.com/) have made this amazing DNS Tutorial for anyone to fill in their gaps on [how DNS works](https://howdns.works/). They explain all about resolvers, root name servers, and much more in a very informative way.

When resolving a [domain name](https://www.cloudflare.com/learning/dns/glossary/what-is-a-domain-name/), a query travels from your end system (i.e. a web browser) to a [recursive DNS service](https://www.cloudflare.com/learning/dns/what-is-recursive-dns/). If the DNS record is not in the service’s local cache, the recursor will query the authoritative DNS hierarchy to find the IP address information you are looking for. The recursor is the part that DNS resolver, 1.1.1.1 plays. It must be fast and these days it must be secure!

### Goals for DNS resolver, 1.1.1.1

Our goals with the public resolver are simple: Cloudflare wants to operate the fastest public resolver on the planet while raising the standard of privacy protections for users. To make the Internet faster, we are already building data centers all over the globe to reduce the distance (i.e. latency) from users to content. Eventually we want everyone to be within 10 milliseconds of at least one of our locations.

In March alone, we enabled thirty-one new data centers globally ([Istanbul](/istanbul-not-constantinople/), [Reykjavík](/reykjavik-cloudflares-northernmost-location/), [Riyadh](/riyadh/), [Macau](/macau/), [Baghdad](/baghdad/), [Houston, Indianapolis, Montgomery, Pittsburgh, Sacramento](/usa-expansion/), [Mexico City](/mexico-city/), [Tel Aviv](/tel-aviv/), [Durban, Port Louis](/durban-and-port-louis/), [Cebu City](/cebu/), [Edinburgh](/edinburgh/), [Riga, Tallinn, Vilnius](/riga-tallinn-vilnius/), [Calgary, Saskatoon, Winnipeg](/welcome-calgary-saskatoon-and-winnipeg/), [Jacksonville, Memphis, Tallahassee](/more-us-data-centers/), [Bogotá](/bogota/), [Luxembourg City, Chișinău](/luxembourg-chisinau/)) and just like every other city in our network, new sites run DNS Resolver, 1.1.1.1 on day-one!

Our fast and highly distributed network is built to serve any protocol and we are currently the fastest authoritative DNS provider on the Internet, a capability enjoyed by over seven million Internet properties. Plus, we already provide an anycast service to two of the thirteen root nameservers. The next logical step was to provide faster recursive DNS service for users. Our recursor can take advantage of the authoritative servers that are co-located with us, resulting in faster lookups for all domain names.

While [DNSSEC](https://www.cloudflare.com/dns/dnssec/how-dnssec-works/) ensures integrity of data between a resolver and an authoritative server, it does not protect the privacy of the “last mile” towards you. DNS resolver, 1.1.1.1, supports both emerging DNS privacy standards - DNS-over-TLS, and DNS-over-HTTPS, which both provide last mile encryption to keep your DNS queries private and free from tampering.

### Making our resolver privacy conscious

Historically, recursor sends the full domain name to any intermediary as it finds its way to the [root or authoritative DNS](https://www.cloudflare.com/learning/dns/glossary/dns-root-server/). This meant that if you were going to [www.cloudflare.com](https://www.cloudflare.com), the root server and the .com server would both be queried with the full domain name (i.e. the `www`, the `cloudflare`, and the `com` parts), even though the root servers just need to redirect the recursive to dot com (independent of anything else in the fully qualified domain name). This ease of access to all this personal browsing information via DNS presents a grave privacy concern to many. This has been addressed by several resolvers’ software packages, though not all solutions have been widely adapted or deployed.

The DNS resolver, 1.1.1.1, provides, on day-one, all defined and proposed DNS privacy-protection mechanisms for use between the stub resolver and recursive resolver. For those not familiar, a stub resolver is a component of your operating system that talks to the recursive resolver. By only using DNS Query Name Minimisation defined in [RFC7816](https://tools.ietf.org/html/rfc7816), DNS resolver, 1.1.1.1, reduces the information leaked to intermediary DNS servers, like the root and [TLDs](https://www.cloudflare.com/learning/dns/top-level-domain/). That means that DNS resolver, 1.1.1.1, only sends just enough of the name for the authority to tell the resolver where to ask the next question.

The DNS resolver, 1.1.1.1, is also supporting privacy-enabled TLS queries on port 853 ([DNS over TLS](https://www.cloudflare.com/learning/dns/dns-over-tls/)), so we can keep queries hidden from snooping networks. Furthermore, by offering the experimental DoH ([DNS over HTTPS](https://developers.cloudflare.com/1.1.1.1/dns-over-https/)) protocol, we improve both privacy and a number of future speedups for end users, as browsers and other applications can now mix DNS and HTTPS traffic into one single connection.

With DNS aggressive negative caching, as described in [RFC8198](https://tools.ietf.org/html/rfc8198), we can further decrease the load on the global DNS system. This technique first tries to use the existing resolvers negative cache which keeps negative (or non-existent) information around for a period of time. For zones signed with DNSSEC and from the NSEC records in cache, the resolver can figure out if the requested name does NOT exist without doing any further query. So if you type `wwwwwww` dot something and then `wwww` dot something, the second query could well be answered with a very quick “no” (NXDOMAIN in the DNS world). Aggressive negative caching works only with DNSSEC signed zones, which includes both the root and a 1400 out of 1544 TLDs are signed today.

We use [DNSSEC](/dnssec-an-introduction/) validation when possible, as that allows us to be sure the answers are accurate and untampered with. The cost of signature verifications is low, and the potential savings we get from aggressive negative caching more than make up for that. We want our users to trust the answers we give out, and thus perform all possible checks to avoid giving bad answers to the clients.

However, [DNSSEC](/dnssec-complexities-and-considerations/) is very unforgiving. Errors in DNSSEC configuration by authoritative DNS operators can make such misconfigured domains unresolvable. To work around this problem, Cloudflare will configure "Negative Trust Anchors" on domains with detected and vetted DNSSEC errors and remove them once the configuration is rectified by authoritative operators. This limits the impact of broken DNSSEC domains by temporarily disabling DNSSEC validation for a specific misconfigured domain, restoring access to end consumers.

### How did we build it?

Initially, we thought about building our own resolver, but rejected that approach due to complexity and go-to-market considerations. Then we looked at all open source resolvers on the market; from this long list we narrowed our choices down to two or three that would be suitable to meet most of the project goals. In the end, we decided to build the system around the [Knot Resolver from CZ NIC](https://www.knot-resolver.cz/). This is a modern resolver that was originally released about two and a half years ago. By selecting the Knot Resolver, we also increase software diversity. The tipping point was that it had more of the core features we wanted, with a modular architecture similar to [OpenResty](https://openresty.org/). The Knot Resolver is in active use and development.

### Interesting things we do that no one else does

The recent advanced features we wanted were:

  * Query Minimization [RFC7816](https://tools.ietf.org/html/rfc7816),

  * DNS-over-TLS (Transport Layer Security) [RFC7858](https://tools.ietf.org/html/rfc7858),

  * DNS-over-HTTPS protocol [DoH](https://datatracker.ietf.org/wg/doh/about/),

  * Aggressive negative answers [RFC8198](https://tools.ietf.org/html/rfc8198),




Small disclaimer: the original main developer of Knot Resolver, [Marek Vavruša](/author/marek/), has been working on the Cloudflare DNS team for over two years.

### How to make our resolver faster

There are many factors that affect how fast a resolver is. The first and foremost is: can it answer from cache? If it can, then the time to answer is only the [round-trip time](https://www.cloudflare.com/learning/cdn/glossary/round-trip-time-rtt/) for a packet from the client to the resolver.

When a resolver needs to get an answer from an authority, things get a bit more complicated. A resolver needs to follow the DNS hierarchy to resolve a name, which means it has to talk to multiple authoritative servers starting at the root. For example, our resolver in Buenos Aires, Argentina will take longer to follow a DNS hierarchy than our resolver in Frankfurt, Germany because of its proximity to the authoritative servers. In order to get around this issue we prefill our cache, out-of-band, for popular names, which means when an actual query comes in, responses can be fetched from cache which is much faster. Over the next few weeks we will post blogs about some of the other things we are doing to make the resolver faster and better, Including our fast caching.

One issue with our expansive network is that the cache hit ratio is inversely proportional to the number of nodes configured in each data center. If there was only one node in a data center that’s nearest to you, you could be sure that if you ask the same query twice, you would get a cached answer the second time. However, as there’s hundreds of nodes in each of our data centers, you might get an uncached response, paying the latency-price for each request. One common solution is to put a [caching load balancer](https://www.cloudflare.com/application-services/products/load-balancing/) in front of all your resolvers, which unfortunately introduces a single-point-of-failure. We don’t do single-point-of-failures.

Instead of relying on a centralized cache, DNS resolver, 1.1.1.1, uses an innovative distributed cache, which we will talk about in a later blog.

### Data Policy

Here’s the deal - we don’t store client IP addresses never, ever, and we only use query names for things that improve DNS resolver performance (such as prefill all caches based on popular domains in a region and/or after obfuscation, APNIC research).

Cloudflare will never store any information in our logs that identifies an end user, and all logs collected by our public resolver will be deleted within 24 hours. We will continue to abide by our [privacy policy](https://developers.cloudflare.com/1.1.1.1/privacy) and ensure that no user data is sold to advertisers or used to target consumers.

### Setting it up

See <https://1.1.1.1/> because it's that simple!

### About those addresses

We are grateful to APNIC, our partner for the IPv4 addresses `1.0.0.1` and `1.1.1.1` (which everyone agrees is insanely easy to remember). Without their years of research and testing, these addresses would be impossible to bring into production. Yet, we still have a way to go with that. Stay tuned to hear about our adventures with those IPs in future blogs.

For IPv6, we have chosen `2606:4700:4700::1111` and `2606:4700:4700::1001` for our service. It’s not as easy to get cool IPv6 addresses; however, we’ve picked an address that only uses digits.

But why use easy to remember addresses? What’s special about public resolvers? While we use names for nearly everything we do; however, there needs to be that first step in the process and that’s where these number come in. We need a number entered into whatever computer or connected device you’re using in order to find a resolver service.

Anyone on the internet can use our public resolver and you can see how to do that by visiting <https://1.1.1.1/> and clicking on **GET STARTED**.

### Why announce it on April first?

For most of the world, Sunday is 1/4/2018 (in America the day/month is reversed as-in 4/1/2018). Do you see the **4** and the **1**? We did and that’s why we are announcing **1.1.1.1** today. Four ones! If it helps you remember **1.1.1.1** , then that’s a good thing!

Sure, It’s also [April Fools' Day](https://en.wikipedia.org/wiki/April_Fools%27_Day) and for a good portion of people it’s a day for jokes, foolishness, or harmless pranks. This is no joke, this is no prank, this is no foolish act. This is DNS Resolver, [1.1.1.1](https://1.1.1.1/) ! Follow it at [#1dot1dot1dot1](https://twitter.com/hashtag/1dot1dot1dot1)

Cloudflare's connectivity cloud protects [entire corporate networks](https://www.cloudflare.com/network-services/), helps customers build [Internet-scale applications efficiently](https://workers.cloudflare.com/), accelerates any [website or Internet application](https://www.cloudflare.com/performance/accelerate-internet-applications/), [wards off DDoS attacks](https://www.cloudflare.com/ddos/), keeps [hackers at bay](https://www.cloudflare.com/application-security/), and can help you on [your journey to Zero Trust](https://www.cloudflare.com/products/zero-trust/).  
  
Visit [1.1.1.1](https://one.one.one.one/) from any device to get started with our free app that makes your Internet faster and safer.  
  
To learn more about our mission to help build a better Internet, [start here](https://www.cloudflare.com/learning/what-is-cloudflare/). If you're looking for a new career direction, check out [our open positions](https://www.cloudflare.com/careers).

[Discuss on Hacker News](https://news.ycombinator.com/submitlink?u=https://blog.cloudflare.com/dns-resolver-1-1-1-1 "Discuss on Hacker News")

[DNS](/tag/dns/)[1.1.1.1](/tag/1-1-1-1/)[Privacy](/tag/privacy/)[Resolver](/tag/resolver/)[Product News](/tag/product-news/)
