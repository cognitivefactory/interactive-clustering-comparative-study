# Interactive Clustering : 3. Annotation Time Study

The main goal of this study is to **estimate the time needed** to annotated constraints.


## Hypotheses

This sub-repository provides an environment to carry out a comparative study of _Interactive Clustering_ implementation around one hypothese.
- **Cost hypothesis**: _It is possible to estimate the required costs of an annotation methodology based on Interactive Clustering to obtain a workable trainset. We will particularly study the costs relating to (1) annotation time,  (2) algorithm execution time, an (3) total time depending on dataset size._

In this study, we focus on annotation time.


## Experimental protocol

The proposed study consists in performing constraints annotation by several operators and estime the time needed for each batch of annotation.

Several instructions are given to annotators:
- *Operator context*: “You are newspapper experts; You want to classify articles into categories based on their title; You do not know precisely which categories you will use to classify your articles; But you know how to identify the similarity of two articles”;
- *Context on the dataset*: "Topics are common newspapper categories; The ground truth contains between 10 and 20 of the most common categories of the press; Ground truth contains between 30 and 100 newspappers per category; You can watch the unannotated dataset as much as you want";
- *Objective of the experiment*: "I want to know the time required to annotate a certain number of constraints; In other words: To annotate 1000 constraints, how long do I need?" ;
- *Annotation instructions*: "Perform at least 15 minutes of annottaion for regularity; If possible, isolate yourself in order to be not disturbed and to not distort the results; For each series, note the annotated time and number of constraints; If you don't know what to annotate (too ambiguous, unknown vocabulary, ...), go to the next one without annotating (you are supposed to be press experts!)".

Then, GLM modelisations are made on annotation time per bacth size and speed evolution over session..

## Implementation

1. Constraints to annotate are randomly selected.
2. Annotation project can be imported in the annotation app with zipped archive.
3. After annotation, time modelization are made based on experiment results.
4. Then, several graphs are made to represent annotation time.


## Installation and Execution

Follow the description of `README.md` repository file in order to setup your `Python` environment.

Use `Interactive Clustering GUI` app in order to perform the annotation : `Schild, E. (2021). cognitivefactory/interactive-clustering-gui. Zenodo. https://doi.org/10.5281/zenodo.4775270.`

Then follow notebooks instructions.


## Results

Due to the volume of data generated (around 1 GB), not all results are versioned on GitHub.

- results are zipped in a `.tar.gz` file and versioned on Zenodo : `TODO`.
- a summary of results are stored in `results`.

In order to make a save in a `.tar.gz` file, you can use the following command:
```bash
tar -czf 3_annotation_time_study.tar.gz experiments/ notebook/ results/ README.md
```


## Scientific contribution

- One section of my PhD report is dedicated to this study : `TODO`.