import zipfile
import os

source_dir = r"C:\Users\HUAWEI\Desktop\1\寻脉方言系统"
output_path = r"C:\Users\HUAWEI\Desktop\寻脉方言系统.zip"

print(f"正在打包: {source_dir}")
print(f"输出路径: {output_path}")

with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, source_dir)
            zipf.write(file_path, arcname)
            print(f"添加: {arcname}")

print("打包完成！")