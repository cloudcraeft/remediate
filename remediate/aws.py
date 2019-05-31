import boto3
from importlib import import_module
from io import StringIO
import sys


class ArgumentError(Exception):
    def __init__(self, message):
        self.message = message


class Client:
    """
    Client represents an AWS Client which can call and capture responses from AWS APIs via runbooks which
    contains the actual logic.
    """
    def __init__(self, **kwargs):
        self.args = kwargs
        self.capture = StringIO()
        self.old_out = sys.stdout
        sys.stdout = self.capture

    def get_session(self):
        region = self.args['region']
        if region is None:
            raise ArgumentError("No default region nor command region given")

        access_key = self.args['access_key']
        role_arn = self.args['role_arn']
        role_session_name = self.args['role_session_name']

        if access_key is None:
            if role_arn and role_session_name:
                sts_client = boto3.client('sts')
                sts_response = sts_client.assume_role(
                    RoleArn=role_arn,
                    RoleSessionName=role_session_name,
                    Policy=self.args['role_policy'],
                    DurationSeconds=self.args['session_duration']
                )
                session = boto3.session.Session(
                    region_name=region,
                    aws_access_key_id=sts_response['Credentials']['AccessKeyId'],
                    aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],
                    aws_session_token=sts_response['Credentials']['SessionToken']
                )
                return session
            else:
                raise ArgumentError("Must have role_arn and role_session_name when no access_key given")
        else:
            if role_arn and role_session_name:
                sts_client = boto3.client(
                    service_name='sts',
                    aws_access_key_id=access_key,
                    aws_secret_access_key=self.args['secret_key'],
                    verify=self.args['verify_certificate'],
                    config=self.args['config']
                )
                sts_response = sts_client.assume_role(
                    RoleArn=role_arn,
                    RoleSessionName=role_session_name,
                    Policy=self.args['role_policy'],
                    DurationSeconds=self.args['session_duration']
                )
                session = boto3.session.Session(
                    region_name=region,
                    aws_access_key_id=sts_response['Credentials']['AccessKeyId'],
                    aws_secret_access_key=sts_response['Credentials']['SecretAccessKey'],
                    aws_session_token=sts_response['Credentials']['SessionToken']
                )
                return session
            else:
                session = boto3.session.Session(
                    region_name=region,
                    aws_access_key_id=access_key,
                    aws_secret_access_key=self.args['secret_key'],
                )
                return session

    def run(self, runbook_id, incident):
        session = self.get_session()
        try:
            runbook = import_module('remediate.runbook.' + runbook_id)
        except ArgumentError as e:
            print(f'ERROR:Bad Arguments {e.message}')
        except Exception as e:
            print(f'ERROR:{runbook_id} ({incident}) {str(e)}')
        else:
            runbook.remediate(session, incident, None)
            print(f"DONE:{runbook_id}")
        sys.stdout = self.old_out
        return self.capture.getvalue()
