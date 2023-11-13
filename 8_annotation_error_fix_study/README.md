# Interactive Clustering : 8. Annotation errors and conflict fix Study

The main goal of this study is to **evaluate errors impact** and **verify conflicts fix importance** on labeling.


## Hypotheses

This sub-repository provides an environment to carry out a comparative study of _Interactive Clustering_ implementation around one hypothese.
- **Robustness hypothesis**: _During an annotation methodology based on Interactive Clustering, it is possible to estimate the rate of inconsistencies appearing in constraints and their impact on the results of the method._

In this study, we focus on the impact of annotation errors during constraints annotation and the importance of conflicts corections.


## Experimental protocol

The proposed study consists in performing _Interactive Clustering_ iterations with specific settings in order to annotate an unlabeled dataset, starting from no known constraints and ending when all the possible constraints between questions are defined.
The human annotator is simulated by the algorithm, and annotations are made by comparing with ground truth labels: two questions are annotated with a `MUST_LINK` if they come from the same intent, and with a `CANNOT_LINK` constraint otherwise. During annotation, some wrong annotations are inserted to simulate operator mistakes (groundtruth is the reference).

The study focus on impact of errors rate in clustering results.
If annotation conflicts are detected, two strategies are compared : (1) no correction and (2) correction with true annotation.

To analyse errors impact, we compare evolution of groundtruth agreement for error experiments and analyze the signifiance of correction.


## Implementation

1. Run full _Interactive Clustering_ annotation methodology and insert a fixed rate of errors at each iteration. If conflicts error, use the experiment strategy to ignore or fix it.
2. When all experiments are run, display mean evolution of groundtruth agreement per errors rate and per conflicts fix strategy.
3. Compare evolution and discuss the signifiance of correction.

All these steps are implemented in `Python`, and can be run within `Jupyter Notebooks`.


## Installation and Execution

Follow the description of `README.md` repository file in order to setup your Python/R environment.

Then follow notebooks instructions.


## Previous data

Some experiments needs data from previous studies.
Here, constraints annotations are expected from `1_convergence_study` study.
See the export notebook of this study and paste the exported files in the `previous` folder.


## Results

Due to the volume of data generated (around 30 GB), not all results are versioned on GitHub.

- results are zipped in a `.tar.gz` file and versioned on Zenodo : `Schild, E. (2021). cognitivefactory/interactive-clustering-comparative-study. Zenodo. https://doi.org/10.5281/zenodo.5648255`.
- a summary of results are stored in `results`.

In order to make a save in a `.tar.gz` file, you can use the following command:
```bash
tar -czf 8_annotation_error_fix_study.tar.gz experiments/ notebook/ previous/ results/ README.md
```


## Scientific contribution

- One section of my PhD is dedicated to this study : `Schild, E. (2024, in press). De l'Importance de Valoriser l'Expertise Humaine dans l’Annotation : Application à la Modélisation de Textes en Intentions à l'aide d’un Clustering Interactif. Université de Lorraine.` (Section 4.6)