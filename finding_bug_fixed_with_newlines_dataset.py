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
GITHUB_PASSWORD = ''
REPO = 'apache/activemq'  # format is username/repo
ISSUES_FOR_REPO_URL = 'https://api.github.com/repos/apache/activemq/pulls?state=all&per_page=100'
AUTH = (GITHUB_USER, GITHUB_PASSWORD)
keys=[]
def create_input_data(filename):
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        issues=[]
        for row in reader:
            #rint(row)
            if(row[0]!="Issue key" and row[0]!=''):
                issue=Issue_Tracking_System_Report(row[0],row[1],row[3],row[4])
                #print(issue.issue_key)
                y=re.findall(r'\b\d+\b', row[0])
                if(y!=[] and len(y[0])==4):
                    key=int(y[0])
                    #print(key)
                    keys.append(key)
                issues.append(issue)
        return issues
def finding_bugs_fixed_with_new_lines(response):
    if not r.status_code == 200:
        raise Exception(r.status_code)
    for pulls in r.json():
        r3=requests.get(pulls['issue_url'], auth=AUTH)
        issue=r3.json()
        y=re.findall(r'\b\d+\b', issue['title'])
        #print(c)
        row1=[issue['title'],issue['body'],pulls['number'],pulls['body']]
        bugout.writerow(row1)
        if(y!=[] and len(y[0])==4):
            key=int(y[0])
           
            if( key in keys):
                index=keys.index(key)
                print(key)
                #print(key in keys)
                #print("hi")
                pull_number='https://api.github.com/repos/apache/activemq/pulls/'+str(pulls['number'])
                r2=requests.get(pull_number, auth=AUTH)
                pull_details=r2.json()
                if(pull_details['deletions']==0 and pull_details['additions']>=1):
                    print(pull_details['deletions'])
                    print(pull_details['additions'])
                    row=[issues[index].issue_key,issues[index].description,pulls['node_id'],pulls['body']]
                    csvout.writerow(row)

r = requests.get(ISSUES_FOR_REPO_URL, auth=AUTH)
csvfile = 'bug_fixed_with_newlines_dataset.csv'
bugfile = 'pull_request_issues.csv'
bfile= open(bugfile, 'w',newline='')
file=open(csvfile, 'w',newline='')
csvout = csv.writer(file)
bugout = csv.writer(bfile)
csvout.writerow(('Bug ID', 'Bug Description', 'BFC Hash', 'BFC Description'))
bugout.writerow(('Issue Title', 'Issue Description', 'Pull Number', 'Pull Description'))
issues = create_input_data("ASF JIRA 2020-01-29T09_19_21+0000.csv")
##print(len(issues))
##print(issues[260].issue_key)
##print(issues[260].description)
finding_bugs_fixed_with_new_lines(r)
if 'link' in r.headers:
    pages = dict(
        [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
            [link.split(';') for link in
                r.headers['link'].split(',')]])
    while 'last' in pages and 'next' in pages:
        r = requests.get(pages['next'], auth=AUTH)
        finding_bugs_fixed_with_new_lines(r)
        if pages['next'] == pages['last']:
            break
        pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])
        
file.close()
bfile.close()


