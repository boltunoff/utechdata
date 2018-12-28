
   Step by Step guide to setup the project on your local system:  
1. Download the project folder
2. Install Python(3.6) on your system
3. Create a Virtual Environment 
4. Activate the Environment 
5. Log into the project folder
    Also, Install Postgresql & ElasticSearch
    Run ElasticSearch service in background
6. Create the Database in PostgreSql
7. Edit the db info in UtechData/settings.py file -> “Databases = {“
8. In terminal, run: pip install -r requirements.txt
9. then run: python manage.py migrate
10. then run: python manage.py runserver
Your are good to go :)
