from logging import basicConfig, getLogger, DEBUG
#import os.path
#import sys
#import glob

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
#from credential import Credential
class GoogleApiClientx:
  def __init__(self, env_table, credential):
    self.logger = getLogger(__name__)
    self.logger.debug('using debug. start running')
    self.logger.debug('finished running')

    self.env_table = env_table
    self.credential = credential
    # The ID and range of a sample spreadsheet.
    # SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
    self.SPREADSHEET_ID = self.env_table['SPREADSHEET_ID'] #'1bx2wC_XhNvQOhdNiK1JTx1UcfXHMHpsMelxuhk0yrEo'

    self.SAMPLE_RANGE_NAME = self.env_table['SAMPLE_RANGE_NAME'] #'A2:E'
    self.RANGE_NAME = self.env_table['RANGE_NAME'] #'A1'
    self.MAJOR_DIMENSION = self.env_table['MAJOR_DIMENSION'] #'ROWS'
    # self.credentials = 'client_secret_5085137207-7htsb4c94uqo61hi3so5oiasbhv4terh.apps.googleusercontent.com.json'


  def get_spreadsheet_service(self):
    sheet = None
    result , creds = self.credential.try_prepare_creds()
    if not result:
      return [result, creds]

    try:
      service = build('sheets', 'v4', credentials=creds)
      sheet = service.spreadsheets()
    except HttpError as err:
      self.logger.debug(err)

    return [result, sheet]

  def upload2gss_append(self, data, clear_flag=False):
    body = {
            "range": self.RANGE_NAME,
            "majorDimension": self.MAJOR_DIMENSION,
            "values": data
            }
    ret = self.upload2gss_append_with_body(body, clear_flag)
    self.logger.debug(ret)
    return ret

  def upload2gss_append_with_body(self, body, clear_flag=False):
    clear_range = self.env_table['clear_range'] #"A1:J"
    ret = None

    result , sheet = self.get_spreadsheet_service()
    if not result:
      return ret

    try:
      resource = sheet.values()
      if clear_flag:
        self.logger.debug("clear all")
        resource.clear(spreadsheetId=self.SPREADSHEET_ID, range=clear_range).execute()
      else:
        self.logger.debug("Not clear all")

      ret = resource.append(spreadsheetId=self.SPREADSHEET_ID, range=self.RANGE_NAME,
                      valueInputOption='USER_ENTERED', body=body).execute()
    except HttpError as err:
      self.logger.debug(err)

    self.logger.debug(ret)
    return ret

  def upload2gss_batchUpdate(self, request):
    self.logger.debug('googleapiclientx.py | upload2gss_batchUpdate')
    body={'requests':request}

    ret = self.upload2gss_batchUpdate_with_body(body)
    return ret

  def upload2gss_update(self, request):
    body = {
            "request": request,
            }
    ret = self.upload2gss_update_with_body(body)

    return ret

  def upload2gss_batchUpdate_with_body(self, body, clear_flag=False):
    self.logger.debug("googleapiclientx.py | upload2gss_batchUpdate_with_body")
    self.logger.debug("body={}".format(body))
    clear_range = self.env_table['clear_range'] #"A1:J"
    response = None
    sheetid = None

    result , sheet = self.get_spreadsheet_service()
    if not result:
      return response

    try:
      resource = sheet.values()
      if clear_flag:
        self.logger.debug("clear all")
        resource.clear(spreadsheetId=self.SPREADSHEET_ID, range=clear_range).execute()
      response = sheet.batchUpdate(spreadsheetId=self.SPREADSHEET_ID, body=body).execute()
      sheetid=response['replies'][0]['addSheet']['properties']['sheetId']
      self.logger.debug(response['replies'][0]['addSheet']['properties'])
    except HttpError as err:
      self.logger.debug(err)
    self.logger.debug(sheetid)

    return response

  def upload2gss_update_with_body(self, body, value_input_option, insert_data_opeion, clear_flag=False):
    clear_range = self.env_table['clear_range'] #"A1:J"
    response = None
    result , sheet = self.get_spreadsheet_service()
    if not result:
      return response

    try:
      resource = sheet.values()
      if clear_flag:
        resource.clear(spreadsheetId=self.SPREADSHEET_ID, range=clear_range)
      result = resource.update(spreadsheetId=self.SPREADSHEET_ID, range=self.RANGE_NAME,
                      valueInputOption='USER_ENTERED', body=body).execute()
      #result = resource.update( spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, body=v).execute()
    except HttpError as err:
      self.logger.debug(err)

    return response

  def gss_get(self, ranges, *, value_render_option='FORMATTED_VALUE', date_time_render_option='FORMATTED_STRING'):
    response = None
    result , sheet = self.get_spreadsheet_service()
    if not result:
      return response

    try:
      request = sheet.values().get(spreadsheetId=self.SPREADSHEET_ID, range=ranges, valueRenderOption=value_render_option, dateTimeRenderOption=date_time_render_option)
      response = request.execute()
      #response = sheet.get(spreadsheetId=self.SPREADSHEET_ID, ranges=ranges,
      #                includeGridData=include_grid_data).execute()
      #result = resource.update( spreadsheetId=spreadsheet_id, range=range_, valueInputOption=value_input_option, body=v).execute()
      self.logger.critical("request={}".format(request))
    except HttpError as err:
      self.logger.critical(err)

    return response
