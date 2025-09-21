import os
import requests
import pandas as pd
from dotenv import load_dotenv
import psycopg2

# load environment variables
load_dotenv()

# get api key from .env
API_KEY = os.getenv('COIN_GECKO_API_KEY')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')


def extract_api_data() -> pd.DataFrame:
    
    url = "https://api.coingecko.com/api/v3/coins/markets"

    # api parameters
    querystring = {"vs_currency":"usd","category":"layer-1","price_change_percentage":"1h","per_page":"30"}

    headers = {"x-cg-demo-api-key": f"{API_KEY}\t"}

    response = requests.get(url, headers=headers, params=querystring)

    # convert api response to json
    json_response = response.json()

    # normalize nested json
    df = pd.json_normalize(json_response) # type: ignore

    # print(df.head())
    # print(df.info())
    
    return df


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    # rename columns
    df.rename(columns={'price_change_percentage_1h_in_currency': 'price_change_pct_1h'}, inplace=True)
    
    # drop columns
    df.drop(['roi', 'roi.times', 'roi.currency', 'roi.percentage', 'image'], axis=1, inplace=True)
    
    # convert columns to appropriate type
    date_columns = ['last_updated', 'atl_date', 'ath_date']
    # df['last_updated'] = pd.to_datetime(df['last_updated'], errors='coerce') # type: ignore
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce') # type: ignore
    print('Transformation Completed....')
    print(df.head())
        
    return df

def load_data_to_postgres():
    try:
        conn = psycopg2.connect(
            database=POSTGRES_DB,
            user=POSTGRES_USER,
            password=POSTGRES_PASSWORD,
            host="localhost",  
            port=5432    # default is 5432
        )
        print("Connection to PostgreSQL successful!")

    except psycopg2.Error as e:
        print(f"Error connecting to PostgreSQL: {e}")


if __name__ == "__main__":
    extract_data = extract_api_data()
    tranform_data = transform_data(extract_data)
    load_data_to_postgres()