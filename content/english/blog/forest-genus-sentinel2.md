---
title: "DeepLearning Tree genus from satellite images"
meta_title: "Tree genus from Sentinel-2"
description: "A small CNN on Sentinel-2 beats a fair tree-based baseline by about 3 accuracy points, not 10.6, and counting predicted labels misstates the area of a rare genus. Experiments run by an AI coding agent and then reviewed."
date: 2026-11-17T12:00:00Z
image: "images/forest2sawmill-cnn-lead.png"
authors: ["Giacomo Vaccario"]
tags:
- "Machine Learning"
- "Remote Sensing"
- "Forestry"
- "Sustainability"
- "Agentic AI"
draft: false
---
Forest inventories increasingly use satellite images to map which trees grow where. Such maps are then turned into estimates of wood volume per genus. Their quality is usually reported as classification accuracy, that is, the share of patches labelled correctly. However, a high accuracy does not guarantee a correct area for each genus.

## Question and experiment
My question was the following. Does a deep network beat a simpler model at telling spruce, pine, beech and oak apart, and what does the remaining error do to a volume estimate? I used the TreeSatAI archive, which holds 27,656 labelled patches of these four genera from Lower Saxony, Germany. The experiments were run unattended by an AI coding agent, in two rounds, and I reviewed the results afterwards.

In the first round, three models were trained. The first is LightGBM, a model built from many small decision trees, fed with summary statistics of a 200 m Sentinel-2 window. Sentinel-2 is a free European satellite mission with 10 m pixels. The second is a small convolutional neural network (CNN), that is, a network that learns spatial patterns, on the same window. The third is a pretrained ResNet-18 network on 20 cm aerial photos. Their errors were then converted into volume errors for synthetic regions. A review raised three doubts about the first round, and the second round tested them. Three findings remain.

<!-- The small CNN has six convolution layers and one output layer, with 290,564 parameters in total. -->

![The small CNN: six 3×3 convolution layers in three pairs, two max-pooling steps, global average pooling and one linear layer, from a 12-band 20 × 20 pixel Sentinel-2 patch to the probabilities of spruce, pine, beech and oak](/images/forest2sawmill-cnn-architecture.png)

## Findings

First, most of the CNN's lead came from an unfair baseline. In the first round, the CNN beat LightGBM by 10.6 accuracy points, with 89.5% against 78.9%. However, the label describes only the central 60 m of each window. The original LightGBM mixed this centre with the surrounding pixels. When it summarised the centre and the surrounding ring separately, it reached 86.4%. The CNN's lead then shrinks to 3.1 points. The figure below shows these gaps.

