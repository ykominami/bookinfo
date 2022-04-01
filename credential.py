from logging import basicConfig, getLogger, DEBUG

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
#from googleapiclient.discovery import build
#from googleapiclient.errors import HttpError
#from google.auth.exceptions import RefreshError
from pathlib import Path
import pickle
import os

class Credential:
  """
  Credentials for OAuth 2.0.
  """

  def __init__(self, env_gcp):
    self.logger = getLogger(__name__)
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.creds = None
    self.SCOPES = env_gcp['SCOPES']
    self.token_path = env_gcp['token']
    self.credentials = env_gcp['credentials']

  def prepare_creds(self):
    self.logger.debug(self.token_path)
    if not self.creds:
      self.logger.debug("credentail 1")
      if os.path.exists(self.token_path):
        self.logger.debug("credentail 12")
        with open(self.token_path, 'rb') as token:
          self.logger.debug("credentail 2")
          self.creds = pickle.load(token)
      else:
        self.logger.debug("credentail 13")
    else:
      self.logger.debug("credentail 3")
    if not self.creds or not self.creds.valid:
      if self.creds and self.creds.expired and self.creds.refresh_token:
        self.creds.refresh(Request())
      else:
        flow = InstalledAppFlow.from_client_secrets_file(
          self.credentials, self.SCOPES)
        self.creds = flow.run_local_server(port=0)
      # Save the credentials for the next run
      with open(self.token_path, 'wb') as token:
        pickle.dump(self.creds, token)
    return self.creds

  def try_prepare_creds(self):
    counter = 0
    creds = None
    while counter < 2:
      try:
        creds = self.prepare_creds()
        return [True, creds]
      except:
        self.logger.critical("RefreshError")
        Path(self.token_path).unlink(True)
        counter += 1
    return [False, creds]

