# Import functionally necessary packages
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import shap
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from imblearn.over_sampling import SMOTE


def custom_plot_matrix(df, max_corr=None):
    '''
    Creates an aesthetic heatmap with pre-defined coloring, adaptive sizing, 
    and adjustable correlation range/scale
    
    Parameters:
    -----------
    df : DataFrame to be plotted
    max_corr : (optional) [0, 1] float for the maximum correlation to show 
                on the legend, which affects coloring

    Returns:
    --------
    None
    '''
    
    ## Compute the correlation matrix
    corr = df.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(np.ones_like(corr, dtype=bool))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Ensure negative and positive distances to zero are the absolute same
    if max_corr == None:
        max_corr = corr.replace(1.0, 0).abs().max().max()

    # Draw the heatmap with the mask and scaled reasonably
    SIZE = 2
    plt.figure(figsize=(SIZE*corr.shape[1]/2, SIZE*corr.shape[1]/3))
    sns.heatmap(corr, mask=mask, cmap=cmap, center=0, vmax=max_corr, 
                vmin=-max_corr, square=True, linewidths=1, 
                cbar_kws={"shrink": .4})
    plt.show()





def get_shap_df(df_train, target_train, df_test):
    '''
    ADAPTED FROM CODE FOUND HERE: 
    towardsdatascience.com/explain-any-models-with-the-shap-values-use-the-kernelexplainer-79de9464897a
    
    Used to manually perform scaling, transforming, and resampling that are 
    typically done in a pipeline due to unique input needs of a SHAP plot
    
    Parameters:
    -----------
    df_train : DataFrame containing training data
    target_train : Series containing target for training data
    df_test : DataFrame containing test data

    Returns:
    --------
    x_train_final : DateFrame transformed from df_train
    y_train_final : DataFrame transformed from target_train
    df_test_expanded_scaled : DataFrame transformed from df_test
    '''
    
    # Reset indices
    df_train.reset_index(inplace=True, drop=True)
    df_test.reset_index(inplace=True, drop=True)  

    # CATEGORICALS
    df_train_cat = df_train.select_dtypes('object')
    df_test_cat = df_test.select_dtypes('object')
    
    # One hot encode df_train_expanded_scaled
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
    df_train_expanded_scaled = pd.DataFrame(df_train_expanded_scaled, 
                                            columns=df_train_expanded.columns)
    df_test_expanded_scaled = pd.DataFrame(df_test_expanded_scaled, 
                                           columns=df_test_expanded.columns)
    
    # APPLY RESAMPLING
    sm = SMOTE()
    x_train_final, y_train_final = sm.fit_resample(df_train_expanded_scaled, target_train)    
    
    # Return encoded, scaled, resampled versions of inputs
    return x_train_final, y_train_final, df_test_expanded_scaled



def produce_shap_plot(df_train, target_train, df_test, target_test, model_shap, title=None, savepath=None):
    '''
    Conveniently creates SHAP summary plot with predefined characteristics
    
    Parameters:
    -----------
    df_train : DataFrame containing Training data
    target_train : Series containing Training Target
    df_test : DataFrame containing Testing data
    target_test : Series containing Testing Target
    model_shap : Pipeline containing model for SHAP plot
    title : (optional) title for plot

    Returns:
    --------
    None
    '''
    
    
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
    
    # Plot findings
    plt.figure()
    shap.summary_plot(shap_values, df_test, show=False, plot_size=(16, 12))
    
    # Add figure title if provided by user
    if title:
        plt.title(title, fontsize=20)
        
    if savepath:
        plt.savefig(savepath)
    
    plt.show();