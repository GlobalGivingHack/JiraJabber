import os
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
        self.set_ticket_data()

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
            print request.text
            self.ticket_url = request.json()['key']
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
        return {self.ISSUETYPE_KEY: {'name': self.data.get(self.ISSUETYPE_KEY, self.CONFIGS['issuetype'])}}

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

