"""
Get Top Gainers/Losers prices

url: https://cotacao.b3.com.br/mds/api/v1/InstrumentPriceFluctuation/ibov
"""

from fastapi import FastAPI
import requests

app = FastAPI()

# Obter os dados da B3
def obter_dados_ibov():
    url = 'https://cotacao.b3.com.br/mds/api/v1/InstrumentPriceFluctuation/ibov'
    response = requests.get(url)
    tikers = response.json()
    return tikers

class GetTopGainers:
    def __init__(self, tikers):
        self.topGainersDay = self._get_top_gainers(tikers)

    def _get_top_gainers(self, tikers):
        return {
            'top gainers':{
            'tickers': [tikers['SctyHghstIncrLst'][i]['symb'] for i in range(5)],
            'prices': [tikers['SctyHghstIncrLst'][i]['SctyQtn']['curPrc'] for i in range(5)]
            }
        }

class GetTopLosers:
    def __init__(self, tikers):
        self.topLosersDay = self._get_top_losers(tikers)

    def _get_top_losers(self, tikers):
        return {
            'top losers':{
            'tickers': [tikers['SctyHghstDrpLst'][i]['symb'] for i in range(5)],
            'prices': [tikers['SctyHghstDrpLst'][i]['SctyQtn']['curPrc'] for i in range(5)]
            }
        }

@app.get("/")
def top_losers():
    tikers = obter_dados_ibov()
    top_gainers = GetTopGainers(tikers)
    top_losers = GetTopLosers(tikers)

    return top_gainers.topGainersDay, top_losers.topLosersDay
