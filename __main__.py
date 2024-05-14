import os
import subprocess

def set_environment_variables():
    # Get the current user's ID
    userId = os.getuid()
    try:
        os.environ["_AIRFLOW_WWW_USER_USERNAME"]
    except:
        userName = "airflow"
    try:
        os.environ["_AIRFLOW_WWW_USER_PASSWORD"]
    except:
        password = "airflow"
    # Environment variables to set
    env_vars = {
        "AIRFLOW_UID": userId,
        "_AIRFLOW_WWW_USER_USERNAME": userName,
        "_AIRFLOW_WWW_USER_PASSWORD": password
    }
    
    # Write to the .env file
    with open('.env', 'w') as file:
        for key, value in env_vars.items():
            file.write(f"{key}={value}\n")

def run_docker_compose():
    # Run docker-compose up command
    subprocess.run(['docker-compose', 'up'])

def main():
    set_environment_variables()
    run_docker_compose()

if __name__ == "__main__":
    main()