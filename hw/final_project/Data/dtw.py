import os
from datetime import datetime, timedelta

from iexfinance.stocks import get_historical_data
from scipy.stats import zscore

os.environ['IEX_TOKEN'] = 'sk_434806dae94a4ee69daa8375f33da6f5'
TIMEOFFSET = timedelta(hours=3)
os.environ['OUTPUT_FORMAT'] = 'pandas'


def dtw(df1, df2):
    """
    :param df1: the first stock time series with only one column
    :param df2: the second stock time series with only one column
    :return: the 'distance' or 'similarity' between the two time series
    """
    length = len(df1)
    dp = [[0 for i in range(length)] for j in range(length)]
    list1 = zscore(df1.to_list())  # Normalizing df1
    list2 = zscore(df2.to_list())  # Normalizing df2
    dp[0][0] = 0
    dist = 0

    # Updating the dp matrix
    for i in range(length):
        for j in range(max(1, i), length):
            if i == 0:
                dp[i][j] = abs(list1[j] - list2[i]) + dp[i][j - 1]
                dp[j][i] = abs(list1[i] - list2[j]) + dp[j - 1][i]
            else:
                dp[i][j] = abs(list1[j] - list2[i]) + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])
                dp[j][i] = abs(list1[i] - list2[j]) + min(dp[j - 1][i - 1], dp[j - 1][i], dp[j][i - 1])

    # Backtracing and calculating the distance of the two time series
    curr_i = curr_j = length - 1
    while not (curr_i == 0 or curr_j == 0):
        dist += dp[curr_i][curr_j]

        # Traversing the elements not on the edge of the matrix
        if not (curr_i == 0 or curr_j == 0):
            if dp[curr_i - 1][curr_j - 1] == min(dp[curr_i - 1][curr_j - 1], dp[curr_i][curr_j - 1],
                                                 dp[curr_i - 1][curr_j]):
                curr_i -= 1
                curr_j -= 1
            else:
                if dp[curr_i - 1][curr_j] >= dp[curr_i][curr_j - 1]:
                    curr_j -= 1
                else:
                    curr_i -= 1

        # Traversing the elements on the edge of the matrix
        if curr_i == 0:
            curr_j -= 1
        elif curr_j == 0:
            curr_i -= 1

    return dist


if __name__ == '__main__':
    start = datetime(2019, 1, 1)
    end = datetime(2019, 3, 1)
    aapl = get_historical_data('AAPL', start, end)
    tsla = get_historical_data('AMZN', start, end)
    print(dtw(aapl['close'], tsla['close']))
