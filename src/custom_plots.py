import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


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