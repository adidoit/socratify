---
title: "A Behind-the-Scenes Look at How We Release the Spotify App (Part 1)"
author: "Unknown"
url: "https://engineering.atspotify.com/2025/4/how-we-release-the-spotify-app-part-1/"
published_date: "Unknown"
downloaded_date: "2025-09-15T10:17:25.931082"
company: "spotify"
---

# A Behind-the-Scenes Look at How We Release the Spotify App (Part 1)
![Feature Image](/_next/image?url=https%3A%2F%2Fimages.ctfassets.net%2Fp762jor363g1%2Fattachment_3dc6a93e79a01019b1a0af444c4ac3eb%2F3e02799f94ce0e7047444f68d890141e%2Fattachment_3dc6a93e79a01019b1a0af444c4ac3eb.png&w=1920&q=75)
Developing and releasing mobile apps at scale is a big challenge. With each weekly release of our mobile app for iOS and Android, hundreds of changes go out to more than 675 million users all over the world and on all kinds of mobile devices. A lot can go wrong, so discovering and mitigating potential and confirmed issues is critical to ensuring a smooth listening experience. Every feature could impact the app’s stability and user experience, so making sure we roll them out in a coordinated and prioritized way is also something that has to be taken care of.
At Spotify, our Release team has a dual mission: (1) to oversee the release of the main Spotify app and (2) to build the necessary tools to support this process. Day-to-day coordination is handled by the full-time Release Manager with the support of the rest of the team.
![attachment_2d23e1ed0ac7144ae71da34e8004b72d](//images.ctfassets.net/p762jor363g1/attachment_2d23e1ed0ac7144ae71da34e8004b72d/d3c133f6c2e27ae796745fb3739ef2a3/attachment_2d23e1ed0ac7144ae71da34e8004b72d.png)
_We have a logo, which means we mean serious business_
When it comes to releasing the app, the core responsibilities of the Release team are twofold:
1. Making sure that the time from when the developer merges their code into the main branch to when it’s available to users is as short as possible
2. To ensure that quality meets our standards
At times, friction exists between these two goals, and much of the craft of release management is about mitigating this, both with tooling and with informed coordination and decision-making. Instances when this balance needs to be struck might include the following:
* **Prioritizing accordingly** — not all bugs are created equal. A crash during signup or playback demands immediate attention, while a post-logout crash might be less urgent.
* **Identifying a fallback** — if a bug affects a specific A/B test group, we can temporarily route all users to the working experience via backend adjustments, addressing the client-side fix in the next release. This keeps the release on track without sacrificing user experience.
* **Acting quickly when necessary** — even a minor bug affecting a small but significant user group (e.g., crashes in a specific region) might warrant a swift resolution.
## The release cycle
To illustrate our release cycle, let’s follow the journey of version 8.9.2 from inception to rollout.
### Friday, September 20: A new version is born
Each release cycle kicks off on a Friday morning, when the release of the previous version has been cut. Once this has been done, it’s time to start the work on the upcoming version.
![attachment_43203db249924653d8a01a6e5106c01a](//images.ctfassets.net/p762jor363g1/attachment_43203db249924653d8a01a6e5106c01a/da0cf623c662931589337f3533593b8a/attachment_43203db249924653d8a01a6e5106c01a.png)
At Spotify, we practice trunk-based development, meaning developers merge their code into the main branch as soon as it’s tested and reviewed.
However, we make an exception for major changes: Large-scale or infrastructure updates are merged earlier in the cycle (typically on the first day, Friday of Week 1). This gives us ample time for thorough testing, leveraging both internal teams and external alpha users to identify and fix issues early on.
With Spotify 8.9.2, we planned to roll out the Audiobooks feature in some markets — it had been available behind a feature flag in the backend for a number of releases, for internal testing to discover any bugs that might impede the planned rollout. This was an important new feature for the company, and we wanted to make sure we got it right, particularly since marketing activities and events were already scheduled.
The Release Manager made sure, well in advance, that it was the only big feature rolling out with this release — another new feature that initially had been scheduled to roll out in the same week was rescheduled for the following week.
Other teams could still merge code at any moment, but we strongly encouraged them to use feature flags. If that wasn’t possible, we asked them to avoid merging any high-risk changes on that particular week.
### Friday, September 20 – Thursday, September 26
![attachment_2c617251e85019cc19bf793b1a9b1d7c](//images.ctfassets.net/p762jor363g1/attachment_2c617251e85019cc19bf793b1a9b1d7c/b44ce19734ea217629ed9831f5054dd4/attachment_2c617251e85019cc19bf793b1a9b1d7c.png)
Apart from the additional actions during the first day, each day of the first week of the release cycle basically looks the same.
* Early each morning, nightly builds of the main branch are sent out internally and to our alpha users.
* Teams develop and merge new code. The developers and their teams make sure that the code is tested and reviewed beforehand.
* Bug reports are filed by internal and external alpha users. When the owner of the affected feature is unknown to the reporter, the Release Manager makes sure that the bug report gets assigned to the correct team.
* Crash rates and other metrics are tracked for each build both automatically and manually. Automatic bug tickets are created when a crash or other issue exceeds our predefined severity threshold; manual tickets are created when something is deemed worthy of investigation by the Release Manager or any other employee.
To help in monitoring the status of an upcoming release, we make use of our Release Manager Dashboard, which collects all the relevant release information in the same place:
![attachment_284f6b46a13107b71fbf9d4c269bfb40](//images.ctfassets.net/p762jor363g1/attachment_284f6b46a13107b71fbf9d4c269bfb40/a6eea4fc9ad9c87858811694d82319f5/attachment_284f6b46a13107b71fbf9d4c269bfb40.jpg)
Some examples of the data found in the dashboard are as follows:
* Blocking bugs
* Latest build available, passing tests, and distributed through the alpha program in the app store
* Crashes and ANRs (App Not Responding) per unit of consumption
* Daily usage
* Status of the distribution jobs that distribute the app internally and externally
By this time, the Audiobooks feature had been turned on for most employees. So in addition to the regular [process](https://open.spotify.com/album/1Dgi0q8i4v7QMdklGzwmU9) for this particular release, both the Release Manager and the Audiobooks team looked through all the crashes happening in the client to see if anything might put the Audiobook rollout in jeopardy. Even a seemingly minor crash affecting a small number of employees could signify a potential issue impacting a large user base upon rollout. Therefore, it’s important to investigate and mitigate any issues as soon as possible.
### Friday, September 27: Fri-_yay_ is branch day!
Once a week passed, it was time for the 8.9.2 version to be branched off for releasing, initiating the most intensive part of the release process. Once a release has been branched off, it is regarded as the _current_ release and only critical bug fixes are permitted. Our weekly release cadence allows less critical bugs and new features to be addressed in subsequent releases, and teams generally avoid last-minute changes to minimize risk.
![attachment_113fcd77653edc427ae0a269f8a910e6](//images.ctfassets.net/p762jor363g1/attachment_113fcd77653edc427ae0a269f8a910e6/e339f4aaf190c8244071e8062000e821/attachment_113fcd77653edc427ae0a269f8a910e6.png)
Once branching is done, the Release Manager coordinates the work of releasing the version as soon as possible with all stakeholders.
To help us gather additional data on the quality of the release branch, we have a public beta program that is taken from the release branch — these builds are expected to be more stable than our alpha builds.
On Fridays during Week 2, teams perform manual regression testing on their owned features and report their results. Teams with high confidence in their automated tests and pre-merge routines can opt out of manual testing.
Throughout the testing process, teams may uncover bugs in their own or in other teams’ features and will file tickets for these. Additionally, crash reports and bug reports from internal and external users also trigger the creation of new bug tickets.
For 8.9.2, the Audiobooks team was particularly vigilant during this phase, meticulously searching for any potential issues. At this point, it’s not uncommon to discuss bugs and decide if they warrant a release blocker. Good release management means objectively looking at risk, potential impact, and workarounds.
### Friday, September 27 – Monday, September 30: Getting it ready for submission
During the weekend after branching, our beta users provide additional runtime of the app, which either increases our confidence in releasing it or helps us to find issues that had not been found earlier, by the time we get back to work on Monday.
Ideally, we aim to submit the app to the app stores on Monday. However, complex bugs or unforeseen issues can extend this process by a few days. To streamline communication and coordination for each release, the Release Manager, feature teams, and other stakeholders share updates, ask questions, and flag potential concerns on a dedicated Slack channel.
The Release Manager ensures bugs are assigned to the correct team and prioritized appropriately, manual testing is executed and reported, and any release-blocking bugs (there tend to be perhaps three to five such bugs per release) are fixed on the release branch.
![Timeline 4_Final](//images.ctfassets.net/p762jor363g1/attachment_add56f8070f8e858b5aff9bb96523dca/13e4f26eea80c51d3307f476efb8aa6f/attachment_add56f8070f8e858b5aff9bb96523dca.png)
Before we submit a build to the app stores, we want to make sure the following criteria are met:
* All commits on the release branch are included in the latest build and have passed automated tests.
* No blocking bug tickets remain open.
* All teams have signed off and approved.
* Crash rates and other key metrics are below our defined thresholds.
* The app version to be released has been used to play a sufficient amount of content.
The Release Manager Dashboard provides a clear overview of these criteria, using color-coding (red/yellow/green) for quick assessment.
For the 8.9.2 release, we provided additional test accounts with the Audiobooks functionality enabled, as well as detailed testing instructions to the various app stores to ensure they were aware of the new features and wouldn’t be caught off guard when we started to roll out the functionality.
### Tuesday, October 1 – Wednesday, October 2: Rollout
Once the app is approved for a platform, we roll it out in two phases: first, to a small percentage of users and, then, the following day, to 100% of users.
When a release has been rolled out to 1%, we expect the dashboard to look like this:
![attachment_ad3295c41b6e64c5df20818b2e1795dc](//images.ctfassets.net/p762jor363g1/attachment_ad3295c41b6e64c5df20818b2e1795dc/96b367805664296581ebe4c2d91325a5/attachment_ad3295c41b6e64c5df20818b2e1795dc.jpg)
The only remaining items, indicated in yellow, needed before full rollout are the ITGC tickets, where we check to see that reporting from the client to the backend is working as necessary. It’s not unusual to uncover minor bugs that, while acceptable in the current version, would be considered blockers for future releases. In severe cases, we might temporarily halt the feature rollout and resume with the next release.
Thanks to our large user base, even a small initial rollout percentage allows us to quickly identify critical issues that may have slipped through the cracks during the internal and public alpha and beta testing.
If we find a severe issue during the first rollout phase, we immediately pause the rollout and the team responsible starts to create a fix. Ideally, the fix is ready before the next version branches, allowing us to submit an updated build. However, if the fix isn’t timely, we may face the difficult decision of canceling either the current or the upcoming release to prevent the complexity of managing two active release branches simultaneously. Once we have reached 100%, we continue monitoring the state of the release over the next week.
For version 8.9.2, once a sufficient user base was using the new version, the Audiobooks team initiated their phased rollout. This involved gradually enabling the Audiobooks feature for a small percentage of users in specific markets using a backend feature flag.
Fortunately, for version 8.9.2, the Audiobooks feature met our quality standards, and the rollout successfully ramped up to 100% over the following days.
Using the release procedure described above, we are able to roll out more than 95% of releases to all our users. The weekly cadence also means that a canceled release is not the end of the world for the feature teams, since a new release will go out the following week. In the same way, users will be able to get a new version of the app every week as long as it meets our quality standards.
![attachment_a67de7a0c50886b1b70292e995d26930](//images.ctfassets.net/p762jor363g1/attachment_a67de7a0c50886b1b70292e995d26930/b9561e75c4b6eeea3fa96e3b84087b46/attachment_a67de7a0c50886b1b70292e995d26930.png)
## Summary
Spotify’s weekly mobile app release process tries to strike a balance between speed and quality. The person at the helm of the process is the Release Manager, who handles communication and coordination with feature teams and other stakeholders throughout the release cycle with the help of the Release Squad. Tools like the Release Manager Dashboard play an important role in enabling the Release Manager to make fast and accurate decisions.
Detailed documentation of the tools and processes helps guide all the teams involved.
This robust system allows Spotify to consistently update its app, quickly address issues, and introduce new features like Audiobooks, all while minimizing disruptions to the user experience.
Stay tuned for part 2, where we’ll look under the hood to see how the systems (and robots!) that power the Release Manager Dashboard work.
Tags: [Developer Experience](/tag/developer-experience), [engineering culture](/tag/engineering-culture), [Mobile](/tag/mobile)