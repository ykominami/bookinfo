import sys
import os
import inspect

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bookinfo.util import Util

class GoogleApiClientx:
    def __init__(self, env_table, credential):
        self.logger = Util.getLoggerx(__name__)
        self.logger.debug("using debug. start running")
        self.logger.debug("finished running")

        self.env_table = env_table
        self.credential = credential
        # The ID and range of a sample spreadsheet.
        # SAMPLE_SPREADSHEET_ID = '1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms'
        self.SPREADSHEET_ID = self.env_table[
            "SPREADSHEET_ID"
        ]  #'1bx2wC_XhNvQOhdNiK1JTx1UcfXHMHpsMelxuhk0yrEo'

        self.SAMPLE_RANGE_NAME = self.env_table["SAMPLE_RANGE_NAME"]  #'A2:E'
        self.RANGE_NAME = self.env_table["RANGE_NAME"]  #'A1'
        self.MAJOR_DIMENSION = self.env_table["MAJOR_DIMENSION"]  #'ROWS'
        # self.credentials = 'client_secret_5085137207-7htsb4c94uqo61hi3so5oiasbhv4terh.apps.googleusercontent.com.json'

    def get_spreadsheet_service(self):
        sheet = None
        result, creds = self.credential.try_prepare_creds()
        if not result:
            return [result, creds]

        try:
            service = build("sheets", "v4", credentials=creds)
            sheet = service.spreadsheets()
        except HttpError as err:
            self.logger.critical(err)
            self.logger.critical("HttpError: {sys.exc_info()[0]}")

        return [result, sheet]

    def gss_get(
        self,
        res_path,
        ranges,
        *,
        value_render_option="FORMATTED_VALUE",
        date_time_render_option="FORMATTED_STRING",
    ):
        self.response = None
        self.resource = None

        if res_path != None:
            self.response = Util.load_pickle(res_path)
            if self.response != None:
                return self.response

        if self.resource == None:
            result, sheet = self.get_spreadsheet_service()
            if not result:
                return self.resource
            self.resource = sheet.values()

        try:
            request = self.resource.get(
                spreadsheetId=self.SPREADSHEET_ID,
                range=ranges,
                valueRenderOption=value_render_option,
                dateTimeRenderOption=date_time_render_option,
            )
            self.response = request.execute()
            self.logger.debug(f"request={request}")
            Util.save_pickle(res_path, self.response)

        except HttpError as err:
            self.logger.critical(err)
            self.logger.critical(f"HttpError: {sys.exc_info()[0]}")
        except Exception as err:
            self.logger.critical(err)

        return self.response

    def upload2gss_batchUpdate_with_body(self, res_path, body, clear_flag):
        self.logger.critical(f"{ inspect.currentframe().f_code.co_name } 0")
        self.logger.debug(f"body={body}")
        clear_range = self.env_table["clear_range"]  # "A1:J"
        self.response = None
        self.resource = None
        self.sheetid = None

        if res_path != None:
            self.response = Util.load_pickle(res_path)
            if self.response != None:
                return self.response

        if self.resource == None:
            result, sheet = self.get_spreadsheet_service()
            if not result:
                return self.response
            self.resource = sheet.values()

        try:
            if clear_flag:
                self.logger.debug("clear all")
                self.resource.clear(
                    spreadsheetId=self.SPREADSHEET_ID, range=clear_range
                ).execute()

            response = sheet.batchUpdate(
                spreadsheetId=self.SPREADSHEET_ID, body=body
            ).execute()
            sheetid = response["replies"][0]["addSheet"]["properties"]["sheetId"]
            self.logger.debug(response["replies"][0]["addSheet"]["properties"])
        except HttpError as err:
            self.logger.critical(err)
            self.logger.critical(f"HttpError: {sys.exc_info()[0]}")
        except Exception as err:
            self.logger.critical(err)
        finally:
            self.logger.debug(self.sheetid)

        try:
            with open(res_path, "wb") as resx_w:
                Util.save_pickle(res_path, self.response)
        except Exception as err:
            self.logger.critical(err)

        self.logger.critical(f"{ inspect.currentframe().f_code.co_name } 1")

        return self.response

    def upload2gss_update_with_body(
        self, res_path, body, value_input_option, clear_flag=False
    ):
        self.logger.critical(f"googleapiclientx.py upload2gss_update_with_body { inspect.currentframe().f_code.co_name } 0")
        self.response = None
        self.resource = None

        if res_path != None:
            self.response = Util.load_pickle(res_path)
            if self.response != None:
                return self.response

        if self.resource == None:
            result, sheet = self.get_spreadsheet_service()
            if not result:
                self.logger.critical(f"upload2gss_update_with_body self.response 1")
                return self.response
            self.resource = sheet.values()

        clear_range = self.env_table["clear_range"]  # "A1:J"
        valid_flag = True

        if clear_flag:
            self.logger.critical(f"{inspect.currentframe().f_code.co_name} 0-3")
            self.response, exc_happen = self.upload2gss_update_with_body_sub_clear(
                clear_range
            )
            if self.response is None or exc_happen:
                valid_flag = False

        self.logger.critical(f"upload2gss_update_with_body { inspect.currentframe().f_code.co_name } 0-4")
        if valid_flag:
            self.logger.critical(f"{inspect.currentframe().f_code.co_name} 0-5")
            # value_input_option = 'USER_ENTERED'
            self.response, exc_happen = self.upload2gss_update_with_body_sub_3(
                body, value_input_option
            )
            Util.save_pickle(res_path, self.response)
        self.logger.critical(f"upload2gss_update_with_body { inspect.currentframe().f_code.co_name } 1")

        return self.response

    def upload2gss_update_with_body_sub_clear(self, clear_range):
        response = None
        exc_happen = False
        self.logger.critical(f"{ inspect.currentframe().f_code.co_name } 0")

        try:
            response = self.resource.clear(
                spreadsheetId=self.SPREADSHEET_ID, range=clear_range
            )
        except HttpError as err:
            self.logger.critical(err)
            self.logger.critical(f"HttpError: 2 {sys.exc_info()[0]}")
            exc_happen = True
        except Exception as err:
            self.logger.critical(err)
            self.logger.critical(f"Exception: 2 {sys.exc_info()[0]}")
            exc_happen = True

        self.logger.critical(f"{ inspect.currentframe().f_code.co_name } 1")
        return [response, exc_happen]

    def upload2gss_update_with_body_sub_3(self, body, value_input_option):
        response = None
        exc_happen = False
        self.logger.critical(f"{ inspect.currentframe().f_code.co_name } 0")

        range_ = self.RANGE_NAME
        body_x = {"values": body}
        try:
            response = self.resource.update(
                spreadsheetId=self.SPREADSHEET_ID,
                range=range_,
                valueInputOption=value_input_option,
                body=body_x,
            ).execute()
        except HttpError as err:
            self.logger.critical(err)
            self.logger.critical(f"HttpError: 3 {sys.exc_info()[0]}")
            exc_happen = True
        except Exception as err:
            self.logger.critical(err)
            self.logger.critical(f"Exception: 3 {sys.exc_info()[0]}")
            exc_happen = True

        self.logger.critical(f"{ inspect.currentframe().f_code.co_name } 1")
        return [response, exc_happen]

    def gss_create(self, title):
        self.response = None
        self.resource = None

        if self.resource == None:
            result, sheet = self.get_spreadsheet_service()
            if not result:
                return self.resource

            body = {"properties": {"title": title}}
            request = sheet.create(body=body)
            self.response = request.execute()
