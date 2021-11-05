# Interactive Clustering Comparative Study

A comparative study of [cognitivefactory-interactive-clustering](https://github.com/cognitivefactory/interactive-clustering/) functionalities on NLP datasets.


## <a name="Description"></a> Quick description

### Description of Interactive Clustering

_Interactive clustering_ is a method intended to assist in the design of a training data set.

This iterative process begins with an unlabeled dataset, and it uses a sequence of two substeps :

1. the user defines constraints on data sampled by the mathine ;

2. the machine performs data partitioning using a constrained clustering algorithm.

Thus, at each step of the process :

- the user corrects the clustering of the previous steps using constraints, and

- the machine offers a corrected and more relevant data partitioning for the next step.

An implementation of this methodology is available here: [cognitivefactory-interactive-clustering](https://github.com/cognitivefactory/interactive-clustering).
For more details, read the [main documentation](https://cognitivefactory.github.io/interactive-clustering/) of this package.

### Goals of Interactive Clustering Comparative Study 

This repository provides a environment to carry out a comparative study of _Interactive Clustering_ implementation around two hypotheses.
- **Hypothesis One**: _An annotation methodology based on Interactive Clustering implementation can converge to a business relevant ground truth_.
- **Hypothesis Two**: _The convergence speed of Interactive Clustering methodology depends on several implementation parameters. We specifically study the influence of data preprocessing, data vectorization, constraints sampling strategy, and constrained clustering algorithm._

In fact, several implementations are available, and the main goal is to determine the best ones.

### Experimetal protocol

The proposed study consists in performing _Interactive Clustering_ iterations in order to annotate an unlabelled dataset, starting from no known constraints and ending when all the possible constraints between questions are defined.
The human annotator is simulated by the algorithm, and annotations are made by comparing with ground truth labels: two questions are annotated with a `MUST_LINK` if they come from the same intent, and with a `CANNOT_LINK` constraint otherwise.

Several parameters can be studied:
- _data preprocessing_: cf. [`cognitivefactory-interactive-clustering.utils.preprocessing`](https://cognitivefactory.github.io/interactive-clustering/reference/utils/preprocessing/)
- _data vectorization_: cf. [`cognitivefactory-interactive-clustering.utils.vectorization`](https://cognitivefactory.github.io/interactive-clustering/reference/utils/vectorization/)
- _constraints sampling algorithms_: cf. [`cognitivefactory-interactive-clustering.sampling.factory`](https://cognitivefactory.github.io/interactive-clustering/reference/sampling/factory/)
- _constrained clustering algorithms_: cf. [`cognitivefactory-interactive-clustering.clustering.factory`](https://cognitivefactory.github.io/interactive-clustering/reference/clustering/factory/)

The study can be done on several datasets, and observations can be done several times with dfferent random seeds.

During _Interactive Clustering_ iterations, the relevance of data segmentation is measured using homogeneity, completeness, and v-measure, computed on the clustering results of each iteration.
Measures are obtained through comparison with the ground truth, corresponding to annotations by business experts prior to the experiment (with no computer guidance). 

To analyse the convergence speed and the effect size of the implementation parameters on the number of annotations required, the authors perform repeated measures ANOVA in R. Post-hoc comparisons are performed using Tukey HSD procedure.
Finally, the optimal set of parameters according to statistical analysis is selected to train a candidate intents classifier.

### Implementation

1. Each experiment to run is modelized by a subfolder path. The path contains the dataset used, the values of parameters studied, and the random seed of the experiment. Several JSON files are needed to store parameters, temporary computations and experiment results.
2. All experiment runs can be parallelized. During the run, clustering evaluation and algorithm speed are stored.
3. When all experiments are run, main effects and post hoc analyzes are made, based on experiment results.
4. Then, best parameters to get the groundtruth can be deduced.

All these steps are implemented in Python and R, and can be run within Jupyter Notebooks.

### Datasets

- "_French trainset for chatbots dealing with usual requests on bank cards_" (Schild 2021): This dataset represents examples of common customer requests relating to bank cards management. It can be used as a training set for a small chatbot intended to process these usual requests.


## <a name="Requirements"></a> Requirements

Interactive Clustering Comparative Study requires:

<details>
<summary>
<a href="https://www.python.org/downloads/">Python 3.8</a> or above.
</summary>
Check that the Python location is in your <code>PATH</code> variable.

For Windows, the following directories should be in your <code> PATH</code>:
- <code>$HOME/AppData/Local/Programs/Python/Python38</code> ;
- <code>$HOME/AppData/Local/Programs/Python/Python38/Scripts</code> ;
- <code>$HOME/AppData/Roaming/Python/Python38/Scripts</code> .
</details>

<details>
<summary>
<a href="https://cloud.r-project.org/index.html">R 4.1</a> or above.
</summary>
Check that the R location is in your <code>PATH</code> variable.

For Windows, if you have installed R in <code>$HOME/AppData/Local/Programs</code>, the following directory should be in your <code>PATH</code>:
- <code>$HOME/AppData/Local/Programs/R/R-4.1.1/bin</code>.
</details>


## <a name="Installation"></a> Installation

Create a virtual environment with `venv`:
```bash
# Upgrade pip.
python3 -m pip install --upgrade pip

# Create a virtual environment.
mkdir -p $HOME/.envs/
python3 -m venv $HOME/.envs/interactive-clustering-comparative-study
```

Install requirements with `pip`, `spacy` and `R`:
```bash
# Activate the virtual environment.
source $HOME/.envs/interactive-clustering-comparative-study/Scripts/activate

# Install Jupyter dependencies.
python -m pip install "jupyter"  # jupyter notebook.
python -m pip install "ipykernel"  # python kernel.
R -e "install.packages('IRkernel', repos='https://cran.r-project.org/')"  # r kernel.
R -e "install.packages('pillar', repos='https://cran.r-project.org/')"
R -e "IRkernel::installspec()"  # r kernel spec settings.

# Install Python dependencies.
python -m pip install "cognitivefactory-interactive-clustering==0.4.2"  # interactive-clustering package.
python -m spacy download "fr_core_news_sm-2.3.0" --direct # spacy language model (the one you want, with version "2.3")
python -m pip install "pandas"  # data management.
python -m pip install "tqdm"  # bar progress.
python -m pip install "matplotlib"  # graph management.

# Install R dependencies.
R -e "install.packages('sjstats', repos='https://cran.r-project.org/')"  # common statistics.
R -e "install.packages('lme4', repos='https://cran.r-project.org/')"  # linear and mixed models.
R -e "install.packages('emmeans', repos='https://cran.r-project.org/')"  # estimated marginal means.
R -e "install.packages('lmerTest', repos='https://cran.r-project.org/')"  # Welch-Satterthwaite effective degrees of freedom analysis.
R -e "install.packages('pbkrtest', repos='https://cran.r-project.org/')"  # Kenward-Roger approach for t test.
```

For developments, some packages can be installed for quality and types checking:
```bash
# Activate the virtual environment.
source $HOME/.envs/interactive-clustering-comparative-study/Scripts/activate

# Install Python dependencies.
python -m pip install "black>=20.8b1"  # code formatting.
python -m pip install "black[jupyter]"  # code formatting.
python -m pip install "isort>=5.7.0"  # code formatting.
python -m pip install "mypy>=0.812"  # type checking.
python -m pip install "darglint>=1.5.8"  # quality checking.
python -m pip install "autoflake>=1.4"  # quality checking.
python -m pip install "flake8-bandit>=2.1"  # quality checking.
python -m pip install "flake8-black>=0.2"  # quality checking.
python -m pip install "flake8-bugbear>=21.3"  # quality checking.
python -m pip install "flake8-builtins>=1.5"  # quality checking.
python -m pip install "flake8-comprehensions>=3.4"  # quality checking.
python -m pip install "flake8-docstrings>=1.5"  # quality checking.
python -m pip install "flake8-pytest-style>=1.4"  # quality checking.
python -m pip install "flake8-string-format>=0.3"  # quality checking.
python -m pip install "flake8-tidy-imports>=4.2"  # quality checking.
python -m pip install "flake8-variables-names>=0.0"  # quality checking.
python -m pip install "pep8-naming>=0.11.1"  # quality checking.
python -m pip install "wps-light>=0.15.2"  # quality checking.
```

## <a name="Execution"></a> Execution

```bash
# Activate the virtual environment.
source $HOME/.envs/interactive-clustering-comparative-study/Scripts/activate

# Run jupyter at http://localhost:8888/tree
jupyter notebook
```

1. Launch `1_Initialize_experiments_environments.ipynb` to set up experiments environments: it creates several subfolders for each combination of parameters to test, and initialize JSON files to store parameters, temporary computations and experiment results.
2. Launch `2_Run_and_evaluate_experiments.ipynb` to run all experiments that have been set up with the previous notebook. Experiment runs are parallelized.
3. Launch `3_Analyze_main_effecets_and_post_hoc.ipynb` to analyze main effects and post hoc based on experiment results.

## <a name="Development"></a> Development

To check code quality of scripts and notebooks, run the following command:
```bash
./scripts/code-quality-checking.sh
```


## <a name="References"></a> References

- **Interactive Clustering**:
    - Theory: `Schild, E., Durantin, G., Lamirel, J.C., & Miconi, F. (2021). Conception itérative et semi-supervisée d'assistants conversationnels par regroupement interactif des questions. In EGC 2021 - 21èmes Journées Francophones Extraction et Gestion des Connaissances. Edition RNTI. ⟨hal-03133007⟩`
	- Implementation: `Schild, E. (2021). cognitivefactory/interactive-clustering. Zenodo. https://doi.org/10.5281/zenodo.4775251`

- **Datasets**:
    - Bank cards management: `Schild, E. (2021). French trainset for chatbots dealing with usual requests on bank cards (Version 1.0.0) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4769950.`

- **Experimental protocol**:
    - Evaluation with _Sklearn_: `Buitinck, L., Louppe, G., Blondel, M., Pedregosa, F., Mueller, A., Grisel, O., Niculae, V., Prettenhofer, P., Gramfort, A., Grobler, J., Layton, R., Vanderplas, J., Joly, A., Holt, B., & Varoquaux, G. (2013). API design for machine learning software: experiments from the scikit-learn project. ArXiv, abs/1309.0238.`
    - Visualization with _matplotlib_: `Caswell, T. A., Droettboom, M., Lee, A., Sales de Andrade, E., Hunter, J., Hoffmann, T., & Ivanov, P. (2021). matplotlib/matplotlib: REL: v3.3.4 (Version v3.3.4). Zenodo. http://doi.org/10.5281/zenodo.4475376`
    - Jupyter Notebooks: `Kluyver, T., Ragan-Kelley, B., Pérez, F., Granger, B., Bussonnier, M., Frederic, J., Kelley, K., Hamrick, J., Grout, J., Corlay, S., Ivanov, P., Avila, D., Abdalla, S., Willing, C. & Jupyter development team, (2016) Jupyter Notebooks - a publishing format for reproducible computational workflows. In Positioning and Power in Academic Publishing: Players, Agents and Agendas. IOS Press. pp. 87-90 . ⟨doi:10.3233/978-1-61499-649-1-87⟩.`
