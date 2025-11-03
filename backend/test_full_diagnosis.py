"""
测试高收入用户的完整诊断和AI建议流程
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.history_diagnosis import diagnose_history
from api.ai_diagnosis import generate_ai_suggestions

# 用户案例：27岁，金融行业，年薪20-24万，缴费1.2万
test_data = [
    {"year": 2022, "salary": 200000, "contribution": 12000},
    {"year": 2023, "salary": 200000, "contribution": 12000},
    {"year": 2024, "salary": 240000, "contribution": 12000}  # 修正：不超过年度上限
]

age = 27

print("="*70)
print("高收入用户完整诊断测试 (PathB流程)")
print("="*70)
print("用户画像:")
print(f"  年龄: {age}岁")
print("  行业: 金融")
print("  历史缴费:")
for record in test_data:
    print(f"    {record['year']}年: 年薪¥{record['salary']:,}, 缴费¥{record['contribution']:,}")

print(f"\n步骤1: 历史数据诊断")
print("-"*70)
diagnosis = diagnose_history(test_data, age=age)

print(f"  累积T2: {diagnosis['cumulativeT2']}%")
print(f"  效率评分: {diagnosis['efficiencyScore']}分")
print(f"  累计补贴: ¥{diagnosis['totalSubsidy']:,.2f}")
print(f"  预测T3: {diagnosis['predictedT3']}%")
print(f"  AI推荐缴费额: ¥{diagnosis['recommendedAmount']:,}/年")
print(f"  潜在优化收益: ¥{diagnosis['potentialGain']:,.2f}")
print(f"  NPV提升空间: {diagnosis['npvImprovement']:.2f}%")
print(f"  诊断消息: {diagnosis['diagnosis']['message']}")

print(f"\n步骤2: 生成AI个性化建议")
print("-"*70)
ai_suggestions = generate_ai_suggestions(diagnosis, current_age=age)

print(f"  优先级: {ai_suggestions['priority'].upper()}")
print(f"  预期收益: {ai_suggestions['expectedBenefit']}")
print(f"  建议数量: {len(ai_suggestions['suggestions'])}条")

print(f"\n详细建议列表:")
for i, sug in enumerate(ai_suggestions['suggestions'], 1):
    priority_text = {'high': '🔴高', 'medium': '🟡中', 'low': '🟢低'}[sug['priority']]
    print(f"\n  [{i}] {sug.get('icon', '•')} {sug['title']} ({priority_text}优先级)")
    print(f"      描述: {sug['description']}")
    print(f"      行动: {sug['action']}")

if ai_suggestions['riskWarnings']:
    print(f"\n风险提示:")
    for warning in ai_suggestions['riskWarnings']:
        print(f"  ⚠️ {warning}")

print(f"\n摘要:")
print(f"  总建议数: {ai_suggestions['summary']['totalSuggestions']}")
print(f"  关键问题: {ai_suggestions['summary']['criticalIssues']}个")
print(f"  优化潜力: {ai_suggestions['summary']['optimizationPotential'].upper()}")

print("\n" + "="*70)
print("✅ 测试完成！所有API正常工作")
