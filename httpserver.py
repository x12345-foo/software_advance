import socket
import threading
import re
import os

HOST = 'localhost';
PORT = 3333;
BUFSIZE = 4096;

#http ヘッダー群
LINE = '\n';
HTTP_200_STATUS = 'HTTP/1.0 200 OK\n';
HTTP_404_STATUS = 'HTTP/1.0 404 Not Found\n';
SERVER_NAME = 'Server: Python Http Server\n';
CONTENT_TYPE = 'Content-Type: text/html; charset=UTF-8\n'

def http_listen(client, path):
    if os.path.isfile(path):
        body = open(path);
        msg = LINE + HTTP_200_STATUS + SERVER_NAME + CONTENT_TYPE + LINE + body.read();
    
    else:
        msg = LINE + HTTP_404_STATUS + SERVER_NAME + CONTENT_TYPE + LINE;
    
    client.sendall(msg.encode('utf-8'));
    client.close();

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM); #ソケットを作成
server.bind((HOST, PORT)); #ソケットにホストとポートを割り当て
server.listen(); #接続準備

while True:
    print("Receiving a requenst");
    client, addr = server.accept(); #受信中
    print("Connectiong from: "+addr[0]);
    data = client.recv(BUFSIZE);

    path = re.search(rb'/[\w\./%]*', data); #HTTPリクエストからpathを抽出したかった
    path = "." + path.group().decode('utf-8');

    thred = threading.Thread(target=http_listen, args=(client, path)); #マルチスレッドの起動
    thred.start(); #実行