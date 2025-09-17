---
title: "Making file encryption fast and secure for teams with advanced key management"
author: "Unknown"
url: "https://dropbox.tech/security/file-encryption-teams-advanced-key-management"
date: "2025-09-15"
---

We know how important security and encryption are to our customers—especially with enterprise standards rapidly evolving. That’s why we engage with our customers to understand what their security teams need and how we can help. Through those conversations, we developed our new advanced key management solution, designed to make [team-based file encryption](https://help.dropbox.com/security/advanced-encryption) faster and more secure. This work also laid the foundation for the encryption approach we’re now bringing to [Dropbox Dash](https://www.dash.dropbox.com/), our [universal search](https://dropbox.tech/infrastructure/multimedia-search-dropbox-dash-evolution) and knowledge management tool.

Two main priorities shaped how we built this solution. First, customers with especially sensitive or confidential data (e.g. those in finance or healthcare fields) told us they wanted their file data encrypted at rest—for example, when it’s not being moved or accessed—using keys unique to their team. This way, they could temporarily, or even permanently, disable _all_ access to their team’s data if needed. Second, they wanted that encryption to be anchored in a hardware security module (HSM)—a physical device designed to securely generate, store, and manage encryption keys—providing stronger protections against unauthorized access. Together, these features help teams limit their security risks and respond more effectively to potential threats or breaches.

In this piece, we’ll walk through how we solved for scalable, secure team-level encryption without slowing down the Dropbox experience. We’ll share our decision-making process, the technical challenges we faced, and how the solution we built is influencing the way we think about security for [AI tools like Dash](https://dropbox.tech/machine-learning/building-dash-rag-multi-step-ai-agents-business-users).

![](https://cdn.prod.website-files.com/65dcd70b48edc3a7b446950e/670692ee7692f74d4834e4f4_Frame%201400006055.svg) Dropbox Dash: Find anything. Protect everything.

Find, organize, and protect your work with Dropbox Dash. Now with advanced search for video and images—plus generative AI capabilities across even more connected apps.

[See what's new →](https://dash.dropbox.com/?utm=blogs)

## Identifying possible solutions

We kicked off this work by mapping out potential solutions. One obvious approach was to implement end-to-end encryption. It offers stronger support for encryption key management and access control—but it also brings tradeoffs, like added complexity for customer teams and reduced usability. For instance, with end-to-end encryption, you can’t search for files by their contents. End-to-end encryption is a powerful enterprise security solution, which is why we offer [end-to-end encryption as a Dropbox feature](https://dropbox.tech/security/end-to-end-encryption-for-dropbox-teams) for the teams that need it. But it makes more sense for some use cases than others, and we wanted to offer another solution for teams where it’s not the right fit.

For teams that don’t need full end-to-end encryption, there’s another solution: team-based key management. The standard here is to use something like [AWS Key Management Service](https://aws.amazon.com/kms/) (AWS KMS) to create a unique top-level key for each team, and then use that key to generate or decrypt individual data encryption keys for every file or record owned by the team. However, this approach doesn’t play well with a core part of the Dropbox experience: file sharing. To understand why, it helps to take a look at how Dropbox stores files and how we handle file copies across teams.

**How Dropbox stores files
**When you upload a file to Dropbox, we break it into 4 MB chunks called “blocks.” Each block is encrypted, managed, and stored separately—sometimes even in different physical locations. And each block gets its own data encryption key; more on this later.

**What happens when you add files to Dropbox
**When someone shares a file or folder with you, you can choose to add it to your _own_ Dropbox. This creates a new copy of the file that’s independent from the original, even though you started with a shared link. Now, imagine doing that in a world where we’ve implemented team-specific, top-level encryption keys. That copy has to be encrypted with the recipient team’s key, meaning Dropbox needs to store a whole new encrypted version of the file.

**Why that’s tricky
**Putting this all together, if we followed the standard model—one top-level team key plus block encryption keys—then every time someone added a large file from another team to their Dropbox, we’d have to re-encrypt the entire thing. For big files or folders, this would be painfully slow. Even a slightly more efficient system that copies only the data encryption keys would still be prohibitively expensive and hard to scale in real time. And scale matters: [Dropbox supports files up to 2 TB](https://help.dropbox.com/sync/upload-limitations), which can mean upwards of half a million blocks per file. Nobody wants to wait for a million tiny re-encryption tasks just to copy a shared folder.

## A three-tiered encryption scheme

To address team-based encryption key management and enable fast copies, we introduced a third tier of encryption keys to the standard model described above. To do this, we leveraged the fact that Dropbox files and folders are internally bucketed into [namespaces](https://dropbox.tech/developers/listing-team-contents). (You can think of a namespace as your root folder—a container that holds all your files and folders.) Every file and its associated data blocks belong to a namespace. This structure allows for an intermediate encryption tier at the namespace level, creating a three-tier key hierarchy:

***Team encryption key (TEK)**: A top-level key unique to each team, generated and stored using AWS KMS within a hardware security module (HSM).
***Namespace encryption key (NEK)**: Each namespace has its own encryption key (NEK), which is generated using AWS KMS along with the team’s top-level encryption key (TEK). The NEK is then encrypted using the TEK and saved securely in persistent storage.
***Block encryption key (BEK)**: Each block has a unique encryption key. It is stored encrypted at rest using the corresponding NEK.

When a file is read, the system first retrieves the team’s top-level encryption key (TEK) from AWS KMS to decrypt the namespace encryption key (NEK). The NEK is then used to decrypt the block encryption keys (BEKs), which are used to decrypt the file’s data blocks. When writing a file, the process is reversed: New BEKs are encrypted with the NEK, and the NEK is encrypted with the TEK. This model adds only one metadata lookup and one extra encryption or decryption step per request.

![](/cms/content/dam/dropbox/tech-blog/en-us/2025/july/akm/diagrams/Security-Advanced-Key-Management-01%20\(1\).png/_jcr_content/renditions/Security-Advanced-Key-Management-01%20\(1\).webp)

Encryption key operations on the read path

**Making copies fast
**This setup really shines in one of our most common workflows: when someone adds a shared file or folder to their own Dropbox. Before, that kind of cross-team copy would require re-encrypting every block in the file. For large files—some with hundreds of thousands of blocks—that would take ages.

With this new model, Dropbox only needs to make a re-encrypted copy of the source namespace’s NEK to grant access. While it’s a huge performance win, it’s not a long-term solution—the recipient shouldn’t hold onto the original team’s NEK forever. So, behind the scenes, Dropbox runs background processes that slowly re-encrypt every block with the recipient’s keys. This way, we return to a clean, steady state without making users wait for all that processing upfront. It also turns out this approach aligns really well with our existing [data locality architecture](https://help.dropbox.com/security/physical-location-data-storage), which meant we could reuse a lot of the foundational setup.

## Additional implementation considerations

**Key caching
**Even though we added a new encryption tier, overall system load is lower because we no longer need to hit the top-level key for every block. But we still need to avoid overwhelming AWS KMS. That’s why we cache NEKs in memory for a short period. Since file operations tend to happen in bursts—like uploading or syncing multiple files at once—this cache is very effective in cutting down on repeated KMS calls.

![](/cms/content/dam/dropbox/tech-blog/en-us/2025/july/akm/diagrams/Security-Advanced-Key-Management-02.png/_jcr_content/renditions/Security-Advanced-Key-Management-02.webp)

How often the system finds encryption keys (NEKs) quickly from memory

**Key rotation
**Despite having more total keys than a two-tiered model, rotating encryption keys remains straightforward in our advanced key management setup. TEKs are stored in AWS KMS and can be [rotated using native tools](https://docs.aws.amazon.com/kms/latest/developerguide/rotate-keys.html). Rotating an NEK does require re-encrypting all the BEKs tied to it, but instead of storing every old version of an NEK indefinitely—which would introduce real security risks—we re-encrypt the BEKs using the new NEK. The good news is that this is an offline process, so while it involves one re-encryption per block, it has no impact on user-facing performance. This setup supports strong compartmentalization and helps teams meet compliance and security requirements, even for keys stored in an HSM.

**Chain of custody
**Memory bit flips are extremely rare, but at our scale, even rare hardware events can’t be ignored. A bit flip—when a single binary digit in memory unexpectedly changes from 0 to 1 or vice versa—can occur for any number of reasons, including hardware failures or even cosmic rays. If this happens while a key is being written to memory, it could silently corrupt the data or store a faulty key that later fails to decrypt the data. So while very unlikely, we still have to account for them because of the sheer volume of operations and keys we handle.

To protect against this, we built a chain-of-custody system for key operations. Whenever a key is used—whether in plaintext or encrypted form—it’s tagged with a cryptographic checksum. That checksum gets verified at every step. For example, if a plaintext NEK is used to encrypt a plaintext BEK, we generate a checksum of the new encrypted BEK. Then we decrypt that encrypted BEK, recompute the checksum, and compare it to the original. We also recompute and verify the checksum of the plaintext NEK. These extra steps make sure we never store corrupted versions of keys or encrypted data, even if something goes wrong halfway through an operation.

## Key takeaways about our development

Building advanced key management pushed us to rethink how we deliver both strong security and a smooth user experience at scale. One of the biggest takeaways? It’s not enough to just meet enterprise security and compliance standards. The system also has to be fast, reliable, and intuitive for both internal developers and our customers. From implementing a three-tier key hierarchy to optimizing key caching and rotation, this project helped us strike that balance between robust protection and ease of use.

Now, we’re applying those same lessons as we bring advanced key management to [Dash](https://www.dash.dropbox.com/). We’re building encryption into Dash from the ground up with the same core principles: strong team-level isolation, efficient access, and customer-managed encryption controls. This means each team’s content—embeddings, interactions, and history—can be encrypted with its own unique keys. The result: more privacy and control for customers, and a foundation for safe, scalable AI experiences.

Our three-tiered encryption scheme for advanced key management represents a leap forward in balancing robust security with practical usability. By introducing an intermediate layer of encryption keys (NEKs) into the standard two-tier model, Dropbox maintains fast file sharing and copying capabilities while still providing team-specific encryption. This approach not only meets the evolving security needs of enterprise customers but also showcases our commitment to innovation in the face of complex technical challenges.

With features like key caching, efficient key rotation, and a meticulous key chain of custody system, Dropbox has developed a solution that offers enhanced security without compromising on performance or user experience. And as cyber threats continue to evolve, such advancements in encryption key management will play a crucial role in safeguarding sensitive data for businesses and organizations around the world.

_Acknowledgments: Stas Ilinskiy, Jon Lee, Joe Eichenhofer, Adam Briand, Candy Xiao, Vicky Xiao, Max Murin, Chung Yang, Taylor Hansen, Anuradha Agarwal, Hemant Thakre, Rajat Goel, Varun Bhardwaj, Bryan Mann, Kshitija Niyogi, Cyrus Gandevia, and Varun Kuppili._

~ ~ ~

_If building innovative products, experiences, and infrastructure excites you, come build the future with us! Visit_[ __dropbox.com/jobs__](https://dropbox.com/jobs) _to see our open roles, and follow @LifeInsideDropbox on_[ __Instagram__](https://www.instagram.com/lifeinsidedropbox/?hl=en) _and_[ __Facebook__](https://www.facebook.com/lifeinsidedropbox/) _to see what it's like to create a more enlightened way of working._

* * *

// Tags

* [ Security ](https://dropbox.tech/security)
* [AI](https://dropbox.tech/tag-results.ai)
* [Dash](https://dropbox.tech/tag-results.dash)
* [encryption](https://dropbox.tech/tag-results.encryption)
* [Teams](https://dropbox.tech/tag-results.teams)

// Copy link

Link copied

![Copy link](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/copy.svg)

* Link copied

![Copy link](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/copy.svg)
* [ ![Share on Twitter](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/twitter.svg) ](https://twitter.com/intent/tweet/?text=Making%20file%20encryption%20fast%20and%20secure%20for%20teams%20with%20advanced%20key%20management&url=https://dropbox.tech/security/file-encryption-teams-advanced-key-management)
* [ ![Share on Facebook](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/facebook.svg) ](https://facebook.com/sharer/sharer.php?u=https://dropbox.tech/security/file-encryption-teams-advanced-key-management)
* [ ![Share on Linkedin](/cms/etc.clientlibs/settings/wcm/designs/dropbox-tech-blog/clientlib-article-content/resources/linkedin.svg) ](https://www.linkedin.com/shareArticle?mini=true&url=https://dropbox.tech/security/file-encryption-teams-advanced-key-management&title=Making%20file%20encryption%20fast%20and%20secure%20for%20teams%20with%20advanced%20key%20management&source=https://dropbox.tech/security/file-encryption-teams-advanced-key-management)
