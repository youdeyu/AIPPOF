"""
读取并显示subsidy_calculator.py的关键行
"""
file_path = r'api\subsidy_calculator.py'

with open(file_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

print("="*70)
print("第105行附近（检查是否使用low_income_cut）")
print("="*70)
for i in range(100, 110):
    if i < len(lines):
        print(f"{i+1:3d}: {lines[i].rstrip()}")

print("\n" + "="*70)
print("第220行附近（检查是否使用low_income_cut）")
print("="*70)
for i in range(215, 225):
    if i < len(lines):
        print(f"{i+1:3d}: {lines[i].rstrip()}")

print("\n" + "="*70)
print("搜索所有包含'low_income'的行")
print("="*70)
for i, line in enumerate(lines):
    if 'low_income' in line.lower():
        print(f"{i+1:3d}: {line.rstrip()}")
