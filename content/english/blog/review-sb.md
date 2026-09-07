---
title: "A Curated Review in Context: An Interactive Knowledge Map of the Structural-Balance Literature"
meta_title: "Interactive knowledge map of structural balance"
description: "How I placed 427 hand-picked references inside 3,000+ signed-network papers from OpenAlex to show, at a glance, that a review is a curated selection and not an exhaustive survey."
date: 2026-09-07T12:00:00Z
image: "images/sb_knowledge_map.png"
authors: ["Giacomo Vaccario", "Piotr Górski", "Georges Anders", "Manuel S. Mariani", "Janusz Hołyst"]
tags:
- "Network Theory"
- "Structural balance"
- "Science of Science"
- "LLM"
- "Machine Learning"
draft: false
---
<!-- # A Curated Review in Context -->

When you write a review, one question follows you around: *did you cover
everything?* For an interpretive, physics-oriented review of **structural
balance** the honest answer is "no, on purpose". The reference list is a
curated selection of the work that matters conceptually, not a systematic
harvest of every paper that mentions a signed network. The map below is an
attempt to *show* that rather than assert it.

## What you are looking at

Every dot is a publication retrieved from [OpenAlex](https://openalex.org). The
large outlined markers are the **427 references** cited in our review (of 431
that resolved on OpenAlex); the small faint dots are a background of **3,068
works** pulled with the phrases *structural balance*, *signed network*, *signed
graph*, *signed social network* and *Heider balance*, keeping only those whose
title or abstract is actually about signed or balance-related structure.

Colours are communities; the panel on the right names them and gives their size
and how many curated papers fall inside each. The curated set piles up in two
**opinion-dynamics / social-influence** communities and the
statistical-physics-of-balance region attached to them, and only brushes past
adjacent bodies of work the map keeps separate, such as signed graph theory,
link-sign prediction, consensus and distributed control on antagonistic
networks, "balance" in political economy. That asymmetry is the whole point.

<div style="position:relative;width:100%;height:78vh;min-height:520px;border:1px solid #e4e4e4;border-radius:8px;overflow:hidden;margin:1.5rem 0;">
  <iframe src="/knowledge_map_interactive.html?bare=1"
          title="Interactive knowledge map of the structural-balance literature"
          loading="lazy"
          style="width:100%;height:100%;border:0;"></iframe>
</div>

<p style="font-size:0.9em;color:#666;margin-top:-0.75rem;">
  <strong>Hover</strong> a point for the paper (title, authors, year, community,
  citations). <strong>Scroll</strong> to zoom, <strong>drag</strong> to pan,
  <strong>type</strong> in the search box to spotlight titles or authors, and
  <strong>click</strong> a community in the legend to isolate it.
  <a href="/knowledge_map_interactive.html" target="_blank" rel="noopener">Open full screen&nbsp;↗</a>
</p>

## How the map is built

The pipeline is a laptop-sized adaptation of the Max Planck Institute for Human
Development "science map" method, with the LLM-heavy parts removed.

1. **Corpus** — resolve every `.bib` entry on OpenAlex (DOI → title search →
   fuzzy title match), then union a focused phrase search for the background
   layer. Abstracts are rehydrated from OpenAlex's inverted index and cleaned.
2. **Representation** — each work becomes the concatenation of three
   L2-normalised spaces: a **sentence embedding** of title + abstract
   (`all-MiniLM-L6-v2`), a **co-authorship** embedding (PPMI + truncated SVD of
   the work×author matrix), and a **bibliographic-coupling** embedding (same
   construction on shared references).
3. **Layout & communities** — [UMAP](https://umap-learn.readthedocs.io) to two
   dimensions, [Leiden](https://www.nature.com/articles/s41598-019-41695-z) for
   communities, each labelled by its dominant OpenAlex research topics with a
   keyword (c-TF-IDF) fallback.
4. **Render** — a static figure for the paper and this interactive version for
   the web. Community colours are assigned by size, so they stay put when the
   corpus is refreshed.

The interactive map is a single self-contained HTML file: no JavaScript
libraries, no network calls, the ~3,000 points embedded as JSON and drawn on a
`<canvas>`.

## Reading it as a statement of scope

Re-clustered on their own, the curated papers split into recognisable
sub-themes: cognitive balance and belief dynamics, signed social-network
analysis, Hamiltonian and statistical-physics models, international relations
and economics, ecological systems, higher-order balance. This is roughly the
table of contents of the review. The big map is the counterpart: it says where
that curated core sits in the wider signed-network landscape, and where it
deliberately does not go.

<!--
DEPLOYMENT NOTES (delete before publishing)

Files:
  static/knowledge_map_interactive.html   -> served at /knowledge_map_interactive.html (iframe src)
  assets/images/sb_knowledge_map.png       -> the `image:` cover (same as other posts)

A raw <iframe> does not run the asset pipeline, so the html must live in
static/ (published as-is), not assets/. The iframe is raw HTML and needs
markup.goldmark.renderer.unsafe = true in hugo.toml -- Hugoplate sets this.

Regenerate after a pipeline re-run:
  python scripts\run_pipeline.py --only interactive
  cp image4SBReview/docs/figs/knowledge_map_interactive.html  static/
-->


