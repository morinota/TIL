## link

- http://shiftleft.com/mirrors/www.hpl.hp.com/personal/Robert_Schreiber/papers/2008%20AAIM%20Netflix/netflix_aaim08(submitted).pdf

## title

Large-Scale Parallel Collaborative Filtering for the Netflix Prize

## abstract

Many recommendation systems suggest items to users by utilizing the techniques of collaborative filtering (CF) based on historical records of items that the users have viewed, purchased, or rated. Two major problems that most CF approaches have to resolve are scalability and sparseness of the user profiles. In this paper, we describe Alternating-Least-Squares with Weighted-λ-Regularization (ALS-WR), a parallel algorithm that we designed for the Netflix Prize, a large-scale collaborative filtering challenge. We use parallel Matlab on a Linux cluster as the experimental platform. We show empirically that the performance of ALS-WR monotonically increases with both the number of features and the number of ALS iterations. Our ALS-WR applied to the Netflix dataset with 1000 hidden features obtained a RMSE score of 0.8985, which is one of the best results based on a pure method. Combined with the parallel version of other known methods, we achieved a performance improvement of 5.91% over Netflix’s own CineMatch recommendation system. Our method is simple and scales well to very large datasets.

# Introduction

Recommendation systems try to recommend items (movies, music, webpages, products, etc) to interested potential customers, based on the information available. A successful recommendation system can significantly improve the revenue of e-commerce companies or facilitate the interaction of users in online communities. Among recommendation systems, content-based approaches analyze the content (e.g., texts, meta-data, features) of the items to identify related items, while collaborative filtering uses the aggregated behavior/taste of a large number of users to suggest relevant items to specific users. Collaborative filtering is popular and widely deployed in Internet companies like Amazon [16], Netflix [2], Google News [7], and others. 

The Netflix Prize is a large-scale data mining competition held by Netflix for the best recommendation system algorithm for predicting user ratings on movies, based on a training set of more than 100 million ratings given by over 480,000 users to nearly 18,000 movies. Each training data point consists of a quadruple (user, movie, date, rating) where rating is an integer from 1 to 5. The test dataset consists of 2.8 million data points with the ratings hidden. The goal is to minimize the RMSE (root mean squared error) when predicting the ratings on the test dataset. Netflix’s own recommendation system (CineMatch) scores 0.9514 on the test dataset, and the grand challenge is to improve it by 10%.

The Netflix problem presents a number of practical challenges. (Which is perhaps why, as yet, the prize has not been won.) First, the size of the dataset is 100 times larger than previous benchmark datasets, resulting in much longer model training time and much larger system memory requirements. Second, only about 1% of the user-movie matrix has been observed, with the majority of (potential) ratings missing. This is, of course, an essential aspect of collaborative filetering in general. Third, there is noise in both the training and test dataset, due to human behavior – we cannot expect people to to be completely predictable, at least where their feelings about ephemera like movies is concerned. Fourth, the distribution of ratings per user in the training and test datasets are different, as the training dataset spans many years (1995-2005) while the testing dataset was drawn from recent ratings (year 2006). In particular, users with few ratings are more prevalent in the test set. Intuitively, it is hard to predict the ratings of a user who is sparsely represented in the training set.

In this paper, we introduce the problem in detail. Then we describe a parallel algorithm, alternating-least-squares with weighted-λ-regularization. We use parallel Matlab on a Linux cluster as the experimental platform, and our core algorithm is parallelized and optimized to scale up well with large, sparse data. When we apply the proposed method to the Netflix Prize problem, we achieve a performance improvement of 5.91% over Netflix’s own CineMatch system. 

The rest of the paper is organized as follows: in Section 2 we introduce the problem formulation. In Section 3 we describe our novel parallel AlternativeLeast-Squares algorithm. Section 4 describes experiments that show the effectiveness of our approach. Section 5 discusses related work and Section 6 concludes with some future directions.

# Problem Formulation

Let $R = {r_{ij}}_{n_uu \times n_m}$ denote the user-movie matrix, where each element rij represents the rating score of movie j rated by user i with its value either being a real number or missing, nu designates the number of users, and nm indicates the number of movies. In many recommendation systems the task is to estimate some of the missing values in R based on the known values.

#  Our Approaches

## ALS with Weighted-λ-Regularization

##  Parallel ALS with Weighted-λ-Regularizatio

# Performance for the Netflix Prize Problem

## Post-processing

## Experimental Results for ALS

## Other Methods and Linear Blending

# Related Work

## Recommendation Systems

## The Netflix Prize Approaches

##  Low-Rank Approximation

# Concluding Remarks


We introduced a simple parallel algorithm for large-scale collaborative filtering which, in the case of the Netflix prize, performed as well as any single method reported in the literature. Our algorithm is designed to be scalable to very large datasets. Moderately better scores can be obtained by refining the RBM and kNN implementation or using more complicated blending schemes. ALS-WR in particular is able to achieve good results without using date or movie title information. The fast runtime achieved through parallelization is a competitive advantage for model building and parameter tuning in general. It will be interesting to develop a theory to explain why ALS-WR never overfits the data. 

As the world shifts into Internet computing and web applications, large-scale data intensive computing becomes pervasive. Traditional single-machine, singlethread computing is no longer viable, and there is a paradigm shift in computing models. Parallel and/or distributed computing becomes an essential component for any computing environment. Google, the leading Internet company, is building its own proprietary parallel/distributed computing infrastructure, based on MapReduce [8], Google File System [10], Bigtable [6], etc. Most technology companies do not have the capital and expertise to develop an in-house large-scale parallel/distributed computing infrastructure, and prefer instead to use readily available solutions to solve computing infrastructure problems. Hadoop [1] is an open-source project sponsored by Yahoo!, which tries to replicate the Google computing infrastructure with open-source development. We have found parallel Matlab to be flexible and efficient, and very straightforward to program. Thus, from our experience, it seems to be a strong candidate for widespread, easily scalable parallel/distributed computing.
