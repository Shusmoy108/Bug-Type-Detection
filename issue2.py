
import re
import csv
import requests
class Issue_Tracking_System_Report:
    def __init__(self, issue_key, issue_id,description,issue_type):
        self.issue_key = issue_key
        self.issue_id = issue_id
        self.description = description
        self.issue_type = issue_type

GITHUB_USER = 'Shusmoy108'
GITHUB_PASSWORD = 'Sucharita13'
REPO = 'apache/activemq'  # format is username/repo
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues' % REPO
AUTH = (GITHUB_USER, GITHUB_PASSWORD)
keys=[]
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/%s/issues' % REPO
AUTH = (GITHUB_USER, GITHUB_PASSWORD)

def write_issues(response):
    "output a list of issues to csv"
    if not response.status_code == 200:
        raise Exception(response.status_code)
    for issue in response.json():
        print(issue['title'])
        csvout.writerow([issue['number'], issue['title'], issue['body'], issue['created_at'], issue['updated_at']])


r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
csvfile = '%s-issues.csv' % (REPO.replace('/', '-'))
csvout = csv.writer(open(csvfile, 'w'))
csvout.writerow(('id', 'Title', 'Body', 'Created At', 'Updated At'))
write_issues(r)

#more pages? examine the 'link' header returned
if 'link' in r.headers:
    pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                r.headers['link'].split(',')]])
    while 'last' in pages and 'next' in pages:
        r = requests.get(pages['next'], auth=AUTH)
        write_issues(r)
        if pages['next'] == pages['last']:
            break

