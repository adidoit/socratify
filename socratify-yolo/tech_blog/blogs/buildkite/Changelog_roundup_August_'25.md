---
title: "Changelog roundup: August '25"
author: "Unknown"
url: "https://buildkite.com/resources/blog/changelog-roundup-august-2025-edition/"
date: "2025-09-15"
---

![](https://www.datocms-assets.com/29977/1754675580-blog-changelog-roundup.jpg?auto=format&fit=crop&h=440&w=880&dpr=2)

Welcome to the latest edition of the [_Buildkite Changelog_](https://buildkite.com/resources/changelog/) roundup! Over the last few months, we've been hard at work on new product features and efficiency improvements designed to help you and your team ship faster than ever before. 🚀

Here's what we're showcasing today:

* Improvements to the Agent Stack for Kubernetes
* The next phase of the build page experience
* Introducing the new Pipeline Examples Gallery
* Many new features and improvements in Test Engine
* Mac M4 Pro support in Buildkite hosted agents — an industry-leading upgrade!

### Improvements to the Agent stack for Kubernetes

We’ve made a series of improvements to the [Buildkite Agent Stack for Kubernetes](https://buildkite.com/docs/agent/v3/agent-stack-k8s) focused on simpler setup, better security, and more reliable scaling:

***Simpler setup:**You can now deploy a stack with just a single cluster-scoped agent token — GraphQL tokens, org slugs, and cluster UUIDs are no longer required. Also, default cluster queues are not recognized automatically, so it's no longer necessary to specify an explicitly named queue called`kubernetes`.
***Better security:**By default, GraphQL tokens are no longer neeeded. For greater security, jobs run on the REST API using scoped agent tokens. In addition, the team has started development on scoped secrets, with the goal of more secure isolation across pipelines and environments.
***More reliable scaling:**The agent stack can now handle even greater volumes of jobs, particularly in high-concurrency environments. To achieve this, job environment variables are passed directly between job containers, reducing per-job Kubernetes object sizes.

Here's a quick walkthrough with Buildkite engineer Josh Deprez:

For more details, including full release notes, [check out the Changelog post](https://buildkite.com/resources/changelog/292-buildkite-agent-stack-for-kubernetes-improvements-easier-to-adopt-scale-and-maintain/).

### The next phase of the build page experience

We know that everyone works differently, so we’ve personalized and streamlined the build page experience according to your own preferences. Whether you're reviewing a failed test, scanning logs, adding annotations, or debugging performance, we hope that these updates improve the experience you have across pipelines of all shapes and sizes.

Here are the updates we’re most excited to share:

***Build header:**We've redesigned the header to be more condensed so you can more easily view actionable information like failed steps and annotations. With this revision, the build status is also now always visible.
***Overview tab:**The new Overview tab contains high-level build information, such as the commit message, build creator, build trigger, and more.
***Step search:**We've also added a new search, allowing you to find and jump to steps across your build. For quicker navigability, you can press`s`to open the search box,`Enter`to open a step, or`Shift`\+`Enter`to focus the step view.
***Jump to failure:**The jump to failure action has moved into the new collapsible sidebar, making it possible to cycle through failures wherever you are in the build.

Here's a demo from Buildkite engineer Chris Campbell that walks you through everything:

To learn more, [check out the Changelog post](https://buildkite.com/resources/changelog/290-the-next-phase-of-the-build-page-experience/).

### Introducing the new Pipeline Examples gallery

Starting from scratch in Buildkite can sometimes feel like opening a blank cookbook — plenty of ingredients at hand, but no idea how to combine them. Now, with the introduction of the new [Pipeline Examples Gallery](https://buildkite.com/resources/examples/), you get full recipes out of the box: you can explore pipelines that run in real time, browse actual build steps and logs, and easily fork and extend the examples yourself — no setup or sign-up required.

Here's Buildkite engineer Sarah Jackson with a demo of how to browse, filter, and search the full set of examples — all of which are backed by publicly accessible Buildkite pipelines:

And here's how to set up a new pipeline from an example in the Buildkite dashboard:

Whether you’re evaluating Buildkite, onboarding a team, or just looking for inspiration, the Examples Gallery gives you a whole new way to explore what’s possible and get started easily. Got an idea for an example? [Let us know](https://forum.buildkite.community/) — or submit one yourself on [_GitHub_](https://github.com/buildkite).

To learn more, [check out the Changelog post](https://buildkite.com/resources/changelog/296-explore-and-launch-new-example-pipelines-now-live/).

### New features and improvements in Test Engine

We’re also excited to share some improvements we've made recently to [_Buildkite Test Engine_](https://buildkite.com/docs/test-engine) to help tighten your feedback loops, expand and improve test coverage and performance, and customize your Test Engine experience.

Key features to check out:

* [**Send automated Slack Notifications**](https://buildkite.com/resources/changelog/288-send-slack-notifications-from-test-engine/)**:**You can now send Slack notifications from Test Engine. Slack notifications can be triggered when a test state changes or when a test label is added or removed.
* [**Send webhooks, label tests, and save test filters**](https://buildkite.com/resources/changelog/285-send-webhooks-from-test-engine/): You can now send webhooks, label tests, and save test filters. Webhooks are triggered by events, labels let you categorize tests, and saved filters let you save your favorite filters using tags and labels.
* [**Customize metrics views**](https://buildkite.com/resources/changelog/294-customize-test-engine-tests-view/)**:**You can now customize which metrics are displayed in the Tests View, and we've added new metrics–like reliability, average duration, executions, and more.
* [**Manage flaky tests**](https://buildkite.com/resources/changelog/295-improved-flaky-test-management-in-test-engine/)**:**You can now see all actively flaky tests in one view automatically update that view by removing the “flaky” label, and use the new Ownership filter to view all tests owned by your team.
* [**Expanded support for PyTest**](https://buildkite.com/resources/changelog/282-python-support-for-test-splitting-and-auto-quarantining/)**:**With our expanded support for test splitting and auto-quarantining, you can achieve faster critical path time, spend less time on manual triage, and better isolate flaky tests.
* [**New support for Vitest**](https://buildkite.com/resources/changelog/291-vitest-support-for-javascript-test-collector/)**:**With our new support, you can collect test results from your Vitest test suites, track test performance and flakiness, automatically quarantine flaky tests, and benefit from built-in, powerful analytics and insights.

![Screenshot of a Slack notification sent from Test Engine](https://www.datocms-assets.com/29977/1749618806-20250611-test-engine-slack-notifications.png?auto=format&fit=max&w=800)

A Slack notification sent from Test Engine

![A screenshot of the Flaky saved view in Test Engine](https://www.datocms-assets.com/29977/1751848316-20250624-test-engine-flaky-view.png?auto=format&fit=max&w=800)

The Flaky saved view in Test Engine

### Mac M4 Pro support in Buildkite hosted agents

All macOS workloads on Buildkite hosted agents have been upgraded to run on Apple’s latest M4 Pro generation hardware, delivering even better price-performance for your CI builds. This generation of hardware features faster startup times and clean, ephemeral environments for each job.

The M4 Pro chip delivers meaningful improvements, including:

***Up to 30-45 % faster CPU performance**in real-world Xcode builds and test runs
***Next-generation GPU architecture**for smoother UI testing and graphics-heavy tasks
***Higher memory bandwidth**for faster access to large codebases and build artifacts

With these upgrades, we’ve updated our Mac shapes two new M4-optimized options:

***Medium**(6x28)
***Large**(12x56)

To learn more, [check out the Changelog post](https://buildkite.com/resources/changelog/293-mac-hosted-agents-now-running-on-m4-pro-hardware/), and if you have any questions, feel free to reach out to us directly at [_support@buildkite.com_](mailto:support@buildkite.com).

### Wrapping up

That's all for now! We hope this latest round of features and improvements make your experience with Buildkite even better, and we'd love to hear how they work out for you and your team.

[Drop us a line in the Buildkite forum](https://forum.buildkite.community/) with your thoughts, questions, or suggestions — and be sure to [keep an eye on the Changelog](https://buildkite.com/resources/changelog/) for the latest improvements as they roll out.

Until next time! 👋

#### Written by

![Headshot of Christian Nunciato](https://www.datocms-assets.com/29977/1734033195-img_7394.jpg?auto=format&fit=crop&h=80&w=80)

Christian Nunciato

#### Tags

[ Kubernetes ](/resources/blog/tag/kubernetes/)[ Pipelines ](/resources/blog/tag/pipelines/)[ Examples ](/resources/blog/tag/examples/)[ Test Engine ](/resources/blog/tag/test-engine/)[ Hosted Agents ](/resources/blog/tag/hosted-agents/)

#### Share

[ ](https://twitter.com/share?url=https://buildkite.com/resources/blog/changelog-roundup-august-2025-edition/%3Futm_source%3Dreferral%26utm_medium%3DTwitter%26text%3DRead%20Changelog%20roundup%3A%20August%20'25%20on%20%40buildkite%20blog) [ ](https://www.linkedin.com/shareArticle?mini=true&url=https://buildkite.com/resources/blog/changelog-roundup-august-2025-edition/?utm_source=referral&utm_medium=LinkedIn)

#### Subscribe to our newsletter

Get product updates and industry insights, direct to your inbox.
