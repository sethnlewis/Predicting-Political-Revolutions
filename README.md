# A Data-Based Understanding of Political Revolutions
Political upheavals have been ever present throughout humanity. Political leaders shape the context for everything we know. For that reason, we as a society need to generate a concrete understanding of when a revolution or political change is imminent. This analysis seeks to forecast whether a given protest will lead to a revolution within 90 days. 

The stakeholders for this analysis are wide reaching, but it is most relevant to political organizers and leadership. They can use this approach to best understand where efforts are best focused and most likely to lead to an impact. 

## Repository Structure

```

│                        
├── data
│   ├── processed                                <-- SQL files containing processed data
│   └── raw                                      <-- Original (immutable) data dump
        ├── Mass-Mobilization-Protests           <-- Data source #1 
        ├── Polity-Project                       <-- Data source #2
        ├── Database-of-Political-Institutions   <-- Data source #3
        
├── images                   <-- Figures used in presentation and notebooks
│
├── notebooks                <-- Jupyter Notebooks for exploration and presentation
│
├── reference_material
│   └── data user manuals    <-- PDFs provided from data sources
│
├── report                   <-- Generated analysis summary
│
├── src                      <-- Custom functions used in notebooks
│
└── README.md                <-- Main README file

```

## Project Structure
Given the complex nature of combining three separate datasets from distinct sources, the analysis was conducted in five different notebooks. The first three "*cleaning_xxx.ipynb*" notebooks clean one dataset of raw data alongside conducting feature engineering and selection. Each of these notebooks exports the final version of that dataset in a form ready to be combined with all others. Next, the "*MODEL.ipynb*" notebook combines these three SQL databases while also conducting substantial feature selection and engineering before beginning the main purpose of the notebook: modeling. The fourth notebook is "*EDA.ipynb*". It is used for exploratory analysis of features. The final notebook, "*FINAL SUMMARY NOTEBOOK.ipynb*" is a high-level summary of each of the other four notebooks, extracting key points from each.



---

## Data Sources
The analysis combines three core datasets from widely different sources to provide a distinctly unique understanding of the subject. They are described below.

### The Mass Mobilization Project

