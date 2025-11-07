"""
检查Python实际导入的模块路径
"""
import sys
sys.path.insert(0, '.')

# 清除缓存
if 'api.subsidy_calculator' in sys.modules:
    del sys.modules['api.subsidy_calculator']
if 'api' in sys.modules:
    del sys.modules['api']

# 导入并检查
from api import subsidy_calculator

print("="*70)
print("模块路径信息")
print("="*70)
print(f"模块文件路径: {subsidy_calculator.__file__}")
print(f"模块名称: {subsidy_calculator.__name__}")

# 检查SubsidyParams的定义位置
from api.subsidy_calculator import SubsidyParams
print(f"\nSubsidyParams类定义在: {SubsidyParams.__module__}")

# 读取实际文件内容
import os
file_path = subsidy_calculator.__file__
print(f"\n实际文件路径: {file_path}")
print(f"文件是否存在: {os.path.exists(file_path)}")
print(f"文件大小: {os.path.getsize(file_path)} 字节")

# 读取文件前50行
print("\n" + "="*70)
print("文件内容（前50行，包含SubsidyParams定义）")
print("="*70)

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()
    in_class = False
    line_count = 0
    for i, line in enumerate(lines):
        if 'class SubsidyParams' in line:
            in_class = True
        if in_class:
            print(f"{i+1:3d}: {line.rstrip()}")
            line_count += 1
            if line_count > 30:  # 打印类定义后30行
                break
