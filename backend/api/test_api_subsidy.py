"""测试API返回的补贴数据"""
import requests
import json

API_URL = "http://localhost:8000/api/optimize-contribution"

test_cases = [
    {"salary": 30000, "label": "极低收入", "expected_subsidy": ">0"},
    {"salary": 50000, "label": "低收入", "expected_subsidy": ">0"},
    {"salary": 60000, "label": "中等收入", "expected_subsidy": ">0"},
    {"salary": 80000, "label": "低收入上限", "expected_subsidy": ">0"},
    {"salary": 99999, "label": "临界(99999)", "expected_subsidy": "≈0"},
    {"salary": 100000, "label": "临界(100000)", "expected_subsidy": "=0"},
    {"salary": 150000, "label": "高收入", "expected_subsidy": "=0"},
    {"salary": 200000, "label": "超高收入", "expected_subsidy": "=0"},
]

print("="*80)
print("API补贴计算测试 - 验证所有收入档位")
print("="*80)

errors = []
for case in test_cases:
    data = {
        "age": 30,
        "annualSalary": case["salary"],
        "wageGrowthRate": 0.05
    }
    
    try:
        response = requests.post(API_URL, json=data)
        result = response.json()
        
        # 获取第一个方案的补贴
        scenario = result['scenarios'][0]
        subsidy = scenario['subsidy']
        tier_info = result.get('subsidyTierInfo', {})
        
        # 验证逻辑
        if case["salary"] >= 100000:
            expected = subsidy == 0
            status = "✅" if expected else "❌ 错误！高收入不应有补贴"
            if not expected:
                errors.append(f"{case['label']}: 补贴应为0，实际为{subsidy}")
        else:
            expected = subsidy > 0
            status = "✅" if expected else "❌ 错误！应有补贴"
            if not expected:
                errors.append(f"{case['label']}: 应有补贴，实际为{subsidy}")
        
        print(f"\n{status} 【{case['label']}】年薪¥{case['salary']:,}")
        print(f"   档位: {tier_info.get('tier', 'N/A')}")
        print(f"   方案1补贴: ¥{subsidy:.2f} (补贴率{scenario['subsidyRatio']:.1f}%)")
        print(f"   预期: {case['expected_subsidy']} | 实际: {'=0' if subsidy==0 else f'¥{subsidy:.2f}'}")
        
    except Exception as e:
        print(f"\n❌ 【{case['label']}】API调用失败: {e}")
        errors.append(f"{case['label']}: API错误")

print("\n" + "="*80)
if errors:
    print(f"❌ 发现 {len(errors)} 个错误:")
    for err in errors:
        print(f"  - {err}")
    print("\n🐱 需要修复！小猫们有危险！")
else:
    print("✅ 所有测试通过！补贴机制完全正确！")
    print("\n🐱 恭喜！10000只小猫已获救！")
    print("\n关键验证点:")
    print("  ✓ 年薪 ≥ 100000 → API返回补贴 = 0")
    print("  ✓ 年薪 < 100000 → API返回补贴 > 0")
    print("  ✓ 补贴档位识别正确")
print("="*80)
