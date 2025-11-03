#!/usr/bin/env python3
"""
测试修复后的功能
"""
from api.history_diagnosis import diagnose_history
from api.ai_diagnosis import generate_ai_suggestions

print("="*80)
print("测试1: 28万年薪用户 (应该补贴为0)")
print("="*80)

test_data_high_income = [
    {'year': 2022, 'salary': 280000, 'contribution': 12000},
    {'year': 2023, 'salary': 300000, 'contribution': 12000}
]

result1 = diagnose_history(test_data_high_income, 35)
print(f"✅ 累积T2: {result1['cumulativeT2']}%")
print(f"✅ 总补贴: ¥{result1['totalSubsidy']} (应该是0)")
print(f"✅ 效率评分: {result1['efficiencyScore']}")

ai_result1 = generate_ai_suggestions(result1, 35)
print(f"✅ AI建议数量: {len(ai_result1['suggestions'])}")
for i, sug in enumerate(ai_result1['suggestions']):
    print(f"  {i+1}. {sug['title']}")

print("\n" + "="*80)
print("测试2: 6万年薪用户 (应该有补贴)")
print("="*80)

test_data_low_income = [
    {'year': 2022, 'salary': 60000, 'contribution': 8000},
    {'year': 2023, 'salary': 65000, 'contribution': 9000}
]

result2 = diagnose_history(test_data_low_income, 30)
print(f"✅ 累积T2: {result2['cumulativeT2']}%")
print(f"✅ 总补贴: ¥{result2['totalSubsidy']} (应该>0)")
print(f"✅ 效率评分: {result2['efficiencyScore']}")

ai_result2 = generate_ai_suggestions(result2, 30)
print(f"✅ AI建议数量: {len(ai_result2['suggestions'])}")
for i, sug in enumerate(ai_result2['suggestions']):
    print(f"  {i+1}. {sug['title']}")

print("\n" + "="*80)
print("测试3: 15万年薪用户 (补贴截断点,应该为0)")
print("="*80)

test_data_cutoff = [
    {'year': 2022, 'salary': 150000, 'contribution': 10000},
    {'year': 2023, 'salary': 155000, 'contribution': 11000}
]

result3 = diagnose_history(test_data_cutoff, 32)
print(f"✅ 累积T2: {result3['cumulativeT2']}%")
print(f"✅ 总补贴: ¥{result3['totalSubsidy']} (应该是0)")
print(f"✅ 效率评分: {result3['efficiencyScore']}")

ai_result3 = generate_ai_suggestions(result3, 32)
print(f"✅ AI建议数量: {len(ai_result3['suggestions'])}")
for i, sug in enumerate(ai_result3['suggestions']):
    print(f"  {i+1}. {sug['title']}")

print("\n" + "="*80)
print("所有测试完成!")
print("="*80)
