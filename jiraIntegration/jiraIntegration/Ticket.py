import requests
import json
from requests.auth import HTTPBasicAuth
from Configs import Configs
from BaseClass import BaseClass


class Ticket(BaseClass):
    FIELDS_KEY = 'fields'
    PROJECT_KEY = 'project'
    SUMMARY_KEY = 'summary'
    DESCRIPTION_KEY = 'description'
    ISSUETYPE_KEY = 'issuetype'
    LABELS_KEY = 'labels'
    CONFIGS = Configs.get()

    def __init__(self, data, is_lambda):
        self.data = data
        self.summary = self.get_summary(data)
        self.ticket_data = {self.FIELDS_KEY: {}}
        self.jira_auth = self.get_jira_auth()
        self.ticket_url = None
        super(Ticket, self).__init__(is_lambda)
        if 'key' in data:
            self._load_ticket_from_key(data['key'])
        self.set_ticket_data()
    
    def _load_ticket_from_key(self, key):
        try:

            find_ticket_url = '{0}/rest/api/2/issue/{1}'.format(self.CONFIGS['jira_url'], key)
            headers = {'Content-Type': 'application/json'}
            request = requests.get(find_ticket_url, headers=headers, auth=self.jira_auth)
            if request.status_code == 200:
                self.load_ticket(request.json())
        except Exception as e:
            super(Ticket, self).print_error('Error occurred while creating ticket', e)
        
    def load_ticket(self, ticket_data):

        self.key = ticket_data['key']
        self.ticket_type = ticket_data['fields']['issuetype']
        self.fixVersions = ticket_data['fields']['fixVersions']
        self.created = ticket_data['fields']['created']
        self.priority = ticket_data['fields']['priority']
        self.labels = ticket_data['fields']['labels']
        self.assignee = ticket_data['fields']['assignee']
        self.updated = ticket_data['fields']['updated']
        self.status = ticket_data['fields']['status']
        self.description = ticket_data['fields']['description']
        self.creator = ticket_data['fields']['creator']
        self.project = ticket_data['fields']['project']
        self.subject = ticket_data['fields']['summary']


    def set_ticket_data(self):
        self.update_ticket(self.get_project_field())
        self.update_ticket(self.get_summary_field())
        self.update_ticket(self.get_description_field())
        self.update_ticket(self.get_issuetype_field())
        self.update_ticket(self.get_labels_field())
        self.set_custom_fields()

    def create(self):
        try:
            headers = {'Content-Type': 'application/json'}
            create_ticket_url = '{0}/rest/api/2/issue/'.format(self.CONFIGS['jira_url'])
            request = requests.post(create_ticket_url, headers=headers, auth=self.jira_auth,
                                    data=json.dumps(self.ticket_data))
            # Printing below will help determine why ticket creation failed. e.g. "custom_fields" your ticket requires
            self._load_ticket_from_key(request.json()['key'])
        except Exception as e:
            super(Ticket, self).print_error('Error occurred while creating ticket', e)

    def update(self):
        pass
        #todo

    def move_to_sprint(self, sprint_id):
        try:
            headers = {'Content-Type': 'application/json'}
            create_ticket_url = '{0}/rest/api/2/issue/{1}'.format(self.CONFIGS['jira_url'], self.key)

            body = {"update": {"customfield_10010": [{"set": sprint_id}]}}
            request = requests.put(create_ticket_url, headers=headers, auth=self.jira_auth,
                                    data=json.dumps(body))
            # Printing below will help determine why ticket creation failed. e.g. "custom_fields" your ticket requires
            self.load_ticket(request.json())
        except Exception as e:
            super(Ticket, self).print_error('Error occurred while creating ticket', e)

    def change_status(self, status):
        try:

            headers = {'Content-Type': 'application/json'}

            status_change_ticket_url = '{0}/rest/api/2/issue/{1}/transitions'.format(self.CONFIGS['jira_url'], self.key)
            status = status.lower()
            status_hash = {
                "todo": "11",
                "in_progress": "21",
                "done": "31"
            }
            if status not in status_hash:
                return False
            body = {"transition": {"id": status_hash[status]}}
            request = requests.post(status_change_ticket_url, headers=headers, auth=self.jira_auth,
                                   data=json.dumps(body))
            print request
            # Printing below will help determine why ticket creation failed. e.g. "custom_fields" your ticket requires
            self.load_ticket(request.json())
        except Exception as e:
            super(Ticket, self).print_error('Error occurred while creating ticket', e)


    def set_custom_fields(self):
        try:
            custom_fields = self.CONFIGS['custom_fields']
            if custom_fields:
                for custom_field, value in custom_fields.iteritems():
                    self.update_ticket({custom_field: value})
        except Exception as e:
            super(Ticket, self).print_error('Could not set custom fields. Please refer to documentation', e)

    def get_issuetype_field(self):
        issue_type = self.data.get(self.ISSUETYPE_KEY, self.CONFIGS['issuetype'])
        if issue_type.lower() == "bug":
            issue_type = "Bug"
        elif issue_type.lower() == "story":
            issue_type = "Story"

        return {self.ISSUETYPE_KEY: {'name': issue_type}}

    def get_project_field(self):
        return {self.PROJECT_KEY: {'key': self.CONFIGS['jira_project']}}

    def get_labels_field(self):
        return {self.LABELS_KEY: self.data.get(self.LABELS_KEY, None)}

    def get_summary_field(self):
        return {self.SUMMARY_KEY: self.summary}

    def get_description_field(self):
        return {self.DESCRIPTION_KEY: "Ticket created by Alexa"}

    def update_ticket(self, data):
        if data is not None:
            self.ticket_data[self.FIELDS_KEY].update(data)

    def get_summary(self, data):
        return data['subject']

    @classmethod
    def get_jira_auth(_self):
        return HTTPBasicAuth(_self.CONFIGS['jira_username'], _self.CONFIGS['jira_password'])

    def to_hash(self):
        return {
            'key': self.key,
            'type': self.ticket_type['name'],
            'project': self.project['key'],
            'description': self.description,
            'subject': self.summary,
            'priority': self.priority['name']
        }
