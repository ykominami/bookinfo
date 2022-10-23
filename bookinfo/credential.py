from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from pathlib import Path
import pickle
import os
# import sys
from bookinfo.util import Util

class Credential:
    """
    Credentials for OAuth 2.0.
    """

    def __init__(self, env_gcp):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("Credentail using debug. start running")
        self.logger.debug("Credentail finished running")

        self.creds = None
        self.SCOPES = env_gcp["SCOPES"]
        self.token_path = env_gcp["token"]
        self.credentials = env_gcp["credentials"]

    def prepare_creds(self):
        self.logger.debug(self.token_path)
        if not self.creds:
            self.logger.debug("credentail 1")
            if os.path.exists(self.token_path):
                self.logger.debug("credentail 12")
                with open(self.token_path, "rb") as token:
                    self.logger.debug("credentail 2")
                    self.creds = pickle.load(token)
            else:
                self.logger.critical(f"Can't find {self.token_path}")
        else:
            self.logger.debug("credentail 3")

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials, self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            if self.creds:
                with open(self.token_path, "wb") as token:
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
                self.logger.critical(
                    "sqlite3.ProgrammingError: {sys.exc_info()[0]}"
                )

                Path(self.token_path).unlink(True)
                counter += 1
        return [False, creds]
