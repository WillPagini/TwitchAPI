from typing import List
import pandas
import pandas_gbq
from google.oauth2 import service_account
import MyAPI
import time
from datetime import datetime
import numpy

def updateBigquery():

    credentials = service_account.Credentials.from_service_account_file(
    'C:\Keys\dataframe_privatekey.json',
    )
    pandas_gbq.context.credentials = credentials
    pandas_gbq.context.project = "uploaddataframe"


    client_id = 'ug6wd68dqnvh7fb1fcijkzgbwazgw0'
    secret_id = 'e9ekqp1aeo5orujwo3boix2omzqq0c'

    client = MyAPI.TwitchAPI(client_id, secret_id)
    client.perform_auth()

    # get df acording to the search parameters
    df = client.get_df(idiom="pt")


    # Formatting df fields
    # 'tag_ids' must be converted to str, otherwise the schema return error
    df['game_id'] = df['game_id'].astype(numpy.int64)
    df['id'] = df['id'].astype(numpy.int64)
    df['is_mature'] = df['is_mature'].astype(bool)
    df['started_at'] = df['started_at'].astype('datetime64')
    df['tag_ids'] = df['tag_ids'].astype(str)
    df['user_id'] = df['user_id'].astype(numpy.int64)
    df['viewer_count'] = df['viewer_count'].astype(numpy.int64)

    #df.drop('is_mature', axis=1, inplace=True)
    #df.drop('tag_ids', axis=1, inplace=True)
    #df.info()

    now = datetime.now()
    current_day = now.strftime("%Y_%m")

    tableName = f"DataSet_test.TopStreams_{current_day}"


    df.to_gbq(destination_table=tableName,
    project_id='uploaddataframe',
    if_exists='append',
    table_schema=[{'name': 'game_id','type': 'INTEGER'},
        {'name': 'game_name','type': 'STRING'},
        {'name': 'id','type': 'INTEGER'},
        {'name': 'is_mature','type': 'BOOL'},
        {'name': 'language','type': 'STRING'},
        {'name': 'started_at','type': 'DATETIME'},
        {'name': 'tag_ids','type': 'STRING'},
        {'name': 'thumbnail_url','type': 'STRING'},
        {'name': 'title','type': 'STRING'},
        {'name': 'user_id','type': 'INTEGER'},
        {'name': 'user_name','type': 'STRING'},
        {'name': 'viewer_count','type': 'INTEGER'}
        ])

    print("dataframe updated at: " + now.strftime("%H:%M:%S"))
