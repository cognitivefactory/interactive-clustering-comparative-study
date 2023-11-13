# Interactive Clustering : 6. Rentability Study

The main goal of this study is to **predict the rentability** of one more iteration.


## Hypotheses

This sub-repository provides an environment to carry out a comparative study of _Interactive Clustering_ implementation around one hypothese.
- **Rentability hypothesis**: _During an annotation methodology based on Interactive Clustering, it is possible to estimate the profitability of an additional iteration of the method, and thus to establish cases of stopping independent of a ground truth to obtain a satisfactory learning base._

In fact, we study two options : (1) evolution of agreement between annotation and previous clustering, (2) evolution of similarity between two successive clusterings.

## Experimental protocol

Based on previous execution of _Interactive Clustering_, we will study the rentability of each new iteration of the method.

Two methods are used :
- evolution of agreement between annotation and previous clustering : if annotations are different from clustering suggestion, then there are still corrections to apply ; otherwise, if annotation and clustering results agreed, then no more corrections are needed.
- evolution of similarity between two successive clusterings : if clustering do not change after several iterations, then clustering is stable and no more corrections are needed.

To choose the best solution, we compute the correction between the evolution of these measures and the evolution of v-measure.


## Implementation

1. Get previous results of convergence, and choose some iterations to analyze.
2. Iteration by iteration, compute agreement score between annotation and previous clustering, then compute correlation between this agreement and the groundtruth v-measure.
3. Iteration by iteration, compute consecutive clustering comparison, then compute correlation between this agreement and the groundtruth v-measure.
4. Compare each methods and display diagrams of evolutions.

All these steps are implemented in `Python`, and can be run within `Jupyter Notebooks`.


## Installation and Execution

Follow the description of `README.md` repository file in order to setup your Python/R environment.

Then follow notebooks instructions.


## Previous data

Some experiments needs data from previous studies.
Here, constraints annotations and clustering results evolutions are expected from `1_convergence_study` study.
See the export notebook of this study and paste the exported files in the `previous` folder.


## Results

Due to the volume of data generated (around 2 GB), not all results are versioned on GitHub.

- results are zipped in a `.tar.gz` file and versioned on Zenodo : `Schild, E. (2021). cognitivefactory/interactive-clustering-comparative-study. Zenodo. https://doi.org/10.5281/zenodo.5648255`.
- a summary of results are stored in `results`.

In order to make a save in a `.tar.gz` file, you can use the following command:
```bash
tar -czf 6_rentability_study.tar.gz experiments/ notebook/ previous/ results/ README.md
```


## Scientific contribution

- One section of my PhD report is dedicated to this study : `Schild, E. (2024, in press). De l'Importance de Valoriser l'Expertise Humaine dans l’Annotation : Application à la Modélisation de Textes en Intentions à l'aide d’un Clustering Interactif. Université de Lorraine.` (Section 4.5)