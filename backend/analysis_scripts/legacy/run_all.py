"""
寻脉——方言地理分布与语言演变可视化系统
主运行脚本 - run_all.py
"""

import subprocess
import os
import sys
import time

PROJECT_ROOT = r'C:\Users\林宝澄\Desktop\寻脉方言系统'

def clear_screen():
    """清屏"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """打印系统标题"""
    clear_screen()
    print("╔════════════════════════════════════════════════════════════════╗")
    print("║                    寻脉——方言地理分布与语言演变可视化系统                 ║")
    print("╚════════════════════════════════════════════════════════════════╝")
    print()

def run_script(script_name, description):
    """运行指定脚本"""
    print(f"\n- {description}")
    print(f"   正在运行: {script_name}...")
    print()
    
    try:
        env = os.environ.copy()
        env['PYTHONPATH'] = PROJECT_ROOT + ';' + os.path.join(PROJECT_ROOT, 'venv', 'Lib', 'site-packages')
        
        result = subprocess.run(
            [sys.executable, f'scripts/{script_name}'],
            capture_output=True,
            timeout=120,
            env=env
        )
        
        stdout_text = result.stdout.decode('utf-8', errors='replace')
        stderr_text = result.stderr.decode('utf-8', errors='replace')
        
        if result.returncode != 0:
            print("   [失败]")
            if stderr_text.strip():
                print("   错误信息:")
                for line in stderr_text.strip().split('\n')[:10]:
                    print("      " + line)
            return False
        
        if stdout_text.strip():
            for line in stdout_text.strip().split('\n'):
                print("   " + line)
        
        return True
    except subprocess.TimeoutExpired:
        print("   [超时]")
        return False
    except Exception as e:
        print(f"   [错误] {e}")
        return False

def show_menu():
    """显示主菜单"""
    print_header()
    print("                         系统功能菜单")
    print("════════════════════════════════════════════════════════════════")
    print("  1. 完整运行 - 执行所有分析脚本")
    print("  2. 数据准备 - 生成方言点数据")
    print("  3. 数据清洗 - 处理数据并添加派生字段")
    print("  4. 统计分析 - 方言区人口和使用率统计")
    print("  5. 空间分析 - 等语线和缓冲区分析")
    print("  6. 可视化 - 生成统计图表")
    print("  7. 交互地图 - 创建方言分布地图")
    print("  8. 相似度分析 - 方言聚类分析")
    print("  9. 演变模拟 - 50年语言演变预测")
    print("  10. 打开地图 - 在浏览器中查看交互地图")
    print("  11. 启动Web平台 - 地理课堂教学平台")
    print("  0. 退出系统")
    print("════════════════════════════════════════════════════════════════")

def run_all():
    """运行所有脚本"""
    print_header()
    print("开始执行完整分析流程...")
    print("════════════════════════════════════════════════════════════════")
    
    scripts = [
        ('1_data_preparation.py', '数据准备 - 创建方言点数据'),
        ('2_data_cleaning.py', '数据清洗 - 处理缺失值和异常值'),
        ('3_statistics.py', '统计分析 - 人口和使用率统计'),
        ('4_spatial_analysis.py', '空间分析 - 等语线和缓冲区'),
        ('5_matplotlib_viz.py', '可视化 - 生成统计图表'),
        ('6_folium_map.py', '交互地图 - 创建方言分布地图'),
        ('7_similarity_analysis.py', '相似度分析 - 层次聚类'),
        ('8_evolution_sim.py', '演变模拟 - 50年预测')
    ]
    
    success_count = 0
    for script, desc in scripts:
        if run_script(script, desc):
            success_count += 1
        time.sleep(0.5)
    
    print("\n════════════════════════════════════════════════════════════════")
    print(f"🏁 分析完成！成功: {success_count}/{len(scripts)}")
    print("════════════════════════════════════════════════════════════════")
    
    # 列出输出文件
    print("\n📁 生成的输出文件:")
    output_dir = 'outputs'
    files = sorted(os.listdir(output_dir))
    for f in files:
        size = os.path.getsize(os.path.join(output_dir, f)) / 1024
        print(f"   ✅ {f} ({size:.1f} KB)")
    
    input("\n按 Enter 键返回菜单...")

def open_map():
    """打开交互地图"""
    print_header()
    print("正在启动地图查看器...")
    
    # 启动HTTP服务器并打开地图
    try:
        import threading
        import webbrowser
        import http.server
        import socketserver
        
        PORT = 8080
        
        def start_server():
            os.chdir('outputs')
            Handler = http.server.SimpleHTTPRequestHandler
            with socketserver.TCPServer(("", PORT), Handler) as httpd:
                httpd.serve_forever()
        
        # 在后台启动服务器
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # 等待服务器启动
        time.sleep(2)
        
        # 打开浏览器
        webbrowser.open(f'http://localhost:{PORT}/dialect_map.html')
        
        print(f"地图已在浏览器中打开")
        print(f"地址: http://localhost:{PORT}/dialect_map.html")
        print("\n按 Ctrl+C 停止服务器并返回菜单...")
        
        # 保持运行
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n服务器已停止")
            
    except Exception as e:
        print(f"启动失败: {e}")
        print("\n请手动访问 outputs/dialect_map.html")
        input("按 Enter 键返回菜单...")

def start_web_platform():
    """启动Web教学平台"""
    print_header()
    print("正在启动Web教学平台...")
    
    try:
        import subprocess
        import webbrowser
        import time
        
        # 启动Flask服务器
        flask_process = subprocess.Popen(
            [sys.executable, 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            encoding='utf-8',
            errors='replace'
        )
        
        # 等待服务器启动
        time.sleep(3)
        
        # 检查是否启动成功
        if flask_process.poll() is None:
            # 打开浏览器
            webbrowser.open('http://localhost:5000')
            
            print("Web教学平台已启动")
            print("地址: http://localhost:5000")
            print("\n按 Ctrl+C 停止服务器并返回菜单...")
            
            # 等待用户停止
            try:
                flask_process.wait()
            except KeyboardInterrupt:
                flask_process.terminate()
                print("\n服务器已停止")
        else:
            stdout, stderr = flask_process.communicate()
            print(f"启动失败: {stderr}")
            input("按 Enter 键返回菜单...")
            
    except Exception as e:
        print(f"启动失败: {e}")
        input("按 Enter 键返回菜单...")

def main():
    """主函数"""
    while True:
        show_menu()
        
        try:
            choice = input("\n请输入选择 (0-11): ")
            
            if choice == '0':
                print("\n👋 感谢使用寻脉系统！再见！")
                break
            
            elif choice == '1':
                run_all()
            
            elif choice == '2':
                run_script('1_data_preparation.py', '数据准备')
                input("按 Enter 键返回菜单...")
            
            elif choice == '3':
                run_script('2_data_cleaning.py', '数据清洗')
                input("按 Enter 键返回菜单...")
            
            elif choice == '4':
                run_script('3_statistics.py', '统计分析')
                input("按 Enter 键返回菜单...")
            
            elif choice == '5':
                run_script('4_spatial_analysis.py', '空间分析')
                input("按 Enter 键返回菜单...")
            
            elif choice == '6':
                run_script('5_matplotlib_viz.py', '可视化')
                input("按 Enter 键返回菜单...")
            
            elif choice == '7':
                run_script('6_folium_map.py', '交互地图')
                input("按 Enter 键返回菜单...")
            
            elif choice == '8':
                run_script('7_similarity_analysis.py', '相似度分析')
                input("按 Enter 键返回菜单...")
            
            elif choice == '9':
                run_script('8_evolution_sim.py', '演变模拟')
                input("按 Enter 键返回菜单...")
            
            elif choice == '10':
                open_map()
            
            elif choice == '11':
                start_web_platform()
            
            else:
                print("❌ 无效选择，请输入 0-11")
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n\n👋 感谢使用寻脉系统！再见！")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            input("按 Enter 键返回菜单...")

if __name__ == "__main__":
    main()