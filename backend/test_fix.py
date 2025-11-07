"""
测试修复后的 calculate_subsidy 调用
"""
import sys
sys.path.append('.')

from api.subsidy_calculator import calculate_subsidy

# 测试1：使用正确的参数名
print("="*60)
print("测试1：使用正确的参数名 (wage, contribution)")
print("="*60)
try:
    result1 = calculate_subsidy(wage=80000, contribution=10000)
    print("✅ 成功！")
    print(f"补贴金额: {result1['subsidy']}")
    print(f"补贴比例: {result1['ratio']}")
except Exception as e:
    print(f"❌ 失败: {e}")

# 测试2：使用位置参数
print("\n" + "="*60)
print("测试2：使用位置参数")
print("="*60)
try:
    result2 = calculate_subsidy(80000, 10000)
    print("✅ 成功！")
    print(f"补贴金额: {result2['subsidy']}")
    print(f"补贴比例: {result2['ratio']}")
except Exception as e:
    print(f"❌ 失败: {e}")

# 测试3：测试不同收入档位
print("\n" + "="*60)
print("测试3：测试不同收入档位")
print("="*60)

test_cases = [
    (30000, 6000, "低收入"),
    (80000, 10000, "中等收入"),
    (150000, 12000, "高收入"),
]

for wage, contrib, desc in test_cases:
    try:
        result = calculate_subsidy(wage, contrib)
        print(f"\n{desc} - 年收入¥{wage:,}, 缴费¥{contrib:,}")
        print(f"  补贴: ¥{result['subsidy']}")
        print(f"  比例: {result['ratio']*100:.2f}%")
        print(f"  是否触发: {result['triggered']}")
    except Exception as e:
        print(f"\n{desc} - ❌ 失败: {e}")

print("\n" + "="*60)
print("所有测试完成！")
print("="*60)
