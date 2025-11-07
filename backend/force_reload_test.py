"""
强制重新加载模块测试
"""
import sys
import importlib

# 清除已加载的模块
if 'api.subsidy_calculator' in sys.modules:
    del sys.modules['api.subsidy_calculator']
if 'api' in sys.modules:
    del sys.modules['api']

sys.path.insert(0, '.')

# 重新导入
from api.subsidy_calculator import SubsidyParams

print("="*70)
print("检查 SubsidyParams 类定义")
print("="*70)

params = SubsidyParams()

print("\n所有属性和值：")
attrs = [attr for attr in dir(params) if not attr.startswith('_')]
for attr in attrs:
    try:
        value = getattr(params, attr)
        print(f"  {attr}: {value}")
    except Exception as e:
        print(f"  {attr}: 无法访问 - {e}")

print("\n" + "="*70)
print("测试访问 low_income_cut")
print("="*70)

try:
    value = params.low_income_cut
    print(f"✅ 成功！low_income_cut = {value}")
except AttributeError as e:
    print(f"❌ 失败：{e}")
    print("\n可用的属性：")
    for attr in attrs:
        if 'income' in attr.lower() or 'cut' in attr.lower():
            print(f"  - {attr}")

print("\n" + "="*70)
print("检查类的 __annotations__（类型注解）")
print("="*70)

if hasattr(SubsidyParams, '__annotations__'):
    print("类型注解：")
    for key, value in SubsidyParams.__annotations__.items():
        print(f"  {key}: {value}")
else:
    print("没有类型注解")

print("\n" + "="*70)
print("检查类的 __dataclass_fields__（dataclass字段）")
print("="*70)

if hasattr(SubsidyParams, '__dataclass_fields__'):
    print("Dataclass字段：")
    for name, field in SubsidyParams.__dataclass_fields__.items():
        print(f"  {name}: default={field.default}, type={field.type}")
else:
    print("不是dataclass或没有字段信息")
