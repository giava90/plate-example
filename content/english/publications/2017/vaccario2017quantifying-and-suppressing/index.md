---
title: Quantifying and suppressing ranking bias in a large citation network
date: '2017-08-01'
volume: '11'
number: '3'
pages: 766-782
publishDate: '2021-02-08T11:56:31.218887Z'
authors:
- Giacomo Vaccario
- Matus Medo
- Nicolas Wider
- Manuel S. Mariani
abstract: It is widely recognized that citation counts for papers from different fields
  cannot be directly compared because different scientific fields adopt different
  citation practices. Citation counts are also strongly biased by paper age since
  older papers had more time to attract citations. Various procedures aim at suppressing
  these biases and give rise to new normalized indicators, such as the relative citation
  count. We use a large citation dataset from Microsoft Academic Graph and a new statistical
  framework based on the Mahalanobis distance to show that the rankings by well known
  indicators, including the relative citation count and Google's PageRank score, are
  significantly biased by paper field and age. Our statistical framework to assess
  ranking bias allows us to exactly quantify the contributions of each individual
  field to the overall bias of a given ranking. We propose a general normalization
  procedure motivated by the z-score which produces much less biased rankings when
  applied to citation count and PageRank score.
publication: Journal of Informetrics
url_pdf: http://www.sciencedirect.com/science/article/pii/S1751157717300974
doi: https://doi.org/10.1016/j.joi.2017.05.014
featured: false
tags:
- Science of Science
- Network Theory
image: '/images/thumbnailQ.png'
---


<p>Citation counts for papers from different fields can't be compared directly because they adopt different citation practices. Researchers have proposed various procedures to suppress these biases, but a new statistical framework shows that existing indicators, including the relative citation count, are still biased by paper field and age. A new normalization procedure motivated by the z-score produces much less biased rankings when applied to citation count and PageRank score. The problem of achieving an ideal unbiased ranking of publications remains open.</p>

<pre>
We propose a general normalization procedure motivated by the z-score which produces much less biased rankings when applied to citation count and PageRank score.
</pre>

<details class="custom-details">
  <summary><strong>Why This Matters for Scientists</strong></summary>
  <p>As a researcher, you may want to use the new normalization procedure to suppress field and age biases in citation-based indicators.</p>
</details>

<details class="custom-details">
  <summary><strong>Quick Technical Overview</strong></summary>
  <p>We analyze a large dataset from Microsoft Academic Graph to show that existing indicators of impact are still biased by age and field. The dataset contains a dump of the Microsoft Academic Graph, which includes publications from various fields and time periods. The bias assessment procedure presented here can be easily extended to detect any other kind of information bias.</p>

  <pre>
It is worth noticing that while we focus on the biases by age and field, our bias assessment procedure can be easily extended to detect any other kind of information bias.
  </pre>
</details>

<details class="custom-details">
  <summary><strong>Summary for Policy Makers</strong></summary>
  <p>The results of this study have implications for how we evaluate and compare research outputs. The new normalization procedure can help to produce more fair and unbiased rankings of papers. However, the problem of achieving an ideal unbiased ranking of publications remains open and requires further research. Policymakers and stakeholders should consider the limitations of existing citation-based indicators and the potential consequences of using biased rankings. They may want to consider alternative evaluation methods that take into account the complexities of academic citation networks.</p>

  <pre>
The problem of achieving an ideal unbiased ranking of the publications remains open.
  </pre>
</details>

<details class="custom-details" data-sentinel="ai-disclaimer-v1">
  <summary><strong>Disclaimer</strong></summary>
  <p>The above summaries were generated with the assistance of an AI system.</p>
</details>
