## 0.1. link

- https://arxiv.org/format/1611.04666

## 0.2. title

A Generic Coordinate Descent Framework for Learning from Implicit Feedback

## 0.3. abstract

In recent years, interest in recommender research has shifted from explicit feedback towards implicit feedback data. A diversity of complex models has been proposed for a wide variety of applications. Despite this, learning from implicit feedback is still computationally challenging. So far, most work relies on stochastic gradient descent (SGD) solvers which are easy to derive, but in practice challenging to apply, especially for tasks with many items. For the simple matrix factorization model, an efficient coordinate descent (CD) solver has been previously proposed. However, efficient CD approaches have not been derived for more complex models. In this paper, we provide a new framework for deriving efficient CD algorithms for complex recommender models. We identify and introduce the property of k-separable models. We show that k-separability is a sufficient property to allow efficient optimization of implicit recommender problems with CD. We illustrate this framework on a variety of state-of-the-art models including factorization machines and Tucker decomposition. To summarize, our work provides the theory and building blocks to derive efficient implicit CD algorithms for complex recommender models.

# 1. Introduction

In recent years, the focus of recommender system research has shifted from explicit feedback problems such as rating prediction to implicit feedback problems. Most of the signal that a user provides about her preferences is implicit. Examples for implicit feedback are: a user watches a video, clicks on a link, etc. Implicit feedback data is much cheaper to obtain than explicit feedback, because it comes with no extra cost for the user and thus is available on a much larger scale. However, learning a recommender system from implicit feedback is computationally expensive because the observed actions of a user need to be contrasted against all the non-observed actions [5, 13].

Stochastic gradient descent (SGD) and coordinate descent (CD) are two widely used algorithms for large scale machine learning. Both algorithms are considered state-of-the-art for learning matrix factorization models from implicit feedback and have been studied extensively. SGD and CD have shown different strengths and weaknesses on various data sets [4, 17, 16, 8, 25, 15, 22, 26]. While SGD is available as a general framework to optimize a broad class of models [13], CD is only available for a few simple models [5, 10]. In fact, it is even unknown if CD can be used to efficiently optimize complex recommender models. Our work closes this gap and identifies a model property called k-separability, that is a sufficient condition to allow efficient learning from implicit feedback. Based on k-separability, we provide a general framework to derive efficient implicit CD solvers.

Our paper is organized as follows: First, we introduce the problem of learning from implicit feedback and show that the number of implicit training examples makes the application of standard algorithms challenging. Next, we provide our general framework for efficient implicit learning with CD. We identify k-separability of a model as a sufficient property to make efficient learning feasible and introduce iCD, a generic learning algorithm for k-separable models. In Section 5, we show how to apply iCD to a diverse set of models, including, matrix factorization (MF), factorization machines (FM) and tensor factorization. This section serves both as solutions to popular models as well as a guide for applying the framework to other complex recommender models.

To summarize, our contributions are:

- We identify a basic property of recommender models that allows efficient CD learning from implicit data.
- We provide iCD, a framework to derive efficient implicit CD algorithms.
- We apply the framework and derive algorithms for MF, MF with side information, FM, PARAFAC and Tucker Decomposition.

# 2. Related Work

Since several years, matrix factorization (MF) is regarded as the most effective, basic recommender system model. Two optimization strategies dominate the research on MF from implicit feedback data. The first one is Bayesian Personalized Ranking (BPR) [13], a stochastic gradient descent (SGD) framework, that contrasts pairs of consumed to nonconsumed items. The second one is coordinate descent (CD) also known as alternating least squares on an elementwise loss over both the consumed and non-consumed items [5]. In terms of the loss formulation, BPR’s pairwise classification loss is better suited for ranking whereas CD loss is better suited for numerical data. With regard to the optimization task, both techniques face the same challenge of learning over a very large number of training examples. BPR tackles this issue by sampling negative items, but it has been shown that BPR has convergence problems when the number of items is large [7, 12]. It requires more complex, nonuniform, sampling strategies for dealing with this problem [12, 6]. On the other hand, for CD-MF, Hu et al. [5] have derived an efficient algorithm that allows to optimize over the large number of non-consumed items without any cost. This computational trick is exact and does not involve sampling. Many authors have compared both CD-MF and BPR-MF on a variety of datasets and some work reports better quality for BPR-MF [4, 17, 16, 8] whereas for other problems CD-MF works better [8, 25, 15, 22, 26]. This large body of results indicates that the advantages of CD and BPR are orthogonal and both approaches have their merits.

Our discussion so far was focused on learning matrix factorization models from implicit data. Shifting from simple matrix factorization to more complex factorization models has shown large success in many implicit recommendation problems [2, 4, 18, 1, 9, 24]. However, work on complex factorization models relies almost exclusively on SGD optimization using the generic BPR framework. Our work, provides the theory as well as a practical framework for deriving CD learners for such complex models. Like CD for MF, our generic algorithm is able to optimize on all nonconsumed items without explicitly iterating over them. To summarize, our paper enables researchers and practitioners to apply CD in their work and gives them a choice between the advantages of BPR and CD.

# 3. Problem Statement

Let I be a set of items and C a set of contexts. Let S be a set of observed feedback where a tuple (c, i, y, α) ∈ S indicates that in context c, a score y has been assigned to item i with confidence α. See Figure 1 for an illustration. We use a general notation of context which can include for instance user, time, location, attributes, history, etc. Section 5 and Section 6 show more examples for context.

## 3.1. Recommender Model

