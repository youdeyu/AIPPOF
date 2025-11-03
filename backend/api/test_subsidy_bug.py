"""测试补贴计算bug"""
from subsidy_calculator import calculate_subsidy

# 测试年薪150000的情况
result = calculate_subsidy(150000, 12000)
print("="*60)
print("年薪150000，缴费12000元：")
print("="*60)
print(f"补贴金额: ¥{result['subsidy']:.2f}")
print(f"补贴率: {result['ratio']:.2f}%")
print(f"是否触发: {result['triggered']}")
print("\n补贴明细:")
for key, value in result['breakdown'].items():
    if isinstance(value, (int, float)):
        print(f"  {key}: {value:.2f}")
    else:
        print(f"  {key}: {value}")

# 测试临界值100000
print("\n" + "="*60)
result2 = calculate_subsidy(100000, 12000)
print("年薪100000，缴费12000元：")
print("="*60)
print(f"补贴金额: ¥{result2['subsidy']:.2f}")
print(f"补贴率: {result2['ratio']:.2f}%")
print(f"是否触发: {result2['triggered']}")

# 测试99999（刚好低于临界值）
print("\n" + "="*60)
result3 = calculate_subsidy(99999, 12000)
print("年薪99999，缴费12000元：")
print("="*60)
print(f"补贴金额: ¥{result3['subsidy']:.2f}")
print(f"补贴率: {result3['ratio']:.2f}%")
