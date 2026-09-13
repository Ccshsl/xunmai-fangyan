import os
import zipfile
from pathlib import Path


def get_desktop_path():
    """获取桌面路径"""
    return os.path.join(os.path.expanduser("~"), "Desktop")


def should_include(path):
    """判断是否应该包含该文件/目录"""
    # 排除 __pycache__ 目录
    if "__pycache__" in path:
        return False

    # 排除 .pyc 文件
    if path.endswith(".pyc"):
        return False

    return True


def package_project():
    """打包寻脉方言系统源代码"""
    source_dir = r'C:\Users\林宝澄\Desktop\寻脉方言系统'
    desktop_dir = get_desktop_path()
    zip_name = "寻脉系统源代码.zip"
    zip_path = os.path.join(desktop_dir, zip_name)

    # 确保桌面目录存在
    os.makedirs(desktop_dir, exist_ok=True)

    print(f"正在打包寻脉方言系统源代码...")
    print(f"源目录: {source_dir}")
    print(f"目标路径: {zip_path}")
    print()

    # 统计文件数量
    file_count = 0
    total_size = 0

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        # 遍历目录
        for root, dirs, files in os.walk(source_dir):
            # 排除 __pycache__ 目录
            dirs[:] = [d for d in dirs if d != "__pycache__"]

            for file in files:
                file_path = os.path.join(root, file)

                # 检查是否应该包含
                if not should_include(file_path):
                    continue

                # 计算相对路径
                arcname = os.path.relpath(file_path, source_dir)

                # 跳过 zip 文件本身（如果之前存在）
                if arcname == zip_name or arcname == "package_source.py":
                    continue

                try:
                    # 添加到压缩包
                    zipf.write(file_path, arcname)
                    file_count += 1
                    total_size += os.path.getsize(file_path)

                    if file_count % 50 == 0:
                        print(f"  已添加 {file_count} 个文件...")
                except Exception as e:
                    print(f"  警告: 无法添加 {arcname}: {e}")

    print()
    print(f"打包完成!")
    print(f"文件总数: {file_count}")
    print(f"压缩包大小: {total_size / 1024:.1f} KB")
    print(f"压缩包路径: {zip_path}")
    print()
    print("包含的内容:")
    print("  - Python 源代码 (app.py, run_all.py 等)")
    print("  - scripts/ 目录下的所有脚本")
    print("  - templates/ 目录下的 HTML 模板")
    print("  - static/ 目录下的 CSS/JS 文件")
    print("  - data/ 目录下的数据文件")
    print("  - outputs/ 目录下的输出文件")
    print("  - utils/ 目录下的工具模块")
    print("  - 启动脚本 (.bat 文件)")
    print()
    print("注意: 已自动排除 __pycache__ 目录和 .pyc 缓存文件")

    return zip_path


if __name__ == "__main__":
    package_project()
