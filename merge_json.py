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

#####################################################################
######################### The main sequence #########################
#####################################################################
import sys
from os import walk

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python %s <output.json>' % sys.argv[0])
        exit(1)

    out_filename = sys.argv[1]

    merged = dict()
    for (_, _, filenames) in walk('issues'):
        for filename in filenames:
            if filename.endswith('.json'):
                print(f'Loading issues from {filename}...')
                with open('issues/' + filename) as file:
                    issue = json.load(file)
                    merged[issue['key']] = issue

    print(f'Will output to {out_filename}')
    with open(out_filename, 'w') as outfile:
        json.dump({
            'issues': merged,
        }, outfile, indent=4)
    print(f'Done: {len(merged)} unique issues')
