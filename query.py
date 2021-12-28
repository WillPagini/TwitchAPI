import pandas
from pandas.io import gbq
from google.cloud import bigquery
import os

def return_query():

    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "C:\Keys\dataframe_privatekey.json"

    client = bigquery.Client()
    table_id = 'uploaddataframe.DataSet_test.TopStreams_2021_12'


    project = "uploaddataframe"
    dataset_id = "DataSet_test"

    dataset_ref = bigquery.DatasetReference(project, dataset_id)
    table_ref = dataset_ref.table("TopStreams_2021_12")
    table = client.get_table(table_ref)

    # Retrieves top views from each streamer on that day
    sql = """
        SELECT *
        FROM 
        (
            SELECT *, row_number() over(partition by stream_day order by max_views DESC) as rn 
            FROM
            (
                SELECT EXTRACT(DATE FROM started_at) AS stream_day, user_name,  max(viewer_count) as max_views
                FROM `uploaddataframe.DataSet_test.TopStreams_2021_12`
                GROUP BY user_name, stream_day
                ORDER BY max_views DESC
        ))
        WHERE rn <= 10
        ORDER BY stream_day
    """

    
    df = client.query(sql).to_dataframe()
    return df

