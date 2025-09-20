import os
import requests
import pandas as pd
from dotenv import load_dotenv

# load environment variables
load_dotenv()

def extract_api_data()-> pd.DataFrame:
    # get api key from .env
    API_KEY = os.getenv('COIN_GECKO_API_KEY')
    
    url = "https://api.coingecko.com/api/v3/coins/markets"

    # api parameters
    querystring = {"vs_currency":"usd","category":"layer-1","price_change_percentage":"1h","per_page":"30"}

    headers = {"x-cg-demo-api-key": f"{API_KEY}\t"}

    response = requests.get(url, headers=headers, params=querystring)

    # convert api response to json
    json_response = response.json()

    # normalize nested json
    df = pd.json_normalize(json_response) # type: ignore

    print(df.head())
    
    return df




if __name__ == "__main__":
    extract_api_data()