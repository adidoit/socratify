---
title: "Docker without Docker"
company: "fly"
url: "https://fly.io/blog/docker-without-docker/"
content_length: 17549
type: "legendary_systems_architecture"
legendary: true
date: "2025-09-15"
---

Author
     ![Thomas Ptacek](/static/images/thomas.webp)

Name
     Thomas Ptacek 
@tqbf
     [ @tqbf ](https://twitter.com/tqbf)
![](/blog/docker-without-docker/assets/starry-containers.webp) Image by [ Annie Ruygt ](https://annieruygtillustration.com/)

We’re Fly.io. We take container images and run them on our hardware around the world. It’s pretty neat, and you [should check it out](https://fly.io/docs/speedrun/); with an already-working Docker container, you can be up and running on Fly in well under 10 minutes.

Even though most of our users deliver software to us as Docker containers, we don’t use Docker to run them. Docker is great, but we’re high-density multitenant, and despite strides, Docker’s isolation isn’t strong enough for that. So, instead, we transmogrify container images into [Firecracker micro-VMs](https://fly.io/blog/sandboxing-and-workload-isolation/).

Let’s demystify that.

## What’s An OCI Image?

They do their best to make it look a lot more complicated, but OCI images — OCI is [the standardized container format used by Docker](https://github.com/opencontainers/image-spec) — are pretty simple. An OCI image is just a stack of tarballs.

Backing up: most people build images from Dockerfiles. A useful way to look at a Dockerfile is as a series of shell commands, each generating a tarball; we call these “layers”. To rehydrate a container from its image, we just start the the first layer and unpack one on top of the next.

You can write a shell script to pull a Docker container from its registry, and that might clarify. Start with some configuration; by default, we’ll grab the base image for `golang`:

Wrap text  Copy to clipboard 
    
    
    image="${1:-golang}"
    registry_url='https://registry-1.docker.io'
    auth_url='https://auth.docker.io'
    svc_url='registry.docker.io'
    

We need to authenticate to pull public images from a Docker registry – this is boring but relevant to the next section – and that’s easy:

Wrap text  Copy to clipboard 
    
    
    function auth_token { 
      curl -fsSL "${auth_url}/token?service=${svc_url}&scope=repository:library/${image}:pull" | jq --raw-output .token
    }
    

That token will allow us to grab the “manifest” for the container, which is a JSON index of the parts of a container.

Wrap text  Copy to clipboard 
    
    
    function manifest { 
      token="$1"
      image="$2"
      digest="${3:-latest}"
    
      curl -fsSL \
        -H "Authorization: Bearer $token" \
        -H 'Accept: application/vnd.docker.distribution.manifest.list.v2+json' \
        -H 'Accept: application/vnd.docker.distribution.manifest.v1+json' \
        -H 'Accept: application/vnd.docker.distribution.manifest.v2+json' \
          "${registry_url}/v2/library/${image}/manifests/${digest}"
    }
    

The first query we make gives us the “manifest list”, which gives us pointers to images for each supported architecture:

Wrap text  Copy to clipboard 
    
    
      "manifests": [
        {
          "digest": "sha256:3fc96f3fc8a5566a07ac45759bad6381397f2f629bd9260ab0994ef0dc3b68ca",
          "platform": {
            "architecture": "amd64",
            "os": "linux"
          },
        },
    

Pull the `digest` out of the matching architecture entry and perform the same fetch again with it as an argument, and we get the manifest: JSON pointers to each of the layer tarballs:

Wrap text  Copy to clipboard 
    
    
       "config": {
          "digest": "sha256:0debfc3e0c9eb23d3fc83219afc614d85f0bc67cf21f2b3c0f21b24641e2bb06"
       },
       "layers": [
          {
             "digest": "sha256:004f1eed87df3f75f5e2a1a649fa7edd7f713d1300532fd0909bb39cd48437d7"
          },
    

It’s as easy to grab the actual data associated with these entries as you’d hope:

Wrap text  Copy to clipboard 
    
    
    function blob {
      token="$1"
      image="$2"
      digest="$3"
      file="$4"
    
      curl -fsSL -o "$file" \
          -H "Authorization: Bearer $token" \
            "${registry_url}/v2/library/${image}/blobs/${digest}"
    }
    

And with those pieces in place, pulling an image is simply:

Wrap text  Copy to clipboard 
    
    
    function layers { 
      echo "$1" | jq --raw-output '.layers[].digest'
    }
    
    token=$(auth_token "$image")
    amd64=$(linux_version $(manifest "$token" "$image"))
    mf=$(manifest "$token" "$image" "$amd64")
    
    i=0
    for L in $(layers "$mf"); do
      blob "$token" "$image" "$L" "layer_${i}.tgz"
      i=$((i + 1 ))
    done
    

Unpack the tarballs in order and you’ve got the filesystem layout the container expects to run in. Pull the “config” JSON and you’ve got the entrypoint to run for the container; you could, I guess, pull and run a Docker container with nothing but a shell script, which I’m probably the [1,000th person to point out](https://github.com/p8952/bocker). At any rate, [here’s the whole thing](https://gist.github.com/tqbf/10006fae0b81d7c7c93513890ff0cf08).

![Vitally important system diagram](/blog/docker-without-docker/assets/gwg.webp?2/3&centered)

You’re likely of one of two mindsets about this: (1) that it’s extremely Unixy and thus excellent, or (2) that it’s extremely Unixy and thus horrifying.

Unix `tar` is problematic. Summing up [Aleksa Sarai](https://www.cyphar.com/blog/post/20190121-ociv2-images-i-tar): `tar` isn’t well standardized, can be unpredictable, and is bad at random access and incremental updates. Tiny changes to large files between layers pointlessly duplicate those files; the poor job `tar` does managing container storage is part of why people burn so much time optimizing container image sizes.

Another fun detail is that OCI containers share a security footgun with git repositories: it’s easy to accidentally build a secret into a public container, and then inadvertently hide it with an update in a later image.

We’re of a third mindset regarding OCI images, which is that they are horrifying, and that’s liberating. They work pretty well in practice! Look how far they’ve taken us! Relax and make crappier designs; they’re all you probably need.

Speaking of which:

## Multi-Tenant Repositories

Back to Fly.io. Our users need to give us OCI containers, so that we can unpack and run them. There’s standard Docker tooling to do that, and we use it: we host a [Docker registry](https://docs.docker.com/registry/spec/api/) our users push to.

Running an instance of the Docker registry is very easy. You can do it right now; `docker pull registry && docker run registry`. But our needs are a little more complicated than the standard Docker registry: we need multi-tenancy, and authorization that wraps around our API. This turns out not to be hard, and we can walk you through it.

A thing to know off the bat: our users drive Fly.io with a command line utility called `flyctl`. `flyctl` is a Go program (with [public source](https://github.com/superfly/flyctl)) that runs on Linux, macOS, and Windows. A nice thing about working in Go in a container environment is that the whole ecosystem is built in the same language, and you can get a lot of stuff working quickly just by importing it. So, for instance, we can drive our Docker repository clientside from `flyctl` just by calling into Docker’s clientside library.

If you’re building your own platform and you have the means, I highly recommend the CLI-first tack we took. It is so choice. `flyctl` made it very easy to add new features, like [databases](https://fly.io/docs/reference/postgres/), [private networks](https://fly.io/blog/incoming-6pn-private-networks/), [volumes](https://fly.io/blog/persistent-storage-and-fast-remote-builds/), and our [bonkers SSH access system](https://fly.io/blog/ssh-and-user-mode-ip-wireguard/).

On the serverside, we started out simple: we ran an instance of the standard Docker registry with an authorizing proxy in front of it. `flyctl` manages a bearer token and uses the Docker APIs to initiate Docker pushes that pass that token; the token authorizes repositories serverside using calls into our API.

What we do now isn’t much more complicated than that. Instead of running a vanilla Docker registry, we built a custom repository server. As with the client, we get a Docker registry implementation just by importing Docker’s registry code as a Go dependency.

[We’ve extracted and simplified some of the Go code we used to build this here](https://gist.github.com/tqbf/ebd504a625813e6b8c5913fc28cc9515), just in case anyone wants to play around with the same idea. This isn’t our production code (in particular, all the actual authentication is ripped out), but it’s not far from it, and as you can see, there’s not much to it.

Our custom server isn’t architecturally that different from the vanilla registry/proxy system we had before. We wrap the Docker registry API handlers with authorizer middleware that checks tokens, references, and rewrites repository names. There are some very minor gotchas:

  * Docker is content-addressed, with blobs “named” for their SHA256 hashes, and attempts to reuse blobs shared between different repositories. You need to catch those cross-repository mounts and rewrite them. 
  * Docker’s registry code generates URLs with `_state` parameters that embed references to repositories; those need to get rewritten too. `_state` is HMAC-tagged; our code just shares the HMAC key between the registry and the authorizer. 



In both cases, the source of truth for who has which repositories and where is the database that backs our API server. Your push carries a bearer token that we resolve to an organization ID, and the name of the repository you’re pushing to, and, well, our design is what you’d probably come up with to make that work. I suppose my point here is that it’s pretty easy to slide into the Docker ecosystem.

## Building And Running VMs

The pieces are on the board:

  * We can accept containers from users 
  * We can store and manage containers for different organizations. 
  * We’ve got a VMM engine, Firecracker, that [we’ve written about already](https://fly.io/blog/sandboxing-and-workload-isolation). 



What we need to do now is arrange those pieces so that we can run containers as Firecracker VMs.

As far as we’re concerned, a container image is just a stack of tarballs and a blob of configuration (we layer additional configuration in as well). The tarballs expand to a directory tree for the VM to run in, and the configuration tells us what binary in that filesystem to run when the VM starts.

Meanwhile, what Firecracker wants is a set of block devices that Linux will mount as it boots up.

There’s an easy way on Linux to take a directory tree and turn it into a block device: create a file-backed [loop device](https://man7.org/linux/man-pages/man4/loop.4.html), and copy the directory tree into it. And that’s how we used to do things. When our orchestrator asked to boot up a VM on one of our servers, we would:

  1. Pull the matching container from the registry. 
  2. Create a loop device to store the container’s filesystem on. 
  3. Unpack the container (in this case, using Docker’s Go libraries) into the mounted loop device. 
  4. Create a second block device and inject our init, kernel, configuration, and other goop into. 
  5. Track down any [persistent volumes](https://fly.io/blog/persistent-storage-and-fast-remote-builds/) attached to the application, unlock them with LUKS, and collect their unlocked block devices. 
  6. Create a [TAP device](https://en.wikipedia.org/wiki/TUN/TAP), configure it for our network, and [attach BPF code to it](https://fly.io/blog/bpf-xdp-packet-filters-and-udp/). 
  7. Hand all this stuff off to Firecracker and tell it to boot . 



This is all a few thousand lines of Go.

This system worked, but wasn’t especially fast. Part of [the point of Firecracker](https://www.usenix.org/system/files/nsdi20-paper-agache.pdf) is to boot so quickly that you (or AWS) can host Lambda functions in it and not just long-running programs. A big problem for us was caching; a server in, say, Dallas that’s asked to run a VM for a customer is very likely to be asked to run more instances of that server (Fly.io apps scale trivially; if you’ve got 1 of something running and would be happier with 10 of them, you just run `flyctl scale count 10`). We did some caching to try to make this faster, but it was of dubious effectiveness.

The system we’d been running was, as far as container filesystems are concerned, not a whole lot more sophisticated than the shell script at the top of this post. So Jerome replaced it.

# This was all Andrew Dunham’s idea.

We asked if he wanted credit and he hesitated and said maybe and we said we’d keep it subtle, so here you go. He doesn’t work for us, he’s just awesome.

[ We ❤️ Andrew → ](https://www.youtube.com/watch?v=n2fM1vc-T94)

![](/static/images/cta-kitty.webp)

What we do now is run, on each of our servers, an instance of [`containerd`](https://containerd.io/). `containerd` does a whole bunch of stuff, but we use it as as a cache.

If you’re a Unix person from the 1990s like I am, and you just recently started paying attention to how Linux storage works again, you’ve probably noticed that _a lot has changed_. Sometime over the last 20 years, the block device layer in Linux got interesting. LVM2 can pool raw block devices and create synthetic block devices on top of them. It can treat block device sizes as an abstraction, chopping a 1TB block device into 1,000 5GB synthetic devices (so long as you don’t actually use 5GB on all those devices!). And it can create snapshots, preserving the blocks on a device in another synthetic device, and sharing those blocks among related devices with copy-on-write semantics.

`containerd` knows how to drive all this LVM2 stuff, and while I guess it’s out of fashion to use the `devmapper` backend these days, it works beautifully for our purposes. So now, to get an image, we pull it from the registry into our server-local `containerd`, configured to run on an LVM2 thin pool. `containerd` manages snapshots for every instance of a VM/container that we run. Its API provides a simple “lease”-based garbage collection scheme; when we boot a VM, we take out a lease on a container snapshot (which synthesizes a new block device based on the image, which containerd unpacks for us); LVM2 COW means multiple containers don’t step on each other. When a VM terminates, we surrender the lease, and containerd eventually GCs.

The first deployment of a VM/container on one of our servers does some lifting, but subsequent deployments are lightning fast (the VM build-and-boot process on a second deployment is faster than the logging that we do). 

## Some Words About Init

Jerome wrote our `init` in Rust, and, after being cajoled by Josh Triplett, [we released the code](https://github.com/superfly/init-snapshot), which you can go read.

The filesystem that Firecracker is mounting on the snapshot checkout we create is pretty raw. The first job our `init` has is to fill in the blanks to fully populate the root filesystem with the mounts that Linux needs to run normal programs. 

We inject a configuration file into each VM that carries the user, network, and entrypoint information needed to run the image. `init` reads that and configures the system. We use our own DNS server for private networking, so `init` overrides `resolv.conf`. We run a tiny SSH server for user logins over WireGuard; `init` spawns and monitors that process. We spawn and monitor the entry point program. That’s it; that’s an init.

## Putting It All Together

So, that’s about half the idea behind Fly.io. We run server hardware in racks around the world; those servers are tied together with an orchestration system that plugs into our API. Our CLI, `flyctl`, uses Docker’s tooling to push OCI images to us. Our orchestration system sends messages to servers to convert those OCI images to VMs. It’s all pretty neato, but I hope also kind of easy to get your head wrapped around.

The other “half” of Fly is our Anycast network, which is a CDN built in Rust that uses BGP4 Anycast routing to direct traffic to the nearest instance of your application. About which: more later.

# You can play with this right now.

It’ll take less than 10 minutes to get almost any container you’ve got running globally on our Rust-powered anycast proxy network.

[ Try Fly for free → ](https://fly.io/docs/speedrun/)

![](/static/images/cta-cat.webp)

Last updated 
•      Apr 8, 2021 
[ Share this post on Twitter ](https://twitter.com/share?text=Docker without Docker&url=https://fly.io/blog/docker-without-docker/&via=flydotio) [ Share this post on Hacker News ](http://news.ycombinator.com/submitlink?u=https://fly.io/blog/docker-without-docker/&t=Docker without Docker) [ Share this post on Reddit ](http://www.reddit.com/submit?url=https://fly.io/blog/docker-without-docker/&title=Docker without Docker)

Author
     ![Thomas Ptacek](/static/images/thomas.webp)

Name
     Thomas Ptacek 
@tqbf
     [ @tqbf ](https://twitter.com/tqbf)

Next post ↑ 
     [ Building a Distributed Turn-Based Game System in Elixir ](/blog/building-a-distributed-turn-based-game-system-in-elixir/)
Previous post ↓ 
     [ The 5-hour CDN ](/blog/the-5-hour-content-delivery-network/)

Next post ↑ 
     [ Building a Distributed Turn-Based Game System in Elixir ](/blog/building-a-distributed-turn-based-game-system-in-elixir/)
Previous post ↓ 
     [ The 5-hour CDN ](/blog/the-5-hour-content-delivery-network/)
