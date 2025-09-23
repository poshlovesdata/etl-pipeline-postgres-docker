import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError


# load environment variables
load_dotenv()

# get api key from .env
api_key = os.getenv('COIN_GECKO_API_KEY')
db_user = os.getenv("POSTGRES_USER")
db_pass = os.getenv("POSTGRES_PASSWORD")
db_name = os.getenv("POSTGRES_DB")
db_host = os.getenv("DB_HOST")

def extract_api_data() -> pd.DataFrame:
    
    url = "https://api.coingecko.com/api/v3/coins/markets"

    # api parameters
    querystring = {"vs_currency":"usd","category":"layer-1","price_change_percentage":"1h","per_page":"30"}

    headers = {"x-cg-demo-api-key": f"{api_key}\t"}

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

def load_data_to_postgres(df: pd.DataFrame) -> None:
    # connection string for postgres
    conn_string = f'postgresql+psycopg2://{db_user}:{db_pass}@{db_host}/{db_name}'

    try:
        print("Connecting to DB...")
        engine = create_engine(conn_string)
        with engine.connect() as conn:
            df.to_sql('coin_price', con=conn, if_exists='replace', index=False)
        print("Connection to PostgreSQL successful!")
    except SQLAlchemyError as e:
        print(f"Error connecting to PostgreSQL: {e}")


if __name__ == "__main__":
    extract_data = extract_api_data()
    tranform_data = transform_data(extract_data)
    load_data_to_postgres(tranform_data)