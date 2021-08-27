# A Data-Based Understanding of Political Revolutions
Political upheavals have been ever present throughout humanity. Political leaders shape the context for everything we know. For that reason, we as a society need to generate a concrete understanding of when a revolution or political change is imminent. This analysis seeks to forecast whether a given protest will lead to a revolution within 90 days. 

The stakeholders for this analysis are wide reaching, but it is most relevant to political organizers and leadership. They can use this approach to best understand where efforts are best focused and most likely to lead to an impact. 

## Project Structure


## Data Sources


## Data Analysis


## Modeling
The next phase is composed of five sections:

1. Test, train, and validation splits
2. "Dummy" model for baseline performance metric
3. Logistic regression model
4. Random forest model
5. XG boost model

Note that in the *MODEL.ipynb* notebook, alternative models are explored, such as K-Nearest Neighbors (KNN), Bayesian classifiers, ADA boost, and Decision Trees. 

Each model type is constructed using elements of encoding, scaling, resampling and hyperparameter optimization.

- One hot encoding was essential given the categorical type of some features
- Standard scaling was essential given the vast array of different numerical feature distributions and ranges. Min-max scaling was considered but proved less effective.
- SMOTE was determined to be essential given the imbalanced nature of the dataset. Only 11% of the target feature values were 1, leaving the other 89% as 0. This is a prime example of the need for resampling, and SMOTE proved highly effective.
- Hyperparameter grid searches are inherently valuable when optimizing a model. Appropriate hyperparameter searches were used for each model type.

The output of each model is provided in terms of four core statistical measures (f1 score, accuracy, precision, and recall), in addition to displaying a confusion matrix for the test data. F1 was selected before the modeling process as the most relevant metric given that it encomasses all possible outcomes, as opposed to the other three metrics which leave out at least one possible outcome from their evaluation. 

Note that the final holdout dataset is not used for evaluation until the final model has been selected based on train-test data performance.


## Evaluation
As can be seen based on the F1 scores – the metric chosen at the beginning of the analysis as most relevant – the XG boost model performs the best. This section will test the final model on the holdout data as well as visualize feature significance to the extent feasible. 

### Evaluate performance on holdout validation dataset


### Feature importance




## Conclusion
Overall, this analysis successfully completes its objective. It creates and tunes a model that helps predict whether a given protest will lead to a regime transition within one year. This incredibly valuable tool can be used by stakeholders far and wide as an indicator of disruption to come, which in turn can be used for proactive or preventative measures by either side. With a very strong performing model, it can be trusted to give an accurate estimate of changes to come. 

Going forward, this project allows for easy growth as more data is released. Each of the three primary datasets receive regular updates, and this new information can easily be incorporated in order to expand the temporal scope of the project and with more data comes to potential for stronger performance. 
