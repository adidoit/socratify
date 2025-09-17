---
title: "How we built the GitHub globe"
company: "github"
url: "https://github.blog/2020-12-21-how-we-built-the-github-globe/"
type: "direct_systems_collection"
date: "2025-09-15"
---

[Home](https://github.blog/) / [Engineering](https://github.blog/engineering/) / [Engineering principles](https://github.blog/engineering/engineering-principles/)

# How we built the GitHub globe

GitHub is where the world builds software. More than 56 million developers around the world build and work together on GitHub. With our new homepage, we wanted to show how…

![](https://github.blog/wp-content/uploads/2020/12/102393310-07478b80-3f8d-11eb-84eb-392d555ebd29.png?resize=1200%2C630)

[Tobias Ahlin](https://github.blog/author/tobiasahlin/ "Posts by Tobias Ahlin")·[@tobiasahlin](https://github.com/tobiasahlin)

December 21, 2020  | Updated February 11, 2021 

| 10 minutes 

  * Share: 
  * [ ](https://x.com/share?text=How%20we%20built%20the%20GitHub%20globe&url=https%3A%2F%2Fgithub.blog%2Fengineering%2Fengineering-principles%2Fhow-we-built-the-github-globe%2F)
  * [ ](https://www.facebook.com/sharer/sharer.php?t=How%20we%20built%20the%20GitHub%20globe&u=https%3A%2F%2Fgithub.blog%2Fengineering%2Fengineering-principles%2Fhow-we-built-the-github-globe%2F)
  * [ ](https://www.linkedin.com/shareArticle?title=How%20we%20built%20the%20GitHub%20globe&url=https%3A%2F%2Fgithub.blog%2Fengineering%2Fengineering-principles%2Fhow-we-built-the-github-globe%2F)



GitHub is where the world builds software. More than 56 million developers around the world build and work together on GitHub. With our new [homepage](https://github.com/home), we wanted to **show** how open source development transcends the borders we’re living in and to tell our product story through the lens of a developer’s journey.

Now that it’s live, we would love to share how we built the homepage-directly from the voices of our designers and developers. In this five-part series, we’ll discuss:

  1. [How our globe is built](https://github.blog/2020-12-21-how-we-built-the-github-globe/)
  2. [How we collect and use the data behind the globe](https://github.blog/2020-12-21-visualizing-githubs-global-community/)
  3. [How we made the page fast and performant](https://github.blog/2021-01-29-making-githubs-new-homepage-fast-and-performant/)
  4. [How we illustrate at GitHub](https://github.blog/2021-02-04-how-we-illustrate-at-github/)
  5. [How we designed the homepage and wrote the narrative](https://github.blog/2021-02-11-how-we-designed-and-wrote-the-narrative-for-our-homepage/)



![](https://github.blog/wp-content/uploads/2020/12/102573836-33a1fb80-40a4-11eb-8c77-e2d328f0a570.gif?resize=640%2C400)

At Satellite in 2019, our CEO [Nat](https://twitter.com/natfriedman) showed off [a visualization of open source activity](https://youtu.be/sGC2rwOiaWc?t=109) on GitHub over a 30-day span. The sheer volume and global reach was astonishing, and we knew we wanted to build on that story.

<https://github.blog/wp-content/uploads/2020/12/globe-longer.mp4#t=0.001>

[__](https://drive.google.com/file/d/1vWoKSkebo9HSPO8Vp8de8xC522t0uLxK/view?usp=sharing)The main goals we set out to achieve in the design and development of the globe were:

  * **An interconnected community**. We explored many different options, but ultimately landed on pull requests. It turned out to be a beautiful visualization of pull requests being opened in one part of the world and closed in another.
  * **A showcase of real work happening now**. We started by simply showing the pull requests’ arcs and spires, but quickly realized that we needed “proof of life.” The arcs could quite as easily just be design animations instead of real work. We iterated on ways to provide more detail and found most resonance with clear hover states that showed the pull request, repo, timestamp, language, and locations. Nat had the idea of making each line clickable, which really upleveled the experience and made it much more immersive. [Read more here](https://github.blog/2020-12-21-visualizing-githubs-global-community/).
  * **Attention to detail and performance.** It was extremely important to us that the globe not only looked inspiring and beautiful, but that it performed well on all devices. We went through many, many iterations of refinement, and there’s still more work to be done.



## Rendering the globe with WebGL

At the most fundamental level, the globe runs in a WebGL context powered by [three.js](https://github.com/mrdoob/three.js/). We feed it data of recent pull requests that have been created and merged around the world through a JSON file. The scene is made up of five layers: a halo, a globe, the Earth’s regions, blue spikes for open pull requests, and pink arcs for merged pull requests. We don’t use any textures: we point four lights at a sphere, use about 12,000 five-sided [circles](https://threejs.org/docs/#api/en/geometries/CircleBufferGeometry) to render the Earth’s regions, and draw a halo with a simple custom shader on the backside of a sphere.

![](https://github.blog/wp-content/uploads/2020/12/layers-loop.h264.2020-12-21-11_16_56.gif?resize=640%2C409)

To draw the Earth’s regions, we start by defining the desired density of circles (this will vary depending on the performance of your machine—more on that later), and loop through longitudes and latitudes in a nested for-loop. We start at the south pole and go upwards, calculate the circumference for each latitude, and distribute circles evenly along that line, wrapping around the sphere:
    
    
    for (let lat = -90; lat <= 90; lat += 180/rows) {
      const radius = Math.cos(Math.abs(lat) * DEG2RAD) * GLOBE_RADIUS;
      const circumference = radius * Math.PI * 2;
      const dotsForLat = circumference * dotDensity;
      for (let x = 0; x < dotsForLat; x++) {
        const long = -180 + x*360/dotsForLat;
        if (!this.visibilityForCoordinate(long, lat)) continue;
    
        // Setup and save circle matrix data
      }
    }
    

To determine if a circle should be visible or not (is it water or land?) we load a small PNG containing a map of the world, parse its image data through canvas’s [context.getImageData()](https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/getImageData), and map each circle to a pixel on the map through the visibilityForCoordinate(long, lat) method. If that pixel’s alpha is at least 90 (out of 255), we draw the circle; if not, we skip to the next one.

After collecting all the data we need to visualize the Earth’s regions through these small circles, we create an instance of [CircleBufferGeometry](https://threejs.org/docs/#api/en/geometries/CircleBufferGeometry) and use an [InstancedMesh](https://threejs.org/docs/#api/en/objects/InstancedMesh) to render all the geometry.

### Making sure that you can see your own location

As you enter the new GitHub homepage, we want to make sure that you can see your own location as the globe appears, which means that we need to figure where on Earth that you are. We wanted to achieve this effect without delaying the first render behind an IP look-up, so we set the globe’s starting angle to center over Greenwich, look at [your device’s timezone offset](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/getTimezoneOffset), and convert that offset to a rotation around the globe’s own axis (in radians):
    
    
    const date = new Date();
    const timeZoneOffset = date.getTimezoneOffset() || 0;
    const timeZoneMaxOffset = 60*12;
    rotationOffset.y = ROTATION_OFFSET.y + Math.PI * (timeZoneOffset / timeZoneMaxOffset);

It’s not an _exact_ measurement of your location, but it’s quick, and does the job.

### Visualizing pull requests

The main act of the globe is, of course, visualizing all of the pull requests that are being opened and merged around the world. The data engineering that makes this possible is a different topic in and of itself, and we’ll be sharing how we make that happen in an [upcoming post](https://github.blog/2020-12-21-visualizing-githubs-global-community/). Here we want to give you an overview of how we’re visualizing all your pull requests.

<https://github.blog/wp-content/uploads/2020/12/zoomed-in-arcs.h264.mp4#t=0.001>

Let’s focus on pull requests being merged (the pink arcs), as they are a bit more interesting. Every merged pull request entry comes with two locations: where it was opened, and where it was merged. We map these locations to our globe, and draw a bezier curve between these two locations:
    
    
    const curve = new CubicBezierCurve3(startLocation, ctrl1, ctrl2, endLocation);

We have three different orbits for these curves, and the longer the two points are apart, the further out we’ll pull out any specific arc into space. We then use instances of [TubeBufferGeometry](https://threejs.org/docs/#api/en/geometries/TubeBufferGeometry) to generate geometry along these paths, so that we can use [setDrawRange()](https://threejs.org/docs/#api/en/core/BufferGeometry.setDrawRange) to animate the lines as they appear and disappear.

As each line animates in and reaches its merge location, we generate and animate in one solid [circle](https://threejs.org/docs/#api/en/geometries/CircleBufferGeometry) that stays put while the line is present, and one [ring](https://threejs.org/docs/#api/en/geometries/RingBufferGeometry) that scales up and immediately fades out. The ease out easings for these animations are created by multiplying a speed (here 0.06) with the difference between the target (1) and the current value (animated.dot.scale.x), and adding that to the existing scale value. In other words, for every frame we step 6% closer to the target, and as we’re coming closer to that target, the animation will naturally slow down.
    
    
    // The solid circle
    const scale = animated.dot.scale.x + (1 - animated.dot.scale.x) * 0.06;
    animated.dot.scale.set(scale, scale, 1);
    
    // The landing effect that fades out
    const scaleUpFade = animated.dotFade.scale.x + (1 - animated.dotFade.scale.x) * 0.06;
    animated.dotFade.scale.set(scaleUpFade, scaleUpFade, 1);
    animated.dotFade.material.opacity = 1 - scaleUpFade;

### Creative constraints from performance optimizations

The homepage and the globe needs to perform well on a variety of devices and platforms, which early on created some creative restrictions for us, and made us focus extensively on creating a well-optimized page. Although some modern computers and tablets could render the globe at 60 FPS with antialias turned on, that’s not the case for all devices, and we decided early on to leave antialias turned off and optimize for performance. This left us with a sharp and pixelated line running along the top left edge of the globe, as the globe’s highlighted edge met the darker color of the background:

![](https://github.blog/wp-content/uploads/2020/12/102573561-8e872300-40a3-11eb-9feb-b480aeae0564.png?resize=1024%2C513)

This encouraged us to explore a halo effect that could hide that pixelated edge. We created one by using a custom shader to draw a gradient on the backside of a sphere that’s slightly larger than the globe, placed it behind the globe, and tilted it slightly on its side to emphasize the effect in the top left corner:
    
    
    const halo = new Mesh(haloGeometry, haloMaterial);
    halo.scale.multiplyScalar(1.15);
    halo.rotateX(Math.PI*0.03);
    halo.rotateY(Math.PI*0.03);
    this.haloContainer.add(halo);
    

![](https://github.blog/wp-content/uploads/2020/12/2-2.png?resize=1024%2C613)

This smoothed out the sharp edge, while being a much more performant operation than turning on antialias. Unfortunately, leaving antialias off also produced a fairly prominent [moiré effect](https://en.wikipedia.org/wiki/Moir%C3%A9_pattern) as all the circles making up the world came closer and closer to each other as they neared the edges of the globe. We reduced this effect and simulated the look of a thicker atmosphere by using a [fragment shader](https://en.wikipedia.org/wiki/Shader#Pixel_shaders) for the circles where each circle’s alpha is a function of its distance from the camera, fading out every individual circle as it moves further away:
    
    
    if (gl_FragCoord.z > fadeThreshold) {
      gl_FragColor.a = 1.0 + (fadeThreshold - gl_FragCoord.z ) * alphaFallOff;
    }
    

### Improving perceived speed

We don’t know how quickly (or slowly) the globe is going to load on a particular device, but we wanted to make sure that the header composition on the homepage is always balanced, and that you got the impression that the globe loads quickly even if there’s a slight delay before we can render the first frame.

We created a bare version of the globe using only gradients in [Figma](http://figma.com/) and exported it as an SVG. Embedding this SVG in the HTML document adds little overhead, but makes sure that _something_ is immediately visible as the page loads. As soon as we’re ready to render the first frame of the globe, we transition between the SVG and the canvas element by crossfading between and scaling up both elements using the [Web Animations API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API). Using the Web Animations API enables us to not touch the DOM at all during the transition, ensuring that it’s as stutter-free as possible.
    
    
    const keyframesIn = [
          { opacity: 0, transform: 'scale(0.8)' },
          { opacity: 1, transform: 'scale(1)' }
        ];
    const keyframesOut = [
          { opacity: 1, transform: 'scale(0.8)' },
          { opacity: 0, transform: 'scale(1)' }
        ];
    const options = { fill: 'both', duration: 600, easing: 'ease' };
    
    this.renderer.domElement.animate(keyframesIn, options);
    const placeHolderAnim = placeholder.animate(keyframesOut, options);
    placeHolderAnim.addEventListener('finish', () => {
      placeholder.remove();
    });
    

### Graceful degradation with quality tiers

We aim at maintaining 60 FPS while rendering an as beautiful globe as we can, but finding that balance is tricky—there are thousands of devices out there, all performing differently depending on the browser they’re running and their mood. We constantly monitor the achieved FPS, and if we fail to maintain 55.5 FPS over the last 50 frames we start to degrade the quality of the scene.

<https://github.blog/wp-content/uploads/2020/12/graceful-degredation.h264.mp4#t=0.001>

There are four quality tiers, and for every degradation we reduce the amount of expensive calculations. This includes reducing the pixel density, how often we raycast (figure out what your cursor is hovering in the scene), and the amount of geometry that’s drawn on screen—which brings us back to the circles that make up the Earth’s regions. As we traverse down the quality tiers, we reduce the desired circle density and rebuild the Earth’s regions, here going from the original ~12 000 circles to ~8 000:
    
    
    // Reduce pixel density to 1.5 (down from 2.0)
    this.renderer.setPixelRatio(Math.min(AppProps.pixelRatio, 1.5));
    // Reduce the amount of PRs visualized at any given time
    this.indexIncrementSpeed = VISIBLE_INCREMENT_SPEED / 3 * 2;
    // Raycast less often (wait for 4 additional frames)
    this.raycastTrigger = RAYCAST_TRIGGER + 4;
    // Draw less geometry for the Earth’s regions
    this.worldDotDensity = WORLD_DOT_DENSITY * 0.65;
    // Remove the world
    this.resetWorldMap();
    // Generate world anew from new settings
    this.buildWorldGeometry();
    

## A small part of a wide-ranging effort

These are some of the techniques that we use to render the globe, but the creation of the globe and the new homepage is part of a longer story, spanning multiple teams, disciplines, and departments, including design, brand, engineering, product, and communications. We’ll continue the deep-dive in this 5-part series, so come back soon or follow us on Twitter [@GitHub](https://twitter.com/github) for all the latest updates on this project and more.

**Next up:** [how we collect and use the data behind the globe](https://github.blog/2020-12-21-visualizing-githubs-global-community/).

In the meantime, don’t miss out on the new GitHub globe wallpapers from the GitHub Illustration Team to enjoy the globe from your desktop or mobile device:

  * [4K UHD 16:9 Footer](https://github.blog/wp-content/uploads/2020/12/wallpaper_footer_4KUHD_16_9.png)
  * [4K Ultrawide 21:9 Footer](https://github.blog/wp-content/uploads/2020/12/wallpaper_footer_4Kultra_wide_21_9.png)
  * [4K Superwide 32:9 Footer](https://github.blog/wp-content/uploads/2020/12/wallpaper_footer_4Ksuper_wide_32_9.png)
  * [4K Superwide 32:9 Header](https://github.blog/wp-content/uploads/2020/12/wallpaper_header_4Ksuper_wide_32_9.png)
  * [4k UHD 16:9 Header](https://github.blog/wp-content/uploads/2020/12/wallpaper_header_4KUHD_16_9.png)
  * [4K Ultrawide 21:9 Header](https://github.blog/wp-content/uploads/2020/12/wallpaper_header_4Kultra_wide_21_9.png)



* * *

_Love the new GitHub homepage or any of the work you see here?__[Join our team](https://github.com/about/careers)! _

* * *

## Tags:

  * [ homepage design ](https://github.blog/tag/homepage-design/)



##  Written by 

![Tobias Ahlin](https://avatars3.githubusercontent.com/u/211284?v=4&s=200)

###  [Tobias Ahlin](https://github.blog/author/tobiasahlin/)

[@tobiasahlin](https://github.com/tobiasahlin)

  * [ homepage design ](https://github.blog/tag/homepage-design/)



## More on [homepage design](https://github.blog/tag/homepage-design/)

### [How we designed and wrote the narrative for our homepage](https://github.blog/news-insights/company-news/how-we-designed-and-wrote-the-narrative-for-our-homepage/)

This post is the fifth installment of our five-part series on building GitHub’s new homepage: How our globe is built How we collect and use the data behind the globe…

[Amanda Swan](https://github.blog/author/amandaswan/ "Posts by Amanda Swan")

### [How we illustrate at GitHub](https://github.blog/engineering/user-experience/how-we-illustrate-at-github/)

In the fourth installment of our five-part series on building GitHub’s new homepage, we’ll explore the artistic pipeline at GitHub to explain story, character and color, and to show how…

[Tony Jaramillo](https://github.blog/author/tonyjaramillo/ "Posts by Tony Jaramillo")

##  Related posts 

![](https://github.blog/wp-content/uploads/2025/05/github-generic-wallpaper-rubber-duck-invertocat.png?resize=400%2C212)

[Engineering](https://github.blog/engineering/)

###  [ How GitHub engineers tackle platform problems ](https://github.blog/engineering/infrastructure/how-github-engineers-tackle-platform-problems/)

Our best practices for quickly identifying, resolving, and preventing issues at scale.

[Fabian Aguilar Gomez](https://github.blog/author/tsusdere/ "Posts by Fabian Aguilar Gomez")

![](https://github.blog/wp-content/uploads/2025/05/github-generic-wallpaper-rubber-duck-invertocat.png?resize=400%2C212)

[Application development](https://github.blog/developer-skills/application-development/)

###  [ GitHub Issues search now supports nested queries and boolean operators: Here’s how we (re)built it ](https://github.blog/developer-skills/application-development/github-issues-search-now-supports-nested-queries-and-boolean-operators-heres-how-we-rebuilt-it/)

Plus, considerations in updating one of GitHub’s oldest and most heavily used features.

[Deborah Digges](https://github.blog/author/deborahdigges/ "Posts by Deborah Digges")

![Some abstract blue shapes contoured with a few git-lines behind text that reads, Design system annotations, part 2, Advanced methods of annotating components.](https://github.blog/wp-content/uploads/2025/05/Design-System-Annotations-Part-2.jpg?resize=400%2C212)

[Engineering](https://github.blog/engineering/)

###  [ Design system annotations, part 2: Advanced methods of annotating components ](https://github.blog/engineering/user-experience/design-system-annotations-part-2-advanced-methods-of-annotating-components/)

How to build custom annotations for your design system components or use Figma’s Code Connect to help capture important accessibility details before development.

[Jan Maarten](https://github.blog/author/janmaartena11y/ "Posts by Jan Maarten")

##  Explore more from GitHub 

![Docs](https://github.blog/wp-content/uploads/2024/07/Icon-Circle.svg)

###  Docs 

Everything you need to master GitHub, all in one place.

[ Go to Docs  ](https://docs.github.com/)

![GitHub](https://github.blog/wp-content/uploads/2024/07/Icon_95220f.svg)

###  GitHub 

Build what’s next on GitHub, the place for anyone from anywhere to build anything.

[ Start building  ](https://github.com/)

![Customer stories](https://github.blog/wp-content/uploads/2024/07/Icon_da43dc.svg)

###  Customer stories 

Meet the companies and engineering teams that build with GitHub.

[ Learn more  ](https://github.com/customer-stories)

![GitHub Universe 2025](https://github.blog/wp-content/uploads/2024/04/Universe24-North_Star.svg)

###  GitHub Universe 2025 

Last chance: Save $700 on your IRL pass to Universe and join us on Oct. 28-29 in San Francisco.

[ Register now  ](https://githubuniverse.com/?utm_source=Blog&utm_medium=GitHub&utm_campaign=module)

## We do newsletters, too

Discover tips, technical guides, and best practices in our biweekly newsletter just for devs.

Your email address

* Your email address

Subscribe

Yes please, I’d like GitHub and affiliates to use my information for personalized communications, targeted advertising and campaign effectiveness. See the [GitHub Privacy Statement](https://github.com/site/privacy) for more details. 

Subscribe
