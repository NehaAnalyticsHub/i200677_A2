# Initialize a new Git repository
git init

# Add a remote repository named 'origin'
git remote add origin https://github.com/NehaAnalyticsHub/i200677_A2.git

# Initialize DVC in the repository
dvc init

# Add a remote storage location for DVC (Google Drive in this case)
dvc remote add -d gdrive_remote gdrive://1HowNwFokXgwUyauSZPv1vUdVDpKU8kxf

# Add the data file to DVC for tracking
dvc add data/combined_articles.csv

# Push the data file to the remote storage location
dvc push

# Add all changes to the Git staging area
git add .

# Commit the changes with a message
git commit -m "adding all files"

# Push the committed changes to the 'master' branch of the remote repository
git push -u origin master


# Report Content

# Data Preprocessing Steps and DVC Setup 

# Introduction
In this report, I document the data preprocessing steps and the setup of Data Version Control (DVC) for a project involving the extraction, transformation, and storage of data from news websites. I'll outline the workflow and any challenges encountered during the implementation process.
Workflow Overview.

The workflow involves the following steps:

1.	Data Extraction: Extracting titles and descriptions from news websites (e.g., Dawn.com, BBC.com).
2.	Data Transformation: Preprocessing the extracted text data.
3.	Data Storage and Version Control: Storing the preprocessed data and managing version control using DVC.

# Data Preprocessing Steps

The data preprocessing steps are implemented in the main.py script. Here's a brief overview:
•	Extracting Data: I use Selenium to load the webpage and BeautifulSoup to parse the HTML content. Titles are extracted from heading tags (h1 to h6), and descriptions are extracted from paragraph tags (p tags).
•	Preprocessing Text: The extracted text data undergoes preprocessing to remove extra whitespace, newline characters, and leading/trailing whitespace. Also check if a text is likely to be a title based on its length. Also remove repeating text.
•	Cleaning Data: I remove rows containing HTML tags in the 'Title' or 'Description' columns to ensure clean data.
•	Saving Data: The cleaned and processed data is saved to a CSV file (articles_data.csv).
# DVC Setup

DVC is used for managing version control of the data and reproducing the workflow. Here's how it's set up:
•	Initializing DVC: DVC is initialized in the project directory (dvc init).
•	Tracking Data Files: The CSV file (articles_data.csv) containing the preprocessed data is tracked using DVC (dvc add articles_data.csv).
•	Committing Changes: Changes to the data file are committed using DVC (dvc push).


# Challenges Encountered
During the implementation, I encountered challenges while setting up and running the Directed Acyclic Graph (DAG) using Apache Airflow (dag.py). The issues mainly revolved around dependencies and environment setup. However, by ensuring proper configuration and resolving dependency conflicts, I was able to overcome these challenges and successfully execute the workflow.
Conclusion
In conclusion, the data preprocessing steps and DVC setup provide a structured approach to manage data extraction, transformation, and version control for the project. By documenting the workflow and addressing challenges encountered, I ensure reproducibility and maintainability of the project.


                             
