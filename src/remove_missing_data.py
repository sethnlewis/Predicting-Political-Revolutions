import numpy as np
import pandas as pd

def remove_missing_data(df, MAX_MISSING_VALUES=250):
    # Max missing values is a semi-arbitrary threshold for the maximum number of missing values to justify keeping
    
    # Constants used throughout analysis
    NA_STRING = "NA_SS"
    NA_NUMBER = -999.0

    # Relace 'placeholder' NaN values, as defined by data dictionary (see raw data directory)
    df.replace(NA_STRING, np.nan, inplace=True)
    df.replace(NA_NUMBER, np.nan, inplace=True)

    # Determine the number of missing values in each column
    for col in df.columns:
        na_ct = df[col].isna().sum()

        if na_ct > MAX_MISSING_VALUES:
            df.drop(col, axis=1, inplace=True)

    df.dropna(inplace=True)
    return df