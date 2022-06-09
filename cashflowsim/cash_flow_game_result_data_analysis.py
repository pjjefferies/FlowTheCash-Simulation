# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 21:19:02 2015

@author: PaulJ
"""


import pandas as pd
import numpy as np


if __name__ == '__main__':
    input_file = "../game_logs/GameLog-20151025-231555.csv"

    cashFlowResultsData = pd.read_csv(input_file)
    cFRD = cashFlowResultsData

    cFRD['adjTurnsForPassCount'] = np.where(
        cFRD['Am I Rich'], cFRD['Turns'], 0)
    cFRD['adjTurnsForStats'] = (
        np.where(cFRD['Am I Rich'], cFRD['Turns'], np.nan))

    # Analyze by combination of Profeesion and Strategy
    # (if you can choose both)
    groupedComb = cFRD.groupby(['professionName', 'strategyName'])
    compSummary1 = groupedComb['adjTurnsForStats'].agg([np.mean, np.std])
    compSummary2 = groupedComb['adjTurnsForPassCount'].agg([np.count_nonzero])
    compSummary = pd.concat([compSummary1, compSummary2], axis=1, join='inner')
    compSummary.sort_values('mean', inplace=True)

    # Analyze by Profeesion only
    groupedProf = cFRD.groupby('professionName')
    profSummary1 = groupedProf['adjTurnsForStats'].agg([np.mean, np.std])
    profSummary2 = groupedProf['adjTurnsForPassCount'].agg([np.count_nonzero])
    profSummary = pd.concat([profSummary1, profSummary2], axis=1, join='inner')
    profSummary.sort_values('mean', inplace=True)

    # Analyze by Strategy only
    groupedProf = cFRD.groupby('strategyName')
    stratSummary1 = groupedProf['adjTurnsForStats'].agg([np.mean, np.std])
    stratSummary2 = groupedProf['adjTurnsForPassCount'].agg([np.count_nonzero])
    stratSummary = pd.concat([stratSummary1, stratSummary2], axis=1,
                             join='inner')
    stratSummary.sort_values('mean', inplace=True)

    filenameBase = input_file[:-4]
    summaryFilename = filenameBase + "-summary.csv"

    with open(summaryFilename, 'w') as f:
        compSummary.to_csv(f)
        profSummary.to_csv(f)
        stratSummary.to_csv(f)
