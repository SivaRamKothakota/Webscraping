import scrapy
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.exceptions import SpreadsheetNotFound
class LinkedJobsSpider(scrapy.Spider):
    name = "linkedin_jobs"
    #job search url
    api_url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?trk=guest_homepage-basic_guest_nav_menu_jobs&start='

    def start_requests(self):
        first_job_on_page = 0
        first_url = self.api_url + str(first_job_on_page)
        yield scrapy.Request(url=first_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})
    #checking whether record is present or not in our google sheets
    def is_duplicate_record(self, sheet, title):
        data = sheet.get_all_records()
        return any(record['JOB_TITLE'] == title for record in data)

    def parse_job(self, response):
        first_job_on_page = response.meta['first_job_on_page']

        job_item = {}
        jobs = response.css("li")

        num_jobs_returned = len(jobs)
        # Load Google Sheets API credentials
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        #adding credential file(give ur path)
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            r"C:\Users\raguk\OneDrive\Desktop\basic-scrapy-project\basic_scrapy_spider\spiders\lexical-helix-410815-fdb10ded490c.json",
            scope)

        client = gspread.authorize(creds)
        #name of ur spreadsheet
        spreadsheet_name = "linkedin_jobs_spreadsheet"
        spreadsheet = client.open(spreadsheet_name)
        try:
            spreadsheet = client.open(spreadsheet_name)
        except SpreadsheetNotFound:
            self.log(f"Spreadsheet '{spreadsheet_name}' not found.")
            return


        sheet = spreadsheet.sheet1

        for job in jobs:
            job_item['job_title'] = job.css("h3::text").get(default='not-found').strip()
            job_item['job_description_url'] = job.css(".base-card__full-link::attr(href)").get(default='not-found').strip()
            job_item['company_name'] = job.css('h4 a::text').get(default='not-found').strip()
            job_item['Job_Post_Url'] = job.css('h4 a::attr(href)').get(default='not-found')
            job_item['company_location'] = job.css('.job-search-card__location::text').get(default='not-found').strip()
            if (
                'Remote' in job_item['job_title'] and
                'United States' not in job_item['company_location'] and 'Canada' not in job_item['company_location']
            ):
                title = job_item['job_title']
                if not self.is_duplicate_record(sheet, title):
                    values = [
                        job_item.get("job_title", ""),
                        job_item.get("job_description_url", ""),
                        job_item.get("company_name", ""),
                        job_item.get("Job_Post_Url", ""),
                        job_item.get("company_location", ""),
                    ]
                    #appending values to google sheets
                    sheet.append_row(values)



                    yield job_item



        if num_jobs_returned > 0:
            first_job_on_page = int(first_job_on_page) + 25
            next_url = self.api_url + str(first_job_on_page)
            yield scrapy.Request(url=next_url, callback=self.parse_job, meta={'first_job_on_page': first_job_on_page})