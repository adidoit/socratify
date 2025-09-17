---
title: "Categories"
company: "heroku"
url: "https://devcenter.heroku.com/articles/http-routing"
type: "final_harvest"
date: "2025-09-15"
---

  * [Heroku Architecture](/categories/heroku-architecture)
  * [Networking & DNS](/categories/networking-dns)
  * [HTTP Routing](/articles/http-routing)



# HTTP Routing

English — [日本語に切り替える](/ja/articles/http-routing)

Last updated July 31, 2025

##  Table of Contents 

  * Legacy Router and Router 2.0
  * Enable and Disable Router 2.0
  * Routing
  * Request Distribution
  * Request Concurrency Limiting
  * Dyno Connection Behavior on the Common Runtime
  * Dyno Connection Behavior in Private Spaces
  * Timeouts
  * Keepalives
  * Simultaneous Connections
  * Request Buffering
  * Response Buffering
  * Heroku Headers
  * Heroku Router Log Format
  * Caching
  * WebSockets
  * Gzipped Responses
  * Supported HTTP Methods
  * Expect: 100-continue
  * HTTP Versions Supported
  * HTTP/2 with Router 2.0
  * HTTP Validation and Restrictions
  * Protocol Upgrades
  * Not Supported
  * Available Cipher Suites on the Common Runtime
  * Available Cipher Suites on Private Spaces
  * Legacy Router Deprecation and EOL



