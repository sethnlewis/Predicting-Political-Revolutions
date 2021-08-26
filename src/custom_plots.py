import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shap
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from imblearn.over_sampling import SMOTE

def custom_plot_matrix(df, max_corr=None):
    ## Compute the correlation matrix
    corr = df.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Ensure negative and positive distances to zero are the absolute same
    if max_corr == None:
        max_corr = corr.replace(1.0, 0).abs().max().max()

    # Draw the heatmap with the mask and correct aspect ratio
    SIZE = 1.8
    plt.figure(figsize=(SIZE*corr.shape[1]/2, SIZE*corr.shape[1]/3))
    sns.heatmap(corr, mask=mask, cmap=cmap, center=0, vmax=max_corr, vmin=-max_corr, 
                square=True, linewidths=1, cbar_kws={"shrink": .4})
    plt.show()




# ADAPTED FROM CODE FOUND HERE: https://towardsdatascience.com/explain-any-models-with-the-shap-values-use-the-kernelexplainer-79de9464897a
def get_shap_df(df_train, target_train, df_test):
    
    df_train.reset_index(inplace=True, drop=True)
    df_test.reset_index(inplace=True, drop=True)
    
    # CATEGORICALS
    df_train_cat = df_train.select_dtypes('object')
    df_test_cat = df_test.select_dtypes('object')
    ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')
    ohe.fit(df_train_cat)
    df_train_cat_ohe = ohe.transform(df_train_cat)
    df_test_cat_ohe = ohe.transform(df_test_cat)
    names_ohe = ohe.get_feature_names(df_train_cat[df_train_cat.columns].columns)
    
    # NUMERIC
    df_train_num = df_train.select_dtypes('number')
    df_test_num = df_test.select_dtypes('number')
    
    # COMBINE CATEGORICAL AND NUMERIC
    df_train_expanded = pd.DataFrame(df_train_cat_ohe, columns=names_ohe)
    df_test_expanded = pd.DataFrame(df_test_cat_ohe, columns=names_ohe)
    
    df_train_expanded[df_train_num.columns] = df_train_num
    df_test_expanded[df_test_num.columns] = df_test_num
    
    # SCALE DATA
    ss = StandardScaler()
    ss.fit(df_train_expanded)
    df_train_expanded_scaled = ss.transform(df_train_expanded)
    df_test_expanded_scaled = ss.transform(df_test_expanded)    
    
    # CONVERT FROM ARRAY TO DF
    df_train_expanded_scaled = pd.DataFrame(df_train_expanded_scaled, columns=df_train_expanded.columns)
    df_test_expanded_scaled = pd.DataFrame(df_test_expanded_scaled, columns=df_test_expanded.columns)
    
    sm = SMOTE()
    x_train_final, y_train_final = sm.fit_resample(df_train_expanded_scaled, target_train)    
    
    return x_train_final, y_train_final, df_test_expanded_scaled


def produce_shap_plot(df_train, target_train, df_test, target_test, model_shap, title=None):
    
    # Gather encoded, scaled, resampled dataframes
    df_train, target_train, df_test = get_shap_df(df_train, target_train, df_test)
    
    # Extract "model" portion of pipeline
    model_shap = model_shap.steps[2][1]
    
    # Fit to training data
    model_shap.fit(df_train, target_train)
    pred = model_shap.predict(df_test)
    
    # Produce shap values
    explainer = shap.TreeExplainer(model_shap)
    shap_values = explainer.shap_values(df_test)
    
    # plot findings
    plt.figure()
    shap.summary_plot(shap_values, df_test, show=False, plot_size=(16, 12))
    
    if title:
        plt.title(title)
    
    plt.show();