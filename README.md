# Webscraping   


The code provided here will scrap the linkedin jobs (https://in.linkedin.com/company/linkedin/jobs) and give append unique ,remote, (excluding USA and Canada) jobs to spreadsheet eveytime we run.

we install scrapy module and create a file in spider folder or use the file i provided and run it.

The folder I named is code and the output from my code will be append to my google spreadsheets.(give your google api credentials and your spreadsheet Name)

Packages used (Scrapy, gspread, gspread oauth2client).

run  (scrapy crawl linkedin_jobs) output will be append to spreadsheets.

You can run whole project just cloning srapy_project folder directly to your system and giving your own API credentials.
