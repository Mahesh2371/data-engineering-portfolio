# Machine Learning Concepts

## What is supervised learning?
Supervised learning is a type of machine learning where the model is trained on labeled data. The algorithm learns to map input features to output labels based on example input-output pairs.

## What is unsupervised learning?
Unsupervised learning involves training a model on data without labels. The model tries to find hidden patterns or structures in the data. Common techniques include clustering and dimensionality reduction.

## What is overfitting?
Overfitting occurs when a model learns the training data too well, including noise and random fluctuations, causing poor performance on new, unseen data. It is detected when training accuracy is high but validation accuracy is low.

## How do you prevent overfitting?
Common techniques include: increasing training data, applying regularization (L1 or L2), using dropout in neural networks, early stopping during training, and cross-validation.

## What is a confusion matrix?
A confusion matrix is a table used to evaluate classification models. It shows the counts of true positives, true negatives, false positives, and false negatives, helping assess accuracy, precision, recall, and F1 score.

## What is the difference between precision and recall?
Precision is the proportion of predicted positives that are actually positive. Recall is the proportion of actual positives that were correctly predicted. High precision means fewer false positives; high recall means fewer false negatives.

## What is cross-validation?
Cross-validation is a technique to evaluate model performance by splitting data into k folds. The model is trained on k-1 folds and tested on the remaining fold. This is repeated k times to get an average performance score.

## What is gradient descent?
Gradient descent is an optimization algorithm that iteratively adjusts model parameters in the direction of the negative gradient of the loss function to minimize prediction error.

## What is the bias-variance tradeoff?
Bias refers to errors from incorrect assumptions in the model. Variance refers to sensitivity to small fluctuations in the training data. A good model balances both: low bias and low variance.

## What is feature engineering?
Feature engineering is the process of using domain knowledge to select, transform, or create new input features from raw data to improve model performance.
