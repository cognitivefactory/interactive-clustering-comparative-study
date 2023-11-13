# Interactive Clustering : 1. Efficience Study

The main goal of this study is to **confirm the technical efficience** of the method by verifying its convergence to a ground truth and by finding the best implementation to increase convergence speed.


## Hypotheses

This sub-repository provides an environment to carry out a comparative study of _Interactive Clustering_ implementation around two hypotheses.
- **Effectiveness hypothesis**: _An annotation methodology based on Interactive Clusterin_ can provide a training set for a conversational assistant that respects the vision given by the business expert during the annotation._
- **Efficiency hypothesis**: _The convergence speed of Interactive Clustering can be optimized by coosing some settings in order to minimize operator workload. We will particularly study the influence of four factors on the number of constraints required : (1) data preprocessing, (2) data vectorization, (3) constraints sampling and (4) constrainted clustering._

In fact, several implementations are available, and the main goal is to determine the best ones.


## Experimental protocol

The proposed study consists in performing _Interactive Clustering_ iterations in order to annotate an unlabeled dataset, starting from no known constraints and ending when all the possible constraints between questions are defined.
The human annotator is simulated by the algorithm, and annotations are made by comparing with ground truth labels: two questions are annotated with a `MUST_LINK` if they come from the same intent, and with a `CANNOT_LINK` constraint otherwise.

Several parameters can be studied:
- _data preprocessing_: cf. [`cognitivefactory-interactive-clustering.utils.preprocessing`](https://cognitivefactory.github.io/interactive-clustering/reference/utils/preprocessing/)
- _data vectorization_: cf. [`cognitivefactory-interactive-clustering.utils.vectorization`](https://cognitivefactory.github.io/interactive-clustering/reference/utils/vectorization/)
- _constraints sampling algorithms_: cf. [`cognitivefactory-interactive-clustering.sampling.factory`](https://cognitivefactory.github.io/interactive-clustering/reference/sampling/factory/)
- _constrained clustering algorithms_: cf. [`cognitivefactory-interactive-clustering.clustering.factory`](https://cognitivefactory.github.io/interactive-clustering/reference/clustering/factory/)

The study can be done on several datasets, and observations can be done several times with different random seeds.

During _Interactive Clustering_ iterations, the relevance of data segmentation is measured using homogeneity, completeness, and v-measure, computed on the clustering results of each iteration.
Measures are obtained through comparison with the ground truth, corresponding to annotations by business experts prior to the experiment (with no computer guidance). 

To analyze the convergence speed and the effect size of the implementation parameters on the number of annotations required, the authors perform repeated measures `ANOVA` in `R`.
Post-hoc comparisons are performed using `Tukey HSD` procedure.
Finally, the optimal set of parameters according to statistical analysis is selected to train a candidate intents classifier.


## Implementation

1. Each experiment (combination of parameters) to run is modelized by a sub-folder path. The path contains the dataset used, the values of parameters studied, and the random seed of the experiment. Several JSON files are needed to store parameters, temporary computations and experiment results.
2. All experiment runs can be parallelized. During the run, clustering evaluation and algorithm speed are stored.
3. When all experiments are run, main effects and post hoc analyzes are made, based on experiment results.
4. Then, best parameters to get the ground truth can be deduced.

All these steps are implemented in `Python` and `R`, and can be run within `Jupyter Notebooks`.


## Installation and Execution

Follow the description of `README.md` repository file in order to setup your `Python`/`R` environment.

Then follow notebooks instructions.


## Results

Due to the volume of data generated (around 2 GB), not all results are versioned on GitHub.

- results are zipped in a `.tar.gz` file and versioned on Zenodo : `Schild, E. (2021). cognitivefactory/interactive-clustering-comparative-study. Zenodo. https://doi.org/10.5281/zenodo.5648255`.
- a summary of results are stored in `results`.

NB: In order to make a save in a `.tar.gz` file, you can use the following command:
```bash
tar -czf 1_efficience_study.tar.gz experiments/ notebook/ results/ README.md
```


## Scientific contribution

- A research paper is dedicated to this study : `Schild, E., Durantin, G., Lamirel, J., & Miconi, F. (2022). Iterative and Semi-Supervised Design of Chatbots Using Interactive Clustering. International Journal of Data Warehousing and Mining (IJDWM), 18(2), 1-19. http://doi.org/10.4018/IJDWM.298007. <hal-03648041>.`
- Two sections of my PhD report are dedicated to this study : `Schild, E. (2024, in press). De l'Importance de Valoriser l'Expertise Humaine dans l’Annotation : Application à la Modélisation de Textes en Intentions à l'aide d’un Clustering Interactif. Université de Lorraine.` (Sections 4.1 and 4.2)