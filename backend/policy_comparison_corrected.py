"""
现行政策 vs 优化方案 - 对比图表（修正版）
包含三大修正：
1. 覆盖率定义修正（理论范围 vs 实际参与率）
2. 财政中性修正（NPV计算）
3. 行为压力测试（退出风险、惰性风险）

基于 chapter6_corrected.py 的修正数据
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from chapter6_simulation import *
from chapter6_corrected import (
    behavioral_participation_rate,
    calculate_fiscal_npv_correct,
    actual_coverage_current,
    actual_coverage_optimized,
    fiscal_current_npv,
    fiscal_optimized_npv
)

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
rcParams['axes.unicode_minus'] = False
rcParams['figure.dpi'] = 100

print("="*80)
print("现行政策 vs 优化方案 - 全面对比分析（修正版）")
print("="*80)
print("\n包含三大修正:")
print("  ✅ 修正1: 覆盖率定义（理论范围 vs 实际参与率）")
print("  ✅ 修正2: 财政中性（NPV计算）")
print("  ✅ 修正3: 行为压力测试")
print("="*80)

# 创建收入五等分
income_quintiles = pd.qcut(incomes, 5, labels=['Q1\n最低20%', 'Q2\n次低20%', 'Q3\n中等20%', 'Q4\n次高20%', 'Q5\n最高20%'])
df_current['income_group'] = income_quintiles
df_optimized['income_group'] = income_quintiles

# 计算实际参与率（修正1）
df_current['participation_rate'] = df_current['net_benefit'].apply(behavioral_participation_rate)
df_optimized['participation_rate'] = df_optimized['net_benefit'].apply(behavioral_participation_rate)

# 计算分组统计
current_stats = df_current.groupby('income_group').agg({
    'income': 'mean',
    'contribution': 'mean',
    't3': 'mean',
    'net_benefit': 'mean',
    'participation_rate': 'mean'
}).reset_index()

optimized_stats = df_optimized.groupby('income_group').agg({
    'income': 'mean',
    'contribution': 'mean',
    't3': 'mean',
    'subsidy': 'mean',
    'net_benefit': 'mean',
    'participation_rate': 'mean'
}).reset_index()

print("\n现行政策统计（含实际参与率）:")
print(current_stats)

print("\n优化方案统计（含实际参与率）:")
print(optimized_stats)

# ============================================================================
# 图1: 修正版核心对比 - 覆盖率的三种定义
# ============================================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('现行政策 vs 优化方案 - 修正版对比分析', fontsize=20, fontweight='bold', y=0.995)

# 子图1: 覆盖率三种定义对比
ax1 = axes[0, 0]

coverage_types = ['理论有效\n覆盖范围', '实际预期\n参与率', '行为压力测试\n最坏情景']

# 理论覆盖率
theoretical_current = (df_current['net_benefit'] > 0).mean() * 100
theoretical_optimized = (df_optimized['net_benefit'] > 0).mean() * 100

# 实际参与率（修正1）
actual_current = actual_coverage_current * 100
actual_optimized = actual_coverage_optimized * 100

# 最坏情景参与率（修正3 - 从chapter6_corrected导入）
# 简化版：假设高收入50%退出，低收入70%惰性
high_income_threshold = np.percentile(incomes, 80)
low_income_threshold = np.percentile(incomes, 40)
worst_case_participation = 0.618 * 100  # 从修正脚本结果

current_values = [theoretical_current, actual_current, worst_case_participation]
optimized_values = [theoretical_optimized, actual_optimized, worst_case_participation]

x_pos = np.arange(3)
width = 0.35

bars1 = ax1.bar(x_pos - width/2, current_values, width, label='现行政策',
                color='#FF6B6B', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax1.bar(x_pos + width/2, optimized_values, width, label='优化方案',
                color='#4ECDC4', alpha=0.8, edgecolor='black', linewidth=1.5)

ax1.set_ylabel('参与率/覆盖率 (%)', fontsize=13, fontweight='bold')
ax1.set_title('(1) 覆盖率的三种定义【修正1+3】', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(coverage_types, fontsize=10)
ax1.legend(fontsize=11, loc='upper right')
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.set_ylim([0, 110])

# 添加数值标签
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=10, fontweight='bold')

# 添加说明文本框
ax1.text(0.5, 0.15, 
         '修正说明:\n理论范围=净收益>0的比例\n实际参与率=考虑行为惰性\n最坏情景=高收入退出+低收入惰性',
         transform=ax1.transAxes, fontsize=9,
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.7),
         verticalalignment='bottom', horizontalalignment='center')

# 子图2: 财政成本对比（NPV vs 名义值）【修正2】
ax2 = axes[0, 1]

categories = ['补贴支出', '税优减收', 'T3税收', '净成本']

# 名义值（未修正）
nominal_subsidy_opt = df_optimized['subsidy'].sum() * 30 / 10000
nominal_tax_saving_current = df_current['tax_saving_pv'].sum() / 10000
nominal_tax_saving_opt = df_optimized['tax_saving_pv'].sum() / 10000
nominal_t3_current = df_current['tax_receive_pv'].sum() / 10000
nominal_t3_opt = df_optimized['tax_receive_pv'].sum() / 10000
nominal_net_current = nominal_tax_saving_current - nominal_t3_current
nominal_net_opt = nominal_subsidy_opt + nominal_tax_saving_opt - nominal_t3_opt

# NPV值（修正2）
npv_subsidy_opt = fiscal_optimized_npv['subsidy_npv'] / 10000
npv_tax_saving_current = fiscal_current_npv['tax_saving_npv'] / 10000
npv_tax_saving_opt = fiscal_optimized_npv['tax_saving_npv'] / 10000
npv_t3_current = fiscal_current_npv['t3_tax_npv'] / 10000
npv_t3_opt = fiscal_optimized_npv['t3_tax_npv'] / 10000
npv_net_current = fiscal_current_npv['net_cost_npv'] / 10000
npv_net_opt = fiscal_optimized_npv['net_cost_npv'] / 10000

# 只展示优化方案的对比
nominal_values = [nominal_subsidy_opt, nominal_tax_saving_opt, -nominal_t3_opt, nominal_net_opt]
npv_values = [npv_subsidy_opt, npv_tax_saving_opt, -npv_t3_opt, npv_net_opt]

x_pos2 = np.arange(4)
bars1 = ax2.bar(x_pos2 - width/2, nominal_values, width, label='名义值（未修正）',
                color='#FF6B6B', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax2.bar(x_pos2 + width/2, npv_values, width, label='NPV（修正后）',
                color='#4ECDC4', alpha=0.8, edgecolor='black', linewidth=1.5)

ax2.set_ylabel('金额 (万元)', fontsize=13, fontweight='bold')
ax2.set_title('(2) 财政成本：NPV vs 名义值【修正2】', fontsize=14, fontweight='bold', pad=15)
ax2.set_xticks(x_pos2)
ax2.set_xticklabels(categories, fontsize=11, fontweight='bold')
ax2.axhline(y=0, color='black', linestyle='-', linewidth=2)
ax2.legend(fontsize=11, loc='upper left')
ax2.grid(axis='y', alpha=0.3, linestyle='--')

# 添加数值标签
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'¥{height:+.0f}',
                ha='center', va='bottom' if height > 0 else 'top',
                fontsize=9, fontweight='bold')

# 子图3: 净收益改善（考虑实际参与率）
ax3 = axes[1, 0]

x_pos3 = np.arange(5)
improvement = optimized_stats['net_benefit'].values - current_stats['net_benefit'].values
colors = ['#2ECC71' if x > 0 else '#E74C3C' for x in improvement]

bars = ax3.bar(x_pos3, improvement, color=colors, alpha=0.8, 
               edgecolor='black', linewidth=1.5)

ax3.set_xlabel('收入组', fontsize=12, fontweight='bold')
ax3.set_ylabel('净收益改善额 (元)', fontsize=12, fontweight='bold')
ax3.set_title('(3) 净收益改善分析', fontsize=14, fontweight='bold', pad=15)
ax3.set_xticks(x_pos3)
ax3.set_xticklabels(current_stats['income_group'])
ax3.axhline(y=0, color='black', linestyle='-', linewidth=2)
ax3.grid(axis='y', alpha=0.3, linestyle='--')

# 添加数值标签
for i, (bar, improve) in enumerate(zip(bars, improvement)):
    height = bar.get_height()
    ax3.text(bar.get_x() + bar.get_width()/2., height,
            f'¥{int(improve):+,}',
            ha='center', va='bottom' if height > 0 else 'top',
            fontsize=10, fontweight='bold')

# 子图4: 行为压力测试结果【修正3】
ax4 = axes[1, 1]

scenarios = ['基准情景\n(理论)', '情景A\n高收入退出', '情景B\n低收入惰性', '情景C\n最坏组合']
# 数据来自chapter6_corrected.py的压力测试结果
coverage_baseline = 100.0
coverage_scenario_a = 100.0  # 高收入退出不影响覆盖率（只影响财政）
coverage_scenario_b = 71.7  # 低收入惰性导致覆盖率下降
coverage_scenario_c = 61.8  # 最坏组合

fiscal_baseline = 100.0  # 基准财政收入
fiscal_scenario_a = 75.7  # T3税收损失24.3%
fiscal_scenario_b = 61.1  # 补贴效率损失38.9%
fiscal_scenario_c = 30.9  # 综合损失最大

x_pos4 = np.arange(4)
coverage_values = [coverage_baseline, coverage_scenario_a, coverage_scenario_b, coverage_scenario_c]
fiscal_values = [fiscal_baseline, fiscal_scenario_a, fiscal_scenario_b, fiscal_scenario_c]

bars1 = ax4.bar(x_pos4 - width/2, coverage_values, width, label='覆盖率',
                color='#3498DB', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax4.bar(x_pos4 + width/2, fiscal_values, width, label='财政健康度',
                color='#E67E22', alpha=0.8, edgecolor='black', linewidth=1.5)

ax4.set_ylabel('指数 (基准=100)', fontsize=12, fontweight='bold')
ax4.set_title('(4) 行为压力测试结果【修正3】', fontsize=14, fontweight='bold', pad=15)
ax4.set_xticks(x_pos4)
ax4.set_xticklabels(scenarios, fontsize=9.5)
ax4.legend(fontsize=11, loc='upper right')
ax4.grid(axis='y', alpha=0.3, linestyle='--')
ax4.axhline(y=100, color='green', linestyle='--', linewidth=2, alpha=0.5)
ax4.set_ylim([0, 110])

# 添加数值标签
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{height:.1f}',
                ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig('修正版对比图1_三大修正展示.png', dpi=300, bbox_inches='tight')
print("\n✅ 已生成: 修正版对比图1_三大修正展示.png")
plt.close()

# ============================================================================
# 图2: 修正前后对比表格
# ============================================================================
print("\n" + "="*80)
print("修正前后对比表格")
print("="*80)

comparison_table = pd.DataFrame({
    '指标': [
        '【修正1】理论有效覆盖范围 (%)',
        '【修正1】实际预期参与率 (%)',
        '【修正1】参与缺口 (百分点)',
        '【修正2】补贴支出 - 名义值 (万元)',
        '【修正2】补贴支出 - NPV (万元)',
        '【修正2】货币时间价值损失 (%)',
        '【修正2】净财政成本 - 名义值 (万元)',
        '【修正2】净财政成本 - NPV (万元)',
        '【修正2】NPV调整幅度 (%)',
        '【修正3】情景A - T3税收损失 (%)',
        '【修正3】情景B - 覆盖率损失 (pp)',
        '【修正3】情景C - 参与率暴跌至 (%)'
    ],
    '未修正版本': [
        f"{theoretical_optimized:.1f}",
        "假设100.0（理性人谬误）",
        "0.0",
        f"{nominal_subsidy_opt:.0f}",
        "未计算",
        "未考虑",
        f"{nominal_net_opt:.0f}",
        "未计算",
        "未考虑",
        "未测试",
        "未测试",
        "未测试"
    ],
    '修正后版本': [
        f"{theoretical_optimized:.1f}",
        f"{actual_optimized:.1f}%",
        f"{(theoretical_optimized - actual_optimized):.1f}",
        f"{nominal_subsidy_opt:.0f}",
        f"{npv_subsidy_opt:.0f}",
        f"{(1-npv_subsidy_opt/nominal_subsidy_opt)*100:.1f}",
        f"{nominal_net_opt:.0f}",
        f"{npv_net_opt:.0f}",
        f"{(npv_net_opt/nominal_net_opt - 1)*100:.1f}",
        "24.3",
        "28.3",
        "61.8"
    ],
    '差异说明': [
        "一致（定义相同）",
        "修正降低5.0pp",
        "修正后发现缺口",
        "一致（定义相同）",
        "修正后折现78.6%",
        "修正后损失21.4%",
        "一致（定义相同）",
        "修正后增加19.2%",
        "NPV更保守",
        "修正后发现风险",
        "修正后发现风险",
        "修正后发现风险"
    ]
})

print(comparison_table.to_string(index=False))

# 保存表格
comparison_table.to_csv('修正版对比表_三大修正对比.csv', index=False, encoding='utf-8-sig')
print("\n✅ 已生成: 修正版对比表_三大修正对比.csv")

# ============================================================================
# 生成修正说明文档
# ============================================================================
print("\n" + "="*80)
print("三大修正的解决方案总结")
print("="*80)

print("\n【修正1】覆盖率定义修正")
print("-" * 40)
print(f"❌ 原问题: 假设净收益>0就100%参与（理性人谬误）")
print(f"✅ 解决方案: 引入行为参与率函数")
print(f"   - 净收益≤0: 参与率0%")
print(f"   - 净收益<500: 参与率30%（惰性）")
print(f"   - 净收益<2000: 参与率60%")
print(f"   - 净收益<5000: 参与率80%")
print(f"   - 净收益≥5000: 参与率95%（仍有5%惰性）")
print(f"📊 结果:")
print(f"   理论有效覆盖范围: {theoretical_optimized:.1f}%")
print(f"   实际预期参与率: {actual_optimized:.1f}%")
print(f"   参与缺口: {(theoretical_optimized - actual_optimized):.1f}个百分点")
print(f"   需要AIPPOF网页工具作为行为助推器")

print("\n【修正2】财政中性修正（NPV计算）")
print("-" * 40)
print(f"❌ 原问题: 忽略货币时间价值，今天的钱≠30年后的钱")
print(f"✅ 解决方案: 使用NPV（净现值）折现，贴现率r=1.75%")
print(f"   - 补贴在缴费期（第1-30年）支出")
print(f"   - T3税在领取期（第31-50年）征收")
print(f"   - 所有现金流折现到第0年")
print(f"📊 结果:")
print(f"   补贴支出 - 名义值: ¥{nominal_subsidy_opt:.0f}万")
print(f"   补贴支出 - NPV: ¥{npv_subsidy_opt:.0f}万")
print(f"   时间价值损失: {(1-npv_subsidy_opt/nominal_subsidy_opt)*100:.1f}%")
print(f"   净财政成本 - 名义值: ¥{nominal_net_opt:.0f}万")
print(f"   净财政成本 - NPV: ¥{npv_net_opt:.0f}万")
print(f"   NPV调整: {(npv_net_opt/nominal_net_opt - 1)*100:+.1f}%")

print("\n【修正3】行为压力测试")
print("-" * 40)
print(f"❌ 原问题: 仅测试经济参数（S0, g, r），未测试行为参数")
print(f"✅ 解决方案: 增加三个行为压力测试情景")
print(f"   情景A - 高收入退出: 最高20%收入群体50%退出")
print(f"     影响: T3税收损失24.3%，财政平衡受威胁")
print(f"   情景B - 低收入惰性: 最低40%收入群体仅30%参与")
print(f"     影响: 覆盖率损失28.3个百分点，补贴效率损失38.9%")
print(f"   情景C - 最坏组合: 同时发生A+B")
print(f"     影响: 参与率暴跌至61.8%，政策目标完全失败")
print(f"📊 结论: 行为风险是模型最大的脆弱点！")

print("\n" + "="*80)
print("✅ 所有修正版对比图表和表格生成完成！")
print("="*80)
