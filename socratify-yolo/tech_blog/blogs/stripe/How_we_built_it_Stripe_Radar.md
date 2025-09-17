---
title: "How we built it: Stripe Radar"
company: "stripe"
url: "https://stripe.com/blog/how-we-built-it-stripe-radar"
system_score: 45
date: "2025-09-15"
---

#  [How we built it: Stripe Radar](/blog/how-we-built-it-stripe-radar)

[March 29, 2023](/blog/how-we-built-it-stripe-radar)

[ ![](https://images.stripeassets.com/fzn2n1nzq965/4X6Q16Ed2wFvW6qyH7EFjd/07951e12397dcf52cec1d4fa4f160084/drapeau.jpg.png?w=96&h=96) ](https://www.linkedin.com/in/rdrapeau/) [Ryan Drapeau](https://www.linkedin.com/in/rdrapeau/) Payment Intelligence

As an engineer on Stripe’s fraud prevention team, I obsess about a single moment that lasts just a fraction of a second. It begins when someone clicks “purchase,” and it ends when their transaction is confirmed.

In that brief interval, [Stripe Radar](https://stripe.com/radar) goes to work. Radar is Stripe’s fraud prevention solution. It assesses more than 1,000 characteristics of a potential transaction in order to determine the likelihood that it’s fraudulent, letting good transactions through and either blocking risky transactions or diverting them to additional security checks. It makes this decision, accurately, in less than 100 milliseconds. Out of the billions of legitimate payments made on Stripe, Radar incorrectly blocks just 0.1%.

Online payment fraud is a hard problem to solve. Any effective tool needs to be accurate, fast, and inexpensive to run for each transaction. It needs to balance blocking bad transactions against false positives (good payments that are blocked), which hurt consumers and our users’ bottom lines. The challenge is compounded by the fact that fraud is rare—on the order of 1 out of every 1,000 payments. 

To identify fraudulent transactions, we rely on the breadth of the Stripe network—our biggest strength. We’ve done so by improving our machine learning (ML) architecture while enhancing the way we communicate with users about the reasons behind fraud decisions. In this post, we want to share what makes Radar so powerful and take you through some of the key decisions we’ve made—and lessons we’ve learned—over the almost seven years we’ve been building it.

## Lesson 1: Don’t get too comfortable with your ML architecture

We started with relatively simple ML models (e.g., logistic regression) and over time have advanced to more complex ones (e.g., deep neural networks), as the Stripe network has grown and ML technology has advanced. With each architectural jump, we have observed an equivalent leap-size improvement in model performance. 

Our most recent architecture evolution occurred in mid-2022 when we migrated from an ensemble “[Wide & Deep model](https://arxiv.org/abs/1606.07792),” composed of an [XGBoost model](https://xgboost.readthedocs.io/en/stable/) and a deep neural network (DNN), to a pure DNN-only model. The result was a model that trains faster, scales better, and is more adaptable to the most cutting-edge ML techniques. 

![Before and after combined](
        
          https://images.stripeassets.com/fzn2n1nzq965/3nriytLBMkQHRV0KlMVluQ/8f7e5b138024b3136d0d60fca7e4f3cb/Before_After_-_combined_FA_3_17.png?w=1620&q=80
        
      )

The previous architecture combined the power of memorization (the wide part, powered by XGBoost) with generalization (the deep part, powered by a DNN). It worked well, but limited the rate at which we could improve. XGBoost was incompatible at scale with more advanced ML techniques we wanted to take advantage of (e.g., transfer learning, embeddings, long training times) and also slowed the rate at which we could retrain the model because an XGBoost model is not very parallelizable—which inhibited the experimentation velocity of the many engineers who worked on the model each day.

We could have just removed the XGBoost component, but that would have caused a 1.5% drop in [recall](https://en.wikipedia.org/wiki/Precision_and_recall)—an unacceptably large regression in performance. While XGBoost is not a deep-learning method or a cutting-edge technique these days, it still provided unique value to our model’s performance. To replace it, we looked for ways to build a DNN-only architecture that added the memorization power we’d been getting from XGBoost, without compromising the DNN’s ability to generalize.

A straightforward way of improving both memorization and generalization is to increase the DNN’s size—both its depth and width. However, achieving a more-performant model wasn’t as easy as that.

Increasing the model’s size immediately improved the representational capacity of the model to learn features at both the abstract level (e.g., payment velocity and “unusual volume on a card”) and the fine-grained level (e.g., correlations between features). However, increasing depth too much ran the risk of overfitting, causing the model to memorize random noise in the features. So, in order to build a DNN-only architecture, we had to find the sweet spot that maximized a representational capacity to learn various levels while remaining resistant to overfitting.

We decided to read up on [popular publications](https://arxiv.org/pdf/1611.05431.pdf) about DNN architecture and adopted a multi-branch DNN-only architecture inspired by ResNeXt. ResNeXt’s architecture adopts a “Network-in-Neuron” strategy. It splits a computation into distinct threads, or branches, where a branch can be thought of as a small network. The outputs from the branches are then summed to produce a final output. Aggregating branches has the benefit of enriching the learned features by expanding a new dimension of feature representation. It does this in a way that is more effective than the brute-force approach of merely increasing depth or width to improve accuracy.

By removing the XGBoost component of the architecture, we reduced the time to train our model by over 85% (to less than two hours). Experiments that previously required running jobs late into the night could now be completed multiple times in a single working day, a massive shift in our ability to prototype new ideas. The improvements were a good reminder to not get too comfortable with the way we were currently doing ML and to ask ourselves: If we were starting over today, what kind of model would we build?

Asking those questions is allowing us to take on even more ambitious initiatives for our next year of work. These include incorporating more advanced ML techniques like transfer learning, embeddings, and multi-task learning, all of which we are actively exploring in 2023.

## Lesson 2: Never stop searching for new ML features

In addition to evolving our model architectures, we also want to ensure our models are incorporating the richest signals. By carefully noting the common behaviors of fraud attempts, Radar has been able to compile a deep understanding of fraudulent activity and trends. This gives Radar an important advantage when put to work: Each increase in the size of Radar’s training data set creates outsized improvements in model quality, which wasn’t the case with XGBoost.

One of the biggest levers we have to make model improvements is through feature engineering. Some features could likely have an outsized impact on model performance, but first we need to identify and implement them. To do this effectively, we’ve created several processes to enable ML engineers. 

We review past fraud attacks in exacting detail, building investigation reports that attempt to get into the minds of the fraudulent actors. We look for signals in the payments, like a common pattern for throwaway emails (e.g., 123test@cactuspractice.com) that might be used by fraudulent actors to quickly set up multiple accounts. We then broaden our search across the Stripe network to look for correlations in timing and signals that could connect to previous fraud attacks. Every week, the Radar team also meets to discuss new fraud trends that emerge from research into activity on the dark web.

We gather all of this information and ideate features that target the specific contours of each attack. We come up with a prioritized list, quickly implement each feature, then prototype each one to understand the impact on our model’s performance. 

Sometimes we strike gold. Other times, even our most promising features don’t pan out. This happened once when we introduced a Boolean feature capturing whether the business was currently under a distributed fraud attack. This feature didn’t improve our model’s performance as much as we’d anticipated. As it turned out, our ML was already incorporating these patterns, even though we never expected it to. This reflects the fact that the current version of Radar is built on top of years of work by many generations of engineers.

Besides developing new features, another method we explore for increasing model performance is increasing the size of our training data. With the success of ML models like ChatGPT, and large language models generally, we wanted to see if we could achieve a similar feat with Radar: Could we start with a relatively simple DNN-only architecture and get large improvements in model performance just by increasing the amount of training data?

The primary impediment to doing this was that the time to train increases linearly with the size of the training data. But thanks to the training-speed improvements we made when we switched to a DNN-only architecture, this was less of an issue. 

We ran some experiments using more transaction data and got encouraging results: We made a 10x increase in training transaction data and still found significant model improvements. We’re currently working on a 100x version to generalize the results even further.

![Increases in performance from more training data](
        
          https://images.stripeassets.com/fzn2n1nzq965/ErE2KdKCedramcReJVjIz/b7ed4cd076f84b6792e9e43df8987034/Training_data_chart_FA_3_17.png?w=1620&q=80
        
      )

In a future post, we will dive deeper into new techniques we’re exploring to further use the power of the Stripe network and our ability to apply these insights to fight fraud, even after a payment has already occurred.

## Lesson 3: Explanation matters as much as detection

Building a great fraud-detection product is about more than just identifying fraud. There’s a large personal dimension to it, too. When a good transaction is flagged—or a fraudulent one gets through—our users want to know why, because false positives hurt their bottom line and frustrate their customers. Explaining fraud decisions is an area in which we’ve made a lot of investments in recent years.

And it’s a challenge. All ML models are black boxes to an extent, and deep neural networks even more so than other types of models. It’s hard to explain to users why Radar scores transactions the way it does. This is another tradeoff we came to accept when deciding to use DNNs over simpler, more traditional ML techniques. But our engineers know the system well and have developed a range of ways to help users understand what’s going on.

In 2020 we built our [risk insights](https://stripe.com/docs/radar/reviews/risk-insights) feature, which lets users see which features of a transaction contributed to a transaction being declined. These can include whether the cardholder’s name matches the provided email and the number of cards previously associated with an IP address. A high number of cards may indicate suspicious behavior, such as a bad actor trying out multiple stolen credit cards. However, there may also be legitimate reasons for this, and our model evaluates this feature in the context of all our signals, understanding the correlations that may exist between them to accurately distinguish between fraudulent and good payments.

Recent improvements to risk insights include displaying maps to users with the locations of purchase and shipping addresses and using Elasticsearch to quickly share related transactions, which further helps users put a specific decline in context.

![Risk insights image](
        
          https://images.stripeassets.com/fzn2n1nzq965/28qBjVgZ1bEjES9fErK6iQ/622ef63e2a1ab6bac615545e2f4ac501/IMG_0058.png?w=1620&q=80
        
      )

In addition to providing users with insight into fraud decisions, we have been working on more sophisticated techniques for gaining deeper understanding of our ML model. This tooling includes a simple table view that displays the exact features that contributed the most to raising and lowering a transaction’s fraud score. Our engineers are actively using these solutions internally to debug support cases, and we are working on plans for sharing these insights with our users as well.

Explaining Radar’s ML outcomes as clearly as possible helps users understand the relative risk of a given payment, which fraud signals may have contributed to that risk score, and how a given payment compares to others. They can then take actions to [improve the quality of data](https://stripe.com/docs/radar/integration) they are sending (in order to generate more accurate fraud decisions) or create [custom allow or block rules](https://stripe.com/docs/radar/rules) to tailor Radar for their specific business needs.

## Evolving strategies, constant focus

Radar is a very different product than it was when we started. We’ve overhauled the models we use, the way we employ transaction data from the Stripe network, and the way we interact with users. Over that same period fraud patterns have changed considerably, too, from primarily stolen credit card fraud to a growing mix of traditional card fraud and high-velocity [card testing attacks](https://stripe.com/docs/disputes/prevention/card-testing) today.

But in the ways that matter most, the goals of the Radar team are the same. We’re still working to create an environment in which businesses and customers can transact with confidence, and we’re still focused on optimizing that brief moment we hope customers don’t even notice: the last step in a checkout, the split second we have to detect fraud before a transaction is confirmed.

We’re excited to continue innovating on ML to solve hard, important problems. If you are, too, consider [joining our engineering team](https://stripe.com/jobs/search?query=engineer). 
