# Interactive Clustering : 7. Inter-annotators Score Study

The main goal of this study is to **estimate the inter-annotators score** during constraints annotation.


## Hypotheses

This sub-repository provides an environment to carry out a comparative study of _Interactive Clustering_ implementation around one hypothese.
- **Robustness hypothesis**: _During an annotation methodology based on Interactive Clustering, it is possible to estimate the rate of inconsistencies appearing in constraints and their impact on the results of the method._

In this study, we focus on inter-annotators score during constraints annotation.

## Experimental protocol

The proposed study consists in performing constraints annotation by several operators and estime the inter-annotators agreement. We reuse the instructions of annotation experiment for annotation time estimation (`3_annotation_time_study`).

Several instructions are given to annotators:
- *Operator context*: “You are newspapper experts; You want to classify articles into categories based on their title; You do not know precisely which categories you will use to classify your articles; But you know how to identify the similarity of two articles”;
- *Context on the dataset*: "Topics are common newspapper categories; The ground truth contains between 10 and 20 of the most common categories of the press; Ground truth contains between 30 and 100 newspappers per category; You can watch the unannotated dataset as much as you want";
- *Objective of the experiment*: "Annotate 400 constraints, and estimate the difference among 4 annotators" ;
- *Annotation instructions*: "Perform at least 15 minutes of annottaion for regularity; If possible, isolate yourself in order to be not disturbed and to not distort the results; For each series; If you don't know what to annotate (too ambiguous, unknown vocabulary, ...), go to the next one without annotating (you are supposed to be press experts!)".

Then, use alpha of Krippendorff to compute agreement scores.


## Implementation

1. Constraints to annotate are selected (200 MUST-LINK, 200 CANNOT-LINK, based on groundtruth).
2. Annotation project can be imported in the annotation app with zipped archive, and operators can use the app to annotate constraints.
3. After annotation, agreement scores are computed based on experiment results.

All these steps are implemented in `Python`, and can be run within `Jupyter Notebooks`.


## Installation and Execution

Follow the description of `README.md` repository file in order to setup your `Python` environment.

Then follow notebooks instructions.


## Results

Due to the volume of data generated (around 1 GB), not all results are versioned on GitHub.

- results are zipped in a `.tar.gz` file and versioned on Zenodo : `Schild, E. (2021). cognitivefactory/interactive-clustering-comparative-study. Zenodo. https://doi.org/10.5281/zenodo.5648255`.
- a summary of results are stored in `results`.

In order to make a save in a `.tar.gz` file, you can use the following command:
```bash
tar -czf 7_inter_annotators_score_study.tar.gz experiments/ notebook/ results/ README.md
```


## Scientific contribution

- One section of my PhD is dedicated to this study : `Schild, E. (2024, in press). De l'Importance de Valoriser l'Expertise Humaine dans l’Annotation : Application à la Modélisation de Textes en Intentions à l'aide d’un Clustering Interactif. Université de Lorraine.` (Section 4.6)