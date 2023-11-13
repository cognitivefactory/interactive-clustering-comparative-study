# Interactive Clustering : 9. Annotation subjectivity Study

The main goal of this study is to **estimate the labeling difference impact** on clustering results.


## Hypotheses

This sub-repository provides an environment to carry out a comparative study of _Interactive Clustering_ implementation around one hypothese.
- **Robustness hypothesis**: _During an annotation methodology based on Interactive Clustering, it is possible to estimate the rate of inconsistencies appearing in constraints and their impact on the results of the method._

In this study, we focus on the impact of annotation subjectivity during constraints annotation and the importance of annotation reviews.


## Experimental protocol

The proposed study consists in performing _Interactive Clustering_ iterations with specific settings in order to annotate an unlabeled dataset, starting from no known constraints and ending when all the possible constraints between questions are defined.
The human annotator is simulated by the algorithm, and annotations are made by comparing with ground truth labels: two questions are annotated with a `MUST_LINK` if they come from the same intent, and with a `CANNOT_LINK` constraint otherwise. During annotation, some wrong annotation are inserted to simulate operator subjectivity (no error runs are reference).

The study focus on impact of difference rate in clustering results.
If annotation conflicts are detected, we choose to fix them by applying the groundtruth annotation.
Several dataset size are use to estimate the impact of difference according to number of data.

To analyse difference impact, we compare agreement evolution between clustering reference and clustering with difference.


## Implementation

1. Run full _Interactive Clustering_ annotation methodology and insert a fixed rate of differences at each iteration. If conflicts error, fix them according to groundtruth.
2. When all experiments are run, display mean evolution of clustering agreement per difference rate and per dataset size.
3. Compare evolution and discuss review strategies to limit subjectivity.

All these steps are implemented in `Python`, and can be run within `Jupyter Notebooks`.


## Installation and Execution

Follow the description of `README.md` repository file in order to setup your Python/R environment.

Then follow notebooks instructions.


## Previous data

Some experiments needs data from previous studies.
Here, constraints annotations are expected from `4_constraints_number_study` study.
See the export notebook of this study and paste the exported files in the `previous` folder.


## Results

Due to the volume of data generated (around 80 GB), not all results are versioned on GitHub.

- results are zipped in a `.tar.gz` file and versioned on Zenodo : `Schild, E. (2021). cognitivefactory/interactive-clustering-comparative-study. Zenodo. https://doi.org/10.5281/zenodo.5648255`.
- a summary of results are stored in `results`.

In order to make a save in a `.tar.gz` file, you can use the following command:
```bash
tar -czf 9_annotation_subjectivity_study.tar.gz experiments/ notebook/ previous/ results/ README.md
```


## Scientific contribution

- One section of my PhD is dedicated to this study : `Schild, E. (2024, in press). De l'Importance de Valoriser l'Expertise Humaine dans l’Annotation : Application à la Modélisation de Textes en Intentions à l'aide d’un Clustering Interactif. Université de Lorraine.` (Section 4.6)