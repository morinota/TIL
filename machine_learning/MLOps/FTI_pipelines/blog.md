## link

https://www.hopsworks.ai/post/mlops-to-ml-systems-with-fti-pipelines

## title

From MLOps to ML Systems with Feature/Training/Inference Pipelines

The Mental Map for MLOps to align your Data-ML-Product Teams

## abstract

Maps help us navigate the world, and communicate ideas, helping us get faster to our destination. Somewhere along the way, MLOps got lost in promoting “waterfall software architecture” maps for ML Systems that include a kitchen sink of requirements. Existing approaches to MLOps prevent teams from following DevOps principles of starting with a small working system and iteratively improving it. In this article, we present a new mental map for ML Systems as three independent ML pipelines: feature pipelines, training pipelines, and inference pipelines that share a common storage layer for the ML artifacts they produce and consume (features, models). In contrast to existing MLOps architectures, we provide a unified architecture that describes both batch ML systems and real-time ML systems. This makes it easier for developers to move to/from batch and real-time systems, and provides clear interfaces between the ML pipelines, enabling easier collaboration between the data, ML, and product teams that work together to develop and operate ML systems. Compared to existing MLOps architectures, the feature/training/inference pipeline architecture helps you get faster to a minimal working ML system that can be iteratively improved, while following best practices for automated testing, versioning, and monitoring. There are now hundreds of ML systems that have been built by the community based on our architecture, showing that building and shipping ML systems is easier if you follow a mental map that starts with building pipelines rather than starting by building ML infrastructure.

# Introduction

“It's impressive how far you can go with contemporary tools like @modal_labs, @huggingface, and @hopsworks! In 2017, having a shared pipeline for training and prediction data that updated automatically and made models available as a UI and an API was a groundbreaking stack at Uber. Now, it's a standard part of a well-done student project.” Charles Frye, Full Stack Deep Learning course leader.

In a course I gave at KTH in 2022/23, students developed a full ML system in only 2 weeks that solved a prediction problem for a novel non-static data source of their choice. As Charles suggests in the above quote, leveraging ML infrastructure makes it easier to build ML systems. You can write a Python program that scrapes data from the Internet and, with a few annotations, runs on a daily schedule with Modal. The program can write the features it computes as DataFrames to Hopsworks Feature Store. From there, a notebook can be used to train a model that is saved in Hopsworks (or any model registry). And, finally, a third Python program uses the trained model to make predictions with new inference data (for example, the data scraped today) read from the Feature Store, and displays the predictions in a nice UI or Dashboard (e.g., written in the Streamlit or Taipy). Some examples of prediction problems were predicting air quality, water levels, snow depth, football scores, electricity demand, and sentiment for posts.

#
