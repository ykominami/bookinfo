from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#from google.auth.exceptions import RefreshError
from pathlib import Path
import os

class Credential:
  """
  Credentials for OAuth 2.0.
  """

  def __init__(self, env_gcp):
    self.creds = None
    self.SCOPES = env_gcp['SCOPES']
    self.token_path = env_gcp['token']
    self.credentials = env_gcp['credentials']

  def prepare_creds(self):
    if not self.creds and os.path.exists(self.token_path):
      self.creds = Credentials.from_authorized_user_file(self.token_path, self.SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not self.creds or not self.creds.valid:
        if self.creds and self.creds.expired and self.creds.refresh_token:
            self.creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials, self.SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(self.token_path, 'w') as token:
            token.write(self.creds.to_json())
    return self.creds

  def try_prepare_creds(self):
    counter = 0
    creds = None
    while counter < 2:
      try:
        creds = self.prepare_creds()
        return [True, creds]
      except google.auth.exceptions.RefreshError:
        self.logger.debug("RefreshError")
        Path(self.token_path).unlink(True)
        count += 1
    return [False, creds]

