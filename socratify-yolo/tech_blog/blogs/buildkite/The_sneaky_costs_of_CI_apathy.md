---
title: "The sneaky costs of CI apathy"
author: "Unknown"
url: "https://buildkite.com/resources/blog/the-sneaky-costs-of-ci-apathy-and-what-top-teams-do-about-it/"
date: "2025-09-15"
---

![](https://www.datocms-assets.com/29977/1745463543-the-sneaky-costs-of-ci-apathy.jpg?auto=format&fit=crop&h=440&w=880&dpr=2)
It starts out simply enough. Your team builds a CI pipeline that works: tests are passing, merges are fast, deployments are uneventful. But over time, cracks appear:
* Build times gradually climb, from 5 minutes to 10, then 20, then 30
* Tests that were once totally reliable now fail intermittently, and for reasons that aren’t clear
* Jobs start hitting resource limits and crash, delaying or blocking important releases
In other words, velocity slows, but in such small increments that nobody quite notices—until every change is an hour-long wait and a roll of the dice. Engineers start planning their days around the quirks of the CI system, rather than around their actual priorities:
> I'll make this change now and then go to lunch. Hopefully it'll pass.
> We should hold off merging this today. With the big release tomorrow, we can't risk taking down the pipeline.
> I wouldn't touch that part of the code unless you have to. The tests are a nightmare.
At some point, you cross a threshold, and what began as an occasional frustration becomes something far more problematic: apathy.
##**CI apathy: when frustration becomes resignation**
CI apathy isn't just accepting the reality that builds are sometimes slow, or that tests are sometimes flaky. It's the collective resignation that slow, flaky CI is _just how it is_ —and that there's not much to be done about it.
No one decides to stop caring about reliable CI. It happens little by little, through a thousand tiny concessions, and a gradual normalization of dysfunction that becomes embedded in the culture.
***Engineers stop advocating for improvements:**"I won't bother filing an issue for this; it won’t get fixed."
***PMs build longer delivery timelines into their schedules:**"We have to account for delivery delays."
***Leadership dismisses the issues as technical complaints rather than business problems:**"This is just an unavoidable cost of growing the team."
***And worst, new team members pick up this mindset:**"It’s painful. But it's just how it is here."
What makes CI apathy especially hard to crack is that it can masquerade as pragmatism. In the spirit of being practical, teams accept the limitations and roll with them—and occasionally work around them by splitting up test suites, adding retry logic, bumping compute and memory allocation, etc. All the while, the long-term cost is adding up.
##**Cost is about more than time and money**
The ultimate cost of CI apathy goes way beyond wasted compute resources or engineering hours (which can certainly pile up), and affects every part of the organization:
**Creative momentum evaporates.**The flow state that drives developer productivity becomes impossible to achieve when it’s constantly interrupted by CI issues. Engineers context-switch away from problems while waiting for builds, fragmenting their thinking and diminishing the quality of their work.
**Innovation suffers.**Simply put, slow build times make it harder to experiment and learn. You don’t get new features into customers’ hands as quickly and your feedback cycles are drawn out. What’s more, flaky CI has a chilling effect: teams opt for safer, incremental changes rather than bold refactorings or architectural improvements.
**Quality degrades.**When tests frequently fail, teams tend to write fewer, less comprehensive tests. Manual testing increases, but human attention is finite and inconsistent, leading to issues that crop up later in production.
**Team dynamics deteriorate.**CI failures create friction between team members: "Who broke the build?" "Why didn't the tests catch this?" "We need to roll this change back because it introduced flakiness."
**Talent walks away.**Your best engineers, the ones who care deeply about craftsmanship and efficiency, become frustrated and leave. Those who remain grow increasingly disengaged.
Perhaps most concerning, the normalization of CI dysfunction reinforces a culture of low standards and workarounds. But this mindset doesn't stay confined to CI—it spreads to other aspects of your engineering practice, creating a downward spiral of technical debt and compromised quality.
The business impact of all this is profound, but often invisible until it's too late. Your competitors, who've mastered their delivery pipelines, ship faster, pivot more readily, and attract and retain better talent. While your team sinks deeper into CI apathy, they're innovating and capturing market share.
##**Recognizing and addressing CI apathy**
Before you can fix a problem, you have to recognize it’s there. Apathy rarely announces itself—you need to look for the subtle signals:
* The language your team uses: "That's just how CI is here", or "Don't expect it to change."
* "Clicked re-run" messages popping up in Slack, often accompanied by eyeroll emojis.
* Engineers adding retry logic to tests rather than addressing the underlying issues.
* The practice of commenting out flaky tests rather than fixing them.
* The absence of improvement initiatives in your CI/CD roadmap.
* The growing gap between local development workflows and CI behavior.
Once you spot these patterns, breaking the cycle requires both technical and cultural intervention:
1.**Make CI performance visible.**Start tracking key metrics like build time, queue time, failure rate, and flakiness. Visualize the trends over time and share them widely within the organization.
2.**Elevate CI reliability to a business concern.**Frame CI issues in terms of delivery velocity and team productivity, not just technical debt. Help leadership understand the direct connection between CI performance and business outcomes.
3.**Create space for improvement.**Dedicate engineering time specifically to CI optimization. This might mean a dedicated working group or rotating engineers through a "build reliability" role.
4.**Celebrate progress.**When you shave minutes off the build time or eliminate a flaky test, recognize that as a meaningful achievement. Wins like these compound over time.
5.**Declare bankruptcy when necessary.**Sometimes, incremental improvement just isn't enough. Be willing to consider rebuilding your CI pipeline if it's becoming too brittle or complex to maintain.
The key insight is that CI excellence isn't just about technology—it's about establishing a feedback loop where improvements are valued, prioritized, and celebrated. This creates momentum that can reverse the spiral of apathy.
##**Building a culture of excellence: the Delivery First mindset**
The journey to CI excellence begins with a simple but powerful acknowledgment: stop pretending broken CI is normal.
Teams _should_ be frustrated by 45-minute builds. They _should_ be annoyed by flaky tests. They _should_ expect better than "just click re-run." These reactions aren't noise to be ignored or suppressed—they're valuable signals pointing to real problems in your delivery system.
At Buildkite, we've seen that forward-thinking teams don't normalize CI pain. When they see mounting problems, they acknowledge the issues, calculate the costs, and prioritize fixing them.
### What it feels like when CI finally works for you
Imagine what your engineering organization could achieve when:
* Builds finish in under five minutes
* Tests only fail when something’s actually wrong
* Engineers don't plan their days around hour-long PR jobs
* Small changes don't get stuck behind large ones
* CI becomes something that helps your team go faster, not something it has to fight with
This isn't a fantasy—it's what we've seen time and again with teams that embrace what we call a [Delivery First mindset](https://buildkite.com/resources/blog/the-delivery-first-mindset/), an approach that places software delivery at the core of your engineering culture, on par with software creation itself.
With this perspective, teams:
* Deploy continuously and confidently
* Make smaller, safer changes more frequently
* Set ambitious targets that drive meaningful improvements
* Build security and compliance directly into the delivery process
* Experiment without fear of breaking the system
Most importantly, they focus their creative energy on solving product problems, not wrestling with their tooling.
## Take the next step
The transformation from CI apathy to delivery excellence doesn't happen overnight. It begins with recognizing that your delivery pipeline isn't just plumbing—it's a key differentiator that directly impacts how quickly and confidently you can deliver value. When you give it the attention it deserves, you transform your entire engineering culture.
At Buildkite, we're committed to helping teams break free from CI apathy by providing the flexibility and scale needed to implement delivery-first principles. The most successful engineering organizations have recognized that the gulf between good and great software often isn't in the code itself, but in how efficiently that code reaches users.
Learn more from some of our customers who've done it:
* [How Uber accelerated its software delivery by moving from Jenkins to Buildkite](https://buildkite.com/resources/webinars/uber-fast-reliable-and-scalable-ci/)
* [How Rippling improved CI performance and developer experience—and cut costs in half—by switching from Jenkins to Buildkite](https://buildkite.com/resources/webinars/reduce-infra-cost-spot-instances/)
### How Uber accelerates software delivery with fast, reliable, and scalable CI
Register to watch the webinar
![Fast, reliable, scalable CI: How Uber accelerates software delivery](https://www.datocms-assets.com/29977/1728392187-webinar-uber-2-feature.png?auto=format&fit=crop&h=440&w=880)
Recorded on
February 11, 2024
Length
24 minutes
