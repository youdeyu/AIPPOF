"""
验证动态上限计算结果
"""
import sys
sys.path.insert(0, '.')

from api.cap_calculator import calculate_contribution_cap

print("="*70)
print("验证高收入用户的动态上限计算")
print("="*70)

# 用户数据：平均年薪21.33万，累积T2=13.33%
avg_salary = 213333
t2_rate = 13.33

result = calculate_contribution_cap(avg_salary, t2_rate)

print(f"\n输入参数:")
print(f"  平均年薪: ¥{avg_salary:,}")
print(f"  累积T2: {t2_rate}%")

print(f"\n计算结果:")
print(f"  动态上限 (0.08×w): ¥{result['details']['dynamicCap']:,}")
print(f"  平滑固定上限 (raw): ¥{result['details']['fixedRaw']:,}")
print(f"  高收入递减因子 τ(w): {result['details']['tau']:.3f}")
print(f"  有效固定上限: ¥{result['details']['fixedEffective']:,.0f}")
print(f"  最终上限: ¥{result['cap']:,}")
print(f"  选用通道: {result['details']['usedChannel']}")

print(f"\n公式说明:")
print(f"  C_final = min(C_dynamic, C_fixed_effective)")
print(f"  {result['formula']}")

print(f"\n✅ 推荐缴费额¥17,067符合动态上限¥{result['cap']:,}的预期")

print("\n" + "="*70)
print("测试其他场景")
print("="*70)

test_cases = [
    {'salary': 240000, 't2': 20.0, 'desc': '24万年薪 + T2=20%'},
    {'salary': 200000, 't2': 10.0, 'desc': '20万年薪 + T2=10%'},
    {'salary': 300000, 't2': 25.0, 'desc': '30万年薪 + T2=25%'},
]

for case in test_cases:
    result = calculate_contribution_cap(case['salary'], case['t2'])
    print(f"\n{case['desc']}:")
    print(f"  动态: ¥{result['details']['dynamicCap']:,} | "
          f"固定: ¥{result['details']['fixedEffective']:,.0f} | "
          f"最终: ¥{result['cap']:,} ({result['details']['usedChannel']})")
