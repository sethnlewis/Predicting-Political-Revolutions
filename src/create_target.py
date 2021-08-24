import pandas as pd

#1. Create column for "next regime change date"
#2. Create column for "days until next regime change"
#3. Create target column for [above column] < 365 (try for other targets too)
def create_target(protests, regimes):

    # Create new dataframe to contain results throughout loop
    working_df = protests[['scode', 'startdate']].copy()
    working_df['parcomp'] = None
    working_df['parreg'] = None
    working_df['xconst'] = None
    working_df['xropen'] = None
    working_df['xrcomp'] = None
    working_df['next_regime_chg_date'] = None
    working_df['days_until_next_regime_chg'] = None


    # Loop over all country names
    for protest_index, protest_scode, protest_start in protests.reset_index()[['index', 'scode', 'startdate']].values:

        # look only at country in question
        regime_country_df = regimes.loc[regimes.scode==protest_scode]


        # Loop over all regime indices
        for regime_index in regime_country_df.index:

            # isolate startdate and enddate for selected regime
            regime_start = regime_country_df.loc[regime_index, 'startdate']
            regime_end   = regime_country_df.loc[regime_index, 'enddate']
            parcomp = regime_country_df.loc[regime_index, 'parcomp']
            parreg = regime_country_df.loc[regime_index, 'parreg']
            xconst = regime_country_df.loc[regime_index, 'xconst']
            xropen = regime_country_df.loc[regime_index, 'xropen']
            xrcomp = regime_country_df.loc[regime_index, 'xrcomp']


            # if protest occurs before statehood,set the 'regime end' to the date it became a state 
            # this would correspond to protests about creating a state. Note that this is very rare in this dataset
            if (regime_index == regime_country_df.index[0]) and (protest_start < regime_start):
                working_df.loc[protest_index, 'next_regime_chg_date'] = regime_start
                working_df.loc[protest_index, 'parcomp'] = parcomp
                working_df.loc[protest_index, 'parreg'] = parreg
                working_df.loc[protest_index, 'xconst'] = xconst
                working_df.loc[protest_index, 'xropen'] = xropen
                working_df.loc[protest_index, 'xrcomp'] = xrcomp


            # if the protest is within selected regime row
            elif (protest_start >= regime_start) and (protest_start <= regime_end):
                working_df.loc[protest_index, 'next_regime_chg_date'] = regime_end
                working_df.loc[protest_index, 'parcomp'] = parcomp
                working_df.loc[protest_index, 'parreg'] = parreg
                working_df.loc[protest_index, 'xconst'] = xconst
                working_df.loc[protest_index, 'xropen'] = xropen
                working_df.loc[protest_index, 'xrcomp'] = xrcomp


    # # Convert from 'object' to 'datetime' format
    working_df['next_regime_chg_date'] = pd.to_datetime(working_df['next_regime_chg_date'])


    # # Incorporate new column for "duration"
    working_df['days_until_next_regime_chg'] = (working_df['next_regime_chg_date'] - working_df['startdate']).dt.days
    
    working_df.drop(['scode', 'startdate', 'next_regime_chg_date'], axis=1, inplace=True)
    
    return working_df