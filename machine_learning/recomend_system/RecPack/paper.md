## 0.1. link

- https://dl.acm.org/doi/fullHtml/10.1145/3523227.3551472

## 0.2. title

RecPack: An(other) Experimentation Toolkit for Top-N Recommendation using Implicit Feedback Data

## 0.3. abstract

RecPack is an easy-to-use, flexible and extensible toolkit for top-N recommendation with implicit feedback data. Its goal is to support researchers with the development of their recommendation algorithms, from similarity-based to deep learning algorithms, and allow for correct, reproducible and reusable experimentation. In this demo, we give an overview of the package and show how researchers can use it to their advantage when developing recommendation algorithms.

# 1. Introduction

Over the past decade, recommender systems have become a staple of online user experiences across industries, from media to tourism or e-commerce. At the same time, the domain of recommender systems’ research has evolved from a focus on rating prediction tasks, e.g. the Netflix 1 Million Dollars Prize [5], to top-N recommendation [26]. Today, the state-of-the-art in top-N recommendation advances at a very fast pace. More and more, researchers are encouraged to share their code to enable reproducibility and increase the transparency of their research process [30]. However, this code is often of low quality and/or is shared without instructions on how to set up your environment to allow reproduction of the study [1, 30]. Even if this code allows the experiments to be reproduced, which Trisovic et al. [30] found to be about 25% of the time, this does not mean that the code can also be reused. Code is considered reusable when it allows other researchers to easily conduct similar experiments, e.g., in new contexts or on new data [1]. Reusable code allows science to progress at an even faster pace. Unfortunately writing reusable code requires significant effort on the part of the researcher [1]. With RecPack, our aim is to assist researchers in this important effort.

RecPack is an experimentation toolkit for top-N recommendation using implicit feedback data written in Python, with a familiar interface and clear documentation. Its goal is to support researchers who advance the state-of-the-art in top-N recommendation to write reproducible and reusable experiments. RecPack comes with a range of different datasets, recommendation scenarios, state-of-the-art baselines and metrics. Wherever possible, RecPack sets sensible defaults. For example, the hyperparameters of all recommendation algorithms included in RecPack are initialized to the best performing settings found in the original experiments. The design of RecPack is heavily inspired by the interface of scikit-learn, a popular Python package for classification, regression, and clustering tasks. Data scientists who are familiar with scikit-learn will already have an intuitive understanding of how to work with RecPack. On top of this, RecPack was developed with a production mindset: All contributions are rigorously reviewed and tested. The RecPack maintainers strive to maintain a test coverage of more than ninety percent at all times. Using RecPack, researchers can:

- Quickly develop algorithms by using one of RecPack’s abstract algorithm base classes, which represent popular recommendation paradigms such as factorization and item-to-item similarity.
- Compare their algorithms against state-of-the-art baselines in several different recommendation scenarios using a variety of performance metrics.
- Tune hyperparameters of both baselines and their own implementations with minimal data leakage.

In recent years, many other Python packages for top-N recommendation have been released [e.g. 3, 29, 35]. However, these focus more on the purpose of ‘benchmarking’, i.e., quick and accurate comparisons of state-of-the-art recommendation algorithms. Consequently, they provide access through the use of a configuration language or command-line interface. RecPack on the other hand wishes to support researchers with the development of their own algorithms through repeated refinement, experimentation and bug-fixing in e.g., a Notebook environment.

In this demo, we will give you an overview of the different components of RecPack and how to use them to run your experiments and speed up the development of your own recommendation algorithms.

# 2. RecPack Library

A typical experimentation pipeline for top-N recommendation is shown in Figure 1 1. RecPack provides a dedicated module to support you with each step. In this Section, we will discuss the functionality of each of these modules.

