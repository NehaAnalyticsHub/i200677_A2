from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import pandas as pd
from bs4 import BeautifulSoup
import re
import requests


# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 5, 15),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

dag = DAG(
    'neha',
    default_args=default_args,
    description='A DAG to extract data from websites',
    schedule_interval='@daily',
)

def preprocess_text(text):
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def extract_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        data = []
        headings = soup.find_all(re.compile('^h[1-6]$'))
        for heading in headings:
            title_text = heading.get_text(strip=True)
            title = preprocess_text(title_text)
            data.append([title, "No description available"])
        
        paragraphs = soup.find_all('p')
        for i, description in enumerate(paragraphs):
            description_text = description.get_text(strip=True)
            description = preprocess_text(description_text)
            if i < len(data):
                data[i][1] = description
        
        return data
    else:
        print(f"Failed to fetch data from {url}")
        return None

def extract_and_save_data(url, csv_file):
    data = extract_data(url)
    if data:
        df = pd.DataFrame(data, columns=['Title', 'Description'])
        df = df[~df['Title'].str.contains(r'<h[1-6]>|<p>', regex=True, case=False)]
        df = df[~df['Description'].str.contains(r'<h[1-6]>|<p>', regex=True, case=False)]
        df = df[df['Title'].str.len() >= 15]
        df.drop_duplicates(subset=['Title'], keep='first', inplace=True)
        df.reset_index(drop=True, inplace=True)
        df.to_csv(csv_file, index=False, encoding='utf-8')
        print(f"Data from {url} has been stored in '{csv_file}'.")
    else:
        print(f"No data extracted from {url}.")

task_extract_dawn_data = PythonOperator(
    task_id='extract_dawn_data',
    python_callable=extract_and_save_data,
    op_kwargs={'url': 'https://www.dawn.com/', 'csv_file': '/mnt/c/dag/data/dawn_articles.csv'},
    dag=dag,
)

task_extract_bbc_data = PythonOperator(
    task_id='extract_bbc_data',
    python_callable=extract_and_save_data,
    op_kwargs={'url': 'https://www.bbc.com/', 'csv_file': '/mnt/c/dag/data/bbc_articles.csv'},
    dag=dag,
)

def combine_data():
    dawn_df = pd.read_csv('/mnt/c/dag/data/dawn_articles.csv')
    bbc_df = pd.read_csv('/mnt/c/dag/data/bbc_articles.csv')

    combined_df = pd.concat([dawn_df, bbc_df], ignore_index=True)
    combined_df.drop_duplicates(subset=['Title'], keep='first', inplace=True)
    combined_df.reset_index(drop=True, inplace=True)

    combined_csv_file = '/mnt/c/dag/data/combined_articles.csv'
    combined_df.to_csv(combined_csv_file, index=False, encoding='utf-8')
    print(f"Combined data has been stored in '{combined_csv_file}'.")

task_combine_data = PythonOperator(
    task_id='combine_data',
    python_callable=combine_data,
    dag=dag,
)

# # Function to upload file to Google Drive
# def upload_file_to_drive():
#     gauth = GoogleAuth()
#     gauth.LoadClientConfigFile('client_secret_462784204705-3rvrlauung4aprfp4c8hom3da6n5tsuf.apps.googleusercontent.com.json')
#     gauth.LocalWebserverAuth()
#     drive = GoogleDrive(gauth)

#     file = drive.CreateFile({'parents': [{'id': '1HowNwFokXgwUyauSZPv1vUdVDpKU8kxf?usp=drive_link'}]})
#     file.SetContentFile('/mnt/c/dag/data/combined_articles.csv')
#     file.Upload()

# # PythonOperator to upload file to Google Drive
# task_upload_to_drive = PythonOperator(
#     task_id='upload_to_drive',
#     python_callable=upload_file_to_drive,
#     dag=dag,
# )



task_extract_dawn_data >> task_extract_bbc_data >> task_combine_data  #>> task_upload_to_drive

