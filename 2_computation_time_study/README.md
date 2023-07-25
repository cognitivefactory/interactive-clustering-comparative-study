# Interactive Clustering : 2. Annotation Error Study

The main goal of this study is to **estimate the execution time needed** for algorithms to reach their objectives.


## Hypotheses

This sub-repository provides an environment to carry out a comparative study of _Interactive Clustering_ implementation around one hypothese.
- **Cost hypothesis**: _It is possible to estimate the required costs of an annotation methodology based on Interactive Clustering to obtain a workable trainset. We will particularly study the costs relating to (1) annotation time,  (2) algorithm execution time, an (3) total time depending on dataset size._

In this study, we focus on execution time.

## Experimental protocol

The proposed study consists in running _Interactive Clustering_ algorithms in order to estimate their execution speed.

Severale task are timed:
- _data preprocessing_: cf. [`cognitivefactory-interactive-clustering.utils.preprocessing`](https://cognitivefactory.github.io/interactive-clustering/reference/utils/preprocessing/)
- _data vectorization_: cf. [`cognitivefactory-interactive-clustering.utils.vectorization`](https://cognitivefactory.github.io/interactive-clustering/reference/utils/vectorization/)
- _constraints sampling algorithms_: cf. [`cognitivefactory-interactive-clustering.sampling.factory`](https://cognitivefactory.github.io/interactive-clustering/reference/sampling/factory/)
- _constrained clustering algorithms_: cf. [`cognitivefactory-interactive-clustering.clustering.factory`](https://cognitivefactory.github.io/interactive-clustering/reference/clustering/factory/)

The study can be done on several datasets, and observations can be done several times with different random seeds.
In order to test various number of settings, dataset are extended by spelling mistake generation, constraints are simulated, ...

To analyze execution speed, main factors analyses are performed based on factors correlation, and GLM modelisation of execiution time is made for all algorithms based on main factors selected.

## Implementation

1. Each experiment (combination of parameters) to run is modelized by a sub-folder path. The path contains the task to evaluate, the dataset generated, the algorithm to mesure and the random seed of the experiment. Several JSON files are needed to store parameters, temporary computations and experiment results.
2. All experiment runs can be parallelized. During the run, algorithm speed is stored.
3. When all experiments are run, time modelization are made (with factor analysis), based on experiment results.
4. Then, several graphs are made to represent execution speed.

All these steps are implemented in `Python`, and can be run within `Jupyter Notebooks`.

## Installation and Execution

Follow the description of `README.md` repository file in order to setup your `Python` environment.

Then follow notebooks instructions.


## Results

Due to the volume of data generated (around 2 GB), not all results are versioned on GitHub.

- results are zipped in a `.tar.gz` file and versioned on Zenodo : `TODO`.
- a summary of results are stored in `results`.

In order to make a save in a `.tar.gz` file, you can use the following command:
```bash
tar -czf 2_computation_time_study.tar.gz experiments/ notebook/ results/ README.md
```


## Scientific contribution

- One section of my PhD report is dedicated to this study : `TODO`.