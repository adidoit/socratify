---
title: "How key-based cache expiration works"
company: "basecamp"
url: "https://signalvnoise.com/posts/3113-how-key-based-cache-expiration-works"
type: "final_harvest"
date: "2025-09-15"
---

#  How key-based cache expiration works 

[![David](https://37assets.37signals.com/svn/1053-DHH.jpg)](/writers/dhh) [David](/writers/dhh) _wrote this on_ Feb 19 2012 [67 comments](/posts/3113-how-key-based-cache-expiration-works?67#comments)

> There are only two hard things in Computer Science: cache invalidation and naming things — Phil Karlton

Doing cache invalidation by hand is an incredibly frustrating and error-prone process. You’re very likely to forget a spot and let stale data get served. That’s enough to turn most people off russian-doll caching structures, [like the one we’re using for Basecamp Next](http://37signals.com/svn/posts/3112-how-basecamp-next-got-to-be-so-damn-fast-without-using-much-client-side-ui).

Thankfully there’s a better way. A much better way. It’s called key-based cache expiration and it works like this:

  1. **The cache key is the fluid part and the cache content is the fixed part.** A given key should always return the same content. You never update the content after it’s been written and you never try to expire it either.
  2. **The key is calculated in lock-step with the object that’s represented in the content.** This is commonly done by making a timestamp part of the key, so for example [class]/[id]-[timestamp], like todos/5-20110218104500 or projects/15-20110218104500, which is what Active Record in Rails does by default when you call #cache_key.
  3. **When the key changes, you simply write the new content to this new key.** So if you update the todo, the key changes from todos/5-2011021810 _4500_ to todos/5-2011021810 _5545_ , and thus the new content is written based on the updated object.
  4. **This generates a lot of cache garbage.** Once we’ve updated the todo, the old cache will never get read again. The beauty of that system is that you just don’t care. Memcached will automatically evict the oldest keys first when it runs out of space. It can do this because it keeps track of when everything was last read.
  5. **You deal with dependency structures by tying the model objects together on updates.** So if you change a todo that belongs to a todolist that belongs to a project, you update the updated_at timestamp on every part of the chain, which will automatically then update the cache keys based on these objects. In Rails, you can declare it like this:

![](https://37assets.37signals.com/svn/787-nested-chain-485-2-1.png)

  6. **The caching itself then happens in the views based on partials rendering the objects in question.** This can be neatly nested like below where each call to `cache` will call #cache_key on the elements of the passed-in array. So in the first case, the cache key ends up being something like v5/projects/5-20110219102600. That key is then updated when the object is updated as described in the process above, and the proper cache is always fetched.
![](https://37assets.37signals.com/svn/785-nested-caching-485.png) 


This process makes it trivial to implement caching schemes and trust that you’re never going to serve stale data. There’s no messy cleanup to deal with since you’re not obligated to track down every spot that might update an object. The updated_at field that’s part of all the caching keys automatically takes care of that for you, wherever that update came from.