Heroku is actively [migrating applications to Router 2.0](https://help.heroku.com/JJ3M1TOM/common-runtime-legacy-router-end-of-life-faq). If you have yet to migrate to Router 2.0 or have recently migrated, we encourage you to read up on [Tips & Tricks for Migrating to Router 2.0](https://www.heroku.com/blog/tips-tricks-router-2dot0-migration/). If your application uses Puma, please see the blog post, [Pumas, Routers & Keepalives—Oh my!](https://www.heroku.com/blog/pumas-routers-keepalives-ohmy/) as it details how to properly use Puma and the new router together.

The Heroku platform automatically routes HTTP requests sent to your app’s hostname(s) to your web dynos. There are different routers used for different [runtimes](https://devcenter.heroku.com/articles/dyno-runtime).

The Common Runtime has a Legacy Router and a Router 2.0 option. The legacy router is deprecated and staged for EOL in Summer 2025. This article provides a detailed reference of how the routers behave, and how they conform to the HTTP specification.

Both [generations](https://devcenter.heroku.com/articles/generations) of the Private Spaces Runtime have different routers than the Common Runtime, but they behave much like the ones described on this page. The router for Fir Private Spaces in particular is very similar, though not exactly like, Router 2.0. Refer to [Routing in Private Spaces](https://devcenter.heroku.com/articles/routing-in-private-spaces) to learn about the differences in the Private Spaces Runtime routers.

## Legacy Router and Router 2.0

The entry point for all applications on the [Common Runtime](https://devcenter.heroku.com/articles/dyno-runtime#common-runtime) stack is the `herokuapp.com` domain which offers a direct routing path to your web dynos. Heroku has two generally available Common Runtime routers, the new [Router 2.0](https://devcenter.heroku.com/changelog/3063) and the deprecated legacy router. Router 2.0 supports additional features over the legacy router, such as HTTP/2.

Basic routing and most functionality remain the same between the two routers, with all differences and enhancements explained in the relevant sections of this document. We recommend using Router 2.0 instead of the legacy router. We’re deprecating our legacy router and it won’t receive new features going forward. See this [Help article](https://help.heroku.com/JJ3M1TOM/common-runtime-legacy-router-end-of-life-faq) for more details about the end-of-life and migration plan.

The legacy router and Router 2.0 support the following features:

Feature | Legacy Router | Router 2.0 | Notes  
---|---|---|---  
[Routing](https://devcenter.heroku.com/articles/http-routing#routing) | x | x | Basic routing, including TLS termination, is supported.  
[Router logs](https://devcenter.heroku.com/articles/http-routing#heroku-router-log-format) | x | x | Per-request router logs appear in your app’s log stream.  
[Error codes](https://devcenter.heroku.com/articles/error-codes) | x | x | Most H codes are supported and reported in router logs. Currently, the only exceptions are H23 and H26.  
[Dyno sleeping](https://devcenter.heroku.com/articles/eco-dyno-hours#dyno-sleeping) | x | x | Dyno sleeping (idling) is supported for Eco dynos.  
[Request concurrency limiting](https://devcenter.heroku.com/articles/http-routing#request-concurrency-limiting) | x | x | Each router maintains an internal per-app request counter and limits the number of concurrent requests per app.  
[Heroku headers](https://devcenter.heroku.com/articles/http-routing#heroku-headers) | x | x | Heroku Headers are a set of headers that Heroku adds to HTTP responses.  
[WebSockets](https://devcenter.heroku.com/articles/http-routing#websockets) | x | x | WebSockets protocol is supported by both routers.  
[Expect 100-continue](https://devcenter.heroku.com/articles/http-routing#expect-100-continue) | x | x | The `Expect: 100-continue` header is supported by both routers.  
[Dyno quarantining](https://devcenter.heroku.com/articles/http-routing#dyno-connection-behavior-on-the-common-runtime) | x | x | The router quarantines unreachable dynos.  
[Preboot](https://devcenter.heroku.com/articles/preboot) | x | x | Preboot release behavior works with both routers.  
[Session affinity](https://devcenter.heroku.com/articles/session-affinity) | x | x | Associates all HTTP requests coming from an end-user with a web dyno.  
HTTP/2 |  | x | HTTP/2 is available for Router 2.0 only.  
Keepalives |  | x | Only Router 2.0 supports HTTP keepalives between routers and dynos.  
IPV6 |  | X | IPv6 is only available for [Fir](https://devcenter.heroku.com/articles/generations#fir)-generation apps  
  
## Enable and Disable Router 2.0

To use the new router, enable the feature:
    
    
    $ heroku features:enable http-routing-2-dot-0 -a <app name>
    

After enabling this feature, your app starts to receive traffic through Router 2.0.

Clients must re-establish their connection to your app after enabling or disabling the `http-routing-2-dot-0` flag.

To stop using Router 2.0:

You can’t disable Router 2.0 on [Eco-](https://devcenter.heroku.com/articles/eco-dyno-hours) or [Basic](https://devcenter.heroku.com/articles/dyno-tiers#basic-tier)-tier apps.
    
    
    $ heroku features:disable http-routing-2-dot-0 -a <app name>
    

You don’t need to do anything else to return your app to its previous routing behavior.

## Routing

Inbound requests are received by a load balancer that offers SSL termination. From here they are passed directly to a set of routers.

The routers are responsible for determining the location of your application’s web [dynos](https://devcenter.heroku.com/articles/dynos) and forwarding the HTTP request to one of these dynos.

A request’s unobfuscated path from the end-client through the Heroku infrastructure to your application allows for full support of [HTTP 1.1](https://datatracker.ietf.org/doc/html/rfc2616 "RFC2616: Hypertext Transfer Protocol -- HTTP/1.1") features such as chunked responses, long polling, websockets, and using an async webserver to handle multiple responses from a single web process. We support HTTP/2 through Router 2.0. We also maintain HTTP 1.0 compatibility.

## Request Distribution

Routers use a random selection algorithm for balancing HTTP requests across web dynos. In cases where there are a large number of dynos, the algorithm may optionally bias its selection towards dynos resident in the same AWS availability zone as the router making the selection.

## Request Concurrency Limiting

Each router maintains an internal per-app request counter. On the Common Runtime, routers limit the number of concurrent requests per app. There is no coordination between routers however, so this request limit is per router. The request counter on each router has a maximum size of 200n (n = the number of web dynos your app has running). If the request counter on a particular router fills up, subsequent requests to that router will immediately return an [H11 (Backlog too deep)](https://devcenter.heroku.com/articles/error-codes#h11-backlog-too-deep) response.

## Dyno Connection Behavior on the Common Runtime

When Heroku receives an HTTP request, a router establishes a new upstream TCP connection to a randomly selected web dyno running in the Common Runtime. If the dyno refuses the connection or can’t successfully establish one after 5 seconds, we quarantine the dyno. That router no longer forwards requests to the dyno for up to 5 seconds. The quarantine only applies to a single router. As each router keeps its own list of quarantined dynos, other routers can continue to forward connections to that dyno.

When a connection is refused or times out, the router processing the request retries to connect with another dyno. It makes a maximum of 10 connection attempts, or fewer if you have less than 10 running web dynos. If it can’t establish a connection, the router returns an [H19: Connection Timeout](https://devcenter.heroku.com/articles/error-codes#h19-backend-connection-timeout) or [H21: Connection Refused](https://devcenter.heroku.com/articles/error-codes#h21-backend-connection-refused) error.

If it quarantined all dynos, the router retries to find an unquarantined dyno for up to 75 seconds with an incremental backoff. If the router finds an unquarantined dyno, it attempts to establish a connection. If the router can’t find an unquarantined dyno after 75 seconds, the router responds with a 503 and serves an [H99](https://devcenter.heroku.com/articles/error-codes#h99-platform-error) error.

The total timeout for a request when attempting to establish a connection is 75 seconds.

## Dyno Connection Behavior in Private Spaces

Dynos in a Private Space run on their own network and routing layer, and communicate to each other over a private network. The router in Private Spaces receives outbound HTTP requests over a set of allowed, stable IP addresses. You can also restrict inbound web requests with [Trusted IPs](https://devcenter.heroku.com/articles/private-spaces-trusted-ip-ranges) or [internal routing](https://devcenter.heroku.com/articles/internal-routing).

Custom Trusted IPs and internal routing aren’t yet available for [Fir](https://devcenter.heroku.com/articles/generations#fir)-generation apps and spaces. Subscribe to our [changelog](https://devcenter.heroku.com/changelog) to stay informed of when we add these features.

Unlike router behavior in the Common Runtime with web dynos, the router in Private Spaces does not forward any connections of HTTP requests from one web dyno to another if a connection is refused or timed out. Instead, the connection times out after 30 seconds and returns a [H12](https://devcenter.heroku.com/articles/error-codes#h12-request-timeout) error. Additional details about the routing behavior in Private Spaces can be found in the [Routing in Private Spaces](https://devcenter.heroku.com/articles/routing-in-private-spaces) article.

## Timeouts

After a dyno connection has been established, HTTP requests have an initial 30 second window in which the web process must return response data (either the completed response or some amount of response data to indicate that the process is active). Processes that do not send response data within the initial 30-second window will see an [H12](https://devcenter.heroku.com/articles/error-codes#h12-request-timeout) error in their [logs](https://devcenter.heroku.com/articles/logging).

After the initial response, each byte sent (either from the client or from your app process) resets a rolling 55 second window. If no data is sent during this 55 second window then the connection is terminated and a [H15](https://devcenter.heroku.com/articles/error-codes#h15-idle-connection) or [H28](https://devcenter.heroku.com/articles/error-codes#h28-client-connection-idle) error is logged.

Additional details can be found in the [Request Timeout](https://devcenter.heroku.com/articles/request-timeout) article.

## Keepalives

Router 2.0 and the [Fir router](https://devcenter.heroku.com/articles/routing-in-private-spaces) uses [Keep-Alive connections](https://datatracker.ietf.org/doc/html/rfc7230#appendix-A.1.2) between itself and the dyno. The legacy router doesn’t support Keep-Alive connections, closing the connection after each request, except in the case of WebSocket connections.

Router 2.0 and the Fir router both maintain a pool of connections between itself and your application’s web dynos. For a connection not currently handling an HTTP request or a WebSockets connection, the **idle timeout is 90 seconds**. When this timeout is hit, the router will quietly close the connection. No Heroku error code is reported. However, if your dyno’s server includes a connection idle timeout of less than 90 seconds, this may introduce a race condition between the router sending a request and the dyno’s server closing a stale connection. This race condition can lead to [H18: Server Request Interrupted](https://devcenter.heroku.com/articles/error-codes#h18-server-request-interrupted) or [H13: Connection closed without response](https://devcenter.heroku.com/articles/error-codes#h13-connection-closed-without-response) errors. **To avoid this race condition, Heroku recommends setting any server idle connection timeouts to 90 seconds or greater. This will allow the router to initiate connection closes. Alternatively, you may disable keepalives altogether (see below).**

You can use the [`http-disable-keepalive-to-dyno`](https://devcenter.heroku.com/articles/heroku-labs-disabling-keepalives-to-dyno-for-router-2-0) labs flag to disable connection reuse between the router and your dynos. Note that you can’t disable keepalives for [Fir](https://devcenter.heroku.com/articles/generations#fir)-generation apps.

## Simultaneous Connections

The `herokuapp.com` routing stack allows many concurrent connections to web dynos. For production apps, you should always choose an embedded webserver that allows multiple concurrent connections to maximize the responsiveness of your app. You can also take advantage of concurrent connections for long-polling requests.

Almost all modern web frameworks and embeddable webservers support multiple concurrent connections. Examples of webservers that allow concurrent request processing in the dyno include [Unicorn](https://devcenter.heroku.com/articles/rails-unicorn) (Ruby), Goliath (Ruby), Puma (JRuby), [Gunicorn](https://devcenter.heroku.com/articles/python-gunicorn) (Python), and Jetty (Java).

## Request Buffering

When processing an incoming request, a router sets up a buffer to receive the entire HTTP request line and request headers. Each of these have further limitations described in HTTP validation and restrictions. The body of a request with a well-defined content-length is transmitted by using a 1024 byte buffer, filled and flushed continuously. This represents a size that encompasses the vast majority of requests in terms of volume. Streamed request bodies (chunk encoding) will be passed through as the data comes in. The request will start being dispatched to a dyno only once the entire set of HTTP headers has been received.

As a result, each router buffers the header section of all requests, and will deliver this to your dyno as fast as our internal network will run. The dyno is protected from slow clients until the request body needs to be read. If you need protection from clients transmitting the body of a request slowly, you’ll have the request headers available to you in order to make a decision as to when you want to drop the request by closing the connection at the dyno.

## Response Buffering

The router maintains a 1 MB buffer for responses from the dyno per connection. This means that you can send a response up to 1 MB in size before the rate at which the client receives the response will affect the dyno - even if the dyno closes the connection, the router will keep sending the response buffer to the client. The transfer rate for responses larger than the 1 MB buffer size will be limited by how fast the client can receive data.

## Heroku Headers

All headers are considered to be case-insensitive, as per [HTTP Specification](http://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.2). The `X-Forwarded-For`, `X-Forwarded-By`, `X-Forwarded-Proto`, and `X-Forwarded-Host` headers are not trusted for security reasons, because it is not possible to know the order in which already existing fields were added (as per [Forwarded HTTP Extension](https://tools.ietf.org/html/rfc7239.html)).

  * `X-Forwarded-For`: the originating IP address of the client connecting to the Heroku router. If the Heroku router receives a request with the `X-Forwarded-For` header already present, the originating IP detected by the router is appended to the right-side of the list.
  * `X-Forwarded-Proto`: the originating protocol of the HTTP request (example: https)
  * `X-Forwarded-Port`: the originating port of the HTTP request (example: 443)
  * `X-Request-Start`: unix timestamp (milliseconds) when the request was received by the router
  * `X-Request-Id`: the Heroku [HTTP Request ID](https://devcenter.heroku.com/articles/http-request-id)
  * `Via`: a code name for the Heroku router



### Network Error Logging

This feature isn’t yet available for [Fir](https://devcenter.heroku.com/articles/generations#fir). Subscribe to our [changelog](https://devcenter.heroku.com/changelog) to stay informed of when we add features to Fir.

Heroku collects select user browser data via [Network Error Logging (NEL)](https://w3c.github.io/network-error-logging/). NEL provides Heroku with more insights to act before an incident starts to negatively impact customers. NEL is a W3C standard (draft) that defines how to measure performance characteristics of web applications in real-time with data from end users.

[Several browsers](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/NEL#browser_compatibility) implement this standard, including Google Chrome and Microsoft Edge. On the server, NEL works by annotating HTTP responses with headers that instruct the browser to submit reports to an endpoint that aggregates the information and processes connectivity and latency metrics. Heroku conducts NEL consistent with the [Salesforce Privacy Statement](https://www.heroku.com/policy/privacy).

Heroku adds the following headers to HTTP responses:

  * `NEL`: the header used to configure network request logging
  * `Report-To`: this field instructs the user agent to store reporting endpoints for an origin
  * `Reporting-Endpoints`: the endpoints used to construct the reporting configuration for a resource



## Heroku Router Log Format

### Legacy Router Logs

The log format for the legacy router follows these formats:

#### Info Logs

This is what is sent to [log drains](https://devcenter.heroku.com/articles/log-drains):
    
    
    264 <158>1 2012-10-11T03:47:20+00:00 host heroku router - at=info method=GET path=/ host=example-app-1234567890ab.herokuapp.com request_id=8601b555-6a83-4c12-8269-97c8e32cdb22 fwd="204.204.204.204" dyno=web.1 connect=1ms service=18ms status=200 bytes=13 tls_version=tls1.1 protocol=http
    

This is the same log line when viewed with `heroku logs`:
    
    
    2012-10-11T03:47:20+00:00 heroku[router]: at=info method=GET path=/ host=example-app-1234567890ab.herokuapp.com request_id=8601b555-6a83-4c12-8269-97c8e32cdb22 fwd="204.204.204.204" dyno=web.1 connect=1ms service=18ms status=200 bytes=13 tls_version=tls1.1 protocol=http
    

  * `method`: HTTP request method
  * `path`: HTTP request path and query string
  * `host`: HTTP request `Host` header value
  * `request_id`: the Heroku [HTTP Request ID](https://devcenter.heroku.com/articles/http-request-id)
  * `fwd`: HTTP request `X-Forwarded-For` header value
  * `dyno`: name of the dyno that serviced the request
  * `connect`: amount of time in milliseconds spent establishing a connection to the backend web process
  * `service`: amount of time in milliseconds spent proxying data between the backend web process and the client
  * `status`: HTTP response code
  * `bytes`: Number of bytes transferred from the backend web process to the client
  * `protocol`: indicates the request protocol
  * `tls_version`: The TLS version used to make the connection. Possible values are ssl3.0, tls1.2, tls1.3, or unknown. Note: this is for Private Spaces only.



#### Error Logs

This is what is sent to [log drains](https://devcenter.heroku.com/articles/log-drains):
    
    
    277 <158>1 2012-10-11T03:47:20+00:00 host heroku router - at=error code=H12 desc="Request timeout" method=GET path=/ host=example-app-1234567890ab.herokuapp.com request_id=8601b555-6a83-4c12-8269-97c8e32cdb22 fwd="204.204.204.204" dyno=web.1 connect= service=30000ms status=503 bytes=0 protocol=http
    

This is the same log line when viewed with `heroku logs`:
    
    
    2012-10-11T03:47:20+00:00 heroku[router]: at=error code=H12 desc="Request timeout" method=GET path=/ host=example-app-1234567890ab.herokuapp.com request_id=8601b555-6a83-4c12-8269-97c8e32cdb22 fwd="204.204.204.204" dyno=web.1 connect= service=30000ms status=503 bytes=0 protocol=http
    

  * `code`: [Heroku error code](https://devcenter.heroku.com/articles/error-codes)
  * `desc`: description of error



### Router 2.0 Logs

With Router 2.0 enabled on your Common Runtime app, `heroku[router]` logs take a slightly different format. This new format provides more information on HTTP and TLS versions used by clients. The below fields are different in Router 2.0:

  * `protocol`: indicates the request protocol, including the HTTP version. Possible values are `http1.1` and `http2.0`.
  * `tls`: indicates whether TLS is in use on the connection. Possible values are `true` and `false`.
  * `tls_version`: indicates the TLS version used on the connection. Possible values are `tls1.2`, `tls1.3` or `unknown`. Note that `unknown` is the value for all TLS connections on the default `herokuapp.com` domain.



Here’s an example of a log line in the new and improved format:
    
    
    2024-04-26T16:58:32.943253+00:00 heroku[router]: at=info method=GET path="/" host=my-app.example.com request_id=6903a168-b79b-ec27-03c8-b8f64d8d8792 fwd=138.68.186.89 dyno=web.1 connect=0ms service=0ms status=200 bytes=0 protocol=http2.0 tls=true tls_version=tls1.3
    

## Caching

Apps serving large amounts of static assets can take advantage of [HTTP caching](https://devcenter.heroku.com/articles/http-caching) to improve performance and reduce load.

## WebSockets

[WebSocket](https://devcenter.heroku.com/articles/websockets) functionality is supported for all applications.

## Gzipped Responses

Since requests to Common Runtime apps are made directly to the application server – not proxied through an HTTP server like nginx – any [compression of responses](https://devcenter.heroku.com/articles/compressing-http-messages-with-gzip) must be done within your application.

## Supported HTTP Methods

The Heroku HTTP stack supports any [HTTP method](https://datatracker.ietf.org/doc/html/rfc2616#section-5.1.1 "HTTP/1.1 Method token") (sometimes called a “verb”), even those not defined in an RFC, except the following: [CONNECT](https://datatracker.ietf.org/doc/html/rfc2616#section-9.9 "CONNECT method").

Commonly used methods include [GET](https://datatracker.ietf.org/doc/html/rfc2616#section-9.3 "HTTP/1.1 - GET"), [POST](https://datatracker.ietf.org/doc/html/rfc2616#section-9.5 "HTTP/1.1 - POST"), [PUT](https://datatracker.ietf.org/doc/html/rfc2616#section-9.6 "HTTP/1.1 - PUT"), [DELETE](https://datatracker.ietf.org/doc/html/rfc2616#section-9.7 "HTTP/1.1 - DELETE"), [HEAD](https://datatracker.ietf.org/doc/html/rfc2616#section-9.4 "HTTP/1.1 - HEAD"), [OPTIONS](https://datatracker.ietf.org/doc/html/rfc2616#section-9.2 "HTTP/1.1 - OPTIONS"), and [PATCH](https://datatracker.ietf.org/doc/html/rfc5789 "PATCH Method for HTTP"). Method names are limited to 127 characters in length.

## Expect: 100-continue

  * Enabling 100-Continue Support
  * Corner Cases
  * Proxy Requirements
  * Heroku Router 100-Continue Support



The HTTP protocol has a few built-in mechanisms to help clients cooperate with servers in order to get better service overall. One of such mechanisms is the `Expect: 100-continue` header that can be sent along with requests[[1]](http://www.w3.org/Protocols/rfc2616/rfc2616-sec8.html#sec8.2.3).

This header and value are to be used by friendly clients when they are sending large HTTP requests, and want to know if the server can safely accept it before sending it, in order to prevent denial of service issues, and allow some optimizations. The [cURL](http://curl.haxx.se/) HTTP client is the most known library using this mechanism, doing it for any content-body larger than 1 KB (undocumented behavior).

Whenever asking for the permission, the server is allowed to respond with a [`100 Continue` HTTP status](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.1.1), which lets the client know that it is ready to accept the request and to let the client proceed. If the server cannot deal with it, it can return any other HTTP response that makes sense for it, such as [`413 Request Entity Too Large`](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.14) if it doesn’t want to handle the load, and can optionally close the connection right after the fact.

As such, between any two clients and server, the mechanism that takes place may look a bit like this for a regular call:
    
    
    [Client]                           [Server]
       |-------- Partial Request -------->|
       |<--------- 100 Continue ----------|
       |--------- Request Body ---------->|
       |<----------- Response ------------|
    

Or, for a denied request:
    
    
    [Client]                           [Server]
       |-------- Partial Request -------->|
       |<-- 413 Request Entity Too Large -|
    

The mechanism needs to be more resilient, however, because not all servers and clients can understand that mechanism. As such, if the client doesn’t know whether the server _can_ accept and honor the `Expect: 100-Continue` headers, it _should_ be sending the actual body after having waited a period of time:
    
    
    [Client]                           [Server]
       |-------- Partial Request -------->|
       |                                  |
       |                                  |
       |                                  |
       |--------- Request Body ---------->|
       |<----------- Response ------------|
    

By default, many web servers do not handle `Expect: 100-continue` as a mechanism. Therefore, the Heroku HTTP routers will automatically insert a `100 Continue` response on behalf of the application it routes to, and will later forward the data.

This more or less disables the mechanism entirely as far as the dyno’s webserver is concerned.

### Enabling 100-Continue Support

End-to-end continue support is now available through a [Heroku Labs](https://devcenter.heroku.com/articles/labs) feature:
    
    
    $ heroku labs:enable http-end-to-end-continue
    

The `http-end-to-end-continue` Heroku Labs feature is only supported for HTTP/1.1 traffic when using Router 2.0.

You can’t enable `http-end-to-end-continue` for [Fir](https://devcenter.heroku.com/articles/generations#fir)-generation apps.

If the extension is enabled, the general flow of 100-Continue feature is restored, and the router will pass on the `expect: 100-continue` headers and their associated `100 continue` responses transparently.

This feature comes with its own set of corner cases and behaviors that have to be specified, however.

### Corner Cases

There are a set of specific corner cases that may come with this kind of request.

The original HTTP 1.1 RFC ([RFC 2068](http://www.ietf.org/rfc/rfc2068.txt)) allowed use of the `100 Continue` partial response to let the server say “the entire request isn’t done parsing, but keep going, I’m not denying it right away”. Later RFCs ([RFC 2616](http://www.w3.org/Protocols/rfc2616/rfc2616-sec8.html) for example) contain the `Expect: 100-continue` mechanism, and reappropriated the `100 Continue` partial response as part of the mechanism defined in the previous section of the text.

For backwards compatibility reasons, the server could possibly send a `100 Continue` without having received the related `Expect` header, but is strongly advised against doing so.

A second corner case is that a server may decide not to send back a `100 Continue` response if it has started receiving and processing body data first hand, which the client should be aware of.

Servers also have to be careful when parsing `Expect` headers, given they _could_ contain [more than one value](http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.20). For example, `Expect: 100-continue, auth` could be sent when expecting the server to handle a large body, while asking to be authenticated before doing so. Technically, there can be as many values as desired within the `Expect` header with the behavior being defined purely for the client and the server’s sake.

Other special cases come from unexpected interactions coming from having multiple headers that manage connection flow. For example:

  * What happens if a client request contains both [a connection Upgrade request (for websockets)](https://datatracker.ietf.org/doc/html/rfc6455#page-17) _and_ an `Expect: 100-continue` header?
  * What happens if a server responds with a `100 Continue` status code, but also includes headers such as [`Connection: close` (http://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html#sec14.10), which should terminate the connection upon reception?



These behaviors are undefined by the original specifications, and the Heroku router has to make a decision regarding them in order to provide consistent behavior.

### Proxy Requirements

Even though the `Expect` header is defined to be an End-To-End header (only the client and the server would have to care about them, explaining why any term can be used in it), the `100 Continue` mechanism itself (and the general `Expect` behavior support) requires coordination with proxies and is hop-by-hop. The RFC has special conditions added for them:

  * The proxy should pass the header as-is, whether it knows if the server can handle it or not.
  * If the proxy knows that the server to which it’s routing has an HTTP version of 1.0 or lower, it must deny the request with a `417 Expectation Failed` status, but it’s possible it doesn’t know about it.
  * An HTTP 1.0 client (or earlier) could send a request without an `Expect: 100-Continue` header, and the server could still respond to it using the `100 Continue` HTTP code (as part of [RFC 2068](http://www.ietf.org/rfc/rfc2068.txt)), in which case the proxy should strip the response entirely and wait to relay the final status.



### Heroku Router 100-continue Support

The router takes some liberties regarding the undefined behaviors and corner cases mentioned earlier:

  * `100 Continue` will be stripped as a response if the client is a HTTP 1.0 (or earlier) client and the `Expect: 100-continue` header isn’t part of the request, and will be forwarded otherwise no matter what.
  * The router will _not_ require a `100 Continue` response to start sending the request body, but will leave the wait time up to the client (without breaking the regular [inactivity rules](https://devcenter.heroku.com/articles/request-timeout#long-polling-and-streaming-responses) for connections on Heroku)
  * The router will automatically respond with a `417 Expectation Failed` response and close the connection to the dyno if the `Expect` header contains any value other than `100 Continue` (case insensitive)
  * If a WebSocket upgrade is requested, it will be sent as-is to the dyno, and the router will honor whichever response comes in: a `100 Continue` status _may_ ignore the WebSocket upgrade and return any code (as usual), and a [`101 Switching Protocol`](http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.1.2) will ignore the `Expect` headers’ behavior. Note that in order to respect the [HTTP spec](http://tools.ietf.org/html/draft-ietf-httpbis-p1-messaging-25#section-6.7), the router will still look for a `101 Switching Protocol` following a `100 Continue` received from the server.
  * The router will ignore `Connection: close` on a `100 Continue` and only honor it after having received the final response. Given that the RFC specifies that the connection should be closed “after the current request/response is complete”, and that `100` is not a terminal status, the connection will be closed only after having received a terminal status. Note however, that because `Connection: close` is a hop-by-hop mechanism, the router will not necessarily close the connection to the client, and may not forward it.
  * The router will strip all headers from a `100 Continue` response, given no header is prescribed by the RFC and it makes the implementation much simpler.
  * The router will return a 5xx error code if the server returns a `100 Continue` following an initial `100 Continue` response. The router does not yet support infinite 1xx streams.
  * The router will close the connection to the server following a terminal status code, whether it was preceded by a `100 Continue` or not beforehand – connections to dynos aren’t keepalive.
  * The router will close the connection to the client following a terminal status code that was _not_ preceded by a `100 Continue` response. This will avoid having the client need to send the request body anyway before having the server being able to process the next request.



Other mechanisms should be respected as-is by the protocol, and the router should forward requests as specified by the RFC.

## HTTP Versions Supported

Four main versions of HTTP are: HTTP/0.9, HTTP/1.0, HTTP/1.1 and HTTP/2.

The legacy Heroku router only supports HTTP/1.0 and HTTP/1.1 clients. Router 2.0 supports HTTP/2. HTTP/0.9 and earlier are no longer supported. We don’t support SPDY at this time. The [Fir router](https://devcenter.heroku.com/articles/routing-in-private-spaces) supports the same versions as Router 2.0, including HTTP/2.

HTTP/1.1 and HTTP/2 are two versions of the Hypertext Transfer Protocol (HTTP) that govern how data is communicated between web servers and browsers. HTTP/2 is significantly faster than HTTP 1.1 by introducing features like multiplexing and header compression to reduce latency.

The router’s behavior is to be as compliant as possible with the HTTP/1.1 and HTTP/2 specifications. Special exceptions must be made for HTTP/1.0 however:

  * The router will advertise itself as using HTTP/1.1 no matter if the client uses HTTP/1.0 or not.
  * The router will take on itself to do the necessary conversions from a chunked response to a regular HTTP response. In order to do so without accumulating potentially gigabytes of data, the response to the client will be delimited by the termination of the connection (See [Point 4.4.5](http://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.4))
  * The router will assume that the client wants to close the connection on each request (no keepalive).
  * An HTTP/1.0 client may send a request with an explicit `connection:keep-alive` header. Despite the keepalive mechanism not being defined back in 1.0 (it was ad-hoc), the router makes the assumption that the behavior requested is similar to the HTTP/1.1 behavior at this point.



## HTTP/2 with Router 2.0

For Common Runtime apps, if you enabled Router 2.0, [HTTP/2](https://www.rfc-editor.org/rfc/rfc9113.html) is on by default. Note the following feature considerations for HTTP/2 on the Common Runtime:

  * HTTP/2 terminates at the Heroku router and we forward HTTP/1.1 from the router to your app.
  * Specifically for the Common Runtime, we support HTTP/2 on custom domains, but not on the built-in `<app-name-cff7f1443a49>.herokuapp.com` domain.
  * A valid TLS certificate is required for HTTP/2. We recommend using [Heroku Automated Certificate Management.](https://devcenter.heroku.com/articles/automated-certificate-management)



You can verify your app is receiving HTTP/2 requests by referencing the `protocol` value in your Heroku Router Logs.

To opt out of HTTP/2 but still use Router 2.0, [disable HTTP/2](https://devcenter.heroku.com/articles/heroku-labs-disabling-http-2-for-router-2-0) on your application. There’s no feature flag for [Fir](https://devcenter.heroku.com/articles/generations#fir), HTTP/2 is always available.

## HTTP Validation and Restrictions

Request validation:

  * In the case of chunked encoding and content-length both being present in the request, the router will [give precedence to chunked encoding](http://www.w3.org/Protocols/rfc2616/rfc2616-sec4.html#sec4.4).
  * If multiple content-length fields are present, and that they have the same length, they will be merged into a single content-length header
  * If a content-length header contain multiple values (`content-length: 15,24`) or a request contains multiple content-length headers with multiple values, the request will be denied with a code 400.
  * Headers are restricted to 8192 bytes per line (and 1000 bytes for the header name)
  * Hop-by-hop headers will be stripped to avoid confusion
  * At most, 1000 headers are allowed per request
  * The request line of the HTTP request is limited to 8192 bytes
  * The request line expects single spaces to separate between the verb, the path, and the HTTP version.



Response validation:

  * Hop-by-hop headers will be stripped to avoid confusion
  * Headers are restricted to 512kb per line
  * Cookies are explicitly restricted to 8192 bytes. This is to protect against common restrictions (for example, imposed by CDNs) that rarely accept larger cookie values. In such cases, a developer could accidentally set large cookies, which would be submitted back to the user, who would then see all of his or her requests denied.
  * The status line (`HTTP/1.1 200 OK`) is restricted to 8192 bytes in length



Applications that break these limits in responses will see their requests fail with a 502 Bad Gateway response, and an [H25 error](https://devcenter.heroku.com/articles/error-codes) will be injected into the application log stream. Clients that break these limits in requests will see their request fail with a 400 Bad Request response.

Additionally, while HTTP/1.1 requests and responses are expected to be `keep-alive` by default, if the initial request had an explicit `connection: close` header from the router to the dyno, the dyno _can_ send a response delimited by the connection termination, without a specific content-encoding nor an explicit content-length.

## Protocol Upgrades

Whereas the previous Heroku router restricted HTTP protocol upgrades to WebSockets only, the new router tolerates any upgrade at all.

Specific points related to the implementation:

  * Any HTTP verb can be used with an upgradable connection
  * Even though `HEAD` HTTP verbs usually do not require having a proper response sent over the line (regarding content-length, for example), `HEAD` requests are explicitly made to work with `101 Switching Protocols` responses. A dyno that doesn’t want to upgrade should send a different status code, and the connection will not be upgraded



## Not Supported

  * SPDY
  * IPv6 is unsupported in the [Cedar](https://devcenter.heroku.com/articles/generations#cedar) generation of Heroku. There is IPv6 support in [Fir](https://devcenter.heroku.com/articles/generations#fir).
  * `Expect` headers with any content other than `100-continue` (yields a 417)
  * HTTP Extensions such as WEBDAV
  * A HEAD, 1xx, 204, or 304 response with a content-length or chunked encoding doesn’t have the proxy try to relay a body that will never come
  * Header line endings other than CRLF (`\r\n`)
  * Caching of HTTP Content
  * Caching the HTTP versions of servers running on dynos
  * Long-standing preallocated idle connections. The limit is set to 1 minute before an idle connection is closed.
  * HTTP/1.0 requests without the `Host` header, even when the full URL is submitted in the request line.
  * TCP Routing



## Available Cipher Suites on the Common Runtime

### Default Domains

The ciphers supported for all default domain `(*.herokuapp.com)` traffic is as follows
    
    
    TLS_ECDHE-ECDSA-AES128-GCM-SHA256
    TLS_ECDHE-RSA-AES128-GCM-SHA256
    TLS_ECDHE-ECDSA-AES128-SHA256
    TLS_ECDHE-RSA-AES128-SHA256
    TLS_ECDHE-ECDSA-AES128-SHA
    TLS_ECDHE-RSA-AES128-SHA
    TLS_ECDHE-ECDSA-AES256-GCM-SHA384
    TLS_ECDHE-RSA-AES256-GCM-SHA384
    TLS_ECDHE-ECDSA-AES256-SHA384
    TLS_ECDHE-RSA-AES256-SHA384
    TLS_ECDHE-RSA-AES256-SHA
    TLS_ECDHE-ECDSA-AES256-SHA
    TLS_AES128-GCM-SHA256
    TLS_AES128-SHA256
    TLS_AES128-SHA
    TLS_AES256-GCM-SHA384
    TLS_AES256-SHA256
    TLS_AES256-SHA
    

### Custom Domains

The ciphers supported for all custom domain traffic is as follows
    
    
    TLS_ECDHE_ECDSA_WITH_AES_256_GCM_SHA384
    TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384
    TLS_ECDHE_ECDSA_WITH_CHACHA20_POLY1305
    TLS_ECDHE_RSA_WITH_CHACHA20_POLY1305
    TLS_ECDHE_ECDSA_WITH_AES_128_GCM_SHA256
    TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256
    TLS_RSA_WITH_AES_256_GCM_SHA384
    TLS_RSA_WITH_AES_128_GCM_SHA256
    

## Available Cipher Suites on Private Spaces

See the SSL Security section in [Routing in Private Spaces](https://devcenter.heroku.com/articles/routing-in-private-spaces#ssl-security) for a list.

## Legacy Router Deprecation and EOL

The [Common Runtime](https://devcenter.heroku.com/articles/dyno-runtime#common-runtime) legacy router is [deprecated](https://devcenter.heroku.com/changelog-items/3063). Heroku is currently migrating Common Runtime applications to the new router in small batches based on [dyno-tier](https://devcenter.heroku.com/articles/dyno-tiers). Note that only **Eco** , **Basic** , **Standard** and **Performance** tiers are available in the Common Runtime.

As of early April 2025, all Eco-tier applications route through Router 2.0 automatically. As of July 2025, all Basic-tier applications also route through Router 2.0 automatically. This includes existing and newly created Eco- and Basic-tier applications. For a complete migration schedule please see the [Legacy Router End-of-Life FAQ](https://help.heroku.com/JJ3M1TOM/common-runtime-legacy-router-end-of-life-faq).

As of [early July 2025](https://devcenter.heroku.com/changelog-items/3296), all newly created applications in the Common Runtime use Router 2.0 by default. You can still disable Router 2.0 on non-Eco, non-Basic apps.

Private Spaces, including both the Cedar and the Fir [generations](https://devcenter.heroku.com/articles/generations), already run a [modern router](https://devcenter.heroku.com/articles/routing-in-private-spaces), similar to Router 2.0. Applications on Private Spaces are exempt from the router migration.

###  Keep reading

  * [Networking & DNS](/categories/networking-dns)



###  Feedback 

[Log in to submit feedback.](/login?back_to=%2Farticles%2Fhttp-routing&utm_campaign=login&utm_medium=feedback&utm_source=web)
