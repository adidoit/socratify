---
title: "Abusing Linux's firewall: the hack that allowed us to build Spectrum"
company: "cloudflare"
url: "https://blog.cloudflare.com/how-we-built-spectrum/"
type: "system_architecture"
date: "2025-09-15"
---

# Abusing Linux's firewall: the hack that allowed us to build Spectrum

2018-04-12

  * [![Marek Majkowski](https://blog.cloudflare.com/cdn-cgi/image/format=auto,dpr=3,width=64,height=64,gravity=face,fit=crop,zoom=0.5/https://cf-assets.www.cloudflare.com/zkvhlag99gkb/1JuU5qavgwVeqR8BAUrd6U/3a0d0445d41c9a3c42011046efe9c37b/marek-majkowski.jpeg)](/author/marek-majkowski/)

[Marek Majkowski](/author/marek-majkowski/)




4 min read

This post is also available in [简体中文](/zh-cn/how-we-built-spectrum), [Deutsch](/de-de/how-we-built-spectrum), [日本語](/ja-jp/how-we-built-spectrum), [한국어](/ko-kr/how-we-built-spectrum), [Español](/es-es/how-we-built-spectrum) and [Français](/fr-fr/how-we-built-spectrum).

![](https://cf-assets.www.cloudflare.com/zkvhlag99gkb/2fBc1UfFU6JKIdXFfqTLE1/4068183ffdde5483b46ed5f857b20bcd/how-we-built-spectrum.jpg)

Today we are [introducing Spectrum](/spectrum/): a new Cloudflare feature that brings [DDoS protection](https://www.cloudflare.com/ddos/), load balancing, and content acceleration to any TCP-based protocol.

[CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/) [image](https://www.flickr.com/photos/liftarn/13334109713) by [Staffan Vilcans](https://www.flickr.com/photos/liftarn)

Soon after we started building Spectrum, we hit a major technical obstacle: Spectrum requires us to accept connections on any valid TCP port, from 1 to 65535. On our Linux edge servers it's impossible to "accept inbound connections on _any_ port number". This is not a Linux-specific limitation: it's a characteristic of the BSD sockets API, the basis for network applications on most operating systems. Under the hood there are two overlapping problems that we needed to solve in order to deliver Spectrum:

  * how to accept TCP connections on all port numbers from 1 to 65535

  * how to configure a single Linux server to accept connections on a very large number of IP addresses (we have many thousands of IP addresses in our anycast ranges)




### Assigning millions of IPs to a server

Cloudflare’s edge servers have an almost identical configuration. In our early days, we used to assign specific /32 (and /128) IP addresses to the loopback network interface[1]. This worked well when we had dozens of IP addresses, but failed to scale as we grew.

Along came the ["AnyIP" trick](https://blog.widodh.nl/2016/04/anyip-bind-a-whole-subnet-to-your-linux-machine/). AnyIP allows us to assign whole IP prefixes (subnets) to the loopback interface, expanding from specific IP addresses. There is already common use of AnyIP: your computer has 127.0.0.0/8 assigned to the loopback interface. From the point of view of your computer, all IP addresses from 127.0.0.1 to 127.255.255.254 belong to the local machine.

This trick is applicable to more than the 127.0.0.1/8 block. To treat the whole range of 192.0.2.0/24 as assigned locally, run:
    
    
    ip route add local 192.0.2.0/24 dev lo

Following this, you can bind to port 8080 on one of these IP addresses just fine:
    
    
    nc -l 192.0.2.1 8080

Getting IPv6 to work is a bit harder:
    
    
    ip route add local 2001:db8::/64 dev lo

Sadly, you can't just bind to these attached v6 IP addresses like in the v4 example. To get this working you must use the `IP_FREEBIND` socket option, which requires elevated privileges. For completeness, there is also a sysctl `net.ipv6.ip_nonlocal_bind`, but we don't recommend touching it.

This AnyIP trick allows us to have millions of IP addresses assigned locally to each server:
    
    
    $ ip addr show
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536
        inet 1.1.1.0/24 scope global lo
           valid_lft forever preferred_lft forever
        inet 104.16.0.0/16 scope global lo
           valid_lft forever preferred_lft forever
    ...

### Binding to ALL ports

The second major issue is the ability to open TCP sockets for any port number. In Linux, and generally in any system supporting the BSD sockets API, you can only bind to a specific TCP port number with a single `bind` system call. It’s not possible to bind to multiple ports in a single operation.

A naive solution would be to `bind` 65535 times, once for each of the 65535 possible ports. Indeed, this could have been an option, but with terrible consequences:

  * [The revenge of the listening sockets](/revenge-listening-sockets/)




Internally, the Linux kernel stores listening sockets in a hash table indexed by port numbers, [LHTABLE](https://elixir.bootlin.com/linux/latest/source/include/net/inet_hashtables.h#L118), using exactly 32 buckets:
    
    
    /* Yes, really, this is all you need. */
    #define INET_LHTABLE_SIZE       32

Had we opened 65k ports, lookups to this table would slow drastically: each hash table bucket would contain two thousand items.

Another way to solve our problem would be to use iptables’ rich NAT features: we could rewrite the destination of inbound packets to some specific address/port, and our application would bind to that.

We didn't want to do this though, since it requires enabling the iptables `conntrack` module. Historically we found some [performance edge cases](http://patchwork.ozlabs.org/cover/810566/), and conntrack cannot cope with some of the large DDoS attacks that we encounter.

Additionally, with the NAT approach we would lose destination IP address information. To remediate this, there exists a poorly known `SO_ORIGINAL_DST` socket option, but [the code doesn't look encouraging](https://github.com/torvalds/linux/blob/b5dbc28762fd3fd40ba76303be0c7f707826f982/net/ipv4/netfilter/nf_conntrack_l3proto_ipv4.c).

Fortunately, there is a way to achieve our goals that does not involve binding to all 65k ports, or use `conntrack`.

### Firewall to the rescue

Before we go any further, let’s revisit the general flow of network packets in an operating system.

Commonly, there are two distinct layers in the inbound packet path:

  * IP firewall

  * network stack




These are conceptually distinct. The IP firewall is usually a stateless piece of software (let's ignore `conntrack` and IP fragment reassembly for now). The firewall analyzes IP packets and decides whether to ACCEPT or DROP them. Please note: at this layer we are talking about _packets_ and _port numbers_ \- not _applications_ or _sockets_.

Then there is the network stack. This beast maintains plenty of state. Its main task is to dispatch inbound IP packets into _sockets_ , which are then handled by userspace _applications_. The network stack manages abstractions which are shared with userspace. It reassembles TCP flows, deals with routing, and knows which IP addresses are local.

### The magic dust

Source: [still from YouTube](https://www.youtube.com/watch?v=9CS7j5I6aOc)

At some point we stumbled upon the `TPROXY` iptables module. The [official documentation](http://ipset.netfilter.org/iptables-extensions.man.html) is easy to overlook:
    
    
    TPROXY
    This target is only valid in the mangle table, in the 
    PREROUTING chain and user-defined chains which are only 
    called from this chain.  It redirects the packet to a local 
    socket without changing the packet header in any way. It can
    also change the mark value which can then be used in 
    advanced routing rules. 

Another piece of documentation can be found in the kernel:

  * [docs/networking/tproxy.txt](https://www.kernel.org/doc/Documentation/networking/tproxy.txt)




The more we thought about it, the more curious we became...

So... What does TPROXY actually _do_?

### Revealing the magic trick

The `TPROXY` code is [surprisingly trivial](https://elixir.bootlin.com/linux/v4.16.1/source/net/netfilter/xt_TPROXY.c#L119):
    
    
    case NFT_LOOKUP_LISTENER:
      sk = inet_lookup_listener(net, &tcp_hashinfo, skb,
    				    ip_hdrlen(skb) +
    				      __tcp_hdrlen(tcph),
    				    saddr, sport,
    				    daddr, dport,
    				    in->ifindex, 0);

Let me read this out loud for you: in an `iptables` module, which is part of the firewall, we call `inet_lookup_listener`. This function takes a src/dst port/IP 4-tuple, and returns the listening socket that is able to accept that connection. This is a core functionality of the network stack’s socket dispatch.

Once again: firewall code calls a socket dispatch routine.

Later on [`TPROXY` actually _does_ the socket dispatch](https://elixir.bootlin.com/linux/v4.16.1/source/net/netfilter/xt_TPROXY.c#L299):
    
    
    skb->sk = sk;

This line assigns a socket `struct sock` to an inbound packet - completing the dispatch.

### Pulling the rabbit from the hat

[CC BY-SA 2.0](https://creativecommons.org/licenses/by-sa/2.0/) [image](https://www.flickr.com/photos/angelaboothroyd/3649474619) by [Angela Boothroyd](https://www.flickr.com/photos/angelaboothroyd)

Armed with `TPROXY`, we can perform the bind-to-all-ports trick very easily. Here's the configuration:
    
    
    # Set 192.0.2.0/24 to be routed locally with AnyIP.
    # Make it explicit that the source IP used for this network
    # when connecting locally should be in 127.0.0.0/8 range.
    # This is needed since otherwise the TPROXY rule would match
    # both forward and backward traffic. We want it to catch 
    # forward traffic only.
    sudo ip route add local 192.0.2.0/24 dev lo src 127.0.0.1
    
    # Set the magical TPROXY routing
    sudo iptables -t mangle -I PREROUTING \
            -d 192.0.2.0/24 -p tcp \
            -j TPROXY --on-port=1234 --on-ip=127.0.0.1

In addition to setting this in place, you need to start a TCP server with the magical `IP_TRANSPARENT` socket option. Our example below needs to listen on tcp://127.0.0.1:1234. The [man page for `IP_TRANSPARENT`](http://man7.org/linux/man-pages/man7/ip.7.html) shows:
    
    
    IP_TRANSPARENT (since Linux 2.6.24)
    Setting this boolean option enables transparent proxying on
    this socket.  This socket option allows the calling applica‐
    tion to bind to a nonlocal IP address and operate both as a
    client and a server with the foreign address as the local
    end‐point.  NOTE: this requires that routing be set up in
    a way that packets going to the foreign address are routed 
    through the TProxy box (i.e., the system hosting the 
    application that employs the IP_TRANSPARENT socket option).
    Enabling this socket option requires superuser privileges
    (the CAP_NET_ADMIN capability).
    
    TProxy redirection with the iptables TPROXY target also
    requires that this option be set on the redirected socket.

Here's a simple Python server:
    
    
    import socket
    
    IP_TRANSPARENT = 19
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.IPPROTO_IP, IP_TRANSPARENT, 1)
    
    s.bind(('127.0.0.1', 1234))
    s.listen(32)
    print("[+] Bound to tcp://127.0.0.1:1234")
    while True:
        c, (r_ip, r_port) = s.accept()
        l_ip, l_port = c.getsockname()
        print("[ ] Connection from tcp://%s:%d to tcp://%s:%d" % (r_ip, r_port, l_ip, l_port))
        c.send(b"hello world\n")
        c.close()

After running the server you can connect to it from arbitrary IP addresses:
    
    
    $ nc -v 192.0.2.1 9999
    Connection to 192.0.2.1 9999 port [tcp/*] succeeded!
    hello world

Most importantly, the server will report the connection indeed was directed to 192.0.2.1 port 9999, _even though nobody actually listens on that IP address and port_ :
    
    
    $ sudo python3 transparent2.py
    [+] Bound to tcp://127.0.0.1:1234
    [ ] Connection from tcp://127.0.0.1:60036 to tcp://192.0.2.1:9999

Tada! This is how to _bind to any port_ on Linux, without using `conntrack`.

### That's all folks

In this post we described how to use an obscure iptables module, originally designed to help transparent proxying, for something slightly different. With its help we can perform things we thought impossible using the standard BSD sockets API, avoiding the need for any custom kernel patches.

The `TPROXY` module is very unusual - in the context of the Linux firewall it performs things typically done by the Linux network stack. The official documentation is rather lacking, and I don't believe many Linux users understand the full power of this module.

It's fair to say that `TPROXY` allows our Spectrum product to run smoothly on the vanilla kernel. It’s yet another reminder of how important it is to try to understand iptables and the network stack!

* * *

_Doing low level socket work sound interesting? Join our_[ _world famous team_](https://boards.greenhouse.io/cloudflare/jobs/589572) _in London, Austin, San Francisco, Champaign and our elite office in Warsaw, Poland_.

* * *

  1. Assigning IP addresses to loopback interface, together with appropriate `rp_filter` and BGP configuration allows us to handle arbitrary IP ranges on our edge servers. ↩︎




Cloudflare's connectivity cloud protects [entire corporate networks](https://www.cloudflare.com/network-services/), helps customers build [Internet-scale applications efficiently](https://workers.cloudflare.com/), accelerates any [website or Internet application](https://www.cloudflare.com/performance/accelerate-internet-applications/), [wards off DDoS attacks](https://www.cloudflare.com/ddos/), keeps [hackers at bay](https://www.cloudflare.com/application-security/), and can help you on [your journey to Zero Trust](https://www.cloudflare.com/products/zero-trust/).  
  
Visit [1.1.1.1](https://one.one.one.one/) from any device to get started with our free app that makes your Internet faster and safer.  
  
To learn more about our mission to help build a better Internet, [start here](https://www.cloudflare.com/learning/what-is-cloudflare/). If you're looking for a new career direction, check out [our open positions](https://www.cloudflare.com/careers).

[Discuss on Hacker News](https://news.ycombinator.com/submitlink?u=https://blog.cloudflare.com/how-we-built-spectrum "Discuss on Hacker News")

[Product News](/tag/product-news/)[Spectrum](/tag/spectrum/)[DDoS](/tag/ddos/)[Security](/tag/security/)[Linux](/tag/linux/)[Speed & Reliability](/tag/speed-and-reliability/)
