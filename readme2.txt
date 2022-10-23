'target' | 'kindle', 'kindlejson', 'calibre', 'bookstore'
'cmd' | 'create', 'createall', 'update','updateall', 'json','json2', 
         'jsonall', 'batchupdate', 'batchupdate2', 'append'
'year' | 2022 2021 2020 2019 2018 2017 2016

createall
 (targetがbookstoreの場合のみ)
updateall
 (targetがbookstoreの場合のみ)

main.py bookstore createall
main.py bookstore 2014

main.py bookstore update 2022
main.py bookstore updateall

=================
# googleapiclientx

get_spreadsheet_service
(spreadsheetsのserviceを得る)
credentialを用いて接続

upload2gss_append(data, clear_flag)
  rangeをself.RANGE_NAMEとする
  valuesを引数data
  upload2gss_append_with_body呼び出し
    get_spreadsheet_service()でサービスを得る
    sheet.values()でデータを得る

    resource.append()で追加する

upload2gss_batchUpdate(request):
  requestからbodyをつくる
  upload2gss_update_with_body(body)
  get_spreadsheet_service() serviceを得る
  sheet.values()でresourceを得る
  resouceに対してclearする
  sheet.batchUpdate()でアップデート

upload2gss_update(self, request)
  upload2gss_update_with_body
    self.get_spreadsheet_service()

    sheet.values()
gss_get

(appbase.py)
get_gss
  gac.get_gss