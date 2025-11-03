"""测试缴费上限API"""
import requests
import json

API_URL = "http://localhost:8000/api/optimize-contribution"

test_cases = [
    {"age": 30, "annualSalary": 50000, "wageGrowthRate": 0.05, "desc": "低收入"},
    {"age": 30, "annualSalary": 80000, "wageGrowthRate": 0.05, "desc": "中低收入"},
    {"age": 30, "annualSalary": 150000, "wageGrowthRate": 0.0565, "desc": "中高收入"},
    {"age": 30, "annualSalary": 300000, "wageGrowthRate": 0.05, "desc": "高收入"},
]

print("="*80)
print("缴费上限API测试")
print("="*80)

for case in test_cases:
    try:
        response = requests.post(API_URL, json=case)
        result = response.json()
        
        cap_info = result.get('cap', {})
        scenarios = result.get('scenarios', [])
        
        print(f"\n【{case['desc']}】年薪¥{case['annualSalary']:,}")
        print(f"  个性化上限: ¥{cap_info.get('personalCap', 0):,}")
        print(f"  计算策略: {cap_info.get('strategy', 'N/A')}")
        print(f"  公式: {cap_info.get('formula', 'N/A')}")
        
        # 检查所有方案是否在上限内
        personal_cap = cap_info.get('personalCap', 12000)
        print(f"\n  三个方案:")
        all_valid = True
        for s in scenarios:
            contrib = s['contribution']
            in_limit = contrib <= personal_cap
            status = "✅" if in_limit else "❌ 超限！"
            print(f"    {status} [{s['label']}] ¥{contrib:,} (T2={s['predictedT2']}%)")
            if not in_limit:
                all_valid = False
        
        if all_valid:
            print(f"  ✅ 所有方案都在上限内")
        else:
            print(f"  ❌ 发现超限方案！")
            
    except Exception as e:
        print(f"\n❌ 【{case['desc']}】API调用失败: {e}")

print("\n" + "="*80)
print("测试完成")
print("="*80)