![The small CNN's accuracy lead over LightGBM on the original and the blocked split, against the original and the fair baseline](/images/forest2sawmill-cnn-lead.png)

Second, the remaining lead is not an artefact of neighbouring patches. Indeed, patch coordinates alone predicted the genus correctly for 71.4% of test patches. In other words, the original split rewards a model for knowing where a patch lies. The second round therefore held out whole 2 km blocks for testing and retrained the models. On this blocked split the CNN still led the fair baseline by 3.7 points, with a 95% interval of 2.7 to 4.8.

Third, counting predicted labels gives good areas only when a region resembles the training data. The volume numbers here use placeholder growing stocks and synthetic regions. This is enough for the comparison, because the percentage error per genus does not depend on the growing stock. In the first round, errors in the dataset's own genus mix largely cancelled. For example, LightGBM misstated spruce volume by only −1.6%. However, that mix was almost identical to the mix the models were trained on. A small example shows what happens otherwise. Consider a region with 60% spruce, 25% pine, 10% beech and 5% oak. Counting the CNN's labels there understates spruce volume by 7.2%. It overstates beech by 19.9% and oak by 31.9%. Each misread spruce stand moves area into a small class, where it weighs much more. At 2% oak, counting overstates oak volume by 182.9% with the CNN. 


This error is adjusted for by expectation–maximisation (EM) correction, which re-estimates the genus shares from the predicted probabilities. 
It starts from the genus mix of the training data. In every patch, it then gives a genus more weight if the region seems to contain more of it than the training data did, and less weight if it seems to contain less. From these weighted probabilities it computes a new estimate of the region's mix. It repeats both steps until the estimate no longer changes. As a result, a patch that the model finds hard to classify is more often assigned to a genus that is common in the region. A patch that the model classifies with high confidence usually keeps its genus. This correction reduced the CNN's root mean squared error, that is, the typical size of the error over 1,000 simulated regions, to 13.7% at 2% oak. The figure below shows how the error grows as oak becomes rarer.

![Oak volume error against the true oak share, for five ways of estimating genus shares and three models](/images/forest2sawmill-oak-sweep.png)

## Take home messages

The deep network's advantage is about 3 points rather than 10.6. Counting errors cancel only in a region with the training mix. The ranking of the Sentinel-2 models, however, held on both splits.

These results have clear bounds. All patches come from one German state, and the satellite images are from summer only. The labels come from administratively mapped stands. Accuracy drops on mixed stands: where the labelled genus covers less than 60% of a patch, the CNN is right for 72.0% of patches. The regions are synthetic, built by resampling test patches, and the growing stocks are placeholder values. Each model was trained once. Nevertheless, two points should hold beyond this setting. A baseline should see the same area as the label, and counted areas inherit the genus mix of the training data.

To conclude, a small CNN on free Sentinel-2 data classifies these four genera a few points better than a well-built tree model. The larger risk lies in how the map is used. A forester who estimates genus areas from such a map should not simply count predicted labels when a genus is rarer in the region than in the training data. Instead, they should correct the shares, for example with EM, and check rare genera against field plots.

## References

Ahlswede, S., Schulz, C., Gava, C., Helber, P., Bischke, B., Förster, M., Arias, F., Hees, J., Demir, B., and Kleinschmit, B. (2023). TreeSatAI Benchmark Archive: a multi-sensor, multi-label dataset for tree species classification in remote sensing. *Earth System Science Data*, 15, 681–695. [doi:10.5194/essd-15-681-2023](https://doi.org/10.5194/essd-15-681-2023)

Schulz, C., Ahlswede, S., Gava, C., Helber, P., Bischke, B., Arias, F., Förster, M., Hees, J., Demir, B., and Kleinschmit, B. (2022). TreeSatAI Benchmark Archive for Deep Learning in Forest Applications, version 1.0.1 (data set, CC BY 4.0). Zenodo. [doi:10.5281/zenodo.6780578](https://doi.org/10.5281/zenodo.6780578)

Drusch, M., Del Bello, U., Carlier, S., Colin, O., Fernandez, V., Gascon, F., Hoersch, B., Isola, C., Laberinti, P., Martimort, P., Meygret, A., Spoto, F., Sy, O., Marchese, F., and Bargellini, P. (2012). Sentinel-2: ESA's optical high-resolution mission for GMES operational services. *Remote Sensing of Environment*, 120, 25–36. [doi:10.1016/j.rse.2011.11.026](https://doi.org/10.1016/j.rse.2011.11.026)

Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., and Liu, T.-Y. (2017). LightGBM: a highly efficient gradient boosting decision tree. *Advances in Neural Information Processing Systems*, 30.

He, K., Zhang, X., Ren, S., and Sun, J. (2016). Deep residual learning for image recognition. *Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition (CVPR)*, 770–778.

Forman, G. (2008). Quantifying counts and costs via classification. *Data Mining and Knowledge Discovery*, 17, 164–206.

Bella, A., Ferri, C., Hernández-Orallo, J., and Ramírez-Quintana, M. J. (2010). Quantification via probability estimators. *Proceedings of the IEEE International Conference on Data Mining (ICDM)*, 737–742.

Saerens, M., Latinne, P., and Decaestecker, C. (2002). Adjusting the outputs of a classifier to new a priori probabilities: a simple procedure. *Neural Computation*, 14(1), 21–41.

Software: Python with PyTorch and torchvision (ImageNet-pretrained ResNet-18 weights), LightGBM, rasterio, NumPy, SciPy, pandas and Matplotlib.
