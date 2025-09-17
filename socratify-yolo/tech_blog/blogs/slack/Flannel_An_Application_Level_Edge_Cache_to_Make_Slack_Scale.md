---
title: "Flannel: An Application-Level Edge Cache to Make Slack Scale"
company: "slack"
url: "https://slack.engineering/flannel-an-application-level-edge-cache/"
content_length: 13721
type: "legendary_systems_architecture"
legendary: true
date: "2025-09-15"
---

May 31, 2017

7 min read

# Flannel: An Application-Level Edge Cache to Make Slack Scale

![](https://slack.engineering/wp-content/uploads/sites/7/2020/05/E12KS1G65-W1JJMLP47-cf36c946a9b5-512.jpeg)

Bing WeiStaff Engineer, Backend

![](https://slack.engineering/wp-content/uploads/sites/7/2020/04/1_9GNzO0TCru9lJ6wWXvI2Rg.jpeg?w=1011) Dolls in the Rain by Joe Lodge licensed under Creative Commons. Adapted.

Search

Latest Posts

  * September 4, 2025

9 min read

##  [Building Slack’s Anomaly Event Response](https://slack.engineering/building-slacks-anomaly-event-response/)

  * April 14, 2025

6 min read

##  [Optimizing Our E2E Pipeline](https://slack.engineering/speedup-e2e-testing/)

  * March 7, 2025

6 min read

##  [How we built enterprise search to be secure and private](https://slack.engineering/how-we-built-enterprise-search-to-be-secure-and-private/)

  * January 7, 2025

14 min read

##  [Automated Accessibility Testing at Slack](https://slack.engineering/automated-accessibility-testing-at-slack/)

  * December 16, 2024

15 min read

##  [Migration Automation: Easing the Jenkins → GHA shift with help from AI](https://slack.engineering/migration-automation-easing-the-jenkins-%e2%86%92-gha-shift-with-help-from-ai/)




Archives

  * [2025](https://slack.engineering/2025/) (4)
  * [2024](https://slack.engineering/2024/) (19)
  * [2023](https://slack.engineering/2023/) (16)
  * [2022](https://slack.engineering/2022/) (21)
  * [2021](https://slack.engineering/2021/) (24)
  * [2020](https://slack.engineering/2020/) (26)
  * [2019](https://slack.engineering/2019/) (21)
  * [2018](https://slack.engineering/2018/) (11)
  * [2017](https://slack.engineering/2017/) (21)
  * [2016](https://slack.engineering/2016/) (19)



Professor Robin Dunbar, when studying [Neolithic farming villages and primate troupes](https://en.wikipedia.org/wiki/Dunbar%27s_number) in the 90s, theorized that the maximum number of stable relationships we can keep is around 148, known popularly as Dunbar’s number. This upper bound is due to the mental dossier kept on individual’s relationships, but more importantly, the number of cross relationships between everyone else, whose number grows geometrically. Today, your Slack client is the window into your workplace, and teams have grown into the tens of thousands of people, much larger than any primitive village. Slack was architected around the goal of keeping teams of hundreds of people connected, and as teams have gotten larger, our initial techniques for loading and maintaining data have not scaled. To address that, we created a system that lazily loads data on demand and answers queries as you go.

Your Slack client strives to be consistent, compact, and searchable replicas of users, files, and messages that a team shares in real time. It initializes with information designed to expedite immediate use. The Slack server sends a full snapshot of a team’s data via the rtm.start API call with many things a client needs: users, channels, members in those channels, the latest messages, DMs, group DMs, etc. The client then uses this data to bootstrap itself and establishes a WebSocket to the server to get a stream of real-time events on the team. Users start typing and messages flow from your keyboard to the screens of your colleagues.

## **The Problem**

This system, where a client loads everything on startup, is viable for small teams. When teams get especially large, however, the number of channels, users and bots become unwieldy; startup time and client overhead both suffer as a result. Teams larger than tens of thousands of users would start to notice:

  * **Connection time starts to take too long** : Users experience wait times on the loading screen; and when switching between channels it takes a long time to show the first handful messages.
  * **Client memory footprint becomes large** : Too much data is stored and processed client-side.
  * **Reconnecting to Slack becomes expensive** : We want you to be able to close your laptop, and immediately get back to work when you reopen it. When each restart is almost as resource-intensive as the first one, that isn’t the case.
  * **Reconnection storms are resource intensive** : When an entire office loses network connection or otherwise needs to connect all at once, the combined weight of those requests manifest as slower connections, more reconnects, more failures, and more retries.



## **The Solution**

How can we maintain all the features of instant access while minimizing client storage size and load on the server? The key is for the client to load minimal data upfront, and only load channel and user data as needed. As long as the experience is seamless from the user’s point of view, we are free to apply resource-saving tactics like lazy loading and just-in-time loading to the architecture of the application.

This lazy loading is the ideological birthplace of Flannel, an application-level caching service developed in-house and deployed to our edge points-of-presence. Upon client startup, Flannel caches relevant data of users, channels, bots, and more. It then provides query APIs for clients to fetch upon demand. It foresees data that will be requested next and pushes data proactively to clients. For example, let’s say you mention a colleague in a channel: While broadcasting that message to people in the channel, Flannel sees that some clients have not loaded the information about the mentioned user recently. It sends the user data to those clients just before sending the message to save them a round-trip query.

![](https://d34u8crftukxnk.cloudfront.net/slackpress/prod/sites/7/1_WxZ1xZvJXqWjs5wtFNv7IA-1.png)Slack architecture pre-Flannel ![](https://d34u8crftukxnk.cloudfront.net/slackpress/prod/sites/7/1_b14wGaxM9n5dqpEAyaM89A.png)Slack architecture with Flannel

Now, when a user wants to connect to Slack, the following happens:

  1. The Slack client connects to Flannel.
  2. Behind the scenes, Flannel gathers the full client startup data. It also opens up a WebSocket connection to Slack servers in the main AWS region to stay current by consuming real-time events.
  3. Flannel returns a slimmed down version of this startup data to the client, allowing it to bootstrap itself.
  4. The Slack client is ready to use.

![](https://d34u8crftukxnk.cloudfront.net/slackpress/prod/sites/7/1_-FKWZ3L4pvZJR7F7uR5yiw.gif)Flannel-powered Quick Switcher

Immediately after connection, the client still only has bare bones data on the state of its constituent channels, so when the user takes advantage of find-as-you-type autocomplete, the client sends requests to Flannel and renders the results. You can test this out right now in your Slack window: If you open the Quick Switcher (_cmd+k on Mac, ctrl+k on Windows_), your client has little to no knowledge of the state or details of your team. However, as soon as you start typing, within moments, the autocomplete query will have been filled and the dropdown menu should then populate with suggestions. A similar cascade of events happen when you start typing a username in the message bar.

We use consistent hashing to choose which Flannel host a user connects to in order to maintain team affinity: Users on the same team who are from the same networking region are directed to the same Flannel instance to achieve optimal cache efficiency. When new or recently disconnected users connect, they are served directly from the Flannel cache, which reduces impact of reconnect storms to the Slack backend servers.

## **Status Quo and Future work**

Flannel has been running in our edge locations since January. It serves 4 million simultaneous connections at peak and 600K client queries per second.

![](https://d34u8crftukxnk.cloudfront.net/slackpress/prod/sites/7/1_zhCy8svD8v8PZ84SzMgEYA.gif)A comparison of loading Team Directory now and pre-Flannel on a big team

This has been an ongoing effort among the Web Client, Mobile and Backend engineering teams. We’re already using Flannel to increase scalability in Slack, but we have even bigger plans ahead:

  * **Users and channel members are already lazily loaded on the client side.** The payload size needed for client bootstrap has reduced tremendously: on a 1.5K user team, it reduced the data size by 7 times; on a 32K user team, it was reduced by 44 times. We are continuing this effort and will be removing channel objects in short order.
  * **We are bringing the Flannel experience to Mobile users** after seeing great success with the Web client.
  * **We are moving event fanout into Flannel.** Today, when a message is broadcast in a channel, the message server recognizes multiple recipients and forwards a copy to Flannel for each connected user. However, it’s much more efficient to send only one copy to each Flannel server and then fan out to multiple destinations. Besides messages, other event types traverse through Slack servers in the same fashion and can be thus optimized. Such a structure will largely reduce network bandwidth consumption and backend CPU overhead.
  * **Finally, we are moving clients to a pub/sub model.** Today, clients listen to all events happening on a team, including messages in all channels you are in, user profile updates, user presence changes, etc. This doesn’t have to be the case: clients can subscribe to the series of events that are relevant in the current view, and change subscriptions when users switch to another view. In fact, we’ve already moved user presence updates to the pub/sub model with great results: the number of presence events received by clients was reduced by a factor of 5. Moving more events to pub/sub will further improve client performance.

![](https://d34u8crftukxnk.cloudfront.net/slackpress/prod/sites/7/1_skNUPQ4-PSjWorQiQfi72A.png)Presence Events Reduction With the pub/sub Model

Hutterite settlements split up when they grew past the magical 148 number, and many Polynesian tribes sent out exploration parties when their island villages grew too large. This was because they could no longer keep track of everyone they interacted with. Their limiting factor was the amount of information each person had to keep in their mental cache. Flannel resolves similar constraints for Slack clients using central servers, providing information on demand. Features like fanout at edge points-of-presence and pub/sub further reduces the computational load on both the server and the client. With advancements like this in place, Slack evolves past its original design and is able to serve teams with hundreds of thousands of users.

We will continue to look for ways to make Slack faster and more reliable. If you’re interested in helping, [get in touch](https://slack.com/jobs/273556/infrastructure-engineer).

#[caching](https://slack.engineering/tags/caching/)#[scalability](https://slack.engineering/tags/scalability/)#[software-architecture](https://slack.engineering/tags/software-architecture/)

[ ](https://x.com/intent/post?url=https%3A%2F%2Fslack.engineering%2Fflannel-an-application-level-edge-cache-to-make-slack-scale%2F)

[ ](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fslack.engineering%2Fflannel-an-application-level-edge-cache-to-make-slack-scale%2F)

[ ](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fslack.engineering%2Fflannel-an-application-level-edge-cache-to-make-slack-scale%2F)

[ ](https://www.threads.net/intent/post?text=+https%3A%2F%2Fslack.engineering%2Fflannel-an-application-level-edge-cache-to-make-slack-scale%2F)

Copied!

Previous Post

[ **Rebuilding Slack’s Emoji Picker in React** ](https://slack.engineering/rebuilding-slacks-emoji-picker-in-react/)

Slack is transitioning its web client to React. When Slack was first built, our frontend… 

May 23, 2017

8 min read

![](https://slack.engineering/wp-content/uploads/sites/7/2020/05/1_1pDqkj6W_98A7NKxpCaGsg.png?w=160&h=160&crop=1)

Next Post

[ **Into the Clouds** ](https://slack.engineering/into-the-clouds/)

At Slack we use push notifications to let you know when someone sends you a… 

June 6, 2017

9 min read

![](https://slack.engineering/wp-content/uploads/sites/7/2020/04/0_Zb3slxZjY91rMBHq.jpeg?w=160&h=160&crop=1)

Recommended Reading

![](https://slack.engineering/wp-content/uploads/sites/7/2024/07/featuredimage.png?w=380&h=250&crop=1)

[](https://slack.engineering/unified-grid-how-we-re-architected-slack-for-our-largest-customers/)

July 31, 2024

11 min read

## [Unified Grid: How We Re-Architected Slack for Our Largest Customers](https://slack.engineering/unified-grid-how-we-re-architected-slack-for-our-largest-customers/)

@Ian Hoffman@Mike Demmer

![](https://slack.engineering/wp-content/uploads/sites/7/2024/04/AI_Marketing_Search_650x450_x2.jpg?w=380&h=250&crop=1)

[](https://slack.engineering/how-we-built-slack-ai-to-be-secure-and-private/)

April 18, 2024

8 min read

## [How We Built Slack AI To Be Secure and Private](https://slack.engineering/how-we-built-slack-ai-to-be-secure-and-private/)

@Slack Engineering

![](https://slack.engineering/wp-content/uploads/sites/7/2023/11/GettyImages-1409390032.jpg?w=380&h=250&crop=1)

[](https://slack.engineering/managing-slack-connect/)

November 28, 2023

10 min read

## [Managing Slack Connect](https://slack.engineering/managing-slack-connect/)

@Yuriy Loginov

![pile of analog clocks](https://slack.engineering/wp-content/uploads/sites/7/2023/09/jon-tyson-FlHdnPO6dlw-unsplash.jpg?w=380&h=250&crop=1)

[](https://slack.engineering/executing-cron-scripts-reliably-at-scale/)

September 28, 2023

6 min read

## [Executing Cron Scripts Reliably At Scale](https://slack.engineering/executing-cron-scripts-reliably-at-scale/)

@Claire Adams
