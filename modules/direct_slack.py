# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: direct_slack

short_description: This is my direct slack module

version_added: "1.0.0"

description: This module dms someone via slack after looking up their email address

author:
    - Your Name (@Jacko161)
'''

from ansible.module_utils.basic import AnsibleModule
import requests
import json

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        email=dict(type='str', required=True),
        slack_token=dict(type='str', required=True),
        message=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    email = module.params['email']
    token = module.params['token']
    message = module.params['message']

    if not email or email == '':
        module.fail_json(msg='No target email was provided', **result)

    result = get_user_slack_id(email, token)

    try:
        user_id = result['user']['id']
    except:
        module.fail_json(msg='Failed to find user id', **result)

    post_message_to_slack(message, token, user_id)
    module.exit_json(**result)



def main():
    run_module()

def post_message_to_slack(text, slack_token, slack_channel):
    headers = {"Authorization" : "Bearer " + slack_token}
    return requests.post('https://slack.com/api/chat.postMessage', {
        'channel': slack_channel,
        'text': text
    }, headers=headers).json()

def get_user_slack_id(email, slack_token):
    headers = {"Authorization" : "Bearer " + slack_token}
    return requests.get('https://slack.com/api/users.lookupByEmail',{'email' : email}, headers=headers).json()


if __name__ == '__main__':
    main()
