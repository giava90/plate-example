---
title: "Framing Agriculture as a Linear Optimization Problem: How Transformed Messy Data and Linear Models Revealed a Hidden Food Security Bottleneck"
meta_title: "ML Swarm Orchestrator"
description: "How I used Google Antigravity to build a multi-agent AI system for end-to-end data science and AutoML workflows."
date: 2026-07-24T15:19:00Z
image: "images/data_flow_food_sec.jpg"
authors: ["Giacomo Vaccario"]
tags:
- "Generative AI"
- "LLM"
- "Agentic AI"
- "Sustainability"
- "Data science"
- "Automation"
draft: false
---
<!-- # Framing Agriculture as a Linear Optimization Problem -->

## 1. The Ambiguous Problem: Is Malnutrition a Land or Nutrients Issue?
Food security in Sub-Saharan Africa is frequently treated as a calorie problem, with many interventions focused primarily on total crop yield or energy intake. But this raises fundamental questions: Are current farming systems constrained by available land, specific crop choices, or something else entirely? Is solving for caloric intake enough to provide genuine nutritional security?

To answer this, I* set out to reframe food security from a simple yield problem into a system-wide optimization challenge: **What does a farming system designed for total nutritional adequacy—rather than just calories—look like, and what is its minimum land cost?**

## 2. Choosing Linear Programming Over Machine Learning
While machine learning was initially considered, I chose Linear Programming (LP) instead. In sensitive domains like regional food security, public health, and land policy, transparency and interpretable mathematical guarantees are far more valuable than black-box predictions. LP allows every assumption, constraint, and trade-off to remain explicit.

I formulated two complementary optimization setups:
1. **Minimize land area** required to achieve a target Mean Adequacy Ratio ($ext{MAR} = 1.0$).
2. **Maximize $\ext{MAR}$** subject to a fixed, existing land allocation constraint.

The decision variables are the specific land areas assigned to $\sim 90$ distinct crop and animal production options. The optimization solves for a whole new farming system tailored to local household requirements.

$$\text{MAR} = \frac{1}{17} \sum_{i=1}^{17} \min\left(1, \frac{p_i}{r_i}\right)$$

Where $p_i$ is the total farm production of nutrient $i$, $r_i$ is the demographic requirement, and the 17 tracked nutrients include essential macronutrients, vitamins, and minerals. The Nutrients Adequacy Ratio ($	ext{NAR}_i$) is capped at $1.0$ so that an excess of one nutrient (like carbohydrates) cannot mathematically mask a severe deficit in another (like Zinc or B12).

## 3. ETL Data Pipeline: Ingesting 35,000 Household Profiles
To ground the model in real-world agricultural conditions, I built an ETL pipeline to ingest household survey datasets spanning 18 Sub-Saharan African countries. 

```
  Raw Surveys (>35,000 Records)
               │
               ▼  [Data Cleaning & Filtering Pipeline]
  ├── Excluded Non-Sub-Saharan Records
  ├── Dropped Entries Missing Production/Land Data
  └── Filtered Extreme Outliers (e.g., 0 or >20 Household Children)
               │
               ▼
  25,617 Cleaned, Optimization-Ready Household Profiles
```

The data pipeline transformed the noisy survey inputs into production matrices ($p_i$) and household requirement vectors ($r_i$) mapped across 9 demographic tiers.

## 4. Production Cloud Architecture & Lean Decisions
The application logic was containerized and deployed to the cloud to make the optimization model interactive and accessible.

* **Database Engine:** Transformed crop composition and yield matrices were loaded into **Azure SQL Database** using chunked inserts to guarantee transaction stability during ingestion.
* **Optimization Compute:** The solver evaluates the constraint matrix dynamically using Python’s `scipy.optimize.linprog` solver.
* **Cloud Hosting:** The application is containerized with **Docker** and deployed to **Azure Container Apps** for automatic scale-to-zero operational efficiency.
* **Dashboard Interface:** Built with **Streamlit** entirely in Python. Selecting a unified Python stack was a deliberate engineering decision to keep the project lean and prevent unnecessary architectural bloat, prioritizing rapid iteration over maintaining separate frontend framework repositories (you can view my separate React/Tailwind frontend work [here](../ml_agent_orchestration_antigravity/)).
<!-- 
 ![Minimalist System Architecture Diagram](/images/data_flow_food_sec.jpg)
 *Caption: High-level data flow from Azure SQL database to the Streamlit frontend.*  
> 💬 **Nano Banana Prompt:** `"A clean, flat vector illustration showing a minimal data pipeline. Simple geometric nodes connected by thin line arrows on a light grey background. Minimalist 2D tech aesthetic, matte dual-tone color scheme (navy blue and pastel orange), no realistic shading, high contrast, zero unnecessary text."` -->

![Streamlit Dashboard View](/images/dashboard_food_sec_1.png)
*Caption: Single household analysis tab showing the MAR-vs-land curve and corresponding dietary preset controls.*

## 5. Using Claude as an Agentic Orchestrator
While earlier phases used standard code completion, I leveraged **Claude** as an agentic pair-programmer to drive the full deployment phase.

* **Delegated Execution:** I tasked Claude with orchestrating the data-engineering setup, refactoring legacy scripts, structuring SQL migration scripts, containerization configurations, and deploying the Streamlit UI to Azure Container Apps.
* **Human Validation & Scientific Oversight:** I retained full ownership over the mathematical formulation, validation, and domain interpretation. Crucially, during code reviews of the optimization pipeline, Claude flagged specific edge-case misinterpretations in constraint bounds, proving to be an exceptionally rigorous reviewer that accelerated full production deployment to just a few days.

## 6. Model Findings: The Vitamin B12 Bottleneck
To validate the optimization output, I conducted sensitivity analyses and performed manual checks on specific household case studies. This manual audit revealed a striking non-linear result.

Reaching **85% nutritional adequacy** requires very little land (around $0.04$ hectares per individual). However, closing the remaining gap to **100% full adequacy** causes land requirements to jump significantly by roughly $0.55$ hectares (nearly half a hectare per individual).

Why? **Vitamin B12.** 
Vitamin B12 alone accounts for a mean of 77% of the total land needed to reach full nutritional adequacy across the dataset. Because B12 is synthesized exclusively in animal-source foods, and livestock require significantly more land per unit nutrient yield, B12 forms an extreme agricultural bottleneck. Did you know B12 held such an overwhelming land footprint compared to all other nutrients combined? (I certainly didn't prior to building this model!)

![B12 Bottleneck](/images/b12-bottleneck.png)
*Caption: Supplying B12 off-farm frees an average of 0.417 hectares per reference adult—roughly 60 times more land than off-farm fortification of any other nutrient.*

 Explore more [here!](https://foodsec-dashboard.politerock-163c694a.switzerlandnorth.azurecontainerapps.io/).

---
*\*Note: "I" is used for narrative clarity; this research was developed collaboratively with three other co-authors: Ivan Novotny, Adelaide Sander and Jaboury Ghazoul.*
