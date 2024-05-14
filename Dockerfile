FROM apache/airflow:2.9.1-python3.11

################# CUSTOM UI
# See airflow repo to understand the structure of the webserver
# https://github.com/apache/airflow/tree/main/airflow/www
# The path /home/airflow/.local/lib/python3.11/site-packages/airflow/www/ is where the webserver files are located
RUN mkdir /home/airflow/.local/lib/python3.11/site-packages/airflow/www/images/
COPY navbar.html /home/airflow/.local/lib/python3.11/site-packages/airflow/www/templates/appbuilder/
COPY logo-cartoon.png /home/airflow/.local/lib/python3.11/site-packages/airflow/www/static/
COPY logo-cartoon.png /home/airflow/.local/lib/python3.11/site-packages/airflow/www/static/pin_32.png
COPY init_appbuilder_links.py /home/airflow/.local/lib/python3.11/site-packages/airflow/www/extensions/init_appbuilder_links.py

################# Install PIP requirements
COPY requirements.txt /requirements.txt
RUN pip install --no-input --no-cache-dir -r /requirements.txt

EXPOSE 8080