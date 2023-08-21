# Copyright (C) 2021 Constantine Kulak (ck@vilia.fr)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import sys
from datetime import datetime
from os import getenv
from time import sleep

from atlassian import Bitbucket
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()
BB = Bitbucket(
    url=getenv("URL"),
    username=getenv("USERNAME"),
    password=getenv("PASSWORD"),
    timeout=int(getenv("TIMEOUT"))
)


def get_history(project, repo, key):
    history = list()
    try:
        for h in BB.get_pull_requests_activities(project, repo, key):
            s = {
                'id': h.get('id'),
                'user': h.get('user', {'name': 'N/A'}).get('name', 'N/A'),
                'action': h.get('action') + (('/' + h.get('commentAction')) if h.get('action') == 'COMMENTED' else ''),
                'when': h.get('createdDate'),
            }
            if 'comment' in h:
                s['comment'] = h.get('comment').get('text')
            history.append(s)
    except:
        print(f"WARNING: Could not get history for {key}")
    return history


def simplify_pr(pr):
    pr['fromCommit'] = pr.get('fromRef').get('latestCommit')
    pr['fromRef'] = pr.get('fromRef').get('displayId')
    
    pr['toCommit'] = pr.get('toRef').get('latestCommit')
    pr['toRef'] = pr.get('toRef').get('displayId')
    
    pr['author'] = pr.get('author').get('user').get('name')

    if 'reviewers' in pr:
        revs = list()
        for r in pr.get('reviewers'):
            revs.append({
                'user': r.get('user').get('name'),
                'status': r.get('status')
            })
        pr['reviewers'] = revs

    if 'participants' in pr:
        parts = list()
        for r in pr.get('participants'):
            parts.append(r.get('user').get('name'))
        pr['participants'] = parts

    return pr


def get_all_pull_requests(project, repo):
    prs = list()
    start_at = 0
    max_results = 10000
    total = max_results + 1
    while start_at < total:
        print(f'Querying starting from {start_at}...')
        res = list(BB.get_pull_requests(project, repo, state='ALL', order='newest', limit=max_results, start=start_at))
        max_results = len(res)
        start_at += max_results
        total = len(prs)
        prs += res
    return prs


def get_pull_requests(project, repo):
    res = get_all_pull_requests(project, repo)
    print(f'Queried {len(res)} pull requests')
    with tqdm(total=len(res)) as pbar:
        for pr in res:
            pr = simplify_pr(pr)
            key = pr['id']
            history = get_history(project, repo, key)
            pr['history'] = history
            dump_one(f'pull_requests/{key}.json', pr)
            sleep(1)
            pbar.update(1)

    print(f'Processed {len(res)} pull requests')


def dump_one(filename, issue):
    with open(filename, 'w') as outfile:
        json.dump(issue, outfile, indent=2)


#####################################################################
######################### The main sequence #########################
#####################################################################

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python %s <PROJECT> <REPO>' % sys.argv[0])
        exit(1)

    project = sys.argv[1]
    repo = sys.argv[2]

    start_time = datetime.now()
    print(f'Bitbucket extract starts at {start_time}')

    all_prs = dict()
    get_pull_requests(project, repo)
    print(f'Downloaded {len(all_prs)} pull requests')

    end_time = datetime.now()
    print(f'Finished at {end_time}, ran for {end_time - start_time}')
