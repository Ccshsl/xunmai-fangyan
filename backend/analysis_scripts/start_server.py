"""
启动本地HTTP服务器来查看地图
"""
import http.server
import socketserver
import os

# 设置服务器目录
os.chdir(r'C:\Users\林宝澄\Desktop\寻脉方言系统\outputs')

# 设置端口
PORT = 8000

# 创建服务器
Handler = http.server.SimpleHTTPRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print("HTTP服务器已启动")
    print(f"访问地址: http://localhost:{PORT}/dialect_map.html")
    print(f"测试地图: http://localhost:{PORT}/test_map.html")
    print("按 Ctrl+C 停止服务器")
    httpd.serve_forever()