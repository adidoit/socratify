---
title: "Starless: How we accidentally vanished our most popular GitHub repos"
author: "Jamie Tanna"
url: "https://www.elastic.co/blog/starless-github-repos"
date: "2025-09-15"
---

# Starless: How we accidentally vanished our most popular GitHub repos
How a change targeting internal GitHub repositories backfired and inadvertently made Elastic's public-facing repositories private.
By
[Jamie Tanna](/blog/author/jamie-tanna)
05 September 2025
![blog-starless.jpeg](https://static-www.elastic.co/v3/assets/bltefdd0b53724fa2ce/blta578154d10c0b504/68baf0c9c9b76af9d1394974/blog-starless.jpeg)
What happens when automation makes a change based on assumptions without confirming the state of the real world? In October 2024, we found out in one of the worst ways possible — our most critical public repositories on GitHub were unintentionally marked as private, resulting in a significant outage for our customers.
Engineers in Elastic's Platform Engineering Productivity and InfoSec Product Security teams worked to close a gap in our internal source code supply chain security, by migrating repositories with the**internal**visibility on GitHub to the**private**visibility.
A combination of contributing factors led to an unintended impact on public-facing repositories. We have learned valuable lessons from this incident that are worth sharing.
## Why were we making the change?
Elastic is a fairly large user of GitHub with around 3,000 repositories that include contributions from a globally distributed set of employees, various contractors, and the amazing global developer community.
Elastic has customers in various environments from small businesses to intelligence agencies who depend on our software, as well as many Open Source users who use our software to manage highly critical data for their organization and naturally expect high levels of integrity and supply chain security. These expectations are true for the supply chain security of the Open Source and proprietary projects that culminate in our public and private repositories.
As part of our ongoing multipronged work to secure Elastic's supply chain security, the security of our source code is one of the areas that we continue to evaluate.
Within GitHub, repositories have three types of visibility:
***Public:**At least read-only from anyone without authentication and is open to the world
***Internal:**At least read-only to any authenticated GitHub user who is part of any of the GitHub organizations under Elastic's GitHub**enterprise**
***Private:**At least read-only to specific users and teams within the Elastic GitHub organization who have explicitly granted access. Private repositories in the Elastic org require single sign-on (SSO).
For most readers, you'll likely have only seen**public**and**private**repositories, as**internal**repositories will generally only be used inside [a GitHub**enterprise**](https://docs.github.com/en/get-started/onboarding/getting-started-with-github-enterprise-cloud).
With**internal**repositories, any member of the**enterprise**has default read-only access, which means that a member of [the Logstash plugins organization](https://github.com/logstash) could see any internal repositories in the Elastic organization.
This implied access is in opposition to Elastic's explicit allowlisting of access, so the usage of**internal**repositories was deprecated at Elastic since mid-2023. But we still had a long tail of repositories created at the time which needed migrating to**private**.
We removed all options for internal tooling to create an**internal**repository. Then in October 2024, we planned to migrate the final repositories from**internal**to**private**.
## How does Elastic manage source repositories?
Before we talk about exactly how we planned to migrate our repositories from**internal**to**private**, it's worth sharing some brief background on some of the internal tooling that we have for managing GitHub repositories since the mix of tools was also a contributing factor to the incident.
Terrazzo manages certain configuration for GitHub repositories as YAML files inside another GitHub repository. Once a pull request (PR) has been merged in that repository, Terrazzo automatically applies the changes.
For reasons out of scope of this post, not all repositories are using Terrazzo to manage their repository's settings, which leads to three states of a repository’s configuration management through Terrazzo:
1. A repository's configuration is completely managed through Terrazzo.
2. Only a subset of repository configuration is managed through Terrazzo.
3. No repository configuration is managed through Terrazzo.
With this in mind, if a repository's Terrazzo-based configuration does not have a visibility setting set, our tooling treats it as visibility: private. This means that the second type of repository management may have an _implied_ visibility that is different to the actual visibility of the repository in GitHub.
At the time, Elastic had a total of ~3,000 repositories — roughly 250 were partially managed by Terrazzo; 450 fully managed by Terrazzo; and 100**internal**repositories (in various Terrazzo management states).
## How did we plan to implement the change?
### Determining repositories in scope
Due to a high number of repositories to update, we looked to automate the steps and migrate all repositories in a single change. But before we could make the change, we needed to determine which repositories were in scope and inform repository owners.
To do this, we first collected a list of**internal**repositories via the GitHub APIs and cross referenced this with the list of repositories we know that Terrazzo manages. We needed to do this to make sure that when we came to make the change, we would not have Terrazzo immediately revert the change, as the repository's configuration would say "I'm visibility: internal." While investigating this, we noticed that some repositories did not even have a visibility set, so we decided to set visibility: private for these repositories to be explicit.
Earlier in the month, we had also foreseen that our deployment tooling may be broken by this change, as a couple of machine users would need explicit access to certain repositories. As part of the migration from**internal**to**private**, we would need to make sure that these service accounts had access.
To inform repository owners, we collated these three lists of repositories into a spreadsheet:
* Current**internal**repositories not managed by Terrazzo
* Current**internal**repositories partially or fully managed by Terrazzo
* Repositories that needed to have the service accounts added (regardless of current visibility)
This spreadsheet (with ~350 repositories) was then sent to all of Elastic Engineering to review, and ~10 days later, we started the change.
Although we had requested that Engineering review the spreadsheet’s contents, there were no active, explicit requirements or checks in place for repository owners to confirm.
Additionally, three days before the change, an additional script was created to find repositories that did not specify the visibility in their repository configuration. Tooling that interacts with the repository configuration will infer that “if the visibility field is absent, the repository should default to Private.” This script followed the same logic but did not validate the repository’s visibility on GitHub.
This lack of validation against the _real world_ state led to this script incorrectly including 63 public repositories that did not specify a visibility configuration, which were then added to a second sheet; but, unfortunately, Engineering was not re-requested for review.
### Scripting the repository settings changes
Instead of performing the changes by hand, we prepared a script, which would:
* Loop through a precollected list of repositories (from the spreadsheet)
* Change the repository visibility to private
* Add the required team for deployment tooling service accounts
Alongside this change, there was also a scripted change to the Terrazzo configuration which would:
* Add an explicit visibility: private to repository configurations, where an existing visibility field was not found
* Change repository configurations that had visibility: internal to visibility: private
* Added the _all of engineering_ GitHub team to have read-access to all affected repos
* Added the deployment tooling service accounts team to have read-access to relevant repos
With all these changes involved, this ended up being a PR with 349 files changed, which was reviewed by two other engineers supporting the change.
## What was the outcome?
As mentioned previously, the outcome was not good. Within six minutes of executing the script, we had a report on Slack that [elastic/kibana](https://github.com/elastic/kibana) was marked as**private**as was [elastic/elasticsearch](https://github.com/elastic/elasticsearch). We canceled the script's execution, but by this time, 63 previously**public**repositories were now**private**. With these repositories now private, automated build pipelines would start failing inside and outside of Elastic, blocking operations for Elastic, our customers, and Open Source users alike.
### Elastic’s incident management process
One of the key factors to this incident being handled well was Elastic’s well-practiced and polished incident management process. Although this was a significant outage, the rigor of our process and having an experienced "major incident" commander led to this being a more smooth process (or at least as much as a significant incident can ever be smooth!) as well as making sure everyone involved was supported.
Within a few minutes of the report on Slack, engineers responsible for the change had created an incident channel, and within 10 minutes they had escalated it to a high severity incident. During the incident, responders worked to confirm impact and ensure that public messaging noted that this was an internal change gone bad, rather than a _bad actor_.
A large amount of the elapsed time during this incident was working in close collaboration with GitHub support, where we worked to understand what would be needed to restore the visibility of the repositories. Although we had the capability to revert the visibility changes for these repositories, we weren’t sure whether this was the right course of action, as we weren’t sure if this may cause unintended impact on GitHub’s side, or prevent GitHub from supporting the restoration of GitHub stars we had lost when the repository went private.
### Collaboration with GitHub
As we found during the incident, when a repository is moved from**public**to**private**, there are a few tasks that GitHub’s platform undertakes, which can take longer depending on the size of the repository.
Firstly, the network of forked repositories needs to be _reparented_ by finding the next fork to show as the _fork parent_ , where new PRs are automagically suggested to be raised. Additionally, there are some internal background processes (e.g., removing any _watchers_ or GitHub stars) that need to be completed before you can update the visibility again.
For Elasticsearch’s case, we had to wait ~90 minutes from the repository being marked as private to being able to make the repository public again, whereas smaller repositories could be moved back to public mere minutes later.
Within a stressful seven hours, all 63 affected repositories were back to**public**.
### Starless to stardom
A much lower priority was for us to restore the GitHub stars on our repositories (as we were "starless"). Although stars are a vanity metric, it didn’t feel great to see zero stars when Elasticsearch was on the edge of 70K stars, and Kibana was at roughly 20K stars. Thanks to the awesome behind-the-scenes work at GitHub, the star counts were restored several weeks later!
## Contributing factors
A combination of contributing factors led to the incident. The most important ones are detailed below.
### Changing too much at once
As we saw above, there were a number of changes being taken at a given time. If we had broken this down into smaller iterations, instead of a big-bang rollout, the impact would likely have been significantly decreased.
Smaller iterations would also have meant that we would have a spreadsheet of maybe 30 repositories to review instead of 350, which would've flagged much more readily that elastic/kibana or elastic/elasticsearch shouldn't have been on the list.
### Making assumptions
Another significant contributing factor to the incident — and one I'll not be forgetting any time soon — was that we assumed our list of repositories we collected were correct.
The scripts we wrote to prepare the list of repositories and then perform the changes should have been far more defensive. And for each repository it processed, we should have confirmed that the repository's visibility was**internal**before changing it to**private**. With changes like this that could have destructive actions, we need to be very strict with the inputs and the real world state.
You should make sure you trust your inputs but still verify them.
## Many lessons learned
Before we’d even completed the incident’s root cause analysis (RCA), we had already taken actions to significantly reduce the chance of this recurring by accident and over the following weeks finalized relevant changes to prevent this incident class from ever occurring again.
For example, a default behavior in GitHub is that a human who has admin privileges on a repository can change the visibility, whether accidentally or maliciously. To prevent this, we implemented a GitHub**enterprise**policy to restrict access to only GitHub organization owners to be able to modify a repository’s visibility and reduce the number of users with that owner privilege.
This immediately reduced the number of people who could make a visibility change on any of our repositories from hundreds of people to roughly a dozen.
In a similar vein, we started inventory tooling to manage settings in the "danger zone" of GitHub's settings and then removed that access or added code-based guardrails to block changes.
Another key change we made in our processes was to make sure that changes like these are always decentralized rather than centralized. In other words, instead of a central team pushing out a change like this, we would seek the repository owners to make this change (with an organization owner's help). This would allow them to be fully in control and able to monitor for unintended side effects.
## The power of collaboration
While we all strive to prevent incidents, the reality is that mistakes happen — sometimes in big, visible ways. As technologists, responding to those moments is just as important as avoiding them.
I’ve been directly involved in a major public outage, and what stood out most was the support I was given. The way the team rallied around me, the genuine commitment to a blameless culture, and the strength of our incident management process made all the difference.
It’s only when things go really wrong that you see whether the culture holds up — and I can honestly say it did.
_This involved a ton of work from the excellent folks over at GitHub. Knowing that it was the first day of GitHub Universe — the company's conference — and many employees were busy there, they still showed up to help. We’re hugely appreciative of the collaboration in supporting the restoration of these repositories!_
##
### [Jamie Tanna](/blog/author/jamie-tanna)
Jamie Tanna (he/him) is a senior software engineer, a passionate advocate for Open Source, and an avid blogger about tech and life. Jamie is an engineer who loves digging into why things are the way they are, thinks through writing, and learns through experimentation and making mistakes. He recently left Elastic to pursue his dream job but is going to miss the great people he worked with. Visit [his website](https://www.jvt.me/).
_The release and timing of any features or functionality described in this post remain at Elastic's sole discretion. Any features or functionality not currently available may not be delivered on time or at all._
![icon-toc-16-blue.svg](/static-res/images/svg/icon-toc-16-blue.svg)
