# Interactive Clustering : 4. Constraints number Study

The main goal of this study is to **estimate the number of constraints needed** of the method one different dataset size.


## Hypotheses

This sub-repository provides an environment to carry out a comparative study of _Interactive Clustering_ implementation around one hypothese.
- **Cost hypothesis**: _It is possible to estimate the required costs of an annotation methodology based on Interactive Clustering to obtain a workable trainset. We will particularly study the costs relating to (1) annotation time,  (2) algorithm execution time, an (3) total time depending on dataset size._

In this study, we focus on constraints needed to complete annotation.


## Experimental protocol

The proposed study consists in performing _Interactive Clustering_ iterations with specific settings in order to annotate an unlabeled dataset, starting from no known constraints and ending when all the possible constraints between questions are defined.
The human annotator is simulated by the algorithm, and annotations are made by comparing with ground truth labels: two questions are annotated with a `MUST_LINK` if they come from the same intent, and with a `CANNOT_LINK` constraint otherwise.

Several dataset size are studied in order to estimate the number of constraints needed per data.
The study can be done on several datasets, and observations can be done several times with different random seeds.

To analyze the constraints nedeed, GLM modelization are performed with experiment results.


## Implementation

1. Each experiment (combination of dataset size and parameters) to run is modelized by a sub-folder path. The path contains the dataset used, the values of parameters studied, and the random seed of the experiment. Several JSON files are needed to store parameters, temporary computations and experiment results.
2. All experiment runs can be parallelized. During the run, clustering evaluation and algorithm speed are stored.
3. When all experiments are run, constraints number requirements are modelized based on experiment results.
4. Graph and total cost can be estimated with these modelization.


## Installation and Execution

Follow the description of `README.md` repository file in order to setup your `Python` environment.

Then follow notebooks instructions.


## Results

Due to the volume of data generated (around 15 GB), not all results are versioned on GitHub.

- results are zipped in a `.tar.gz` file and versioned on Zenodo : `TODO`.
- a summary of results are stored in `results`.

In order to make a save in a `.tar.gz` file, you can use the following command:
```bash
tar -czf 4_constraints_number_study.tar.gz experiments/ notebook/ results/ README.md
```


## Scientific contribution

- One section of my PhD report is dedicated to this study : `TODO`.