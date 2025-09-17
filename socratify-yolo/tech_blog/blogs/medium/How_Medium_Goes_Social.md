---
title: "How Medium Goes Social"
company: "medium"
url: "https://medium.engineering/how-medium-goes-social-b7dbefa6d413"
type: "direct_systems_collection"
date: "2025-09-15"
---

# How Medium Goes Social

## Using Golang and Neo4j to help you keep up with all your friends

[![Tess Rinearson](https://miro.medium.com/v2/resize:fill:64:64/0*xz9wFDs3BLfw67qH.jpeg)](https://medium.com/@tessr?source=post_page---byline--b7dbefa6d413---------------------------------------)

[Tess Rinearson](https://medium.com/@tessr?source=post_page---byline--b7dbefa6d413---------------------------------------)

4 min read

·

Nov 20, 2014

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fvote%2Fmedium-eng%2Fb7dbefa6d413&operation=register&redirect=https%3A%2F%2Fmedium.engineering%2Fhow-medium-goes-social-b7dbefa6d413&user=Tess+Rinearson&userId=c16152863954&source=---header_actions--b7dbefa6d413---------------------clap_footer------------------)

\--

2

[](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2F_%2Fbookmark%2Fp%2Fb7dbefa6d413&operation=register&redirect=https%3A%2F%2Fmedium.engineering%2Fhow-medium-goes-social-b7dbefa6d413&source=---header_actions--b7dbefa6d413---------------------bookmark_footer------------------)

Listen

Share

 _Have any of my friends liked this post?_

_Can I tell all my friends once I’ve published something new?_

_How can I find new people to follow?_

We answer these questions (and many others) through our social graph:

Press enter or click to view image in full size

This is sort of what our social graph looks like. (Or a very small part of it looks like this, anyways.) The turquoise nodes are people, and the orange nodes are posts. That turquoise node in the middle-right is actually _me._

We store the social graph in Neo4j, which is a graph database. That is, instead of storing data in tables or key-value pairs, it stores data in nodes and relationships. We chose Neo4j specifically because it’s an open-source project, and because it has a well-established community.

It makes a lot of sense to store social data in a graph database. Medium users, posts and collections are represented by graph nodes, and the edges between them describe relationships — users following users, users recommending posts, or users editing collections, to name a few common examples. Using a graph database also makes our queries simpler: we don’t have to do any complicated joins or other query wizardry.

Instead we can write simple queries in Neo4j’s intuitive query language, called [cypher](http://docs.neo4j.org/chunked/stable/cypher-query-lang.html). For example, to get all the people I follow, I can run a query like this:
    
    
    **MATCH (** u:**USER**{user_id: my_user_id})-[:**FOLLOWED**]->(friends:**USER)**  
    **RETURN** friends

(This is the real cypher query. That’s how simple and powerful cypher is.)

Our Neo4j database is managed by a service written in Go. We’ve affectionately and creatively named it _GoSocial._

### Why Go?

There are a few reasons we chose to write GoSocial in Go, the least of which is the cute name.

  * **Performance.**[Go is performant and fast](http://dave.cheney.net/2014/06/07/five-things-that-make-go-fast). Empirically, it’s much faster to fetch a bunch of data from Neo4j and do all the post-processing in GoSocial. But at the same time, Go has a nice balance of performance and ease-of-use. It’s performant, but it doesn’t make you, say, manage your own memory.
  * **Concurrency.** Concurrency is baked right into Go, in the form of goroutines and channels, which are nice, useful concurrency primitives. This is great for GoSocial: We can break large Neo4j queries down into smaller, less exhaustive queries. Neo4j is multi-threaded, so it can then run those small queries in parallel and combine their results later. This is much faster than running single large query.
  * **HTTP.** Go has a full-featured native http package. It’s natural and easy to write a web service in Go, without adding fancy frameworks that clutter and complicate the code. This makes it really easy for our application server to talk to our social service.
  * **Not-JavaScript.** Go provides different strengths from our other language, JavaScript. (Our application server is written in Node.) As we considered adding another language to our stack, we wanted a “systems language” — that is, something that’s strongly typed, high performance, compiled. By having two languages with different strengths, we can always choose the best one for the job.
  * **Opinionatedness.** Go is opinionated. There are definitively correct ways to do things, which means it’s a good choice for teams. Tools like _gofmt_ , which automatically formats all Go the same way, means that the whole team is immediately on the same page. This “opinionatedness” goes beyond formatting — there is almost always a most “Go-like” way to do anything. As a younger engineer, especially, I appreciate this. I can be shy about disagreeing with more senior engineers, but I’m empowered by Go’s opinionatedness!
  * **Libraries.** There are substantial libraries in Go. Specifically, we were comfortable writing our Neo4j/social service in Go with [Neoism](https://github.com/jmcvetta/neoism), a Neo4j client written in Go.



### Why create a separate service?

Before we wrote GoSocial, most of our application lived in a monolithic codebase written in Node.js. In fact, we still keep most of our application in this codebase, and we enjoy some of the benefits of having a monolith — for example, we don’t have to worry about versioning or interfaces between services, and our application server can reuse its library code.

But creating a separate social service has a lot of advantages, too:

  1. We can move computationally heavy tasks, such as sorting a bunch of followers, away from the application server. This reduces the load on the application server.
  2. Relatedly, we can have our social features fail without blocking the whole page. For instance, every time we load a post we try to show the avatars of people who have recommended it. If GoSocial fails to fetch “people who have recommended a post,” that failure happens independently of the other, more important tasks on the application server — like retrieving the text of the post.
  3. GoSocial creates a clean interface for social data. If we ever decide to replace Neo4j, keeping GoSocial separate prevents Neo4j from being a concern for the application server.
  4. Keeping GoSocial separate means that we can scale it up and down, separately. If our social needs increase, we can scale GoSocial up without affecting the application server.
  5. We get to use Go instead of Javascript.



So we decided to split our social processing out into its own service—and GoSocial was born.

So far, GoSocial has served us well. It’s been performant and reliable, and it’s allowed us to quickly prototype social experiments.

If you liked this post, you should recommend it below, so that more connections will be made in GoSocial. And you should check out [How we run concurrent GoSocial queries](https://medium.com/p/28e5841b05b5)—it’s a slightly deeper dive into one use of GoSocial.
