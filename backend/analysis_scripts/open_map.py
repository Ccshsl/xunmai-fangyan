"""
启动服务器并自动打开地图
"""
import http.server
import socketserver
import threading
import webbrowser
import os

PORT = 8080

PROJECT_ROOT = r'C:\Users\林宝澄\Desktop\寻脉方言系统'

def start_server():
    os.chdir(os.path.join(PROJECT_ROOT, 'outputs'))
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("服务器运行在端口", PORT)
        httpd.serve_forever()

# 在后台启动服务器
server_thread = threading.Thread(target=start_server, daemon=True)
server_thread.start()

# 等待服务器启动
import time
time.sleep(1)

# 打开浏览器
webbrowser.open(f'http://localhost:{PORT}/dialect_map.html')

print("请在浏览器中查看地图")
print(f"地址: http://localhost:{PORT}/dialect_map.html")
print("按 Ctrl+C 停止")

# 保持脚本运行
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("服务器已停止")