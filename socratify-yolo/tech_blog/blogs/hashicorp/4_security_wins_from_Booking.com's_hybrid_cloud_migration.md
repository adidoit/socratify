---
title: "4 security wins from Booking.com's hybrid cloud migration"
author: "Unknown"
url: "https://www.hashicorp.com/blog/4-security-wins-from-booking-com-s-hybrid-cloud-migration"
date: "2025-09-15"
---

[](/en/blog/products/vault)Customer stories & success

* Twitter share
* LinkedIn share
* Facebook share
* Copy URL

# 4 security wins from Booking.com's hybrid cloud migration

Learn how Booking.com leveraged HashiCorp Vault to accelerate and secure their hybrid/multi-cloud transformation while maintaining operational efficiency.

Sep 03 2025[Mitch Pronschinske](/blog/authors/mitch-pronschinske)

Booking.com operates at a massive scale — handling millions of travelers daily across a complex infrastructure spanning bare metal, AWS, GCP, and Alibaba Cloud. When Dan Popescu joined their secrets management team four years ago, the travel giant was already deep into a hybrid cloud migration that presented unique security challenges.

In a recent HashiDays talk, Dan shared how his team transformed Booking.com's approach to secrets management, scaling [HashiCorp Vault](https://www.hashicorp.com/products/vault) to handle 500+ requests per second across 100+ Kubernetes clusters. His team's mission: "Deliver a unified secrets management solution that provides a self-service experience for seamless and secure secret sharing and lifecycle management across cloud platforms."

Here are four key security wins from their hybrid cloud journey.

## »**1\. A central security bridge for hybrid infrastructure**

The biggest security risk in hybrid cloud environments is a lack of consistent controls across interconnected systems. Booking.com wanted to create a bridge for identity and secrets brokering between their public cloud services and their internal infrastructure without developers having to reinvent the wheel; creating security toolchains and workflows for each environment.

Booking.com positioned Vault as a security communications bridge between their multi-cloud environments and bare metal infrastructure. When developers create resources in their internal service catalog, Vault automatically onboards cloud resources and configures authentication.

**The security win**: Developers get consistent access patterns whether applications run on bare metal, AWS, GCP, or internal OpenStack clusters. This consistency eliminates the security misconfigurations that typically emerge when teams build custom solutions for each environment.

For technical leaders, this addresses a critical hybrid cloud challenge: maintaining security standards while enabling developer productivity across diverse platforms.

## »**2\. Consolidated authentication complexity**

Early in their journey, Booking.com discovered that authentication sprawl creates major security risks. They were managing hundreds of mount points and thousands of identity entities across Kubernetes clusters — each application deployed across 100 clusters required 100 separate mount points and 200 configuration changes.

This complexity made security oversight nearly impossible and scaling extremely dangerous.

The breakthrough came with JWT authentication migration. By leveraging JWK/JWS endpoints available in all Kubernetes clusters, they consolidated to a single mount point containing public keys from all environments. They built a JWS manager that automatically discovers clusters and updates authentication keys every five minutes.

Now adding a new cluster requires just a few configuration changes rather than hundreds.

**The security win**: Reduced complexity means fewer misconfiguration opportunities and better visibility into access patterns across all environments. It enables faster security incident response since there's only one authentication system to monitor and audit.

## »**3\. Strategic cloud-native secrets management**

Booking.com also has to consider cost and performance when making strategic secrets management decisions. "We're talking about millions of secrets. 30,000 AWS roles across hundreds of accounts and 6,500 Snowflake roles." Dan noted.

