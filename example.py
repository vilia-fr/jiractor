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
import datetime
import json
from datetime import timedelta, datetime

import iso8601

one_month_ago = (datetime.today() - timedelta(days=30)).astimezone()

# Extract all reopened issues in the last 30 days
with open('all.json') as file:
    issues = json.load(file)['issues']
    reopened = dict()
    for issue_id in issues:
        issue = issues[issue_id]
        for sprint in issue.get('Sprint', list()):
            for h in issue.get('history', list()):
                if h['what'] == 'status' and h['to'] == 'Reopened' and iso8601.parse_date(h['when']) >= one_month_ago:
                    if issue_id not in reopened:
                        reopened[issue_id] = list()
                    reopened[issue_id].append(h["when"].split('T')[0])

    print(f"{len(reopened)} issues were reopened since {one_month_ago.strftime('%Y-%m-%d')}:")
    for issue in reopened:
        print(f" - {issue} was reopened {len(reopened[issue])} times: {', '.join(reopened[issue])}")
