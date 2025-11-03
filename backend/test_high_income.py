"""
测试高收入用户的推荐缴费额
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.history_diagnosis import diagnose_history

# 用户案例：27岁，金融行业，前两年年薪20万缴费1.2万，第三年年薪24万缴费1.5万
test_data = [
    {"year": 2022, "salary": 200000, "contribution": 12000},
    {"year": 2023, "salary": 200000, "contribution": 12000},
    {"year": 2024, "salary": 240000, "contribution": 15000}  # 注意：15000已超出年度上限12000
]

print("="*70)
print("高收入用户缴费策略诊断测试")
print("="*70)
print("用户画像:")
print("  年龄: 27岁")
print("  行业: 金融")
print("  历史数据:")
for record in test_data:
    print(f"    {record['year']}年: 年薪¥{record['salary']:,}, 缴费¥{record['contribution']:,}")

result = diagnose_history(test_data, age=27)

print(f"\n诊断结果:")
print(f"  平均年薪: ¥{result['historicalDetails']['averageSalary']:,.2f}")
print(f"  平均缴费: ¥{result['historicalDetails']['averageContribution']:,.2f}")
print(f"  累积T2: {result['cumulativeT2']}%")
print(f"  效率评分: {result['efficiencyScore']}分")
print(f"  累计补贴: ¥{result['totalSubsidy']:,.2f}")
print(f"  预测T3: {result['predictedT3']}%")

print(f"\n推荐策略:")
print(f"  AI推荐缴费额: ¥{result['recommendedAmount']:,}/年")
print(f"  潜在优化收益: ¥{result['potentialGain']:,.2f} (全生命周期)")
print(f"  NPV提升空间: {result['npvImprovement']:.2f}%")

print(f"\n诊断意见:")
print(f"  {result['diagnosis']['message']}")

print(f"\n历年详情:")
for detail in result['historicalDetails']['t2ByYear']:
    print(f"  {detail['year']}年: T2={detail['t2']}%, 年薪¥{detail['salary']:,}, 缴费¥{detail['contribution']:,}")
