# Interactive Clustering : 5. Relevance Study

The main goal of this study is to **confirm the relevance** of clustering results.


## Hypotheses

This sub-repository provides an environment to carry out a comparative study of _Interactive Clustering_ implementation around one hypothese.
- **Relevance hypothesis**: _During an annotation methodology based on Interactive Clustering, it is possible for a business expert to quickly assess the relevance of the training set under construction without any ground truth._

In fact, we study three options : (1) manual verification, (2) linguistic analysis with Feature Maximisation method, and (3) automatic topic summary with large language models.


## Experimental protocol

Based on previous execution of _Interactive Clustering_, we will study the business relevance of results.

The first step is manual annotation of relevance, based on several questions :
- "does the cluster have a well-defined main topic?"
- "is the cluster made up of a sufficient number of data?"
- "is the cluster not too noisy?"

Answers are categorized in three levels:
- `usable`: the cluster has (1) a well-defined topic, (2) a sufficient number of data to train a classification model and (3) little noise ; this cluster can therefore be used as is or with few manual modifications;
- `partially usable`: either the cluster is made up of several topics, or it does not contain enough data (less than 20), or it is noisy (at least a quarter of noise); this cluster gives a first base to train a class, but manual work is necessary (adding data, sorting noise, ...);
- `not usable`: either the cluster does not contain or contains too many topics, or it is a singleton cluster or a trash cluster, or this cluster is completely noisy; in any case, it is absolutely not exploitable without a lot of manual work.

The second step is an evolution of manuel verification by adding a linguistic analysis : relevant patterns of each cluster are identified with the Features Maximization Metric, a features selection method.
Each relevant pattern can be highlight in texts, and business relevance annotation can be redo with this help.

Finaly, the last step use a large language model to sum up the topic of each clusters.
Business relevance annotations are redo and are focused on summary (not on clusters themself).

## Implementation

1. Get previous results of convergence, and choose some iterations to analyze.
2. Perform manuel business relevance annotation.
3. Compute linguistic analysis, then perform semi-assisted business relevance annotation.
4. Call large language model to resume topics in clusters, then perform assisted business relevance annotation.
5. Compare each methods.


## Installation and Execution

Follow the description of `README.md` repository file in order to setup your Python/R environment.

Use the `Features Maximization Metric` in order to perform the linguistic analysis : `Schild, E. (2023). cognitivefactory/features-maximization-metric. Zenodo. https://doi.org/10.5281/zenodo.7646382.`

Use `OpenAI` API in order to perform the topic summary with a large language model : `OpenAI. (2023). ChatGPT (Feb 13 version) [Large language model]. https://chat.openai.com`

Then follow notebooks instructions.


## Previous data

Some experiments needs data from previous studies.
Here, constraints annotations and clustering results evolutions are expected from `1_convergence_study` study.
See the export notebook of this study and paste the exported files in the `previous` folder.


## Results

Due to the volume of data generated (around 1 GB), not all results are versioned on GitHub.

- results are zipped in a `.tar.gz` file and versioned on Zenodo : `TODO`.
- a summary of results are stored in `results`.

In order to make a save in a `.tar.gz` file, you can use the following command:
```bash
tar -czf 5_relevance_study.tar.gz experiments/ notebook/ previous/ results/ README.md
```


## Scientific contribution

- One section of my PhD report is dedicated to this study : `TODO`.