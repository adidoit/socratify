---
title: "Your System is not a Sports Team"
author: "dropbox"
url: "https://dropbox.tech/infrastructure/your-system-is-not-a-sports-team"
system_score: 37
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

# Your System is not a Sports Team

// By James Cowling • Jun 06, 2019

  1. System bias
  2. Defining a mission
  3. Avoiding silos
  4. Summary



_It’s the responsibility of an engineering team to do what’s right for the company, not to advocate for the system they own. Engineering teams need to be oriented around a mission not a system to avoid narrow-minded decision-making._

Do you have a team at your company called the Kafka Team, or the HBase Team, or the Docker Team? Hmm, you may have screwed up. Don’t worry, there’s time to fix this.

Years ago at Dropbox we started the [Magic Pocket](https://blogs.dropbox.com/tech/2016/05/inside-the-magic-pocket/) team to design and build the block storage system of the same name. It was a silly internal codename that somehow ended up sticking. The Magic Pocket team had a lot of successes but as soon as the system was stable and launched in production I had the team go through all the effort of rebranding to the Storage Infrastructure Team. This was a huge pain and prompted a lot of eye-rolling from folks who saw this as a meaningless management gesture. At least in this one occasion there was some method to this madness.

The method here is that  _this_ is the team of block storage domain experts at the company. If the system ever ceases to meet our needs and we need to pursue an alternative,  _this_ is the team that needs to advocate for that strategy. Magic Pocket is not a sport team and and our people not a bunch of zealous fans. They’re highly skilled engineers with a responsibility to design, build, and operate the best storage system in the world. If we can’t trust that team to drive this strategy who can we trust?

Orienting a team around a mission and not a specific system is critical to ensure that their priorities are aligned with what’s best for the company.

The Storage Infrastructure team mission was brought into sharp focus when our lead engineer proactively killed a cold-storage project that he was in charge of. The system was “his baby,” but he felt like it turned out being excessively complex and not in the long-term interest of the company. People who make these kinds of decisions are the ones you want to celebrate.

As a fortunate twist he came up with [a far simpler and better design](https://blogs.dropbox.com/tech/2019/05/how-we-optimized-magic-pocket-for-cold-storage/) a few days later. We end up launching it ahead of schedule. It’s nice when things work out like that.

## System bias

It’s natural to be biased towards a system you’ve spent countless hours building or operating. We’ve all seen examples of “system bias” gone wrong. This can sometimes be painfully obvious: the team spending six months to improve performance by 10% when it was completely fine to begin with; the team trying to desperately force their tooling on clients who are better off without it; the team riding their outdated system to the grave like the captain going down with the Titanic.  


System bias can also show up in far more insidious ways. If a team views their responsibility as owning and advocating for a system then they’ll find creative ways to fill up sprint plans with work on that system, whether or not that actually matters. The same problem happens  _within_ a team when an engineer is a DRI (Directly Responsible Individual) for a specific system or sub-component. You’ll start seeing features get developed that are good in theory, but which we’d be fine without.

There’s always  _something_ to work on on a given system, you can always polish that gemstone a little more, but that doesn’t mean it’s worthwhile doing so. Many engineers have a tendency to focus inwardly on improving their pet system, unless encouraged to have a broader outlook by virtue of a mission that’s aligned with company value.

One question I like to ask engineers is:

If we could be spending these resources working on any project at the company right now, would this still be the best use of our time?

If the answer to this question is “no” then you might have scoped your mission too tightly. Either that or you’re over-staffed! (You’re probably not over-staffed.)

## Defining a mission

If system bias is a natural consequence of a sense of ownership, we’re certainly not doing the team any favors by burdening them further with a job description that codifies this bias.  


Orient your team around the problem you solve, not the tools you use to do it.

Someone else can probably give you better advice on how to define a mission than me. It should be focused enough to give a sense of team identity but broad enough so as to not codify any implementation decisions. It should also be short — one or two sentences. Start by asking yourself “what problem do we solve?” That’s probably your mission.

## Avoiding silos

Organizational structures can lead to excessive constraints on the mission of a team. Sometimes this is just an inevitable consequence of a large company. The more lightweight these structures are the more engineers will be empowered to focus on broad company impact in their decision-making, rather than staring at their shoes and only thinking about their own system.  


For a tech lead it’s usually easier to reason about system bias  _within_ a team. If a team is split up into too many small silos the engineers within a silo will be forced to prioritize their tiny domain. Formal structures like tech leads can serve to make this even worse if the domains are particularly small. I tend to prefer establishing DRIs for sub-priorities with a team. The DRI is responsible for a sub-priority or sub-component but it’s not their  _identity_ ; they’re still expected to work on other stuff on the team and to focus their energies on whatever matters most to the team as a whole.

## Summary

You want your engineers to focus on solving problems that matter, not on advocating for systems they own. Establish a mission for the team and make that mission your team identity.  


View [original post](https://medium.com/@jamesacowling/your-system-is-not-a-sports-team-e17f9eb16b94) on Medium.

* * *

// Tags   


  * [ Infrastructure ](https://dropbox.tech/infrastructure)
  * [Leadership](https://dropbox.tech/tag-results.leadership)
  * [Culture](https://dropbox.tech/tag-results.culture)



// Copy link   


Link copied

![Copy link](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/copy.svg)

  * Link copied

![Copy link](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/copy.svg)
  * [ ![Share on Twitter](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/twitter.svg) ](https://twitter.com/intent/tweet/?text=Your%20System%20is%20not%20a%20Sports%20Team&url=https://dropbox.tech/infrastructure/your-system-is-not-a-sports-team)
  * [ ![Share on Facebook](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/facebook.svg) ](https://facebook.com/sharer/sharer.php?u=https://dropbox.tech/infrastructure/your-system-is-not-a-sports-team)
  * [ ![Share on Linkedin](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/linkedin.svg) ](https://www.linkedin.com/shareArticle?mini=true&url=https://dropbox.tech/infrastructure/your-system-is-not-a-sports-team&title=Your%20System%20is%20not%20a%20Sports%20Team&source=https://dropbox.tech/infrastructure/your-system-is-not-a-sports-team)



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


