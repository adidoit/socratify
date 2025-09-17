---
title: "Postman (Free) is secure by design"
author: "Sam Chehab"
url: "https://blog.postman.com/postman-free-is-secure-by-design/"
date: "2025-09-15"
---

# Postman (Free) is secure by design
![Sam Chehab](https://blog.postman.com/engineering/wp-content/uploads/2025/06/sam-chehab-postman-150x150.jpg)
[Sam Chehab](https://blog.postman.com/engineering/author/sam-chehab/)
August 12, 2025
As Postman’s Head of Security, I am dedicated to ensuring that all Postman users (paying or not) benefit from enterprise-grade security baked into the platform. Why? Because security doesn’t start at the enterprise license, it starts at the first request.
In speaking to CIOs and CISOs, I find that one of the most overlooked risks they face is a lack of visibility into how their teams are _actually_ collaborating. If users are blocked from using tools that they feel make them productive, they don’t stop collaborating, they just find workarounds. These shadow workflows create risk for a security team. This typically manifests itself as sensitive data being shared, exposed credentials, or APIs released without adequate controls. Without visibility, you can’t enforce policy, detect risks, or respond to incidents, leaving the organization vulnerable in ways you can’t easily measure or mitigate. That’s why enabling secure, visible collaboration—even at the free tier—isn’t just a product choice for Postman, it’s a core part of my security philosophy.
Postman’s platform is built with a secure-by-design philosophy that we, as security leaders, can trust. Our mission is to empower our customers with the controls, visibility, and data ownership necessary to confidently secure their APIs.
## Postman Cloud Security
Postman has chosen a cloud-first architecture because the API development process is an intrinsically collaborative process across teams, between departments, with partners, and often with the public. It’s my responsibility to ensure enterprise-grade security is embedded at every layer of the platform.
At Postman, security is integrated throughout the entire development lifecycle. To accomplish this, we work closely with trusted partners like Okta, AWS, and Wiz to enhance our posture across identity, cloud infrastructure, and data protection. Regular third-party penetration testing is conducted against both our cloud platform and endpoint agent to proactively surface vulnerabilities. And, through rigorous, ongoing compliance efforts, we align with [global standards](https://security.postman.com/) to meet the evolving needs of our users—no matter their size or industry.
## Is Postman Secure? Absolutely.
My team and I routinely evaluate the Postman Free plan through a security lens to ensure it offers the flexibility and features needed to support your organization’s unique security requirements. This also helps us get insight into the most common questions we hear from users, some of which I’ll share below.
***Does Postman’s API response history contain sensitive data?**
History is disabled by default, but fully supported in the Postman Free plan. We also allow workspaces to be purged.
***Can I manage secrets securely?**
Postman has several methods for managing secrets. It can be done locally through the Postman Local Vault, which will store credentials locally and never syncs them to the cloud, ensuring that even workspace admins and teammates can’t access them. The vault clears on sign-out, preventing data from being compromised if your device or account is ever at risk.
***What is the risk of external secret exposure when I use Postman?**
Postman has several built-in capabilities to help minimize impact. Postman Secret Scanner proactively scans your private and public workspaces, documentation, and [GitHub](https://learning.postman.com/docs/administration/managing-your-team/secret-scanner/#protect-postman-api-keys-in-github)/[GitLab](https://learning.postman.com/docs/administration/managing-your-team/secret-scanner/#protect-postman-api-keys-in-gitlab) repos for exposed secrets. If something sensitive is detected, Postman alerts you immediately. Postman also supports variable masking for risks with screen sharing use cases and Postman Local Vault for ensuring credentials don’t leave your machine.
***Does Postman scan for secrets before making Collections public?**
Yes, before any collection is published or made visible in a public workspace, the Postman Secret Scanner will detect and [redact](https://blog.postman.com/public-api-network-security-updates-secret-protection-policy/) and notify the admin of any sensitive values such as API tokens, credentials, or private keys.
***What about Phishing? How does Postman protect users in my org from Phishing attacks?**
From the moment you sign up, Postman enforces strong password practices and supports passwordless login via Google and GitHub. I’m still closely watching Microsoft’s Passkey journey for the consumer space, after all, I’ve got 40M users to ensure they have a safe and delightful experience.
***The leading cause of data loss is human error. How does Postman help me prevent these kinds of human-driven risks?**
Postman backs its security tooling with ongoing user education videos, empowering developers to follow best practices and reduce risk. Educate your teams with this article and [Postman’s security one-pagers.](https://security.postman.com/?itemUid=12ebc5f7-ca96-4d0e-876d-2e6dd39f7988)
***Are****Postman Environment Variables****encrypted?**
Postman Environment Variables are just that—variables. Their scope is restricted to a workspace and they are encrypted at rest and in transit, but in essence, they are non-secret configuration parameters used to set constants, define hosts, or feed parameters into an application environment. We have several mechanisms available for storing secret or sensitive configuration values (keys, etc.) which can be fed into your requests where care and sensitivity apply.
***Can I disable the “export” function from a workspace to mitigate risk?**
At Postman, we believe ‘you’ own your data, and while that could be considered a data loss prevention (DLP) risk, it’s paramount you can collaborate and protect your intellectual property any way you see fit.
***What is on prem vs cloud?**
****“On prem” refers to software and infrastructure that are installed, run, and managed locally within that user’s ecosystem. In contrast, “cloud” refers to software and infrastructure that are hosted and managed by a third-party provider (such as AWS or Azure) and accessed over the internet.
***What is more secure:****on prem vs cloud****?**
It is common to assume an application running on your managed endpoint is inherently safe. Sadly, it’s almost a daily occurrence where local files with secrets find their way to sites such as [GitHub](https://github.blog/security/application-security/next-evolution-github-advanced-security/). Instead, I see the argument flawed as the hosting model isn’t the challenge, it’s your approach to data security that matters. To learn more about Postman’s approach, check out our Data Security one-pager [here](https://security.postman.com/?itemUid=12ebc5f7-ca96-4d0e-876d-2e6dd39f7988).
## API security best practices on Postman Free
Ultimately, Postman Free is designed for 1–3 users to experiment and prototype. If you’re looking for a solution that can support a larger team or organization, Postman Professional or Enterprise would be a better fit. These plans are built for collaboration at scale and include enhanced safeguards to help protect your sensitive data.
However, if the Postman Free plan meets your organization’s needs and you’re simply looking to strengthen [API security best practices](https://security.postman.com/item/postman-api-security-best-practices), here are some tips we recommend to help your team use Postman more securely and effectively.
***Use****Postman Vault****for Secrets**: Postman Vault provides secure, local storage for sensitive data; never syncing to the cloud. It lets you centrally manage and secure API keys (create, expire, revoke), scope secrets to workspaces, and rotate them easily. This helps you keep secrets out of shared environments, avoid leaks in exports, and store tokens securely and locally.
***Review Collections before you publish publicly:**Before sharing a collection or publishing it to the Public API Network:
* Open the Authorization tab
* Check the pre-request and tests tabs
* Look at all attached Postman environments
* Search for words like token, secret, password, key, or Bearer
* If any of those contain real values, remove or replace them with placeholders
***Use Secret Scanning before making Collections public**: Before a collection is published or made visible in a public workspace, Postman scans for secrets and proactively alerts users if sensitive data is detected to recommend its removal before sharing publicly.
***When in doubt, keep it private:**If you’re not sure whether a collection should be public, don’t publish it. Share it privately within your team or generate a temporary link that expires. Public collections are amazing for education and community, but they’re not the right place for confidential work.
***Don’t treat Postman’s Free plan like a production workflow:**Postman Free is ideal for prototyping, exploring APIs, and learning, but production environments deserve policy enforcement and visibility.
**Security features you already have, even on free:**
* Local Vault for secrets
* Automatic secret scanning
* Visual warnings before publishing
* Token masking
* Granular workspace visibility
Security is a journey, not a checkbox—and adopting strong API security best practices is essential for keeping your team and your data protected. By sharing these best practices with your team, you can foster safer collaboration and build a more secure development environment on the Postman platform. As API ecosystems grow more complex, staying vigilant and informed is key. I’ll continue to explore and write about Postman security in future posts, offering updates and insights to help you navigate evolving security needs with confidence.
Tags: [API Security](https://blog.postman.com/engineering/tag/api-security/) [Security](https://blog.postman.com/engineering/tag/security/)
![Sam Chehab](https://blog.postman.com/engineering/wp-content/uploads/2025/06/sam-chehab-postman-150x150.jpg)
Sam Chehab
[View all posts by Sam Chehab →](https://blog.postman.com/engineering/author/sam-chehab/)
