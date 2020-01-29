

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
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/apache/activemq/pulls?state=closed'
AUTH = (GITHUB_USER, GITHUB_PASSWORD)
def create_input_data(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        issues=[]
        for row in reader:
            #rint(row)
            if(row[0]!="Issue key" and row[0]!=''):
                issue=Issue_Tracking_System_Report(row[0],row[1],row[3],row[4])
                print(issue.issue_key)
                issues.append(issue)
        return issues

def write_issues(response):
    "output a list of issues to csv"
    if not r.status_code == 200:
        raise Exception(r.status_code)
    #print(r.json())
    for pulls in r.json():
        print(pulls['title'])
        pull_number='https://api.github.com/repos/apache/activemq/pulls/'+str(pulls['number'])
        r2=requests.get(pull_number, auth=AUTH)
        print(r2.json())
        if 'deletions' in pulls:
            print(pulls['deletions'])
            print("\n")


r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
csvfile = '%s-issues.csv' % (REPO.replace('/', '-'))
csvout = csv.writer(open(csvfile, 'w'))
csvout.writerow(('id', 'Title', 'Body', 'Created At', 'Updated At'))
create_input_data("ASF JIRA 2020-01-29T09_19_21+0000.csv")
#write_issues(r)

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
