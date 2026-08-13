---
title: 'Machine learning for modeling forest dynamics using National Forest Inventory and climate data'
date: '2026-05-05'
publishDate: '2026-05-05'
authors:
- Dea Rieder
- Maximiliano Costa
- Christian Temperli
- Francesco Giardina
- Giacomo Vaccario
abstract: 'Accurate prediction of forest structure and composition is essential for forest management, as planning depends on anticipating future stand dynamics under changing environmental conditions. Machine learning algorithms have proven useful for this task due to their ability to capture non-linear ecological patterns in forest dynamics. However, current machine learning applications in forest ecology mostly focus on component growth rates, leaving approaches that directly predict future stand-level states like total basal area and species composition under-explored. This study develops a national-scale XGBoost model for Swiss forests, using Swiss National Forest Inventory data and CH2018 climate scenarios to predict changes in basal area and broadleaf proportion. Tested on a later inventory not used for training, XGBoost predicts the next inventory state with an R² of 0.66 for basal area and 0.91 for broadleaf proportion, slightly above a linear Lasso model (0.65 and 0.90). When applied recursively to generate exploratory projections to 2099, the model indicates an overall increase in basal area, although unmanaged lower-elevation belts decrease, and an increase in broadleaf proportion mainly at lower elevations, especially under high emissions. These trends are similar to patterns reported by established process-based and empirical forest models. This work offers a computationally efficient approach for projecting forest dynamics over large areas, without the extensive parameterization required by process-based models.'
publication: Ecological Modelling
url_pdf: https://doi.org/10.1016/j.ecolmodel.2026.111763
doi: 10.1016/j.ecolmodel.2026.111763
featured: false
sg-areas:
tag:
- Machine learning
- Sustainability
- Data Science
image: 'images/pred.png'
---