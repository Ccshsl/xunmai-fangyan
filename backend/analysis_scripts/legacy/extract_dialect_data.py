# -*- coding: utf-8 -*-
"""
提取 dialect_info 字典并保存为 JSON 文件
运行方法：在命令行中执行 python extract_dialect_data.py
"""
import json
import re
import os

# 项目根目录 - 固定为桌面路径
script_dir = r'C:\Users\林宝澄\Desktop\寻脉方言系统'
app_path = os.path.join(script_dir, 'app.py')
output_path = os.path.join(script_dir, 'data', 'dialect_data.json')

print(f"正在读取: {app_path}")
print(f"输出路径: {output_path}")

# 读取 app.py 文件
with open(app_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 使用正则表达式提取 dialect_info 字典
start_pattern = r'dialect_info\s*=\s*\{'
start_match = re.search(start_pattern, content)

if start_match:
    start_pos = start_match.end() - 1  # 包含 { 字符
    
    # 找到对应的闭合 }
    brace_count = 0
    end_pos = start_pos
    
    for i, char in enumerate(content[start_pos:], start_pos):
        if char == '{':
            brace_count += 1
        elif char == '}':
            brace_count -= 1
            if brace_count == 0:
                end_pos = i + 1
                break
    
    # 提取字典字符串
    dict_str = content[start_pos:end_pos]
    
    # 使用 eval 解析字典
    dialect_info = eval(dict_str)
    
    # 保存为 JSON 文件
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(dialect_info, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ 成功提取 {len(dialect_info)} 个城市的方言数据")
    print(f"✓ 已保存到: {output_path}")
    
    # 显示城市列表
    print(f"\n城市列表:")
    for i, city in enumerate(dialect_info.keys(), 1):
        print(f"  {i}. {city}")
else:
    print("未找到 dialect_info 字典")
