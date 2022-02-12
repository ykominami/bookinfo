import json
import sqlite3
import cv2
import requests
import winsound
import threading
import xml.etree.ElementTree as et
from pyzbar.pyzbar import decode
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from websocket_server import WebsocketServer


class OrenoServer:

    def __init__(self):
        self.HOST = 'localhost'
        self.HTTP_PORT = 8080
        self.WS_PORT = 8081
        self.client = None
        self.wss = WebsocketServer(host=self.HOST, port=self.WS_PORT)
        self.wss.set_fn_new_client(self.new_client)
        self.https = ThreadingHTTPServer((self.HOST, self.HTTP_PORT), HttpHandler)

    def start(self):
        threading.Thread(target=self.wss.run_forever).start()
        threading.Thread(target=self.https.serve_forever).start()

    def shutdown(self):
        self.wss.shutdown()
        self.https.shutdown()

    def new_client(self, client, server):
        if self.client is None:
            self.client = client
            threading.Thread(target=self.cam_capture).start()

    def cam_capture(self):
        cap = cv2.VideoCapture(1)
        font = cv2.FONT_HERSHEY_SIMPLEX
        barcodes = []
        db = OrenoDataBase()

        while cap.isOpened():
            ret, frame = cap.read()

            if ret:
                d = decode(frame)

                if d:
                    for barcode in d:
                        barcode_data = barcode.data.decode('utf-8')

                        if self.is_isbn(barcode_data):

                            if barcode_data not in barcodes:
                                barcodes.append(barcode_data)

                                winsound.Beep(2000, 50)
                                font_color = (0, 0, 255)
                                result = self.fetch_book_data(barcode_data)
                                self.wss.send_message(self.client, json.dumps(result))
                                db.set(result)
                            else:
                                font_color = (0, 154, 87)

                            x, y, w, h = barcode.rect
                            cv2.rectangle(frame, (x, y), (x + w, y + h), font_color, 2)
                            frame = cv2.putText(frame, barcode_data, (x, y - 10), font, .5, font_color, 2, cv2.LINE_AA)

            cv2.imshow('BARCODE READER Press Q -> Exit', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        db.close()
        cap.release()
        self.shutdown()

    def fetch_book_data(self, isbn):
        endpoint = 'https://iss.ndl.go.jp/api/sru'
        params = {'operation': 'searchRetrieve',
                  'query': f'isbn="{isbn}"',
                  'recordPacking': 'xml'}

        res = requests.get(endpoint, params=params)
        root = et.fromstring(res.text)
        ns = {'dc': 'http://purl.org/dc/elements/1.1/'}
        title = root.find('.//dc:title', ns).text
        creator = root.find('.//dc:creator', ns).text
        publisher = root.find('.//dc:publisher', ns).text
        subject = root.find('.//dc:subject', ns).text

        return isbn, title, creator, publisher, subject

    def is_isbn(self, code):
        return len(code) == 13 and code[:3] == '978'


class OrenoDataBase:

    def __init__(self):
        self.table_def_stmt = f"""CREATE TABLE if not exists {self.table_name}(
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          isbn STRING,
          title STRING,
          creator STRING,
          publisher STRING,
          subject STRING
)"""

        self.conn = sqlite3.connect(r'C:\Users\ykomi\cur\python\isbn\book.sqlite')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.create_table()

    def create_table(self):
      try:
        self.cur.execute(self.table_def_stmt)
        # データベースへコミット。これで変更が反映される。
        self.conn.commit()
      except sqlite3.OperationalError as err:
        print( "Sqlite3db create_table sqlite3.OperationalError: {0}".format(err) )

    def get(self):
        self.cur.execute('SELECT * FROM ndl')
        rows = []

        for r in self.cur.fetchall():
            rows.append({'isbn': r['isbn'], 'title': r['title'], 'creator': r['creator'], 'publisher': r['publisher'], 'subject': r['subject']})

        return rows

    def set(self, values):
        place_holder = ','.join('?'*len(values))
        self.cur.execute(f'INSERT INTO ndl VALUES ({place_holder})', values)
        self.conn.commit()

    def close(self):
        self.cur.close()
        self.conn.close()


class HttpHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        with open(r'D:\bookshelf\template.html', mode='r', encoding='utf-8') as html:
            response_body = html.read()
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(response_body.encode('utf-8'))

    def do_POST(self):
        db = OrenoDataBase()
        rows = db.get()
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response_body = json.dumps(rows)
        self.wfile.write(response_body.encode('utf-8'))
        db.close()


server = OrenoServer()
server.start()

