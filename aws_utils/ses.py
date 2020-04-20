import boto3
import json

from aws_utils.s3 import S3

class SES:
    """ Class for the Simple Email Service """

    def __init__(self, region='eu-west-2'):
        """ Initialise Object """
        self.client = boto3.client(
            service_name='ses', region_name=region)
        self.recipients = ['usama.blavins1@gmail.com']
        self.source = 'infrastructure.provisioner@gmail.com'

    def upload_cft_deploy_email(self, template, region):
        """ Method that emails account owner about cft deployments """
        bucket_name = S3.get_bucket_from_cloudformation_template(template)

        email_subject = 'Deployment of {} in account'.format(bucket_name)
        email_message = \
            '{} has been deployed in {} through infrastructure provisioner'.format(
                bucket_name, region)
        message = Message()
        message.set_subject(email_subject)
        message.set_body('Text', email_message)
        return self.send_ses_email(message=message.get_message())

    def send_ses_email(self, message):
        """ Send an email using SES SMTP server """
        return self.client.send_email(
            Source=self.source,
            Destination={'ToAddresses':self.recipients},
            Message=message
        )

    def set_source(self, source):
        """ Setter for source email address """
        self.source = source

    def set_recipients(self, recipients):
        """ Setter for the recipients """
        if isinstance(recipients, list):
            self.recipients = recipients


class Message:
    """ Class for creating a message """

    def __init__(self):
        self.subject = {}
        self.body = {}

    def set_subject(self, data):
        """ Set the subject of the email """
        if isinstance(data, str):
            self.subject = {'Data':data}
    
    def get_subject(self):
        """ Get the subject of the email """
        return self.subject

    def set_body(self, body, data):
        """ Set the body of the email """
        bodies = ['Text', 'Html']

        if body in bodies:
            if isinstance(data, str) and data != '':
                self.body = {body: {'Data':data}}

    def get_body(self):
        """ Get the body of the email """
        return self.body

    def get_message(self):
        """ Get the email message """
        return {
            'Subject': self.subject,
            'Body': self.body
        }
