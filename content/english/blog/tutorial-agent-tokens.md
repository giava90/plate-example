---
title: "More Thinking Made It Worse: Measuring Cost and Accuracy Across Five Claude Configurations"
meta_title: "Agent Token Economics"
description: "I turned my own review paper into a citation-grounding benchmark and ran five model configurations against it. The cheapest Opus setting was also the most accurate."
date: 2026-09-28T15:19:00Z
image: "images/token-cost-quality.svg"
authors: ["Giacomo Vaccario"]
tags:
- "Generative AI"
- "LLM"
- "Agentic AI"
- "Benchmarking"
- "Data science"
- "Automation"
draft: false
---

Advice about agent costs is everywhere and almost none of it carries a number. Cache your prompts. Use a smaller model for the easy work. Let the big model think harder when the task is hard. All of that is roughly right, and none of it tells you whether it holds on *your* workload.

So I built something where every number is measurable, spent nine dollars, and measured it. The main result came out backwards from what I expected.

**What this is and isn't.** This measures a *single-call classification* over a large cached prefix: one request in, one verdict out. There is no agent loop, no growing context, no tool results, no idle gap between turns. Those are the things I originally set out to test — an agent that idles and reloads its context, an orchestrator delegating to cheaper workers — and none of them is tested here. What follows is solid for the setup described and says nothing yet about multi-turn agent architectures.

# The task: check my own citations

I recently finished a review on structural balance in signed networks: 393 references, 923 citations. That turns out to be an unusually good benchmark substrate.

Take a sentence from the review, remove its citation, hand an agent one candidate reference, and ask whether that reference supports the claim. The citation keys I wrote are the ground truth. No rubric, no LLM-as-judge, no hand-labelling — grading is string comparison against my own bibliography.

The shape matters more than the topic. A large, byte-stable bibliography plus a tiny per-claim question is the best case for prompt caching. A task where every sub-task drags in its own large unique document is the opposite, and would make the caching question unmeasurable.

| | |
|---|---|
| Claim sentences with citations | 117 |
| Unique references cited | 93 |
| Balanced pairs, supported / not | 59 / 58 |
| Cached bibliography prefix | ~37,000 tokens |

# What the agent actually sees

A sentence in the review, as I wrote it:

```
...by the theorems of \citet{harary1953notion} and
\citet{davis1967clusteringSB}, a network either admits the
required partition or it does not.
```

Simply stripping the citations breaks it. In LaTeX, `\citet` *is* the subject of the sentence:

```
...by the theorems of and, a network either admits the
required partition or it does not.
```

So I mask each one instead. The sentence stays readable, and the marker shows where a reference belongs:

```
...by the theorems of [CITATION] and [CITATION], a network
either admits the required partition or it does not.
```

The agent then gets one masked sentence and one candidate reference, and answers a single question:

```
CLAIM      Real-world signed networks almost never do, which is why
           they are described as being in a state of partial
           balance [CITATION].

CANDIDATE  [aref2017measuring]
           Measuring partial balance in signed networks

ANSWER     supported
```

In half the items I swap in a reference I never cited there:

```
CANDIDATE  [wey2008social]
           Social network analysis of animal behaviour

ANSWER     not_supported
```

Half of those swaps come from a different topic entirely — easy to reject. The other half come from the *same subsection*: topically adjacent, genuinely confusable, the kind of mis-citation that survives peer review. That hard tier is where the configurations separate.

# The three models

All current-generation, one per price tier. Every configuration runs the identical prompt over the identical 117 items and the identical cached bibliography.

| Model | Input | Output | Context | Reasoning effort |
|---|---|---|---|---|
| Claude Opus 5 | `$5` / MTok | `$25` / MTok | 1M | `low` – `max` |
| Claude Sonnet 5 | `$2` / MTok | `$10` / MTok | 1M | `low` – `max` |
| Claude Haiku 4.5 | `$1` / MTok | `$5` / MTok | 200K | not available |

