import csv
import json
import re

import requests

from bs4 import BeautifulSoup
from utils import get_raw_data, write_data


def extract_data(total_data):
    index = total_data[0].index('2/1/20')  # 14
    korea_date = total_data[0][index:]
    korea_date = [i[:-3] for i in korea_date]

    for i in total_data:
        if i[1] == 'Korea, South':
            korea_data = i[index:]
            break

    return korea_data, korea_date


def build_result(korea_data):
    result = [[korea_data[0][0], int(korea_data[0][1]), 1, int(
        korea_data[0][2]), int(korea_data[0][3])]]
    for i, _ in enumerate(korea_data[1:]):
        result.append([
            korea_data[i][0],
            int(korea_data[i][1]),
            int(korea_data[i][1]) - int(korea_data[i - 1][1]),
            int(korea_data[i][2]),
            int(korea_data[i][3])
        ])
    return result


def run():
    confirmed_CSV_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
    deaths_CSV_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
    recovered_CSV_URL = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'

    confirmed_total_data = get_raw_data(confirmed_CSV_URL)
    deaths_total_data = get_raw_data(deaths_CSV_URL)
    recovered_total_data = get_raw_data(recovered_CSV_URL)

    korea_deaths, _ = extract_data(confirmed_total_data)
    korea_recovered, _ = extract_data(recovered_total_data)
    korea_confirmed, korea_deaths_date = extract_data(deaths_total_data)
    korea_data = list(zip(korea_deaths_date, korea_confirmed,
                          korea_deaths, korea_recovered))

    result = build_result(korea_data)

    save_dir = './data/koreaRegionalCumulativeData.js'
    crawler_name = 'crawlKoreaRegionalCumulativeData.py'
    var_name = 'koreaRegionalCumulativeData'

    write_data(result, save_dir, crawler_name, var_name)


print("#####################################")
print("############ 한국 지역별 누적 데이터 #############")
print("######## koreaRegionalCumulativeData.js #########")

run()

print("############### 완료!! ###############")
print("#####################################")
