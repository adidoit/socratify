---
title: "Infrastructure Update: Pushing the edges of our global performance"
author: "dropbox"
url: "https://dropbox.tech/infrastructure/infrastructure-update-pushing-the-edges-of-our-global-performance"
system_score: 44
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

![](/cms/content/dam/dropbox/tech-blog/en-us/infrastructure/Infrastructure-1-1440x305px-light.png) ![](/cms/content/dam/dropbox/tech-blog/en-us/infrastructure/Infrastructure-1-1440x305px-dark.png)

# Infrastructure Update: Pushing the edges of our global performance

// By Akhil Gupta • Nov 16, 2016

Dropbox has hundreds of millions of registered users, and we’re always hard at work to ensure our customers have a speedy, reliable experience, wherever they are. Today, I am excited to announce an expansion to our global infrastructure that will deliver faster transfer speeds and improved performance for our customers around the world.

To give all of our users fast, reliable network performance, we’ve launched new Points of Presence (PoPs) across Europe, Asia, and parts of the US. We’ve coupled these PoPs with an [open-peering policy](https://www.dropbox.com/peering), and as a result have seen consistent speed improvements. In fact, we’ve already doubled the transfer speeds for some Dropbox clients around the world.

To upload a file to Dropbox, a user’s client needs to establish a secure connection with our servers. Before we launched these PoPs, a user that lives across the Pacific Ocean could expect this process to take as much as 450 milliseconds—half a second gone, and the client hasn’t even begun sending data.

![](/cms/content/dam/dropbox/tech-blog/en-us/2016/11/dbx-infra.png)

It can take up to 180 milliseconds for data traveling by undersea cables at nearly the speed of light to cross the Pacific Ocean. Data traveling across the Atlantic can take up to 90 milliseconds. This travel time is compounded by the way [TCP](https://en.wikipedia.org/wiki/Transmission_Control_Protocol) works. To establish a reliable connection for uploads, the client initiates what’s called a slow start. It sends a few packets of data, then waits for an ACK (or acknowledgement), confirming that the data has been received. The client will then send a larger group of packets and await confirmation, repeating this process until ultimately transmitting data at the user’s full available link capacity. Given the limitations we encounter here—the distance across the Pacific Ocean, and the speed of light—there are only so many optimizations we can make before physics stands in the way. 

So we’ve established proxy servers at the network edge, giving us accelerators in California, Texas, Virginia, New York, Washington, the UK, the Netherlands, Germany, Japan, Singapore and Hong Kong. A user’s client connects to these edge proxies, completing the initial TLS and TCP handshakes quickly—the proxies have enough buffer space to let the client get through the slow start without having to wait for an ACK from our data centers. This gets that connection between clients and our data centers (via those edge proxy servers) started quickly. 

We also wanted to minimize the average Round Trip Time (RTT) per HTTPS request to our data centers. To do this, we connected our PoP to our data centers via our private Backbone links for increased stability and control, and also configured our proxies to keep the connections to our data centers alive. This helps us avoid the latency cost of opening a new connection when you want your data synced and start the transfer immediately.

At the same time, we are committed to ensuring your data remains secure. We use TLS 1.2 and a PFS cipher suite at both our origin data centers and proxies. Additionally, we’ve enabled upstream certificate validation and certificate pinning on our proxy servers. This helps ensure that the edge proxy server knows it’s talking to our upstream server, and not someone attempting a man-in-the-middle attack. 

We’ve tested and applied this configuration in various markets in Europe and Asia. In France, for example, median download speeds are 40% faster after introducing proxy servers, while median upload speeds are approximately 90% faster. In Japan, median download speeds have doubled, while median upload speeds are three times as fast. 

As part of this expansion we also offer an open-peering policy, free of charge. Our open-peering agreements help us provide faster connections and improved network performance, to better serve local populations. With open-peering, major ISPs can route Dropbox traffic directly to and through our networks, improving transfer speeds for our users, and reducing bandwidth costs for Dropbox and our ISP partners. More than 400 ISPs are participating in the program globally, including BT in England, Hetzner Online in Germany and Vocus Communications in New Zealand, through their Orcon, Slingshot and Flip brands. Open-peering helps large companies like Google and LinkedIn manage their networks, and it’s helping Dropbox improve network performance too.

![](/cms/content/dam/dropbox/tech-blog/en-us/2016/11/image_preview-1.png)

![](/cms/content/dam/dropbox/tech-blog/en-us/2016/11/image_preview-2.png)

Earlier this year we introduced Magic Pocket, our in-house multi-exabyte storage system. We’re now storing over 90% of our users’ data on this custom-built architecture, which allows us to customize the entire stack end-to-end and improve performance. We plan to continue this expansion in new regions over the next six to twelve months, and will continue to make infrastructure investments as the needs of our customers evolve and change. This expansion we’re announcing today is another part of that ongoing investment in our infrastructure, as we strive to offer the best possible experience for all of our users. 

* * *

// Tags   


  * [ Infrastructure ](https://dropbox.tech/infrastructure)
  * [Peering](https://dropbox.tech/tag-results.peering)
  * [Pop](https://dropbox.tech/tag-results.pop)



// Copy link   


Link copied

![Copy link](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/copy.svg)

  * Link copied

![Copy link](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/copy.svg)
  * [ ![Share on Twitter](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/twitter.svg) ](https://twitter.com/intent/tweet/?text=Infrastructure%20Update%3A%20Pushing%20the%20edges%20of%20our%20global%20performance&url=https://dropbox.tech/infrastructure/infrastructure-update-pushing-the-edges-of-our-global-performance)
  * [ ![Share on Facebook](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/facebook.svg) ](https://facebook.com/sharer/sharer.php?u=https://dropbox.tech/infrastructure/infrastructure-update-pushing-the-edges-of-our-global-performance)
  * [ ![Share on Linkedin](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/linkedin.svg) ](https://www.linkedin.com/shareArticle?mini=true&url=https://dropbox.tech/infrastructure/infrastructure-update-pushing-the-edges-of-our-global-performance&title=Infrastructure%20Update%3A%20Pushing%20the%20edges%20of%20our%20global%20performance&source=https://dropbox.tech/infrastructure/infrastructure-update-pushing-the-edges-of-our-global-performance)



Related posts 

[ See more ](https://dropbox.tech/infrastructure)

  * [ Seventh-generation server hardware at Dropbox: our most efficient and capable architecture yet ](https://dropbox.tech/infrastructure/seventh-generation-server-hardware)

// Jul 02, 2025 

  * [ How we brought multimedia search to Dropbox Dash ](https://dropbox.tech/infrastructure/multimedia-search-dropbox-dash-evolution)

// May 29, 2025 

  * [ Evolving our infrastructure through the messaging system model in Dropbox ](https://dropbox.tech/infrastructure/infrastructure-messaging-system-model-async-platform-evolution)

// Jan 21, 2025 




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


