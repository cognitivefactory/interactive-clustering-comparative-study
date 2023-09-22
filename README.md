# Interactive Clustering : Comparative Studies

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.5648255.svg)](https://doi.org/10.5281/zenodo.5648255)

Several comparative studies of [cognitivefactory-interactive-clustering](https://github.com/cognitivefactory/interactive-clustering/) functionalities on NLP datasets.


## Quick description

### Description of Interactive Clustering

_Interactive clustering_ is a method intended to assist in the design of a training data set.

This iterative process begins with an unlabeled dataset, and it uses a sequence of two substeps :

1. the user defines constraints on data sampled by the machine ;

2. the machine performs data partitioning using a constrained clustering algorithm.

Thus, at each step of the process :

- the user corrects the clustering of the previous steps using constraints, and

- the machine offers a corrected and more relevant data partitioning for the next step.

An implementation of this methodology is available here: [cognitivefactory-interactive-clustering](https://github.com/cognitivefactory/interactive-clustering).
For more details, read its [main documentation](https://cognitivefactory.github.io/interactive-clustering/).

Furthermore, a web application based on Interactive Clustering Methodologoy is available here: [cognitivefactory-interactive-clustering-gui](https://github.com/cognitivefactory/interactive-clustering-gui).
For more details, read its [main documentation](https://cognitivefactory.github.io/interactive-clustering-gui/).

### Description of studies

Several studies are provided here:

1. `efficience`: Aims to **confirm the technical efficience** of the method by verifying its convergence to a ground truth and by finding the best implementation to increase convergence speed.
2. `computation time`: Aims to **estimate the time needed** for algorithms to reach their objectives.
3. `annotation time`: Aims to **estimate the time needed** to annotated constraints.
4. `constraints number`: Aims to **estimate the number of constraints needed** to have a relevant annotated dataset.
5. `relevance`: Aims to **confirm the relevance** of clustering results.
6. `rentability`: Aims to **predict the rentability** of one more iteration.
7. `conflicts fix`: Aims to **verify conflicts fixes importance** on labeling error.
8. `annotation errors`: Aims to **estimate the labeling error impact** on clustering results.
9. `inter annotator`: Aims to **estimate the inter-annotators score** during constraints annotation.

### Datasets

Used datasets are:

- "_French trainset for chatbots dealing with usual requests on bank cards_" (Schild, 2021): This dataset represents examples of common customer requests relating to bank cards management. It can be used as a training set for a small chatbot intended to process these usual requests.
- "_MLSUM: The Multilingual Summarization Corpus_" (Scialom et al., 2020): A subset of newspapers articles in most popular category. It can be used to train a small newspaper classifier.


## Requirements

Interactive Clustering Comparative Study requires:

<details>
<summary>
<a href="https://www.python.org/downloads/">Python 3.8</a> or above.
</summary>
Check that the Python location is in your <code>PATH</code> variable.

For Windows, the following directories should be in your <code>PATH</code>:
- <code>$HOME/AppData/Local/Programs/Python/Python38</code> ;
- <code>$HOME/AppData/Local/Programs/Python/Python38/Scripts</code> ;
- <code>$HOME/AppData/Roaming/Python/Python38/Scripts</code> .
</details>

<details>
<summary>
<a href="https://cloud.r-project.org/index.html">R 4.Y</a> or above.
</summary>
Check that the R location is in your <code>PATH</code> variable.

For Windows, it can be:
- <code>C:\Program Files\R\R-4.Y.Z/bin</code>.
- <code>$HOME/AppData/Local/Programs/R/R-4.Y.Z/bin</code>.
</details>


## Installation

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
python -m pip install "cognitivefactory-interactive-clustering==0.5.4"  # interactive-clustering package.
python -m spacy download "fr_core_news_sm-3.1.0" --direct # spacy language model (the one you want, with version "3.1.x").
python -m pip install "cognitivefactory-features-maximization-metric==0.1.1"  # Features Maximization Metric.
python -m pip install "datasets"  # Hugging Face datasets.
python -m pip install "matplotlib"  # graph management.
python -m pip install "openai"  # llm call.
python -m pip install "openpyxl"  # xlsx file management.
python -m pip install "pandas"  # data management.
python -m pip install "simpledorff"  # krippendorff's alpha.
python -m pip install "tqdm"  # bar progress.
python -m pip install "xlsxwriter"  # xlsx file management.

# Install R dependencies.
R -e "install.packages('sjstats', repos='https://cran.r-project.org/')"  # common statistics.
R -e "install.packages('lme4', repos='https://cran.r-project.org/')"  # linear and mixed models.
R -e "install.packages('emmeans', repos='https://cran.r-project.org/')"  # estimated marginal means.
R -e "install.packages('lmerTest', repos='https://cran.r-project.org/')"  # Welch-Satterthwaite effective degrees of freedom analysis.
R -e "install.packages('pbkrtest', repos='https://cran.r-project.org/')"  # Kenward-Roger approach for t test.
R -e "install.packages('pbnm', repos='https://cran.r-project.org/')"  # parametric bootstrap, see https://support.posit.co/hc/en-us/articles/200711843-Working-Directories-and-Workspaces-in-the-RStudio-IDE#:~:text=The%20current%20working%20directory%20is,getwd()%20in%20the%20console.
```

For developments, some packages can be installed for quality and types checking:
```bash
# Activate the virtual environment.
source $HOME/.envs/interactive-clustering-comparative-study/Scripts/activate

# Install Python dependencies.
python -m pip install "black>=21.10b0"  # code formatting.
python -m pip install "black[jupyter]"  # code formatting.
python -m pip install "isort>=5.7.0"  # code formatting.
python -m pip install "mypy>=0.910"  # type checking.
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


## Execution

Launch `Jupyter Notebook` with:
```bash
# Activate the virtual environment.
source $HOME/.envs/interactive-clustering-comparative-study/Scripts/activate

# Run jupyter at http://localhost:8888/tree (the port number can change)
jupyter notebook
```

Then follow notebooks instructions.

Use the command `tar -czf ../experiments.tar.gz ../experiments/` to wrap results in a `.tar.gz` file,
and use `tar -xzf ../experiments.tar.gz -C ../` to unwrap them.


## Development

To check code quality of scripts and notebooks:
```bash
./scripts/code-quality-checking.sh
```


## References

- **Interactive Clustering**:
    - Theory: `Schild, E., Durantin, G., Lamirel, J.C., & Miconi, F. (2021). Conception itérative et semi-supervisée d'assistants conversationnels par regroupement interactif des questions. In EGC 2021 - 21èmes Journées Francophones Extraction et Gestion des Connaissances. Edition RNTI. <hal-03133007>`
	- Implementation: `Schild, E. (2021). cognitivefactory/interactive-clustering. Zenodo. https://doi.org/10.5281/zenodo.4775251`

- **Datasets**:
    - Bank cards management: `Schild, E. (2021). French trainset for chatbots dealing with usual requests on bank cards [Data set]. Zenodo. http://doi.org/10.5281/zenodo.4769949.`
	- MLSUM: `Scialom, T., Dray, P.-A., Lamprier, S., Piwowarski, B., & Staiano, J. (2020). MLSUM: The Multilingual Summarization Corpus (Version 1). arXiv. https://doi.org/10.48550/ARXIV.2004.14900.`

- **Experimental protocol**:
    - Evaluation with _Sklearn_: `Buitinck, L., Louppe, G., Blondel, M., Pedregosa, F., Mueller, A., Grisel, O., Niculae, V., Prettenhofer, P., Gramfort, A., Grobler, J., Layton, R., Vanderplas, J., Joly, A., Holt, B., & Varoquaux, G. (2013). API design for machine learning software: experiments from the scikit-learn project. ArXiv, abs/1309.0238.`
    - Visualization with _matplotlib_: `Caswell, T. A., Droettboom, M., Lee, A., Sales de Andrade, E., Hunter, J., Hoffmann, T., & Ivanov, P. (2021). matplotlib/matplotlib: REL: v3.3.4 (Version v3.3.4). Zenodo. http://doi.org/10.5281/zenodo.4475376`
    - Jupyter Notebooks: `Kluyver, T., Ragan-Kelley, B., Pérez, F., Granger, B., Bussonnier, M., Frederic, J., Kelley, K., Hamrick, J., Grout, J., Corlay, S., Ivanov, P., Avila, D., Abdalla, S., Willing, C. & Jupyter development team, (2016) Jupyter Notebooks - a publishing format for reproducible computational workflows. In Positioning and Power in Academic Publishing: Players, Agents and Agendas. IOS Press. pp. 87-90 . ⟨doi:10.3233/978-1-61499-649-1-87⟩.`
