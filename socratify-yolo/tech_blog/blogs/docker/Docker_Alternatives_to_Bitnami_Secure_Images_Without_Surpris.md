---
title: "Docker Alternatives to Bitnami: Secure Images Without Surprises"
author: "Michael Donovan"
url: "https://www.docker.com/blog/broadcoms-new-bitnami-restrictions-migrate-easily-with-docker/"
date: "2025-09-15"
---

For years, Bitnami has played a vital role in the open source and cloud-native community, making it easier for developers and operators to deploy popular applications with reliable, prebuilt container images and Helm charts. Countless teams have benefited from their work standardizing installation and updates for everything from WordPress to PostgreSQL.**We want to acknowledge and thank Bitnami’s contributors**for that important contribution.

Recently, however, Bitnami announced significant changes to how their images are distributed. Starting this month, access to most versioned images will move behind a paid subscription under Bitnami Secure Images (BSI), with only the :latest tags remaining free. Older images are being shifted into a Bitnami Legacy archive that will no longer receive updates. For many teams, this raises real challenges around cost, stability, and compliance.

Docker remains committed to being a trusted partner for developers and enterprises alike.**Docker Official Images (DOI) are one of the two most widely used catalogs of open source container images in the world, and by far the most adopted.**While Bitnami has been valuable to the community, Docker Official Images see billions of pulls every month and are trusted by developers, maintainers, and enterprises globally. This is the standard foundation teams already rely on.

For production environments that require added security and compliance,**Docker Hardened Images (DHI) are a seamless drop-in replacement for DOI**. They combine the familiarity and compatibility of DOI with enterprise-ready features: minimal builds, non-root by default, signed provenance, and near-zero-CVE baselines. Unlike Bitnami’s new paid model, DHI is designed to be affordable and transparent, giving organizations the confidence they need without unpredictable costs.

## Bitnami’s Access Changes Are Already Underway

On July 16, Broadcom’s Bitnami team [announced changes](https://github.com/bitnami/charts/issues/35164) to their container image distribution model, effective September 29. Here’s what’s changing:

***Freely built and available images and Helm charts are going away.**The [bitnami](https://hub.docker.com/u/bitnami) organization will be deleted.
***New Bitnami Secure Images offering.**Users that want to use Bitnami images will need to get a paid subscription to a new Binami Secure Images offering, hosted on the Bitnami registry. This provides access to stable tags, version history,

***Free tier of Bitnami Secure Images**. The [bitnamisecure org](https://hub.docker.com/u/bitnamisecure) has been created to provide a set of hardened, more secure images. Only the :latest tags will be available and the images are intended for development purposes only.

***Unsupported legacy fallback**. Older images are moved to a “Bitnami Legacy Registry”, available on Docker Hub in the [bitnamilegacy org](https://hub.docker.com/r/bitnamilegacy). These images are unsupported, will no longer receive updates or patches, and are intended to be used while making plans for alternatives.

***Image and Helm chart source still available.**While the built artifacts won’t be published, organizations will still be able to access the source code for Debian-based images and Helm charts. They can build and publish these on their own.

**The timeline is tight too.**Brownouts have already begun, and the public catalog deletion is set for**September 29, 2025**.

## What Bitnami Users Need to Know

For many teams, this means Helm charts, CI/CD pipelines, and Kubernetes clusters relying on Bitnami will soon face broken pulls, compliance risks, or steep new costs.

The community reaction has been strong. Developers and operators voice concerns around:

***Trust and stability concerns**. Many see this as a “bait and switch,” with long-standing free infrastructure suddenly paywalled.

***Increased operational risk.**Losing version pinning or relying on :latest tags introduces deployment chaos, security blind spots, and audit failures.

***Cost and budget pressure**. Early pricing reports suggest that for organizations running hundreds of workloads, Bitnami’s new model could mean six-figure annual costs.

In short: teams depending on Bitnami for reliable, stable images and Helm charts now face an urgent decision.

## Your Fastest Path Forward: Docker

At Docker, we believe developers and enterprises deserve choice, stability, and stability. That’s why we continue to offer two strong paths forward:

### Docker Official Images – Free and Widely Available

Docker is committed to building and maintaining its Docker Official Image catalog. This catalog:

***Fully supported with a dedicated team.**This team reviews, publishes, and maintains the Docker Official Images.

***Focused on collaboration.**The team works with upstream software maintainers, security experts, and the broader Docker community to ensure images work, are patched, and support the needs of the Docker community.

***Trusted by millions of developers worldwide.**The Docker Official Images are pulled billions of times per month for development, learning, and production.

### Docker Hardened Images – Secure, Minimal, Production-Ready

Docker Hardened Images are secure, production-ready container images designed for enterprise use.

***Smaller near-zero known CVEs.**Start with images that are up to 95% smaller, fewer packages, and a much-reduced attack surface.**
**
***Fast, SLA-backed remediation.**Critical and High severity CVEs are patched within 7 days, faster than typical industry response times, and backed by an enterprise-grade SLA.

***Multi-distro support.**Use the distros you’re familiar with, including trusted Linux distros like Alpine and Debian

***Signed provenance, SBOMs, and VEX data**– for compliance confidence.

***SLSA Level 3 builds, non-root by default, distroless options**– following secure-by-default practices.

***Self-service customization.**Add certificates, packages, environment variables, and other configuration right into the build pipelines without forking or secondary patching.

* Fully integrated into Docker Hub for a familiar developer workflow.

## Start Your Move Today

If your organization is affected by the Bitnami changes,we are here to help. Docker offers you a fast path forward:

1.**Audit your Bitnami dependencies**. [Identify](https://hub.docker.com/usage/pulls) which images you’re pulling.

2.**Choose your path**. Explore the [Docker Official Images catalog](https://hub.docker.com/u/library) or learn more about [Docker Hardened Images](https://www.docker.com/products/hardened-images/). Many of the Bitnami images can be easily swapped with images from either catalog.

**Need help?
**[**Contact our sales team**](https://www.docker.com/products/hardened-images/#getstarted)**to learn how Docker Hardened Images can provide secure, production-ready images at scale.**