A recommender model ˆy : C × I → R is a function that assigns a score to every context-item pair. The model ˆy is parameterized by a set of model parameters Θ. The model ˆy is typically used to decide which items to present in a given context.
The learning task is to find the values of the model parameters that minimize a loss over the data S, e.g., a squared loss

$$
formula (1)
$$

where λθ is an regularization constant for parameter θ.

## 3.2. Coordinate Descent Algorithm

Objective (1) can be minimized by coordinate descent (CD). CD iterates through the model parameters and updates one parameter at a time. For a selected parameter θ ∈ Θ, CD computes the first L 0 and second derivative L 00 of L with respect to the selected coordinate θ:

$$
\tag{2}
$$

$$
\tag{3}
$$

and performs a Newton update step:

$$
\tag{4}
$$

where η ∈ (0, 1] is the step size. For multilinear models, a full step, i.e., η = 1, can be chosen without risking divergence [11]. All models in Section 5 fall into this category. Such CD algorithms have been well studied and the runtime complexity is typically linear in the complexity of the training examples and embedding dimension. For MF, [23] shows a complexity of O(|S| k) and for FM, [11] derives a complexity of O(NZ (X) k) where NZ (X) is the number of non-zero entries in the design matrix X. The linear runtime complexity in the number of training examples makes these algorithms well suited for explicit recommendation settings, however, they become infeasible for implicit problems.

## 3.3. Learning from Implicit Feedback

In an implicit recommendation problem, the non-consumed items are meaningful and cannot be ignored. For instance, in Figure 1 (right), the data depicts how often each item was consumed in a context in the past. The non-consumed items, i.e., the ones with a count of zero, are useful to learn user preferences. To formalize, the training data $S_{impl}$ of an implicit problem consists of a set $S^+$ of observed feedback and all the non-consumed tuples $S^0$

$$
\tag{5}
$$

with

$$
\tag{6}
$$

$S^+$ contains the observed feedback and is of much smaller scale than Simpl, usually $|S^+| <<|C||I|$.

The implicit learning problem can be stated as minimizing the objective in eq. (1) over the implicit data $S_{impl}$. While possible in theory, in practice, it is infeasible to apply the learning algorithms of Section 3.2 to this problem due to their linear computational runtime in the size of the training data which is $|S_{impl}| = |C||I|$ for implicit problems. Our paper shows how to derive efficient CD algorithms for optimizing eq. (1) over implicit data.

# 4. Generic Coordinate Descent ALgorithm for Implicit Feedback

## 4.1. Implicit Regularizer

## 4.2. iCD Algorithm for k-separable Models

# 5. Applications

## 5.1. Matrix Factorization

## 5.2. Feature-Based Factorization Models

### 5.2.1. MF with Side Information (MFSI)

### 5.2.2. Factorization Machines

## 5.3. Tensor Factorization

### 5.3.1. Parallel Factor Analysis (PARAFAC)

### 5.3.2. Tucker Decomposition

# 6. Experiments

## 6.1. Expemrimental Setup

## 6.2. Result

### 6.2.1. Cold-Start Recommendation

### 6.2.2. Offline Recommendation

### 6.2.3. Instant Recommendation

In large-scale industrial applications, online training is often not feasible due to complex serving stacks. Commonly, models are periodically trained offline (e.g., every day or week) and applied on a stream of user interactions. When the model is queried to generate recommendations for a user, all feedback until the current time is taken into account for prediction. We simulate this setting by choosing a global cutoff time where all the events before the cutoff are used for training and all the remaining ones for evaluation. 

In such settings, models relying on user ids, such as MF, cannot capture recent feedback. Instead, describing a user by the sequence of previously watched videos allows for instant personalization. Such a model can be configured using a feature-based FM model (Section 5.2) and we experiment with four configurations (1) iCD-FM A: FM using user attributes, (2) iCD-FM P: a sequential FM based on the previously watched video, (3) iCD-FM H: a FM based on all previously watched videos, (4) iCD-FM A+P+H: an FM combining all signals. As expected, the complex FM model with all features achieves the best quality. Again, we would like to note the generality of the iCD framework, which enables flexible feature engineering.

## 6.3. Computational Costs

As stated in Section 3.3, any conventional CD solver, e.g. [11], could solve the implicit feedback problem. Now, we substantiate that this is infeasible because of the large number of implicit examples. Figure 8 compares the computational cost for learning an FM with a conventional CD to the costs of iCD on our dataset with 70k items. We use three different context features from Figure 6. The plot shows relative costs to iCD-FM P. For all three context choices, conventional CD shows four orders of magnitude higher compuational costs than iCD. The empirical measured runtime for iCD was in the order of minutes; consequently, CD’s four order of magnitude increase in runtime translates to weeks of training for each iteration. Clearly, using a conventional CD solver to optimize the implicit loss directly is infeasible.

# 7. Conclusion

In this work, we have presented a general, efficient framework for learning recommender system models from implicit feedback. First, we have shown that learning from implicit feedback can be reformulated as optimizing a cheap explicit loss and an expensive implicit regularizer. Then we have introduced the concept of k-separable models. We have shown that the implicit regularizer of any k-separable model can be computed efficiently without iterating over all context-item pairs. Finally, we have shown that many popular recommender models are k-separable, including matrix factorization, factorization machines and tensor factorization. Moreover, we have provided efficient learning algorithms for these models based on our framework. Our framework is not limited to the models discussed in the paper but designed to serve as a general blueprint for deriving learning algorithms for recommender systems.