![](https://dl.acm.org/cms/attachment/0b77448a-4224-4264-a434-aef7e6883db2/recsys22-147-fig1.jpg)

Figure 1: Top-N Recommendation Pipeline: First, a dataset is preprocessed and transformed into a user-item interaction matrix. Next, this matrix is split into a training, validation and test dataset. These datasets are then used to first train algorithms and later make recommendations. Finally recommendations are postprocessed, after which performance metrics are computed.

Datasets. RecPack’s datasets provide easy access to many of the most popular collaborative filtering datasets [4, 13, 14, 18, 21, 24, 33]. To use one, simply instantiate a Dataset object, e.g., d = MovieLens25M(). Using RecPack’s datasets saves you time in two ways. First, if the dataset is publicly available RecPack will download it for you. If you already have a copy of the dataset or access to the dataset is restricted, you can specify a path and filename to tell RecPack where to find it. Second, for each dataset a set of default preprocessing filters is defined. Using these default preprocessing filters increases the comparability between your experiments and those of other researchers. Of course, this default filtering can be turned off when creating the Dataset, after which you can add your own preprocessing filters, as detailed in the next paragraph. If your dataset of choice is not included in RecPack we recommend you load it as a pandas DataFrame [34].

Preprocessing. In collaborative filtering, it is customary to first apply preprocessing filters to the raw dataset and then transform it into a user-item interaction matrix [2, 8, 29]. If you use one of RecPack’s built-in datasets with the default preprocessing filters, this is done for you. If you are using your own dataset or wish to override the default preprocessing filters, the first step is to create the filters of your choice.

RecPack currently supports a choice of seven popular preprocessing filters. MinUsersPerItem, MinItemsPerUser and MaxItemsPerUser are used to remove outliers that can negatively impact recommendation performance. NMostPopular an NMostRecent can be used to limit the size of the item catalogue. Deduplicate eliminates repeat interactions by retaining only the first occurrence of every user-item pair. Finally, MinRating selects ratings equal to or higher than a minimum rating value. It is used to transform rating data into implicit feedback data.

To apply these filters to your own DataFrame, create a DataFramePreprocessor. This DataFramePreprocessor will apply the filters and transform the user and item identifiers into consecutive matrix indices. To add filters to either a Dataset or a DataFramePreprocessor, use their add_filter method.

Matrix. In RecPack, a user-item interaction matrix, optionally with timestamps, is represented by an InteractionMatrix object. To create one, call the load method of your Dataset or pass your pandas DataFrame to the DataFramePreprocessor’s process

method. You can also create an InteractionMatrix directly from your own preprocessed pandas DataFrame or a SciPy [32] Sparse csr_matrix. The InteractionMatrix provides different views of your data. For example, you can extract your data as a csr_matrix with user-item interaction counts, the same user-item interactions binarized, or a list of items interacted with for every user, sorted from first to last interaction. The best thing about the InteractionMatrix is that for most experiments you do not have to worry about it. The Scenarios, Algorithms and Pipeline, discussed in the following paragraphs, know exactly what to do with it.

Scenarios. Avoiding data leakage, yet evaluating a recommendation algorithm on a representative task is a difficult challenge. Recommendations are used in many different contexts. In one, it may be most important to make reasonable recommendations for previously unseen users. In another, it is important to get the user's next move exactly right. RecPack comes with an elaborate set of recommendation scenarios, covering virtually all train-validation-test splits encountered in the scientific literature on recommender systems [2, 6, 8, 25, 29]. When you do not need to tune any hyperparameters, pass validation=False to the constructor of your Scenario to split your InteractionMatrix into a training and test set. When you do wish to tune your hyperparameters, pass validation=True instead to obtain a training, validation, and test set. For a complete overview of all supported scenarios, see the documentation.

Algorithms. RecPack currently includes over twenty state-of-the-art recommendation algorithms that cover some of the most popular recommendation paradigms: Item-to-item similarity [7, 12, 22, 31], factorization [2, 17, 23], auto-encoders [19, 27, 28], session-based [10, 16] and time-aware recommendation algorithms [20]. Additionally, it provides three abstract base classes that you can use to accelerate the development of your own algorithm: ItemSimilarityMatrixAlgorithm, FactorizationAlgorithm, and

TorchMLAlgorithm. These base classes implement a significant portion of the shared recommendation logic so that you can focus your efforts on the things that make your recommendation algorithm unique. All of RecPack’s algorithms implement scikit-learn’s BaseEstimator interface: They have fit and predict methods and expect hyperparameters to be passed when the object is created.

Postprocessing. Real world recommender systems often apply postprocessing, in the form of business rules, to the predictions made by the recommendation algorithm. In an e-commerce context, for example, it is customary to exclude sensitive or age-restricted items. In a news context, the recommendations are limited to articles published in the last two days. RecPack currently allows you to either select a subset of items through the use of SelectItems or exclude unwanted items via the ExcludeItems PostFilter.

Metrics. Of course, the ultimate goal of a recommendation experiment is to evaluate the performance of a recommendation algorithm. RecPack comes with a selection of the most commonly used metrics in Top-N ranking [2, 25]. For example, to obtain the NDCG@20 of your algorithm, first create the metric ndcg = NDCGK(20). Next, pass the targets and predictions to the metric's calculate method. To obtain the average NDCG@20 over users, use ndcg.value. However, RecPack’s metrics also allow for a more fine-grained analysis of the performance of your algorithms. To inspect detailed performance results, e.g., the NDCG@20 of individual users, use ndcg.results. For a complete overview of all metrics, see the documentation.

Pipelines. RecPack’s Pipeline helps you to determine the optimal hyperparameters for a given algorithm and dataset, apply postprocessing, and evaluate the performance of your algorithm (and baselines) on a selection of performance metrics. To use it, first create a pb = PipelineBuilder(). Then, pass your Scenario to its set_data_from_scenario method to initialize the training, validation and test set. Use the add_algorithm method to add any algorithms you want to evaluate and add_metric to add performance metrics. To obtain a Pipeline, call p = pb.build() and then use p.run() to run your pipeline. For more advanced use, see the documentation.

# 3. SETUP

RecPack is available for download from PyPI. In the documentation, you will find Getting Started Guides as well as detailed documentation of each of RecPack’s modules. The code is open-source and available on GitLab. RecPack is licensed under AGPL [9]. To raise issues or ask questions about the use of RecPack, check out the source code and contribution guidelines on GitLab.

# 4. DEMO

In the demo, we first implement MLP, a neural matrix factorization algorithm proposed in He et al. [15], to showcase how RecPack’s TorchMLAlgorithm’s base class assists you in the development of your own recommendation algorithms. We then carry out a recommendation experiment. First, we select the MovieLens25M Dataset and transform it into an InteractionMatrix. Next, we split this InteractionMatrix into a training, validation and test dataset using the WeakGeneralization Scenario. Subsequently, we create a PipelineBuilder and start building a Pipeline in which we compare the performance of MLP to WMF and BPRMF, two baselines included in RecPack. We define a parameter grid for hyperparameter tuning, an optimization metric, and evaluation metrics. Finally, we build and run our pipeline and evaluate the performance of each of the algorithms.

# 5. FUTURE WORK

RecPack is being actively maintained and developed. In the near future, its maintainers plan to add beyond-accuracy metrics [11] and hybrid and content-based recommendation algorithms [2].
