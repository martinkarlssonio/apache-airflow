from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import polars as pl
import random
import os
import logging
## Set logging level
logging.basicConfig(level=logging.INFO)

# Define default arguments
defaultArgs = {
    'owner': 'martinkarlssonio',
    'start_date': datetime(2023, 9, 29),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Instantiate your DAG
dag = DAG('martinkarlssonio_example',
          default_args=defaultArgs,
          description='Example data pipeline',
          schedule_interval='@daily',
          catchup=False)

def createDataFrame(ti):
    logging.info("############## Creating DataFrame")
    dfSize = 100000
    ## Create a list of timestamps starting from now and reduce by 1 minute for each row
    timestampList = [datetime.now() - timedelta(minutes=i) for i in range(dfSize)]
    idList = [random.randint(1, 5) for _ in range(dfSize)]
    valueList = [random.randint(10, 50) for _ in range(dfSize)]
    groupList = [random.choice(['A', 'B']) for _ in range(dfSize)]
    df = pl.DataFrame({
        'id': idList,
        'timestamp': timestampList,
        'value': valueList,
        'group': groupList
    })
    filePath = f"data/dataframe_{datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]}.parquet"
    df.write_parquet(filePath)
    ti.xcom_push(key='filePath', value=filePath)

def aggregateDataFrame(ti):
    logging.info("############## Aggregating DataFrame")
    filePath = ti.xcom_pull(task_ids='createDataFrame', key='filePath')
    if filePath is None:
        logging.error("No DataFrame file path found")
        return
    logging.info(f"Reading DataFrame from {filePath}")
    aggregatedDf = pl.read_parquet(filePath)
    logging.info(f"Dataframe read from {filePath}")
    logging.info(aggregatedDf.head())
    ## Aggregate and take the mean of 'value' column for each group+id+hour
    # Convert 'timestamp' to hour granularity
    aggregatedDf = aggregatedDf.with_columns(
        pl.col('timestamp').dt.truncate("1h").alias('timestamp_hour')
    )
    # Group by 'group', 'id', and 'timestamp_hour', then calculate mean of 'value'
    aggregatedDf = aggregatedDf.groupby(['group', 'id', 'timestamp_hour']).agg(
        pl.col('value').mean().alias('average_value')
    )
    aggregatePath = f"data/aggregated_{datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]}.parquet"
    aggregatedDf.write_parquet(aggregatePath)
    ti.xcom_push(key='aggregatePath', value=aggregatePath)
    return aggregatePath

def statistics(ti):
    logging.info("############## Calculating statistics")
    filePath = ti.xcom_pull(task_ids='createDataFrame', key='filePath')
    if filePath is None:
        logging.error("No aggregated DataFrame file path found")
        return
    logging.info(f"Reading aggregated DataFrame from {filePath}")
    df = pl.read_parquet(filePath)
    logging.info(f"Dataframe read from {filePath}")
    logging.info(df.head())
    ## Calculate statistics
    statistics = df.describe()
    logging.info(statistics)
    return

def sendNotifictionToSlack():
    logging.info("############## Sending notification")
    ## Send a notifiction to a Slack channel that the pipeline has completed
    return

def cleanupFiles(ti):
    logging.info("############## Cleaning up created files")
    paths = [
        ti.xcom_pull(task_ids='createDataFrame', key='filePath'),
        ti.xcom_pull(task_ids='aggregateDataFrame', key='aggregatePath')
    ]
    for path in paths:
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted {path}")

# Define tasks
taskCreateDf = PythonOperator(
    task_id='createDataFrame',
    python_callable=createDataFrame,
    provide_context=True,
    dag=dag,
)

taskAggregateDf = PythonOperator(
    task_id='aggregateDataFrame',
    python_callable=aggregateDataFrame,
    provide_context=True,
    dag=dag,
)

taskStatistics = PythonOperator(
    task_id='statistics',
    python_callable=statistics,
    provide_context=True,
    dag=dag,
)

taskSendNotificationToSlack = PythonOperator(
    task_id='sendNotifictionToSlack',
    python_callable=sendNotifictionToSlack,
    provide_context=True,
    dag=dag,
)

taskCleanupFiles = PythonOperator(
    task_id='cleanupFiles',
    python_callable=cleanupFiles,
    provide_context=True,
    dag=dag,
)

# Set task dependencies
taskCreateDf >> taskAggregateDf >> taskCleanupFiles >> taskSendNotificationToSlack
taskCreateDf >> taskStatistics
