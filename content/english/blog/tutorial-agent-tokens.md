---
title: "More Thinking Made It Worse: What I Learned Measuring What an AI Agent Actually Costs"
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

So I built something where every number is measurable, spent nine dollars, and measured it. One of the three headline results came out backwards from what I expected.

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

Opus and Sonnet each ran twice, at default and at low reasoning effort. Haiku exposes no effort parameter, so it contributes one configuration. Five in total.

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

The per-tier breakdown points at a mechanism. On easy negatives — an obviously unrelated paper — low effort scored 100% and default scored 83%. Given more room to reason, the model talks itself into a connection. It constructs a plausible-sounding bridge between a claim about signed networks and a paper about animal behaviour, and then believes it. Less thinking left less room to rationalise.

I would not have predicted this, and I would not have found it without a hard negative tier to expose it.

## But effort is model-specific, not a universal setting

Sonnet went the other way. Default effort scored 79.5%, low effort 68.4%, and the difference is significant (p = 0.035). At low effort Sonnet collapses on negatives: 55% on easy ones, **38% on hard ones** — worse than a coin flip.

So "lower the effort to save money" is not a portable recommendation. On the same task, in the same week, with the same prompt, it was a clear win on one model and a clear loss on the tier below.

## Aggregate accuracy hides opposite failure modes

Haiku and Sonnet-at-low-effort land 8 points apart overall, but they fail in mirror-image ways:

| | Positives | Easy negatives | Hard negatives |
|---|---|---|---|
| Haiku 4.5 | 64% | 93% | 86% |
| Sonnet 5, low | 90% | 55% | 38% |

Haiku is sceptical — it rejects citations that are actually fine. Sonnet at low effort is credulous — it accepts almost anything. Both are "about 70–77% accurate" and they would fail a real citation-checking job in completely different directions. A single accuracy number would have hidden that entirely.

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

**One task, one domain.** Citation verification rewards scepticism. A task rewarding fluent synthesis might reverse the effort result entirely.

**117 items is enough for the tier comparisons and thin for the subgroups.** The per-difficulty cells hold 29 items each, so those intervals are wide — the direction is clear, the exact numbers are not.

**Four replies out of 585 failed to parse** and were scored as wrong. That is under 1% and does not change any ranking, but the affected configurations are marginally understated.

**The orchestrator question is still open.** Published measurements say a frontier-plus-cheap-workers split pays off only when the work exceeds a single context window. My 117 claims over a 37k-token bibliography fit comfortably inside a million-token window, so at this scale an orchestrator should lose. Finding the crossover means scaling to all 923 citations.

That is the next run.

---

*Rates and endpoint behaviour verified against the Claude platform documentation in September 2026. All figures measured; nothing modelled except the uncached baseline, which is derived arithmetic as described above.*
