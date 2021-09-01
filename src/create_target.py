# Import functionally necessary packages
import pandas as pd


def create_target(protests, regimes):
    '''
    Objective : create a "target" feature for the primary analysis that 
    successfully corresponds to the number of days until a regime transition 
    occurs
    Methodology:
    -----------
    1. Create column for "next regime change date" in country for each protest
    2. Using (1), create column for "days until next regime change"
    3. Typecasting and removal of unnecessary "helper" features
    
    Parameters:
    -----------
    protests : DataFrame of cleaned dataset of political protests, originally 
               derived from Mass Mobilizations dataset
    regimes : DataFrame of cleaned dataset of political regimes across time, 
              as provided by Polity Project dataset

    Returns:
    --------
    working_df : DataFrame combining the data from "protests" and "regimes" and 
                 adding the feature for the number of "days until next 
                 regime change"
    '''
    
    
    # Create new dataframe to contain results throughout loop
    working_df = protests[['scode', 'startdate']].copy()
    
    # Add empty columns that will iteratively be updated in loop
    working_df['xconst'] = None
    working_df['next_regime_chg_date'] = None
    working_df['days_until_next_regime_chg'] = None

    # Move "index" into its own column to be used in loop
    protests.reset_index(inplace=True, drop=False)
    
    # Eliminate unnecessary features
    protests = protests[['index', 'scode', 'startdate']].values
    
    # Loop over all country names
    for protest_index, protest_scode, protest_start in protests:

        # Narrow to only the country in question
        regime_country_df = regimes.loc[regimes.scode==protest_scode]

        # Loop over all regime indices
        for regime_index in regime_country_df.index:

            # isolate each metric for the selected regime and country
            regime_start = regime_country_df.loc[regime_index, 'startdate']
            regime_end   = regime_country_df.loc[regime_index, 'enddate']
            xconst = regime_country_df.loc[regime_index, 'xconst']


            # if protest occurs before statehood,set the 'regime end' to the 
            # date it became a state this would correspond to protests about 
            # creating a state. Note that this is very rare in this dataset
            if (regime_index == regime_country_df.index[0]) and \
                (protest_start < regime_start):
                working_df.loc[protest_index, 'next_regime_chg_date'] = regime_start
                working_df.loc[protest_index, 'xconst'] = xconst


            # if the protest is within selected regime row. Most common.
            elif (protest_start >= regime_start) and \
                 (protest_start <= regime_end):
                working_df.loc[protest_index, 'next_regime_chg_date'] = regime_end
                working_df.loc[protest_index, 'xconst'] = xconst


    # Convert from 'object' to 'datetime' format
    chg_date = working_df['next_regime_chg_date']
    working_df['next_regime_chg_date'] = pd.to_datetime(chg_date)

    # # Incorporate new column for "duration"
    working_df['days_until_next_regime_chg'] = (working_df['next_regime_chg_date'] - \
                                                working_df['startdate']).dt.days
    
    # Eliminate "helper" features that are no longer used
    working_df.drop(['scode', 'startdate'], axis=1, inplace=True)
    
    return working_df