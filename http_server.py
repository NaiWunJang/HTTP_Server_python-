from http.server import BaseHTTPRequestHandler, HTTPServer
import time
import logging
import sys
import codecs

hostName = "127.0.0.1"
serverPort = 8000

class MyServer(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        if self.path == '/':
            fileName = './index.html'
        else :
            fileName = '.'+self.path
        #content = open(fileName, 'rb').read()
        #self.wfile.write(content)
        with codecs.open(fileName, encoding='utf-8') as f:
            for line in f:
                if u'<!--name-->' in line:
                    #line = u'<p>YTHsueh</p>'
                    line = line.replace(u'<!--name-->',u'YTHsueh')
                elif u'<!--DOB-->' in line:
                    line = u'<p>110年12月23日</p>'
                self.wfile.write(bytes(line, 'utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        #content_length = int(self.headers.get('Content-Length')) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_response()
        #post_data from byte to utf-8
        data_str = post_data.decode()
        data_dict = {}
        s1 = data_str.split('&')
        #將s1分解成兩個子字串s1[0] = 'acct=abc', s1[1] = 'pwd=123'
        for s in s1:
            s2 = s.split('=')
            #將s分解成兩個子字串s2[0] = 'acct', s2[1] = 'abc'
            data_dict[s2[0]] = s2[1]
        if u'data_display.html' in self.path:
            with codecs.open('.'+self.path, encoding='utf-8') as f:
                for line in f:
                    if u'<!--T1-->' in line:
                        line = line.replace(u'<!--T1-->', data_dict['T1'])
                    if u'<!--V1-->' in line:
                        line = line.replace(u'<!--V1-->', data_dict['V1'])
                    if u'<!--I1-->' in line:
                        line = line.replace(u'<!--I1-->', data_dict['I1'])
                    if u'<!--T2-->' in line:
                        line = line.replace(u'<!--T2-->', data_dict['T2'])
                    if u'<!--V2-->' in line:
                        line = line.replace(u'<!--V2-->', data_dict['V2'])
                    if u'<!--I2-->' in line:
                        line = line.replace(u'<!--I2-->', data_dict['I2'])
                    if u'<!--T3-->' in line:
                        line = line.replace(u'<!--T3-->', data_dict['T3'])
                    if u'<!--V3-->' in line:
                        line = line.replace(u'<!--V3-->', data_dict['V3'])
                    if u'<!--I3-->' in line:
                        line = line.replace(u'<!--I3-->', data_dict['I3'])
                    if u'<!--T4-->' in line:
                        line = line.replace(u'<!--T4-->', data_dict['T4'])
                    if u'<!--V4-->' in line:
                        line = line.replace(u'<!--V4-->', data_dict['V4'])
                    if u'<!--I4-->' in line:
                        line = line.replace(u'<!--I4-->', data_dict['I4'])
                    self.wfile.write(bytes(line, 'utf-8'))
                self.wfile.write(bytes(line, 'utf-8'))
            self.wfile.write(post_data)
        else:
            if data_dict['acct'] == 'abc' and data_dict['pwd']=='123':
                if self.path == u'/data_input.html':
                    content = open('.'+self.path, 'rb').read()
                    self.wfile.write(content)
            else:
                content = open('./error.html', 'rb').read()
                self.wfile.write(content)
            data = self.path + ':' + post_data.decode()
            self.wfile.write(bytes(data,'utf-8'))

if __name__ == "__main__":        
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received, exiting.")
        webServer.server_close()
        print("Server stopped.")
        sys.exit(0)
