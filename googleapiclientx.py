import os.path
import argparse
import csv
import sys
import glob

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleApiClientx:
  def __init__(self, env):
    self.env = env
    self.SCOPES = env.get_SCOPES()
    # The ID and range of a sample spreadsheet.
    # SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    self.SPREADSHEET_ID = self.env.SPREADSHEET_ID #'1bx2wC_XhNvQOhdNiK1JTx1UcfXHMHpsMelxuhk0yrEo'

    self.SAMPLE_RANGE_NAME = self.env.SAMPLE_RANGE_NAME #'A2:E'
    self.RANGE_NAME = self.env.RANGE_NAME #'A1'
    self.MAJOR_DIMENSION = self.env.MAJOR_DIMENSION #'ROWS'
    # self.credentials = 'client_secret_5085137207-7htsb4c94uqo61hi3so5oiasbhv4terh.apps.googleusercontent.com.json'
    self.credentials = self.env.credentials

  def get_file_paths(self, path):
    target_path = os.path.join(path , 'webapi*.csv')
    print( 'target_path=%s'  % (target_path) )
    files = glob.glob( target_path )
    return files

  def get_content(self, path):
    f = open(path, 'r', encoding='UTF-8')
    data = f.read()
    f.close()
    return data

  def prepare_creds(self):
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    #
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json',self.SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                self.credentials, self.SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

  def upload2gss(self, data):
    creds = self.prepare_creds()
    clear_range="A1:J"
    # X clear_range="Sheet1:A1J900"
    try:
      body = {
              "range": self.RANGE_NAME,
              "majorDimension": self.MAJOR_DIMENSION,
              "values": data
              }
      service = build('sheets', 'v4', credentials=creds)
      sheet = service.spreadsheets()
      resource = sheet.values()
      resource.clear(spreadsheetId=self.SPREADSHEET_ID, range=clear_range).execute()
      resource.append(spreadsheetId=self.SPREADSHEET_ID, range=self.RANGE_NAME,
                      valueInputOption='USER_ENTERED', body=body).execute()
    except HttpError as err:
      print(err)
