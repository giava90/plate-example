---
title: "Keeping a large AI model running on a satellite cluster"
meta_title: "AI model on a satellite cluster"
description: "A network model of an 81-satellite cluster aged over five years: where model stages sit matters more than how lasers are pointed, letting satellites switch stage lifts output from 88% to 94%, and weights should be copied from neighbours, not the ground."
date: 2026-11-17T12:00:00Z
image: "images/satellite-cluster-cover.png"
authors: ["Giacomo Vaccario"]
tags:
- "Machine Learning"
- "Networks"
- "Resilience"
- "Space"
- "Agentic AI"
draft: false
---

Several companies now plan to run AI models on satellites in low Earth orbit. Google's [Project Suncatcher](https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design/) [launched its first prototype](https://www.npr.org/2026/10/01/nx-s1-5983697/project-suncatcher-google-ai-data-center-space), with Google's own AI chips on board, in October 2026 [[1]](https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design/)[[2]](https://www.npr.org/2026/10/01/nx-s1-5983697/project-suncatcher-google-ai-data-center-space). The main argument is energy: in a suitable orbit, solar panels are in sunlight almost all the time [[1]](https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design/). So far, most of the discussion has been about launch costs, cooling and radiation.

I looked at a different problem. A large model may not fit on one satellite. Its parts must then run on many satellites that pass data to each other over laser links. My question was how such satellites should be connected, and what should happen when some of them fail, as they will over the years.

To study this, I built a small network model of a cluster like the one Google describes in its [design paper](https://arxiv.org/abs/2511.19468). It has 81 satellites on a grid, with neighbours 100 to 200 m apart [[3]](https://arxiv.org/abs/2511.19468). The satellites move relative to each other, so the grid stretches and shrinks twice per orbit [[3]](https://arxiv.org/abs/2511.19468). The model is split into nine consecutive stages, and each satellite holds one stage. A query has to pass through all nine stages in order.
A stage’s capacity depends on how many working satellites and chips hold it, and it falls as chips fail.

![Legend: each satellite is a circle whose number and shade of blue give its model stage, from 1 (light) to 9 (dark). A ring around it shows the capacity left: a full ring when all 32 chips work, three quarters for 24 of 32, half for 16 of 32, a quarter for 8 of 32. A grey cross marks a lost satellite.](/images/satellite-cluster-legend.png)

Laser links work at full speed up to a design range of 200 m. Beyond it, they become slower and cost more energy. I then let the cluster age for five years, with published failure rates for chips (9% per year) [[4]](https://www.forethought.org/research/will-we-really-put-data-centers-in-space) and whole satellites (2% per year) [[5]](https://arxiv.org/abs/2608.27499). On this cluster, I compared simple rules for re-connecting satellites and for moving work between them.

## Three results

**First, where the stages sit matters more than how the links are pointed.** If each stage occupies one column of the grid, a query needs eight short hops. If the stages are scattered at random, the same query uses about three and a half times as much link energy.

![Two 9×9 grids of satellites, each labelled with the model stage it holds. Left: stages in columns, so a query moves 1 → 9 in eight hops between direct neighbours. Right: stages scattered at random, so the same query needs longer hops that cross the grid, using about 3.5 times the link energy.](/images/satellite-cluster-stage-placement.png)
<!-- *Figure: The same query on two layouts of the 81-satellite cluster. Each dot is a satellite, and its number is the model stage it holds. The orange route visits stages 1 to 9 in order, each time going to the nearest satellite with the next stage. The scattered layout is one random example. The 3.5× energy ratio is the average from the simulation, not from this single route.* -->

**Second, moving work between satellites pays.** Over five years, the cluster loses about 40% of its computing capacity, mostly through failing chips. The losses are uneven, and the slowest stage limits the whole cluster. A simple rule corrects this: when one stage has more than one satellite's worth of capacity above another, a satellite switches stage. 
This raised five-year output from 88% to 94% of what the surviving hardware could deliver. The whole cluster needed only 10 to 30 such switches in five years.
<!-- 
![Bar chart of capacity per model stage, before and after one satellite switches stage. Before: stage 5 is the weakest at 3.75 and limits the cluster, while stage 3 has 7.5. After a satellite moves from stage 3 to stage 5, the weakest stage rises to 4.75.](/images/satellite-cluster-rebalance.png)

*Figure: How the stage-switching rule works, on illustrative numbers. Each block is one surviving satellite, and its height is the capacity it has left after chip failures. Every query passes through all nine stages, so the cluster runs at the speed of its weakest stage. Capacity above that level sits idle. Moving one satellite from the strongest to the weakest stage lifts the whole cluster.* -->

![Two 9×9 grids of satellites, one column per model stage, with a ring around each satellite showing its remaining capacity. Before: stage 5 is the lowest at 3.75 and stage 2 the strongest at 8.25. After the first step of the chain rule, one satellite each passes from stage 4 to 5, from 3 to 4 and from 2 to 3, so stage 5 rises to 4.75 and stage 2 falls to 7.25.](/images/satellite-cluster-stage-switch.png)
<!-- 
*Figure: The chain rule on the cluster itself, on illustrative numbers. The ring around each satellite shows the share of its 32 chips that still work. The strongest stage, stage 2, is the donor, but its satellite does not jump straight to stage 5. Instead, one satellite each passes from stage 4 to 5, from 3 to 4 and from 2 to 3, so every stage stays in neighbouring columns. Each switching satellite stays in place and copies its new weights from a neighbour. The rule repeats until no two stages differ by more than one satellite.* -->

**Third, a satellite that switches stage should copy the new weights from a neighbour.** From the ground, 100 GB over a 200 Mbps radio link, available 5% of the time, takes about 22 hours. From a neighbour over a 10 Tbps laser link, the order of magnitude targeted in Google's design [[3]](https://arxiv.org/abs/2511.19468), it takes less than a tenth of a second. In other words, the ground link can be kept for new model versions.

In contrast, linking distant satellites did not pay. Re-pointing links to the nearest satellites holding the right stage added 2 to 3% output. Longer links added nothing measurable. A fixed grid of links was enough until about a fifth of the satellites were lost. Beyond that point, it broke apart.

<!-- TODO: add the figure file to assets/images/ and uncomment
![Throughput of the cluster over five years, in units of one healthy satellite. The dotted line is the limit set by the surviving hardware. With stage switching, the cluster stays close to that limit; with fixed links alone, it falls further behind each year.](/images/satellite-cluster-throughput.png)
-->

## Limits

These results have clear limits. The energy figures are relative, because I have no absolute power figure for a laser terminal, and computing probably dominates a satellite's energy budget. Failures are treated as independent, whereas a solar storm or a faulty production batch would hit many satellites at once. Silent computation errors are not modelled, although Google's revised radiation tests identify them as the main radiation effect on its chips [[3]](https://arxiv.org/abs/2511.19468). The failure rates are not measured in orbit: the chip rate comes from ground data centres [[4]](https://www.forethought.org/research/will-we-really-put-data-centers-in-space), and the satellite rate is a design target [[5]](https://arxiv.org/abs/2608.27499). Some inputs, such as the failure rate of a laser terminal and the 32 chips per satellite, are my own assumptions. Still, the ranking of the rules was the same in two independent sets of runs.

## The practical message

For anyone designing such a cluster, the practical message is short. Decide where each part of the model sits before deciding how to point the links. Keep several copies of every part, and let satellites copy weights from each other. Keep links short: in my runs, links to distant satellites never helped.

The simulation was built and run with an AI assistant ([Claude](https://www.anthropic.com/claude), Anthropic). The [technical report](/reports/satellite_cluster_report.pdf) (PDF) gives all assumptions and results. The code is available on request.

## References

1. Google Research (2025). [Project Suncatcher: exploring a space-based, scalable AI infrastructure system design](https://research.google/blog/exploring-a-space-based-scalable-ai-infrastructure-system-design/). Google Research Blog.
2. NPR (2026, October 1). [Google launches Project Suncatcher, a step towards AI data centers in space](https://www.npr.org/2026/10/01/nx-s1-5983697/project-suncatcher-google-ai-data-center-space). See also Google's follow-up post: [We've received our first response from the Project Suncatcher prototype satellite](https://blog.google/innovation-and-ai/models-and-research/google-research/project-suncatcher-satellite-response/).
3. Agüera y Arcas, B., Beals, T., Biggs, M., Bloom, J. V., Fischbacher, T., Gromov, K., Köster, U., Pravahan, R., & Manyika, J. (2025). [Towards a future space-based, highly scalable AI infrastructure system design](https://arxiv.org/abs/2511.19468). arXiv:2511.19468 (v2). Source of the 81-satellite cluster geometry, the ~10 Tbps link target and the radiation test results.
4. Parrack, A., & Moorhouse, F. (2026). [Will we really put data centers in space?](https://www.forethought.org/research/will-we-really-put-data-centers-in-space) Forethought. Source of the chip failure rate: about 9% per year, based on failure rates observed in ground data centres.
5. Turyshev, S. G. (2026). [Operations, maintenance, and industrial scaling of MW-class orbital data centers](https://arxiv.org/abs/2608.27499). arXiv:2608.27499. Source of the satellite loss rate: a target of 0.01 to 0.03 catastrophic losses per year for a 100 kW node; I used 2%.