The first dataset, used as the center of the analysis, is incredibly valuable. It is described in the source documentation as "an effort to understand citizen movements against governments, what citizens want when they demonstrate against governments, and how governments respond to citizens. The MM data cover 162 countries between 1990 and 2018. These data contain events where 50 or more protesters publicly demonstrate against government, resulting in more than 10,000 protest events. Each event records location, protest size, protester demands, and government responses." [(1)](https://massmobilization.github.io/about.html) The project is sponsored by the Political Instability Task Force (PITF). The PITF is funded by the Central Intelligence Agency (CIA). [(1)](https://massmobilization.github.io/about.html) Throughout the  analysis, this dataset is referred to as the "Protests" dataset.

Although the data source does specify that the dataset is not entirely comprehensive of all country across this entire time period. That said, it does contain over 17,000 recorded protests, each composed of 31 features. The data span 167 countries from 1990 to 2020. Seemingly the only large country to be ommitted is the United States, which is undoubtedly tied back to the source of the project funding.


#### Citation:

Clark, David; Regan, Patrick, 2016, "Mass Mobilization Protest Data", https://doi.org/10.7910/DVN/HTTWYL, Harvard Dataverse, V5, UNF:6:F/k8KUqKpCa5UssBbL/gzg== [fileUNF]



### The Polity Project
The second dataset is equally as valuable. It codes "authority characteristics of states in the world system for purposes of comparative, quantitative analysis." [(2)](https://www.systemicpeace.org/polityproject.html) "The Polity5 dataset covers all major, independent states in the global system over the period 1800-2018 (i.e., states with a total population of 500,000 or more in the most recent year; currently 167 countries. The Polity conceptual scheme is unique in that it examines concomitant qualities of democratic and autocratic authority in governing institutions, rather than discreet and mutually exclusive forms of governance. This perspective envisions a spectrum of governing authority that spans from fully institutionalized autocracies through mixed, or incoherent, authority regimes (termed "anocracies") to fully institutionalized democracies." [(2)](https://www.systemicpeace.org/polityproject.html). Most relevant to this analysis, "it also records changes in the institutionalized qualities of governing authority."  [(2)](https://www.systemicpeace.org/polityproject.html). These changes in governing authority are the target feature of this analysis. It also contains 1,693 rows of data, each with 24 features. Throughout the analysis, this dataset is referred to as the "Regime Changes" or "Regimes" dataset.


#### Citation: 

“The Polity Project.” PolityProject, Center for Systemic Peace, www.systemicpeace.org/polityproject.html. 



### The Database of Political Institutions

The third dataset is provided by the Inter-American Development Bank (IDB). "The Database of Political Institutions presents institutional and electoral results data such as measures of checks and balances, tenure and stability of the government, identification of party affiliation and ideology, and fragmentation of opposition and government parties in the legislature ... [it covers] about 180 countries [from] 1975-2020. It has become one of the most cited databases in comparative political economy and comparative political institutions, with more than 4,500 article citations on Google Scholar as of December 2020." [(3)](https://publications.iadb.org/en/database-political-institutions-2020-dpi2020) For the context of this analysis, it includes 8,200 rows of data, each with 77 features. Throughout the analysis, this dataset is referred to as the "Governments" dataset.


#### Citation:

Cruz, Cesi, Philip Keefer, and Carlos Scartascini. 2021. Database of Political Institutions 2020. Washington, DC: Inter-American Development Bank Research Department.


---

## Data Analysis


#### Understanding Protester Demands

The below chart provides insight into the most common demands from protesters from 1990 to 2020.

<img src="https://github.com/sethschober/Capstone/blob/main/images/protest_demands.png" width="500">


#### Understanding Protest Locations

Below is a geographical distribution of protests by region. Do note that the Protests data source explicity excludes some countries, so this figure should not be construed as an understanding of *all* protests. Instead, it is the distribution within this dataset. 


<img src="https://github.com/sethschober/Capstone/blob/main/images/protests_by_region.png" width="500">

---

## Modeling
The models explored include K-Nearest Neighbors (KNN), Bayesian classifiers, ADA boost, Decision Trees, Random Forests, and XG Boost. In addition, each type of model is constructed using elements of encoding, scaling, resampling and hyperparameter optimization.

- One hot encoding was essential given the categorical type of some features
- Standard scaling was essential given the vast array of different numerical feature distributions and ranges. Min-max scaling was considered but proved less effective.
- SMOTE was determined to be essential given the imbalanced nature of the dataset. Only 11% of the target feature values were 1, leaving the other 89% as 0. This is a prime example of the need for resampling, and SMOTE proved highly effective.
- Hyperparameter grid searches are inherently valuable when optimizing a model. Appropriate hyperparameter searches were used for each model type.

The output of each model is provided in terms of four core statistical measures (f1 score, accuracy, precision, and recall), in addition to displaying a confusion matrix for the test data. F1 was selected before the modeling process as the most relevant metric given that it encomasses all possible outcomes, as opposed to the other three metrics which leave out at least one possible outcome from their evaluation. 


---

## Evaluation
The XG boost model was found to perform the best all around. This decision was based on the F1 score, but the XG boost also outperformed other models on other metrics.


### Evaluate performance on holdout validation data
The model has a strong performance on the holdout data:
- F1 score: XX
- Accuracy: XX
- Precision: XX
- Recall: XX

The confusion matrix below shows the performance on the holdout data (left) and the performance on the full dataset (right), including train, test and holdout data. In addition to overall performance, the similar performance on training, test and holdout indicates that the model has not been overfit.

<img src="https://github.com/sethschober/Capstone/blob/main/images/confusion_matrices.png" width="500">



### Feature importance

Although XG boost models are notoriously difficult to extract meaningful feature importance data from, the plot below does provide an indication per the SHAP summary plot. 

<img src="https://github.com/sethschober/Capstone/blob/main/images/shap_summary_plot.png" width="500">


Here, we see that the four most significant features are:
1. XX
2. XX
3. XX
4. XX

---


## Conclusion
Overall, this analysis successfully completes its objective. It creates and tunes a model that helps predict whether a given protest will lead to a regime transition within one year. This incredibly valuable tool can be used by stakeholders far and wide as an indicator of disruption to come, which in turn can be used for proactive or preventative measures by either side. With a very strong performing model, it can be trusted to give an accurate estimate of changes to come. 

Going forward, this project allows for easy growth as more data is released. Each of the three primary datasets receive regular updates, and this new information can easily be incorporated in order to expand the temporal scope of the project and with more data comes to potential for stronger performance. 
