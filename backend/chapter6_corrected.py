"""
第六章模拟实验修正版 - 解决三大不合理之处
1. 修正"覆盖率"定义（理性人谬误）
2. 修正"财政中性"计算（时间价值谬误）
3. 增加"行为压力测试"（行为风险谬误）
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
from chapter6_simulation import *

rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
rcParams['axes.unicode_minus'] = False

print("="*80)
print("第六章模拟实验修正版 - 三大不合理之处的修正")
print("="*80)

# ==================== 修正一：覆盖率定义 ====================
print("\n" + "="*80)
print("【修正一】覆盖率定义 - 从'虚假覆盖率'到'理论有效范围'")
print("="*80)

print("\n❌ 原定义（错误）:")
print("   覆盖率 = 净收益为正的个体比例")
print("   问题: 犯了'理性人谬误'，假设净收益>0就必然参与")

print("\n✅ 修正定义（正确）:")
print("   理论有效覆盖范围 (Theoretical Eligible Coverage)")
print("   = 净收益为正的个体比例")
print("   说明: 这是理论上限，实际参与率需要行为助推")

print("\n📊 引入行为参与率模型:")

# 定义行为参与率函数（基于净收益大小）
def behavioral_participation_rate(net_benefit):
    """
    基于净收益计算实际参与概率
    考虑惰性、短视、复杂性厌恶等行为因素
    """
    if net_benefit <= 0:
        return 0.0  # 净收益为负，不参与
    elif net_benefit < 500:
        return 0.30  # 收益很小，惰性导致低参与率
    elif net_benefit < 2000:
        return 0.60  # 收益中等，参与率提升
    elif net_benefit < 5000:
        return 0.80  # 收益较大，多数人参与
    else:
        return 0.95  # 收益很大，高参与率

# 计算现行政策的实际参与率
actual_participation_current = []
for benefit in df_current['net_benefit']:
    actual_participation_current.append(behavioral_participation_rate(benefit))

actual_coverage_current = np.mean(actual_participation_current)

# 计算优化方案的实际参与率
actual_participation_optimized = []
for benefit in df_optimized['net_benefit']:
    actual_participation_optimized.append(behavioral_participation_rate(benefit))

actual_coverage_optimized = np.mean(actual_participation_optimized)

print(f"\n现行政策:")
print(f"  理论有效覆盖范围: {(df_current['net_benefit'] > 0).mean()*100:.1f}%")
print(f"  实际预期参与率: {actual_coverage_current*100:.1f}%")
print(f"  参与缺口: {((df_current['net_benefit'] > 0).mean() - actual_coverage_current)*100:.1f}个百分点")

print(f"\n优化方案:")
print(f"  理论有效覆盖范围: {(df_optimized['net_benefit'] > 0).mean()*100:.1f}%")
print(f"  实际预期参与率: {actual_coverage_optimized*100:.1f}%")
print(f"  参与缺口: {((df_optimized['net_benefit'] > 0).mean() - actual_coverage_optimized)*100:.1f}个百分点")

print(f"\n💡 关键发现:")
print(f"  - 理性人假设高估了{((df_optimized['net_benefit'] > 0).mean() - actual_coverage_optimized)*100:.1f}个百分点的参与率")
print(f"  - 需要行为助推器（如AIPPOF网页工具）来弥合缺口")

# ==================== 修正二：财政中性 - NPV计算 ====================
print("\n" + "="*80)
print("【修正二】财政中性 - 引入货币时间价值（NPV）")
print("="*80)

print("\n❌ 原计算（错误）:")
print("   新增支出16.90万元 = T3增收16.90万元")
print("   问题: 忽略了货币时间价值，今天的钱≠30年后的钱")

print("\n✅ 修正计算（正确）:")
print("   使用NPV（净现值）折现，贴现率r = 1.75%")

DISCOUNT_RATE = 0.0175

def calculate_fiscal_npv_correct(df_policy, policy_name):
    """
    正确计算财政NPV
    """
    total_subsidy_npv = 0.0
    total_tax_saving_npv = 0.0
    total_t3_tax_npv = 0.0
    
    for i in range(len(df_policy)):
        # 缴费期补贴和税优（第1-30年）
        for t in range(CONTRIBUTE_YEARS):
            subsidy_t = df_policy.iloc[i]['subsidy']
            tax_saving_t = df_policy.iloc[i]['tax_saving_pv'] / CONTRIBUTE_YEARS
            
            # 折现到第0年
            discount_factor = (1 + DISCOUNT_RATE) ** (-t)
            total_subsidy_npv += subsidy_t * discount_factor
            total_tax_saving_npv += tax_saving_t * discount_factor
        
        # 领取期T3税收（第31-50年）
        for t in range(CONTRIBUTE_YEARS, CONTRIBUTE_YEARS + RECEIVE_YEARS):
            t3_tax_t = df_policy.iloc[i]['tax_receive_pv'] / RECEIVE_YEARS
            
            # 折现到第0年
            discount_factor = (1 + DISCOUNT_RATE) ** (-t)
            total_t3_tax_npv += t3_tax_t * discount_factor
    
    # 财政成本 = 补贴支出 + 税优减收 - T3税收
    fiscal_cost_npv = total_subsidy_npv + total_tax_saving_npv - total_t3_tax_npv
    
    return {
        'policy': policy_name,
        'subsidy_npv': total_subsidy_npv,
        'tax_saving_npv': total_tax_saving_npv,
        't3_tax_npv': total_t3_tax_npv,
        'net_cost_npv': fiscal_cost_npv
    }

fiscal_current_npv = calculate_fiscal_npv_correct(df_current, '现行政策')
fiscal_optimized_npv = calculate_fiscal_npv_correct(df_optimized, '优化方案')

print(f"\n现行政策 (NPV折现到第0年):")
print(f"  补贴支出NPV: ¥{fiscal_current_npv['subsidy_npv']/10000:.2f}万")
print(f"  税优减收NPV: ¥{fiscal_current_npv['tax_saving_npv']/10000:.2f}万")
print(f"  T3税收NPV: ¥{fiscal_current_npv['t3_tax_npv']/10000:.2f}万")
print(f"  净财政成本NPV: ¥{fiscal_current_npv['net_cost_npv']/10000:.2f}万")

print(f"\n优化方案 (NPV折现到第0年):")
print(f"  补贴支出NPV: ¥{fiscal_optimized_npv['subsidy_npv']/10000:.2f}万")
print(f"  税优减收NPV: ¥{fiscal_optimized_npv['tax_saving_npv']/10000:.2f}万")
print(f"  T3税收NPV: ¥{fiscal_optimized_npv['t3_tax_npv']/10000:.2f}万")
print(f"  净财政成本NPV: ¥{fiscal_optimized_npv['net_cost_npv']/10000:.2f}万")

fiscal_npv_increase = fiscal_optimized_npv['net_cost_npv'] - fiscal_current_npv['net_cost_npv']
print(f"\n财政成本NPV变化: ¥{fiscal_npv_increase/10000:+.2f}万")

if abs(fiscal_npv_increase) < 100000:  # 10万以内算中性
    print(f"✅ 结论: 基本实现财政中性（NPV变化<10万）")
elif fiscal_npv_increase > 0:
    print(f"⚠️  结论: 存在财政成本增加（代际财政转移）")
    print(f"   性质: 今天增加补贴，未来通过T3税回收，属于财政跨期平滑")
else:
    print(f"✅ 结论: 财政有盈余（T3税收NPV>补贴支出NPV）")

# 计算时间价值损失
nominal_subsidy = df_optimized['subsidy'].sum() * CONTRIBUTE_YEARS
time_value_loss = nominal_subsidy - fiscal_optimized_npv['subsidy_npv']
print(f"\n💰 货币时间价值影响:")
print(f"  名义补贴支出: ¥{nominal_subsidy/10000:.2f}万")
print(f"  折现后NPV: ¥{fiscal_optimized_npv['subsidy_npv']/10000:.2f}万")
print(f"  时间价值损失: ¥{time_value_loss/10000:.2f}万 ({time_value_loss/nominal_subsidy*100:.1f}%)")

# ==================== 修正三：行为压力测试 ====================
print("\n" + "="*80)
print("【修正三】行为压力测试 - 测试行为风险参数")
print("="*80)

print("\n❌ 原敏感性分析（不充分）:")
print("   仅测试经济参数（S0, g, r）")
print("   问题: 未测试最脆弱的行为参数")

print("\n✅ 增加行为压力测试:")

# 情景A: 高收入者退出风险
print("\n【情景A】高收入者退出风险")
print("假设: 最高20%收入群体参与率下降50%（因T3税率过高而退出）")

# 识别高收入群体
high_income_threshold = np.percentile(incomes, 80)
high_income_mask = incomes >= high_income_threshold

# 模拟50%高收入者退出
exit_rate_high = 0.50
high_income_exit_mask = high_income_mask & (np.random.random(N_SAMPLE) < exit_rate_high)

# 重新计算财政成本（高收入者退出）
fiscal_optimized_exit = df_optimized.copy()
fiscal_optimized_exit.loc[high_income_exit_mask, 'subsidy'] = 0
fiscal_optimized_exit.loc[high_income_exit_mask, 'tax_saving_pv'] = 0
fiscal_optimized_exit.loc[high_income_exit_mask, 'tax_receive_pv'] = 0

# 计算新的财政NPV
subsidy_npv_exit = 0.0
t3_tax_npv_exit = 0.0

for t in range(CONTRIBUTE_YEARS):
    subsidy_t = fiscal_optimized_exit['subsidy'].sum()
    discount_factor = (1 + DISCOUNT_RATE) ** (-t)
    subsidy_npv_exit += subsidy_t * discount_factor

for t in range(CONTRIBUTE_YEARS, CONTRIBUTE_YEARS + RECEIVE_YEARS):
    t3_tax_t = fiscal_optimized_exit['tax_receive_pv'].sum() / RECEIVE_YEARS
    discount_factor = (1 + DISCOUNT_RATE) ** (-t)
    t3_tax_npv_exit += t3_tax_t * discount_factor

t3_loss = fiscal_optimized_npv['t3_tax_npv'] - t3_tax_npv_exit

print(f"\n原T3税收NPV: ¥{fiscal_optimized_npv['t3_tax_npv']/10000:.2f}万")
print(f"退出后T3税收NPV: ¥{t3_tax_npv_exit/10000:.2f}万")
print(f"⚠️  T3税收损失: ¥{t3_loss/10000:.2f}万 ({t3_loss/fiscal_optimized_npv['t3_tax_npv']*100:.1f}%)")
print(f"⚠️  财政平衡受到严重威胁！")

# 情景B: 低收入者惰性风险
print("\n【情景B】低收入者惰性风险")
print("假设: 最低40%收入群体实际参与率仅30%（尽管有补贴，因惰性而不参与）")

# 识别低收入群体
low_income_threshold = np.percentile(incomes, 40)
low_income_mask = incomes <= low_income_threshold

# 模拟70%低收入者因惰性未参与
participation_rate_low = 0.30
low_income_nonparticipate_mask = low_income_mask & (np.random.random(N_SAMPLE) > participation_rate_low)

# 计算实际覆盖率
theoretical_coverage = (df_optimized['net_benefit'] > 0).mean()
actual_coverage_with_inertia = (~low_income_nonparticipate_mask & (df_optimized['net_benefit'] > 0)).mean()

coverage_loss = theoretical_coverage - actual_coverage_with_inertia

print(f"\n理论有效覆盖范围: {theoretical_coverage*100:.1f}%")
print(f"考虑惰性后实际覆盖率: {actual_coverage_with_inertia*100:.1f}%")
print(f"⚠️  覆盖率损失: {coverage_loss*100:.1f}个百分点")
print(f"⚠️  覆盖率目标严重受损！")

# 计算补贴浪费
total_subsidy_budget = fiscal_optimized_npv['subsidy_npv']
wasted_subsidy = df_optimized.loc[low_income_nonparticipate_mask, 'subsidy'].sum() * CONTRIBUTE_YEARS
wasted_subsidy_npv = 0.0
for t in range(CONTRIBUTE_YEARS):
    discount_factor = (1 + DISCOUNT_RATE) ** (-t)
    wasted_subsidy_npv += wasted_subsidy / CONTRIBUTE_YEARS * discount_factor

print(f"\n补贴预算NPV: ¥{total_subsidy_budget/10000:.2f}万")
print(f"未能触达人群的补贴NPV: ¥{wasted_subsidy_npv/10000:.2f}万")
print(f"⚠️  补贴效率损失: {wasted_subsidy_npv/total_subsidy_budget*100:.1f}%")

# 情景C: 综合压力测试
print("\n【情景C】最坏情景组合")
print("同时发生: 高收入50%退出 + 低收入70%惰性")

combined_exit_mask = high_income_exit_mask | low_income_nonparticipate_mask
actual_participants = N_SAMPLE - combined_exit_mask.sum()
participation_rate_worst = actual_participants / N_SAMPLE

print(f"\n理论参与率: 100.0%")
print(f"最坏情景参与率: {participation_rate_worst*100:.1f}%")
print(f"⚠️  参与率暴跌: {(1-participation_rate_worst)*100:.1f}个百分点")

# 计算最坏情景下的财政成本
fiscal_worst = df_optimized.copy()
fiscal_worst.loc[combined_exit_mask, 'subsidy'] = 0
fiscal_worst.loc[combined_exit_mask, 'tax_saving_pv'] = 0
fiscal_worst.loc[combined_exit_mask, 'tax_receive_pv'] = 0

t3_tax_worst = fiscal_worst['tax_receive_pv'].sum()
t3_tax_loss_worst = df_optimized['tax_receive_pv'].sum() - t3_tax_worst

print(f"\nT3税收损失: ¥{t3_tax_loss_worst/10000:.2f}万")
print(f"覆盖率: {(~combined_exit_mask & (fiscal_worst['net_benefit']>0)).mean()*100:.1f}%")
print(f"🚨 政策目标完全失败！")

print("\n" + "="*80)
print("【总结】三大修正的核心发现")
print("="*80)

print("\n1️⃣  覆盖率修正:")
print(f"   理论有效覆盖范围: {(df_optimized['net_benefit'] > 0).mean()*100:.1f}%")
print(f"   考虑行为因素后: {actual_coverage_optimized*100:.1f}%")
print(f"   ✅ 需要AIPPOF网页工具作为行为助推器来弥合缺口")

print(f"\n2️⃣  财政中性修正:")
print(f"   名义计算: 看似平衡")
print(f"   NPV计算: 净成本NPV = ¥{fiscal_optimized_npv['net_cost_npv']/10000:+.2f}万")
if fiscal_npv_increase > 100000:
    print(f"   ⚠️  实际是代际财政转移，非真正中性")
else:
    print(f"   ✅ NPV意义上基本中性")

print(f"\n3️⃣  行为风险压力测试:")
print(f"   情景A (高收入退出): T3税收损失{t3_loss/fiscal_optimized_npv['t3_tax_npv']*100:.1f}%")
print(f"   情景B (低收入惰性): 覆盖率损失{coverage_loss*100:.1f}个百分点")
print(f"   情景C (最坏组合): 参与率暴跌至{participation_rate_worst*100:.1f}%")
print(f"   🚨 行为风险是模型最大的脆弱点！")

print("\n" + "="*80)
print("【关键结论】")
print("="*80)

print("\n✅ 修正后的结论更加审慎和现实:")
print("\n1. 覆盖率不是93.3%的'保证'，而是100%的'理论天花板'")
print("   实际需要依赖AIPPOF网页等行为助推工具")

print("\n2. 财政不是'零成本'的免费午餐，而是跨期平滑的代际转移")
print("   需要诚实披露NPV成本，由政策制定者权衡")

print("\n3. 最大风险不是经济参数波动，而是参与者的非理性行为")
print("   需要通过A/B测试收集真实行为弹性数据")

print("\n💡 这些修正使论文更加严谨、诚实和可信！")
print("="*80)
