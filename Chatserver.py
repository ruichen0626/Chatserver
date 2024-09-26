import socket
import threading

# 設定伺服器的 IP 和端口
SERVER_IP = '127.0.0.1'
SERVER_PORT = 12345

# 創建 socket 物件
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER_IP, SERVER_PORT))
server.listen()

clients = []
nicknames = []

# 廣播訊息給所有客戶端
def broadcast(message):
    for client in clients:
        client.send(message)

# 處理客戶端訊息
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} 離開了聊天室!'.encode('utf-8'))
            nicknames.remove(nickname)
            break

# 接受新連接
def receive():
    while True:
        client, address = server.accept()
        print(f"連接來自 {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"暱稱是 {nickname}")
        broadcast(f"{nickname} 加入了聊天室!".encode('utf-8'))
        client.send('連接到伺服器!'.encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print("伺服器正在運行...")
receive()