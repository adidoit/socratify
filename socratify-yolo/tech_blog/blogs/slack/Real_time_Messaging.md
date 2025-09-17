---
title: "Real-time Messaging"
company: "slack"
url: "https://slack.engineering/real-time-messaging/"
content_length: 13833
type: "legendary_systems_architecture"
legendary: true
date: "2025-09-15"
---

11.04.23

8 min read

# Real-time Messaging

![](https://slack.engineering/wp-content/uploads/sites/7/2023/03/E12KS1G65-WE3KQQ6AX-9e3a91c67738-512.jpeg)

Sameera ThanguduSenior Software Engineer

![](https://slack.engineering/wp-content/uploads/sites/7/2023/03/ezgif-3-b10c99350f-1.jpg?w=800)

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



Did you know that ground stations transmit signals to satellites 22,236 miles above the equator in geostationary orbits, and that those signals are then beamed down to the entire North American subcontinent? Satellite radios today serve hundreds of channels across 9,540,000 square miles. Unless you’re working at a secret military facility, deep underground, you can enjoy satellite radio everywhere. 

Just like the satellites, Slack sends millions of messages every day across millions of channels in real time all around the world. If we look at the traffic on a typical work day, it shows that most users are online between 9am and 5pm local time, with peaks at 11am and 2pm and a small dip in between for lunch hour. Though the working hours are similar across regions, looking at the two peaks in the graph below, it is evident that prime time is not the same: It’s post-noon in some regions and pre-noon in other regions. Each colored line in the below graph represents a region.

![](https://slack.engineering/wp-content/uploads/sites/7/2023/03/users-online-1.jpg?w=594)

In this blog post we’ll describe the architecture that we use to send real-time messages at this scale. We’ll take a closer look at the services that send the chat messages and various events to these online users in real time. Our core services are written in Java: They are Channel Servers, Gateway Servers, Admin Servers, and Presence Servers.

## **Server overview**

Channel Servers (CS) are stateful and in-memory, holding some amount of history of channels. Every CS is mapped to a subset of channels based on consistent hashing. At peak times, about 16 million channels are served per host. A “channel” in this instance is an abstract term whose ID is assigned to an entity such as user, team, enterprise, file, huddle, or a regular Slack channel. The ID of the channel is hashed and mapped to a unique server. Every CS host receives and sends messages for those mapped channels. A single Slack team has all of its channels mapped across all the CSs.

Consistent hash ring managers (CHARMs) manage the consistent hash ring for CSs. They replace unhealthy CSs very quickly and efficiently; a new CS is ready to serve traffic in under 20 seconds. With a team’s channels spread across all CSs, a small number of teams’ channels are mapped to a CS. When a channel server is replaced, users of those teams’ channels experience elevated latency in message delivery for less than 20 seconds.

The diagram below shows how CSs are registered in Consul, our service discovery tool. Each consistent hash is defined and managed by CHARMs, and then Admin Servers (AS) and CS discovers them by querying Consul for the up-to-date config.

![](https://slack.engineering/wp-content/uploads/sites/7/2023/03/CHARMS-1.jpg?w=544)

Gateway Servers (GS) are stateful and in-memory. They hold users’ information and websocket channel subscriptions. This service is the interface between Slack clients and CSs. Unlike all other servers, GSs are deployed across multiple geographical regions. This allows a Slack client to quickly connect to a GS host in its nearest region. We have a draining mechanism for region failures that seamlessly switches the users in a bad region to the nearest good region.

Admin Servers (AS) are stateless and in-memory. They interface between our Webapp backend and CSs. Presence Servers (PS) are in-memory and keep track of which users are online. It powers the green presence dots in Slack clients. The users are hashed to individual PSs. Slack clients make queries to it through the websocket using the GS as a proxy for presence status and presence change notifications. A Slack client receives presence notifications only for a subset of users that are visible in the app screen at any moment.

## **Slack client set up**

Every Slack client has a persistent websocket connection to Slack’s servers to receive real-time events to maintain its state. The client sets up a websocket connection as below.

![](https://slack.engineering/wp-content/uploads/sites/7/2023/03/client-websocket-setup-slim-e1680215351716.jpg?w=640)

On boot up, the client fetches the user token and websocket connection setup information from the Webapp backend. Webapp is a Hacklang codebase that hosts all the APIs called by our Slack Clients. This service also includes JavaScript code that renders the Slack clients. A client initiates a websocket connection to the nearest edge region. Envoy forwards the request to GS. [Envoy](https://www.envoyproxy.io) is an open source edge and service proxy, designed for cloud-native applications. Envoy is used at Slack as a load-balancing solution for various services and TLS termination. GS fetches the user information, including all the user’s channels, from Webapp and sends the first message to the client. GS then subscribes to all the channel servers that hold those channels based on consistent hashing asynchronously. The Slack client is now ready to send and receive real time messages.

## **Send a message to a million clients in real time**

Once the client is set up, each message sent in a channel is broadcasted to all clients online in the channel. Our message stats shows that the multiplicative factor for message broadcast is different across regions, with some regions having a higher rate than others. This could be due to multiple factors, including team sizes in those regions. The chart below shows message received count and message broadcasted count across multiple regions.

![](https://slack.engineering/wp-content/uploads/sites/7/2023/03/broadcast-1.jpg?w=563)

Let’s take a look at how the message is broadcasted to all online clients. Once the websocket is set up, as discussed above, the client hits our Webapp API to send a message. Webapp then sends that message to AS. AS looks at the channel ID in this message, discovers CS through a consistent hash ring, and routes the message to the appropriate CS that hosts the real time messaging for this channel. When CS receives the message for that channel, it sends out the message to every GS across the world that is subscribed to that channel. Each GS that receives that message sends it to every connected client subscribed to that channel id.

Below is a journey of a message from the client through our stack. In the following example, Slack client A and B are in the same edge region, and C is in a different region. Client A is sending a message, and client B and C are receiving it.

![](https://slack.engineering/wp-content/uploads/sites/7/2023/03/journey-of-a-message-slim-Page-1.jpg?w=640)

## **Events**

Aside from chat messages, there is another special kind of message called an event. An event is any update a client receives in real time that changes the state of the client. There are hundreds of different types of events that flow across our servers. Some examples include when a user sends a reaction to a message, a bookmark is added, or a member joins a channel. These events follow a similar journey to the simple chat message shown above. 

Look at the message delivery graph below. The count spikes at regular intervals. What could cause these spikes? Turns out, events sent for reminders, scheduled messages, and calendar events tend to happen at the top of the hour, explaining the regular traffic spikes.

![](https://slack.engineering/wp-content/uploads/sites/7/2023/03/spiky-messages.jpg?w=566)

Now let’s take a look at a different kind of event called Transient events. These are a category of events that are not persisted in the database and are sent through a slightly different flow. User typing in a channel or a document is one such event.

![](https://slack.engineering/wp-content/uploads/sites/7/2023/03/user-typing.png?w=640)

Below is a diagram that shows this scenario. Again, Slack client A and B are in the same edge region, and C is in a different region. Slack client A is typing in a channel and this is notified to other users B and C in the channel. Client A sends this message via websocket to GS. GS looks at the channel ID in the message and routes to the appropriate CS based on a consistent hash ring. CS then sends to all GSs across the world subscribed to this channel. Each GS, on receiving this message, broadcasts to all the users websockets subscribed to this channel

![](https://slack.engineering/wp-content/uploads/sites/7/2023/03/events-flow-slim.jpg?w=640)

## **What’s next**

Our servers serve tens of millions of channels per host, tens of millions of connected clients, and our system delivers messages across the world in 500ms. With the linear scalability of our current architecture, our projections show that we can serve many more customers. However, there is always room for improvement and we are looking to extend our architecture to serve the scale of our next biggest customers. If this work sounds interesting to you, come join us: we have an [open role](https://salesforce.wd1.myworkdayjobs.com/Slack/job/California---Remote/Software-Engineer---Realtime-Services--Core-Infrastructure_JR172389) !

Lastly, a huge shout out to everyone who contributed to this architecture, and to Serguei Mourachov for reviewing and giving feedback on this blog post.

#[infrastructure](https://slack.engineering/tags/infrastructure/)#[scalability](https://slack.engineering/tags/scalability/)#[software-architecture](https://slack.engineering/tags/software-architecture/)

[ ](https://x.com/intent/post?url=https%3A%2F%2Fslack.engineering%2Freal-time-messaging%2F)

[ ](https://www.linkedin.com/shareArticle?mini=true&url=https%3A%2F%2Fslack.engineering%2Freal-time-messaging%2F)

[ ](https://www.facebook.com/sharer/sharer.php?u=https%3A%2F%2Fslack.engineering%2Freal-time-messaging%2F)

[ ](https://www.threads.net/intent/post?text=+https%3A%2F%2Fslack.engineering%2Freal-time-messaging%2F)

Copied!

Previous Post

[ **Tracing Notifications** ](https://slack.engineering/tracing-notifications/)

Notifications are a key aspect of the Slack user experience. Users rely on timely notifications… 

April 4, 2023

12 min read

![](https://slack.engineering/wp-content/uploads/sites/7/2023/03/daria-nepriakhina-_XR5rkprHQU-unsplash-1.jpg?w=160&h=160&crop=1)

Next Post

[ **Service Delivery Index: A Driver for Reliability** ](https://slack.engineering/service-delivery-index-a-driver-for-reliability/)

Customer-first: Moving from Hero Engineering to Reliability Engineering From the beginning, Slack has always had… 

July 26, 2023

10 min read

![A stack of pebbles, or a rock cairn with an ocean backdrop](https://slack.engineering/wp-content/uploads/sites/7/2023/07/jeremy-thomas-FO7bKvgETgQ-unsplash.jpg?w=160&h=160&crop=1)

Recommended Reading

![](https://slack.engineering/wp-content/uploads/sites/7/2024/10/54040277712_ab333a09d9_b.jpg?w=380&h=250&crop=1)

[](https://slack.engineering/were-all-just-looking-for-connection/)

October 10, 2024

9 min read

## [We’re All Just Looking for Connection](https://slack.engineering/were-all-just-looking-for-connection/)

@Brett Wines

![](https://slack.engineering/wp-content/uploads/sites/7/2024/09/myles-tan-IWCljYv1TJw-unsplash.jpg?w=380&h=250&crop=1)

[](https://slack.engineering/advancing-our-chef-infrastructure/)

September 17, 2024

14 min read

## [Advancing Our Chef Infrastructure](https://slack.engineering/advancing-our-chef-infrastructure/)

@Archie Gunasekara

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