Opus and Sonnet each ran twice, at default and at low reasoning effort. Haiku 4.5 exposes no `effort` parameter, so it contributes one configuration. It does support extended thinking through an explicit token budget, which I deliberately left disabled — the comparison I wanted was against each model's out-of-the-box behaviour, and enabling it on Haiku alone would have made the tiers less comparable rather than more. That leaves Haiku's thinking cost at zero, which is worth remembering when reading its cost breakdown.

# The results

Total spend: `$8.66`, against a `$9.09` forecast built beforehand from free token counts.

![Cost versus accuracy for five configurations](/images/token-cost-quality.svg)

| Configuration | Accuracy | 95% CI | Cost | Per correct answer |
|---|---|---|---|---|
| Opus 5, low effort | **94.9%** | 89.3 – 97.6 | `$2.68` | `$0.0241` |
| Opus 5, default | 87.2% | 79.9 – 92.1 | `$3.29` | `$0.0323` |
| Sonnet 5, default | 79.5% | 71.3 – 85.8 | `$1.23` | `$0.0132` |
| Haiku 4.5 | 76.9% | 68.5 – 83.6 | `$0.38` | **`$0.0042`** |
| Sonnet 5, low effort | 68.4% | 59.5 – 76.1 | `$1.09` | `$0.0136` |

Because every configuration saw the identical items, these comparisons are paired, and McNemar's exact test is the right instrument rather than eyeballing whether intervals overlap.

## More thinking made Opus worse

Opus at low effort beat Opus at default effort — **94.9% against 87.2%** — while costing 19% less.

This is not a near-miss. Of the items where the two disagreed, low effort was right on **9 and wrong on 0** (p = 0.004). Low effort got everything default got right, plus nine more.

The per-tier breakdown is *consistent with* a specific mechanism, though I have not verified it. On easy negatives — an obviously unrelated paper — low effort scored 100% and default scored 83%. The natural reading is that given more room to reason, the model talks itself into a connection: it builds a plausible bridge between a claim about signed networks and a paper about animal behaviour, then accepts it. That is a hypothesis, not a finding. Confirming it means reading the model's stated reasoning on those nine items, which I did not capture in this run.

I would not have predicted this, and I would not have found it without a hard negative tier to expose it.

## Effort may be model-specific — but this one doesn't survive correction

Sonnet went the other way. Default effort scored 79.5%, low effort 68.4%, raw p = 0.035. At low effort Sonnet collapses on negatives: 55% on easy ones, **38% on hard ones** — worse than a coin flip.

But I ran six paired comparisons on one dataset, and under Holm-Bonferroni that result lands at **p = 0.105 and does not survive**. The three Opus-low comparisons do survive correction; this one does not.

So the honest statement is narrower than I first wrote it: the direction is suggestive and the effect size is large, but on a single run of 117 items I cannot claim the Sonnet effort difference is real. Settling it means replicates — about a dollar each — and this study has none. That is a gap against my own plan, which called for repeat runs.

## Aggregate accuracy hides opposite failure modes

Haiku and Sonnet-at-low-effort land 8 points apart overall, but they fail in mirror-image ways:

| | Positives | Easy negatives | Hard negatives |
|---|---|---|---|
| Haiku 4.5 | 64% | 93% | 86% |
| Sonnet 5, low | 90% | 55% | 38% |

Haiku is sceptical — it rejects citations that are actually fine. Sonnet at low effort is credulous — it accepts almost anything. Both are "about 70–77% accurate" and they would fail a real citation-checking job in completely different directions. A single accuracy number would have hidden that entirely.

## Which means "cost per correct answer" is the wrong ranking

For a citation checker the two errors are not worth the same. Waving through a bad citation puts an error into a published paper. Rejecting a good one wastes a few minutes of review. Treating them as equal is what lets Haiku look like the efficiency winner.

| Configuration | False accepts | False rejects |
|---|---|---|
| Opus 5, low | 5.2% | 5.1% |
| Haiku 4.5 | 10.3% | **35.6%** |
| Sonnet 5, default | 27.6% | 13.6% |
| Opus 5, default | 17.2% | 8.5% |
| Sonnet 5, low | **53.4%** | 10.2% |

