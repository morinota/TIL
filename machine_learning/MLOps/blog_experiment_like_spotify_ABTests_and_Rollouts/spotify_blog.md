## link

https://confidence.spotify.com/blog/ab-tests-and-rollouts

# Experiment like Spotify: A/B Tests and Rollouts

This post is part of a series that showcases how you can use Confidence. Make sure to check out our earlier post Experiment like Spotify: With Confidence.

At Spotify, we've been exercising our experimentation muscle for more than 10 years. We now have over 300 teams running tens of thousands of experiments annually. Experimentation is integral to the way we develop the Spotify experience — but it's a lot more than just running A/B tests to find the winning ideas. This post talks about A/B tests and rollouts, how they're used at Spotify, and how you can use them in Confidence.

## The dual purpose of experimentation

The workhorse of experimentation is the A/B test, which lets you test your new ideas with users. You randomly give the new experience to one set of users, while another set of users gets the current experience. The A/B test evaluates how these users react after they've been subjected to one of the experiences. You compare the groups with a test metric, like minutes of music played in the Spotify case. You conclude whether your new idea was a hit based on this experiment.

The A/B test fits into the larger product development narrative of think it, build it, ship it, tweak it. With A/B tests, we come up with new ideas, both big and small, and build simpler versions of them that we test with users. Based on feedback, we tweak and repeat continuously to improve the product.

A/B testing and online experimentation is often narrowly described from this perspective only — as a tool for evaluating new, untested ideas. In practice, the product development phase that uses A/B tests to validate good ideas is more of an inner loop within a larger, outer loop. In fact, at Spotify, experimentation serves an equally important second purpose: it's the way we release changes to our users.

## Ship changes safely with rollouts

After you've found the winning variant and verified that it's a success with users, you still need to release it. Your earlier tests indicate a success — but the unknown unknowns of releasing your new experience to everyone can make users react in unexpected ways. For example, maybe your systems aren't able to handle the increased load when releasing the new experience fully, which you failed to detect in your earlier tests on only a subset of users.

Luckily, there's no need to be in the dark when you're rolling out the experience. With rollouts in Confidence, you can be in full control of what percentage of your users receive the new experience — all while you're monitoring the impact on the metrics you care about. Concerned that there's a risk your new experience could increase the share of users that have their app crash? Just add it as a metric to understand how it evolves as you gradually increase the proportion of users that get the new experience. All the while Confidence summarizes the results for you, recommending what to do next.

## Differences between A/B tests and rollouts

Just like an A/B test, a rollout is an experiment that randomizes users into a control or a treatment group. In contrast to an A/B test, a rollout has an adjustable reach — a percentage that determines what share of users should receive the new treatment. You can adjust the level of reach up and down when the rollout is live.

While an A/B test is a product development tool that sets out to find evidence that a new idea is successful, the rollout is about releasing changes safely. For this reason, an A/B test has a fixed allocation that you can't change, while the flexible allocation of the rollout is its main perk. A/B tests track both success and guardrail metrics, whereas rollouts only use guardrail metrics. The table below shows the main differences between A/B tests and rollouts in Confidence.

## Rollouts are the appetizers of experimentation

At Spotify, we've seen an incredible increase in the use of rollouts. If you've been working on building your experimentation culture, you know it's a challenging job — not everyone is as bought in to evaluating all their ideas with A/B tests as you are. Rollouts are different, though, and releasing changes safely and gradually while monitoring metrics resonates with almost everyone. A lot of teams at Spotify have begun their experimentation journey with rollouts and have later, after having gotten a taste of data-informed decision making, moved on to more traditional A/B testing. The ratio of new rollouts to new A/B tests continues to grow at Spotify, and has shown a steady increase throughout 2023:

## Experiment on your own terms with Confidence

Don't agree with how we define and separate A/B tests and rollouts? Maybe you want to use success metrics in rollouts, or make the total allocation of A/B tests adjustable for a live test. One of the best aspects of Confidence is that you set your own practices and that you're not forced to experiment like we do. With the custom workflows that Confidence offers, you can define your own experiment designs. Use our implementation of A/B tests and rollouts as a starting point, and adjust them so they fit your needs. No one knows better what works for you than you. Confidence lets you run high-quality experiments on your own terms.

## What's next

This post is part of a series that showcases how you can use Confidence. Make sure to check out our earlier post Experiment like Spotify: With Confidence. Coming up in the series are posts on flags, analysis of experiments, metrics, workflows, and more.

Confidence is currently available in private beta. If you haven't signed up already, sign up today and we'll be in touch.
