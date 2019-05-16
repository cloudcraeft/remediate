import boto3
from importlib import import_module
from io import StringIO
import sys


class Client:
    """
    Client represents and AWS Client which can call and capture responses from AWS APIs via runbooks which
    contains the actual logic.
    """
    def __init__(self, access_key_id, secret_access_key, region_name):
        self.access_key_id = access_key_id
        self.secret_access_key = secret_access_key
        self.region_name = region_name
        self.capture = StringIO()
        self.old_out = sys.stdout
        sys.stdout = self.capture

    def run(self, runbook_id, incident, region_name=None):
        session = boto3.Session(self.access_key_id, self.secret_access_key, region_name=region_name)
        try:
            runbook = import_module('remediate.runbook.' + runbook_id)
        except Exception as e:
            print(f'Cannot import/find runbook for {runbook_id} ({incident}). Error: {str(e)}')
        else:
            runbook.remediate(session, incident, None)
            print(f"{runbook_id} done")
        sys.stdout = self.old_out
        return self.capture.getvalue()

