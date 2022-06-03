# Import functionally necessary packages
import numpy as np

# Global constants used throughout analysis
NA_STRING = "NA_SS"
NA_NUMBER = -999.0


def remove_missing_data(df, MAX_MISSING_VALUES=250):
    """
    Determines which features to remove from DataFrame based on the defined
    threshold. There is a definitive trade-off between dropping features and
    dropping rows. *Features* with excessive missing rows must be dropped.
    If they are not dropped, *rows* with missing values must be dropped. This
    function allows experimentation with and fine-tuning of that trade-off.

    Parameters:
    -----------
    df : DataFrame containing input data, with NA_STRING and NA_NUMBER
         corresponding to missing values
    MAX_MISSING_VALUES : semi-arbitrary threshold for missing rows in each
                         feature beyond which the feature is dropped

    Returns:
    --------
    df : DataFrame containing only rows + features with no missing/null values
    """

    # Relace 'placeholder' NaN values, as defined by data dictionary
    df.replace(NA_STRING, np.nan, inplace=True)
    df.replace(NA_NUMBER, np.nan, inplace=True)

    # Determine the number of missing values in each column
    for col in df.columns:
        # Count of missing values
        na_ct = df[col].isna().sum()

        # Drop column if more than given threshold of missing values
        if na_ct > MAX_MISSING_VALUES:
            df.drop(col, axis=1, inplace=True)

    # Drop rows with missing data
    df.dropna(inplace=True)

    return df
