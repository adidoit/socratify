---
title: "Tailscale Monthly Update: August 2025"
author: "Unknown"
url: "https://tailscale.com/blog/august-25-product-update"
date: "2025-09-15"
---

[Blog](/blog)|productAugust 22, 2025

# This month at Tailscale: Visual policy editor, state encryption, and Grafana Cloud

![Darker green shapes, like squares and cut circle corners, against a lighter green background.](https://cdn.sanity.io/images/w77i7m8x/production/e96a13f39f18b7a23ab7ac08755f9c7143a2dd11-600x315.svg?w=1200&q=75&fit=clip&auto=format)

We continuously ship updates to make your network more reliable, manageable, and secure. Each month, we highlight some of the most impactful changes across clients, admin tools, integrations, and infrastructure—so you can stay on top of what’s new and what’s better.

This month's updates include a visual policy editor, encryption of data at rest, and a Grafana Cloud integration. For instructions on how to update to the latest version, visit our [update guide](https://tailscale.com/kb/1067/update).

## Visual policy editor

Tailscale now gives you the option of using web-based forms, buttons, and other visual tools to manage your tailnet access permissions. The [visual policy editor](https://tailscale.com/blog/visual-editor-beta), now in beta, provides an alternative to the policy editor's HuJSON format (JSON for Humans), but it's not a replacement. You can switch back and forth between JSON writing and visual tools, use visual tools to preview changes made in JSON, and individual users and administrators can pick their preference.

## Encrypting data at rest

With the latest client releases, Tailscale now encrypts its state file while it is stored on disk, or at rest. This makes it much harder for attackers with disk access to "clone" nodes or otherwise disrupt tailnet operation. Read more about how it works, on every OS, [in our blog post](https://tailscale.com/blog/encrypting-data-at-rest).

## Grafana Cloud integration

Tailscale and Grafana have partnered on a new integration that can securely connect data sources inside a tailnet to a Grafana Cloud stack, without exposing data sources to the public internet. Read more, and sign up for onboarding, [at our blog post](https://tailscale.com/blog/grafana-integration-secure-data-sources).

## Client updates

###**Tailscale v1.86.0, 1.86.2, and 1.86.4**

We released a series of updates and fixes to improve security and stability across all platforms.

#### All platforms

* tsStateEncrypted [device posture](https://tailscale.com/kb/1288/device-posture#device-posture-attributes) attribute available
* [Recommended exit node](https://tailscale.com/kb/1392/auto-exit-nodes) can now be set with`tailscale up —exit-node=auto:any`and`tailscale set —exit-node=auto:any.`Clients will automatically switch to recommended exit nodes when available exit nodes or network conditions change. (Windows/Mac/Linux)
* Hostnames are now verified as expected when using CONNECT HTTPS proxy to connect to the [control plane](https://tailscale.com/kb/1508/control-data-planes).
* Fixed a [cross-site request forgery (CSRF)](https://en.wikipedia.org/wiki/Cross-site_request_forgery) issue that may have resulted in a log in error when accessing the [web interface](https://tailscale.com/kb/1325/device-web-interface).
* Fixed [`tailscale syspolicy`](https://tailscale.com/kb/1080/cli#syspolicy) CLI command output displaying correctly when the`KeyExpirationNotice`or`ReconnectAfter`[system policies](https://tailscale.com/kb/1315/mdm-keys) are configured (Windows/Mac).

#### Android

Fixed a persistent notification asking users to pick a directory for Taildrop files. The notification now only displays on the first attempt to use the feature.

#### iOS

Fixed issues with Shortcut actions, Taildrop sending, and keychain resets.

#### Windows

* [`tailscale syspolicy`](https://tailscale.com/kb/1080/cli#syspolicy) CLI command output displays correctly when the`KeyExpirationNotice`or`ReconnectAfter`[system policies](https://tailscale.com/kb/1315/mdm-keys) are configured.
* A system tray icon now shows when a selected exit node is unavailable.
* [Mullvad exit node](https://tailscale.com/kb/1258/mullvad-exit-nodes) picker hides after switching from a profile with Mullvad exit nodes to one without any exit nodes.

#### macOS

* [`OnboardingFlow`](https://tailscale.com/kb/1315/mdm-keys#suppress-the-first-launch-onboarding-flow) system policy enforces the suppression of the onboarding flow that displays when the client is installed. This replaces the deprecated [`TailscaleOnboardingSeen`](https://tailscale.com/kb/1315/mdm-keys#suppress-the-first-launch-onboarding-flow) system policy.
*`Remove all accounts`option added to the [Debug](https://tailscale.com/kb/1023/troubleshooting#debug-menu-and-options) menu.
* Fixed Shortcut action issues
* [`EncryptState`](https://tailscale.com/kb/1315/mdm-keys#encrypt-node-state-file) system policy changes are applied without needing to restart the [system extension](https://tailscale.com/kb/1340/macos-sysext)

All of these fixes and changes are available in the current stable release, 1.86.4.

## Container, Kubernetes, and`tsrecorder`updates

The 1.86.5 release for containers, Kubernetes, and`tsrecorder`contained library updates, along with a Kubernetes DNS lookup fix for certain API server proxy configurations.

###**Container image v1.86.2 and 1.86.5**

**Note:**We previously referred to this as the Tailscale Docker image and now refer to it more generically as the Tailscale container image.

* Improved direct connectivity to`ProxyGroup`Pods by using external node IP addresses as [static endpoints](https://tailscale.com/kb/1445/kubernetes-operator-customization#static-endpoints).
* Pod-specific state is cleared on start when running in Kubernetes.

###**Kubernetes operator v1.86.2**

A number of new features and fixes were added to the [Kubernetes operator](https://tailscale.com/kb/1236/kubernetes-operator), including:

* The first release of [Tailscale Kubernetes proxy](https://tailscale.com/kb/1437/kubernetes-operator-api-server-proxy) is available.
* Record`kubectl attach`and`kubectl debug`sessions to [`tsrecorder`](https://tailscale.com/kb/1454/kubernetes-operator-session-recording)
*`ProxyGroup`type`kube-apiserver`for running the [API server proxy](https://tailscale.com/kb/1437/kubernetes-operator-api-server-proxy) in a high-availability mode available.
*`ProxyClass`can use [annotations instead of labels](https://tailscale.com/kb/1445/kubernetes-operator-customization#customizing-tags).

###**tsrecorder v1.86.2**

* Library updates only

* * *

That's everything for this month. If you have questions or feedback, [we're here to help](https://tailscale.com/contact/support). Thank you for using Tailscale.

Share

Author

![Headshot of Kevin Purdy](https://cdn.sanity.io/images/w77i7m8x/production/1b9caf64d6989e00c3bf4ae1aff20b57ae125f6b-512x512.jpg?w=1080&q=75&fit=clip&auto=format)Kevin Purdy

Author

![Headshot of Kevin Purdy](https://cdn.sanity.io/images/w77i7m8x/production/1b9caf64d6989e00c3bf4ae1aff20b57ae125f6b-512x512.jpg?w=1080&q=75&fit=clip&auto=format)Kevin Purdy

Share

Loading...