Weight a false accept at five times a false reject — an arbitrary but defensible ratio for this job — and the ranking moves. Opus at low effort scores 99 of a possible 117. Haiku drops to 66, because it rejects a third of my perfectly good citations. **Sonnet at low effort goes net negative**: it admits more bad citations than it catches, so running it is worse than not checking at all.

The cheapest-per-correct-answer column is still Haiku. Whether that is the column you should rank on depends entirely on what an error costs you — and since total cost is linear in both error prices, you can just draw the whole decision space:

![Which configuration is cheapest, once errors have a price](/images/token-error-cost-regions.svg)

Total cost is `model price + false_accepts × x + false_rejects × y`, so each configuration is a plane over the two error prices and the boundaries between them are straight lines. Three things fall out.

**Haiku's win is smaller than it looks.** It is cheapest only inside a triangle bounded by `x + 6y = $0.77`. Put a price of one dollar on letting a bad citation through, with false rejects free, and Opus at low effort is already the cheaper option overall. If a false reject costs anything at all, the threshold drops fast: at 13 cents per false reject with free false accepts, Haiku has already lost.

**Sonnet at low effort survives only in a sliver** where a false accept is essentially free — which, for a citation checker, is not a real operating point.

**Opus at default effort wins nowhere.** Not at any pair of error prices. Opus at low effort is cheaper *and* makes fewer of both error types, so it dominates for every possible weighting. That is a stronger claim than the equal-weight ranking supports, and it is the one result here I would bet on.

## Two of five configurations are strictly dominated

Sonnet at low effort is beaten by Haiku on both axes: worse accuracy, higher cost. Opus at default is beaten by Opus at low effort on both axes. Neither has any reason to exist on this task.

And paying 3.2× more for Sonnet over Haiku buys nothing detectable: 79.5% against 76.9%, p = 0.74. On this workload that price difference is not purchasing accuracy.

# Where the money actually goes

![What each configuration pays for](/images/token-cost-configurations.svg)

This is the result with the widest application beyond my benchmark.

**Between 71% and 88% of every configuration's bill is re-reading the same bibliography.** Writing the answer is never more than 11%. The money is spent moving context, not producing conclusions.

Thinking is the one component that varies a lot: 20.8% of the bill for Opus at default effort, 2.7% at low. That is the same 10× drop in thinking tokens that made it *more* accurate.

The implication for anyone optimising an LLM system: the lever is rarely "make the model think less." It is "stop re-transmitting the same context." Caching is what converts that 71–88% slice from full price to a tenth of it.

# The baseline I never paid for

Running the same pass with caching disabled would cost `$22.46` on Opus 5, against `$3.29` cached — a factor of 6.8. I never ran it.

Caching is a billing transformation, not a behavioural one. The model sees byte-identical tokens whether or not the prefix is cached — caching changes what you are charged, not what comes back. So the uncached cost is arithmetic over the cached run's own usage fields:

```
uncached = (input + cache_creation + cache_read) × input_rate
         + output_tokens × output_rate
```

Every term is already logged. Paying twenty-two dollars to observe a number you can compute exactly is spending money to confirm multiplication.

# Building it without spending anything first

The whole pipeline was built and debugged on free endpoints, because the expensive failure mode is paying for a run whose harness is subtly broken.

The harness talks to a **mock client** that returns no real answers but faithfully reproduces every cache rule that decides the numbers: prefix matching, the per-model minimum cacheable prefix, lifetime measured from request start, free refresh on read, model-scoped entries, and the rule that a cache entry becomes readable only once the request writing it has begun responding.

That last rule matters in production. Fire eight parallel workers at the same cached prefix and none can read what the others are still writing — eight cache writes, zero reads. Send one request, wait for its first token, then fan out the rest. The real run used exactly that pattern and logged **116 cache reads against 1 write** per configuration.

The mock also paid for itself. It caught a bug where my uncached comparison arm was not *sending* the bibliography at all, only skipping the cache — which made waste look cheap and would have inverted the headline result.

