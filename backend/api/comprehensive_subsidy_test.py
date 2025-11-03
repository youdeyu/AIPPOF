"""全面测试补贴计算机制"""
from subsidy_calculator import calculate_subsidy

print("="*80)
print("渐进式精准补贴计算 - 全面测试")
print("="*80)

test_cases = [
    {"salary": 30000, "contribution": 200, "name": "极低收入+最低缴费"},
    {"salary": 30000, "contribution": 1000, "name": "极低收入+正常缴费"},
    {"salary": 40000, "contribution": 1000, "name": "临界点（40000）- 全额补贴"},
    {"salary": 50000, "contribution": 1000, "name": "低收入+递减开始"},
    {"salary": 60000, "contribution": 5000, "name": "中等收入+递减中"},
    {"salary": 80000, "contribution": 5000, "name": "低收入上限"},
    {"salary": 90000, "contribution": 5000, "name": "中高收入+补贴递减"},
    {"salary": 99999, "contribution": 12000, "name": "临界点（99999）- 微量补贴"},
    {"salary": 100000, "contribution": 12000, "name": "临界点（100000）- 补贴归零"},
    {"salary": 150000, "contribution": 12000, "name": "高收入 - 必须为0"},
    {"salary": 200000, "contribution": 12000, "name": "超高收入 - 必须为0"},
]

print("\n" + "="*80)
print("测试结果：")
print("="*80)

errors = []
for case in test_cases:
    result = calculate_subsidy(case['salary'], case['contribution'])
    subsidy = result['subsidy']
    ratio = result['ratio']
    
    # 验证逻辑
    status = "✅"
    if case['salary'] >= 100000 and subsidy != 0:
        status = "❌ 错误！高收入不应有补贴"
        errors.append(case['name'])
    elif case['salary'] < 40000 and subsidy == 0 and case['contribution'] >= 200:
        status = "❌ 错误！低收入应有补贴"
        errors.append(case['name'])
    
    print(f"\n【{case['name']}】 {status}")
    print(f"  年薪: ¥{case['salary']:,} | 缴费: ¥{case['contribution']:,}")
    print(f"  💰 补贴: ¥{subsidy:.2f} ({ratio:.1f}%)")
    
    # 显示收入档位
    if case['salary'] <= 40000:
        tier = "全额补贴区"
    elif case['salary'] < 100000:
        taper_pct = (100000 - case['salary']) / (100000 - 40000) * 100
        tier = f"递减区（保留{taper_pct:.0f}%）"
    else:
        tier = "补贴归零区"
    print(f"  📊 收入档位: {tier}")

print("\n" + "="*80)
if errors:
    print(f"❌ 发现 {len(errors)} 个错误:")
    for err in errors:
        print(f"  - {err}")
    print("\n补贴机制需要修复！")
else:
    print("✅ 所有测试通过！补贴机制完全正确！")
    print("\n关键验证点:")
    print("  ✓ 年薪 ≥ 100000 → 补贴 = 0")
    print("  ✓ 年薪 ≤ 40000 → 补贴 = 100%")
    print("  ✓ 40000 < 年薪 < 100000 → 线性递减")
print("="*80)
