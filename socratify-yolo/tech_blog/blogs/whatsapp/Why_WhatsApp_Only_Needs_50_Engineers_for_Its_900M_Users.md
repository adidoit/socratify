---
title: "Why WhatsApp Only Needs 50 Engineers for Its 900M Users"
company: "whatsapp"
url: "https://www.wired.com/2015/09/whatsapp-serves-900-million-users-50-engineers/"
type: "final_harvest"
date: "2025-09-15"
---

[Cade Metz](/author/cade-metz/)

[Business](/category/business)

Sep 15, 2015 7:00 AM

# Why WhatsApp Only Needs 50 Engineers for Its 900M Users

One of the (many) intriguing parts of the WhatsApp story is that it has achieved such enormous scale with such a tiny team.

Save StorySave this story

Save StorySave this story

Earlier this month, in a post to his Facebook page, WhatsApp CEO Jan Koum announced that his company's instant messaging service is now used by [more than 900 million people](https://www.facebook.com/jan.koum/posts/10153580960970011?pnref=story). And then Facebook CEO Mark Zuckerberg promptly responded with two posts of his own. One said "congrats," and the other included a cheeky photo Zuckerberg had taken of Koum as the WhatsApp CEO keyed his 900-million-user post into a smartphone. "Here's an action shot of you writing this update," Zuckerberg wrote.

WhatsApp is owned by Facebook, after Zuckerberg and company paid $19 billion for the startup a little more than a year ago. That means Facebook now runs three of the most popular apps on the internet. Its primary social networking service is used by more than 1.5 billion people worldwide, and Facebook Messenger, an instant messaging service spun off from Facebook proper, spans 700 million. But the 900 million-user milestone announced by Koun is very much a WhatsApp achievement, not a product of the formidable Facebook machine.

> WhatsApp shows the way forward to a world where internet services can serve a massive audience with help from few people.

One of the (many) intriguing parts of the WhatsApp story is that it has achieved such enormous scale with such a tiny team. When the company was acquired by Facebook, it had 35 engineers and reached more than 450 million users. Today, it employs only about 50 engineers, though the number of WhatsApp users has doubled, and this tiny engineering staff continues to run things almost entirely on its own. In a world where so many internet services are rapidly expanding to millions upon millions of users, WhatsApp shows the way forward---at least in part.

WhatsApp doesn't talk much about its engineering work---or any other part of its operation, for that matter---but yesterday, at an event in San Jose, California, WhatsApp software engineer Jamshid Mahdavi [took the stage](https://www.youtube.com/watch?v=57Ch2j8U0lk) to briefly discuss the company's rather unusual methods. Part of the trick is that the company builds its service using a programming language called Erlang. Though not all that popular across the wider coding community, Erlang is particularly well suited to juggling communications from a huge number of users, and it lets engineers deploy new code on the fly. But Mahdavi says that the trick is as much about attitude as technology.

Mahdavi joined WhatsApp about two years ago, after the startup was up and running, and its approach to engineering was unlike any he had seen---in part because it used Erlang and a computer operating system called FreeBSD, but also because it strove to keep its operation so simple. "It was a completely different way of building a high-scale infrastructure," he said on Monday. "It was an eye-opener to see the minimalistic approach to solving ... just the problems that needed to be solved."

Code in Parallel

In using Erlang, WhatsApp is part of a larger push towards programming languages that are designed for _concurrency_ , where many processes run at the same time. As internet services reach more people---and juggle more tasks from all those people---such languages become more attractive. Naturally.

With its new anti-spam system---a system for identifying malicious and otherwise unwanted messages on its social network---Facebook [uses a language called Haskell](https://www.wired.com/2015/09/facebooks-new-anti-spam-system-hints-future-coding/). Haskell began as a kind of academic experiment in the late '80s, and it's still not used all that often. But it's ideal for Facebook's spam fighting because it's so good at juggling parallel tasks---and because it lets coders tackle urgent tasks so quickly. Meanwhile, Google and Mozilla, maker of the Firefox browser, are striving for a similar sweet spot with new languages called Go and Rust.

> In essence, WhatsApp is a replacement for telecoms' texting services.

Like Haskell, Erlang is a product of the '80s. Engineers at Ericsson, the Swedish multinational that builds hardware and software for telecom companies, developed the language for use with high-speed phone networks. "Instead of inventing a language and then figuring out what to do with it, they set out to invent a language which solved a very specific problem," says Francesco Cesarini, an Erlang guru based in the UK. "The problem was that of massive scalability and reliability. Phone networks were the only systems at the time who had to display those properties."

Erlang remains on the fringes of the modern coding world, but at WhatsApp and other internet companies, including WeChat and Whisper, it has found a home with new applications that operate not unlike a massive phone network. In essence, WhatsApp is a replacement for cellphone texting services. It too requires that "scalability and reliability."

What's more, Erlang lets coders work at high speed---another essential part of modern software development. It offers a way of deploying new code to an application even as the application continues to run. In an age of constant change, this is more useful than ever.

Keep It Simple, Smarty

The language does have its drawbacks. Relatively few coders know Erlang, and it doesn't necessarily dovetail with a lot of the code already built by today's internet companies. Facebook built its original Facebook Chat app in Erlang but eventually rebuilt so that it would better fit with the rest of its infrastructure. "You had this little island that was Erlang, and it was hard to build enough boats back to the island to make everything hook in," says Facebook vice president of engineering Jay Parikh.

Of course, WhatsApp didn't have to integrate with an existing infrastructure in this way. And Mahdavi believes the relative scarcity of Erlang coders isn't a problem. "Our strategy around recruiting is to find the best and brightest engineers. We don't bring them in specifically because the engineer knows Erlang," Mahdavi said on Monday. "We expect the engineer to come in and spend their first week getting familiar with the language and learning to use the environment. If you hire smart people, they'll be able to do that."

The company has succeeded by hiring engineers who are adaptable---in more ways than one. Asked to explain the company's secret, Mahdavi's response seems far too simple. But that's the point. "The number-one lesson is just be very focused on what you need to do," he said. "Don't spend time getting distracted by other activities, other technologies, even things in the office, like meetings."

At WhatsApp, employees almost never attend a meeting. Yes, there are only a few dozen of them. But that too is the point.
