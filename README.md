# Data Pipelines with Airflow
## Example of Data Pipelines infrastructure

<!--
*** Written by Martin Karlsson
*** www.martinkarlsson.io
-->

[![LinkedIn][linkedin-shield]][linkedin-url]
<!-- ABOUT THE PROJECT -->
## About The Project
#### Overview
Intention with this project is to provide a boilerplate for a Data Pipeline infrastructure using Apache Airflow. The project is intended to be used as a starting point for a more complex data pipeline infrastructure.
<br>
Apache Airflow is an open-source tool for orchestrating complex computational workflows and data processing pipelines. It is a platform to programmatically author, schedule, and monitor workflows. Use airflow to author workflows as directed acyclic graphs (DAGs) of tasks. The airflow scheduler executes your tasks where the workload is shared on workers in a cluster.
<br>
This project have containerized the Airflow environment and added customizations to the Airflow configuration.
<br>

#### DAGs
The repository contains one example DAG that will create a mocked Polars dataframe and perform various tasks on the data.
It uses xcom to pass information between tasks and uses the PythonOperator to run Python functions. The data is stored as parquet files during the DAG run.
<br>


##### Push information to xcom
```
def createDataFrame(ti):
    logging.info("############## Creating DataFrame")
    ...
    filePath = f"data/dataframe_{datetime.now().strftime('%Y%m%d_%H%M%S%f')[:-3]}.parquet"
    df.write_parquet(filePath)
    ti.xcom_push(key='filePath', value=filePath)
```

##### Pull information from xcom
```
def statistics(ti):
    ...
    filePath = ti.xcom_pull(task_ids='createDataFrame', key='filePath')
    df = pl.read_parquet(filePath)
    statistics = df.describe()
```

<br>

#### Screenshots
When the container is running, the User Interface can be accessed on http://localhost:8080.
Here's some screenshots of it!<br>

<img src="images/screenshot1.png"/>
<img src="images/screenshot2.png"/>
<img src="images/screenshot3.png"/>
<img src="images/screenshot4.png"/>


### Pre-requisite
You need to have Docker and Docker-Compose installed on your machine.

### How to start the project
```python __main__.py```

### Permission error
If you see an error related to permission, ensure that the folders (config, dags, logs, plugins) have the right permissions, on Unix systems you can run the following command:<br>
```bash chmod -R 777 config dags logs plugins```

<!-- CONTACT -->

## Contact

### Martin Karlsson

LinkedIn : [martin-karlsson][linkedin-url] \
Twitter : [@HelloKarlsson](https://twitter.com/HelloKarlsson) \
Email : hello@martinkarlsson.io \
Webpage : [www.martinkarlsson.io](https://www.martinkarlsson.io)


Project Link: [github.com/martinkarlssonio/apache-airflow](https://github.com/martinkarlssonio/apache-airflow)


<!-- MARKDOWN LINKS & IMAGES -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/martin-karlsson