Then four canary runs, about 85 cents total, checked the forecast against reality before the full run. Every one landed within 10% of prediction, and one corrected a bad assumption: I had budgeted 120 output tokens per reply, and Opus at default effort produced 378.

# Three rules for any LLM system

**Report money per completed task, never tokens.** Opus 5 and Haiku 4.5 use different tokenizers — the same bibliography is 37,251 tokens on one and 25,248 on the other, a 48% gap on identical bytes. "Configuration B used 40% fewer tokens" can be a statement about tokenizers rather than about your system.

**`input_tokens` is not the prompt size.** It is the uncached remainder. The true size is `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`. An agent that ran an hour and reports 4,000 input tokens read the rest from cache.

**Test effort per model, on your own hard cases.** The effort setting moved accuracy 8 points up on one model and 11 points down on the tier below. There is no portable default, and the easy cases will not show you the difference.

# What this doesn't tell you

**No replicates.** Each configuration ran once. My own plan called for repeat runs and this study has none, which is why the Sonnet effort result stays a hypothesis. The Opus result — 9 to 0 on discordant items, surviving correction — is too lopsided to be a fluke, but "surviving correction on one run" is weaker than "reproduced."

**No agent loop.** Single call in, single verdict out. No growing context, no tool results, no idle gaps. The architectures I originally set out to compare are all untested.

**One task, one domain.** Citation verification rewards scepticism. A task rewarding fluent synthesis might reverse the effort result entirely.

**117 items is enough for the tier comparisons and thin for the subgroups.** The per-difficulty cells hold 29 items each, so those intervals are wide — the direction is clear, the exact numbers are not.

**Four replies out of 585 failed to parse** and were scored as wrong. That is under 1% and does not change any ranking, but the affected configurations are marginally understated.

**The orchestrator question is still open.** Published measurements say a frontier-plus-cheap-workers split pays off only when the work exceeds a single context window. My 117 claims over a 37k-token bibliography fit comfortably inside a million-token window, so at this scale an orchestrator should lose. Finding the crossover means scaling to all 923 citations.

# What I'd run next

In order of what each would actually settle.

**Settle what's already published, about `$8`.** Replicate the Sonnet effort comparison three times — either the reversal is real or it isn't, and right now I can't say. And capture the model's stated reasoning on the nine items where Opus default failed and low effort succeeded, which turns the over-reasoning story into evidence or kills it.

**Test the Batch API, about `$1.50`.** Everything here ran as live synchronous calls; batch never appears in this post. It offers a flat 50% discount, but it is submitted all at once, so the send-one-then-fan-out trick that produced 116 cache reads per configuration is impossible, and the docs call cache hits inside a concurrent batch best-effort. Since cache reads *are* 71–88% of the bill, the two outcomes are far apart:

| Opus 5, low effort, 117 items | |
|---|---|
| Live, cached (measured) | `$2.68` |
| Batch, if cache reads land | ~`$1.34` |
| Batch, if every item re-reads the prefix | ~`$10.90` |

Batch is either the best lever here or a 4× regression, and nothing I ran distinguishes them.

**Run the idle-then-reload scenario, about `$5`.** Everything above ran against a warm cache. An agent that goes idle long enough for the cache to lapse, and has to re-import its context, is the scenario that started this project, and it is still untested. Four arms — idle, kept warm by real work, kept warm by a `max_tokens: 0` ping, and a one-hour cache — differing only in what happens in the gaps.

**Find the orchestrator crossover, `$20–50`.** With a caveat I got wrong at first: scaling to all 923 citations does *not* force decomposition. 923 claims plus a 37k bibliography is about 132k tokens, comfortably inside a million-token window. Forcing the issue needs full paper texts rather than abstracts — roughly 3.1M tokens — which is what makes chunking unavoidable and gives an orchestrator something to orchestrate. That is the second of the two questions this project was built to answer, and the one I haven't started.

---

*Rates and endpoint behaviour verified against the Claude platform documentation in September 2026. All figures measured; nothing modelled except the uncached baseline, which is derived arithmetic as described above.*