This year Booking.com is planning to use Vault’s [secrets sync](https://developer.hashicorp.com/vault/docs/sync) to add flexibility to their secrets management systems while also keeping the benefits of having Vault as the single source of truth for secrets management. Secrets sync will allow teams to use other secrets management tools like AWS Secrets Manager for specific AWS use cases where they can keep a smaller footprint.

Instead of unrestricted cloud-native adoption, they require teams to explicitly request specific secrets for specific regions. Vault remains the single source of truth, but teams can access secrets through AWS Secrets Manager for cloud-native workloads that will run more efficiently with that system.

**The security win**: Centralized secrets governance with tactical flexibility. All secrets flow through Vault's policy engine and audit logging, ensuring consistent security controls even when teams use cloud-native tools. This prevents security fragmentation while meeting specific use case requirements.

## »**4\. Cost-effective secret management**

Security solutions that become prohibitively expensive often get abandoned or compromised. Booking.com's approach prioritizes both security and cost efficiency — critical at their scale.

Their cost-conscious security strategies include:

***Smart TTL management**: Initially they had no time-to-live (TTL) settings on some Vault secrets engines, leading to keys piling up with the potential to cause outages. Proper TTL configuration prevented resource waste and costly downtime.
***Static user patterns**: For Snowflake and CockroachDB, they switched from dynamic provisioning to static users with [password rotation](https://www.hashicorp.com/en/blog/rotated-vs-dynamic-secrets-which-should-you-use), reducing overhead.
***Selective cloud integration**: Using Vault's sync capabilities to place secrets strategically for cost and performance.

**The security win**: Sustainable costs ensure long-term security investment. Predictable expenses allow continued security improvements rather than budget battles, and prevent teams from circumventing tools due to cost pressures.

## »The impact: Vault as the foundation for seamless migration

The results demonstrate the power of foundational security architecture:

***Eliminated authentication complexity**across 100+ Kubernetes clusters
***Enabled self-service onboarding**without sacrificing security oversight
***Streamlined multi-cloud operations**with consistent security policies
***Supported massive scale**— 500+ requests per second, millions of secrets
***Accelerated Vault adoption**with Terraform infrastructure as code workflows

Using Terraform Enterprise, Booking.com now provisions new Vault clusters quickly and reliably. Machines are constantly refreshed for stability without manual intervention, and their upcoming secrets sync implementation will maintain Vault as the single source of truth while enabling tactical use of cloud-native tools.

Most importantly, their approach enables developer**self-service without sacrificing security**. Teams can onboard applications and migrate to cloud platforms without waiting for security reviews because security patterns are built into the platform itself.

## »**Learn more**

Booking.com's experience shows that security doesn't have to be a migration bottleneck — with the right foundational tools and architectural decisions, security becomes an enabler of faster, more reliable cloud adoption.

For organizations planning hybrid and multi-cloud migrations, consider how a unified secrets management foundation can transform security from a constraint into a competitive advantage.

To learn more about HashiCorp’s vision for expanding unified lifecycle management to hybrid cloud operations read our guide: [Deliver innovation at scale with The Infrastructure Cloud](https://www.hashicorp.com/en/on-demand/deliver-innovation-at-scale-with-the-infrastructure-cloud?utm_source=hashicorp.com&utm_medium=referral&utm_campaign=26Q3_WW_SPEED_4-security-wins_WHITEPAPER&utm_content=blog-learn-more-conclusion&utm_offer=whitepaper)

For the full technical details on Booking.com's cloud migration journey, watch Dan's complete HashiDays session.

* * *

[Speed & agility](/en/blog/tags/speed-agility)[Risk & compliance](/en/blog/tags/risk-compliance)[Optimize operations](/en/blog/tags/optimize-operations)[Secrets & identity management](/en/blog/tags/secrets-identity-management)[Kubernetes](/en/blog/tags/kubernetes)

#### Sign up for the latest HashiCorp news

Email

Required

Send me news about HashiCorp products, releases, and events.

By submitting this form, you acknowledge and agree that HashiCorp will process your personal information in accordance with the [Privacy Policy](https://www.hashicorp.com/trust/privacy).

Sign Up

#### More blog posts like this one

[![5 DevEx and platform-mindset lessons from BT Group's hybrid cloud journey](/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F2885%2F1757054124-16_9-social-image-btgroup.png&w=3840&q=75)September 08 2025 | Customer stories & success5 DevEx and platform-mindset lessons from BT Group's hybrid cloud journeyLearn how highly-regulated BT Group transformed its security and operations approach using HashiCorp's platform.](/en/blog/5-devex-and-platform-mindset-lessons-from-bt-group-s-hybrid-cloud-journey)[![5 lessons from Moneybox’s Terraform journey](/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F2885%2F1755552449-moneybox-ed-fretwell.jpg&w=3840&q=75)August 19 2025 | Customer stories & success5 lessons from Moneybox’s Terraform journeyLearn about Moneybox’s infrastructure-scaling transformation, and how the transition to HCP Terraform supported it.](/en/blog/5-lessons-from-moneybox-s-terraform-journey)[![Helvetia’s journey building an enterprise serverless product with Terraform](/_next/image?url=https%3A%2F%2Fwww.datocms-assets.com%2F2885%2F1742506469-16_9-social-image-helvetia.jpg&w=3840&q=75)July 02 2025 | Customer stories & successHelvetia’s journey building an enterprise serverless product with TerraformWhat started as a basic compliance challenge for one team at Helvetia Insurance evolved into a comprehensive enterprise solution for running self-managed installations like a cloud service, using Terraform to manage a serverless architecture.](/en/blog/helvetia-s-journey-building-an-enterprise-serverless-product-with-terraform)
