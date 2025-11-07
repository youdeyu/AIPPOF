"""
测试用例：27岁金融行业初级人员的完整分析
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.history_diagnosis import diagnose_history
from api.contribution_suggestions import generate_5tier_suggestions
from api.cap_calculator import calculate_contribution_cap
from api.t3_calculator import calculate_t3

# 用户历史数据
history_data = [
    {"year": 2022, "salary": 66000, "contribution": 5000},
    {"year": 2023, "salary": 72000, "contribution": 5000},
    {"year": 2024, "salary": 80000, "contribution": 6000}
]

current_age = 27
current_salary = 80000

print("="*80)
print("【个人养老金诊断分析报告】")
print("="*80)
print(f"基本信息: 27岁, 金融行业, 初级人员")
print(f"历史缴费记录:")
for record in history_data:
    print(f"  {record['year']}年: 年薪¥{record['salary']:,}, 缴费¥{record['contribution']:,}")
print("="*80)

# 1. 历史诊断
print("\n【步骤1: 历史缴费诊断】")
print("-"*80)
diagnosis = diagnose_history(history_data, current_age)

print(f"\n✅ 累积加权平均T2: {diagnosis['cumulativeT2']:.2f}%")
print(f"   (基于蓝浩歌公式: T2 = 实际税收节约 / 缴费额)")

print(f"\n✅ 缴费效率评分: {diagnosis['efficiencyScore']}分")

print(f"\n✅ 累计获得补贴: ¥{diagnosis['totalSubsidy']:,.2f}")

print(f"\n✅ 预测领取期T3: {diagnosis['predictedT3']:.2f}%")

print(f"\n✅ 推荐未来缴费额: ¥{diagnosis['recommendedAmount']:,}")

print(f"\n📊 历年T2详情:")
for item in diagnosis['historicalDetails']['t2ByYear']:
    print(f"   {item['year']}年: T2={item['t2']:.2f}%, 缴费¥{item['contribution']:,}, 年薪¥{item['salary']:,}")

print(f"\n💰 历年补贴明细:")
for item in diagnosis['historicalDetails']['subsidyByYear']:
    print(f"   {item['year']}年: 补贴¥{item['subsidy']:,.2f}, 缴费¥{item['contribution']:,}")

# 2. 动态上限
print("\n" + "="*80)
print("【步骤2: 动态缴费上限计算】")
print("-"*80)

cumulative_t2 = diagnosis['cumulativeT2']
cap_result = calculate_contribution_cap(current_salary, cumulative_t2)

print(f"\n📐 上限计算公式 (Formula 5-5):")
print(f"   C_final(w, t₂) = min(C_dynamic, C_fixed_effective)")
print(f"   C_dynamic = 0.08 × w")
print(f"   C_fixed_effective = C_fixed_smooth(t₂) × τ(w)")

details = cap_result['details']
print(f"\n✅ 动态上限 C_dynamic: ¥{details['dynamicCap']:,.0f}")
print(f"✅ 固定上限平滑值 C_fixed_smooth: ¥{details['fixedRaw']:,.0f}")
print(f"✅ 高收入递减因子 τ(w): {details['tau']:.4f}")
print(f"✅ 固定上限有效值 C_fixed_effective: ¥{details['fixedEffective']:,.0f}")
print(f"✅ 使用通道: {details['usedChannel']}")
print(f"\n🎯 最终推荐上限: ¥{cap_result['cap']:,.0f}")

# 3. T3详解
print("\n" + "="*80)
print("【步骤3: T3计算公式详解】")
print("-"*80)

t3_result = calculate_t3(cumulative_t2, current_salary, current_age)

print(f"\n📐 T3双Logistic函数公式:")
print(f"   t3 = L1 + (L2-L1)/(1+e^(-k1*(T2-5))) + L3/(1+e^(-k2*(w-500k)))")

print(f"\n✅ T3组成部分:")
print(f"   - 基础税率: {t3_result['components']['baseTax']:.4f}%")
print(f"   - 收入调整: {t3_result['components']['incomeAdjustment']:.4f}%")
print(f"   - 年龄折扣: {t3_result['components']['ageDiscount']:.4f}%")

print(f"\n🎯 最终T3: {t3_result['components']['finalRate']:.2f}%")

# 4. 五档方案
print("\n" + "="*80)
print("【步骤4: 五档缴费方案推荐】")
print("-"*80)

tiers_result = generate_5tier_suggestions(
    current_salary=current_salary,
    current_age=current_age,
    current_contribution=6000,
    t2_rate=cumulative_t2,
    wage_growth_rate=3.5
)

print(f"\n基于年薪¥{current_salary:,}, 年龄{current_age}岁, 累积T2={cumulative_t2:.2f}%")
print(f"动态上限: ¥{cap_result['cap']:,.2f}\n")

for i, tier in enumerate(tiers_result['tiers'], 1):
    print(f"\n{'='*70}")
    print(f"【方案{i}: {tier['name']}】 {tier['icon']}")
    print(f"{'='*70}")
    print(f"年度缴费额: ¥{tier['contribution']:,}")
    print(f"上限利用率: {tier['cap_utilization']:.1f}%")
    print(f"全周期总NPV: ¥{tier['npv']['total_npv']:,.2f}")
    print(f"年均收益: ¥{tier['annual_benefit']:,.0f}")
    print(f"风险等级: {tier['risk_level']}")
    print(f"适合人群: {tier['suitable_for']}")
    print(f"\n特点:")
    for char in tier['characteristics']:
        print(f"  • {char}")

print("\n" + "="*80)
print("【分析完成】")
print("="*80)
print(f"\n💡 建议: 推荐选择方案3【{tiers_result['tiers'][2]['name']}】")
print(f"   年缴费¥{tiers_result['tiers'][2]['contribution']:,}, NPV¥{tiers_result['tiers'][2]['npv']['total_npv']:,.2f}")
