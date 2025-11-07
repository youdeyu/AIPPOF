"""
现行政策 vs 优化方案 - 全面对比图表
现行政策: 固定上限¥12,000/年, 固定T3税率3%
优化方案: 动态上限6%-12%, T3双逻辑0-14%, 两段式补贴
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
from chapter6_simulation import *

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
rcParams['axes.unicode_minus'] = False
rcParams['figure.dpi'] = 100

print("="*80)
print("现行政策 vs 优化方案 - 全面对比分析")
print("="*80)

# 创建收入五等分
income_quintiles = pd.qcut(incomes, 5, labels=['Q1\n最低20%', 'Q2\n次低20%', 'Q3\n中等20%', 'Q4\n次高20%', 'Q5\n最高20%'])
df_current['income_group'] = income_quintiles
df_optimized['income_group'] = income_quintiles

# 计算分组统计
current_stats = df_current.groupby('income_group').agg({
    'income': 'mean',
    'contribution': 'mean',
    't3': 'mean',
    'net_benefit': 'mean'
}).reset_index()

optimized_stats = df_optimized.groupby('income_group').agg({
    'income': 'mean',
    'contribution': 'mean',
    't3': 'mean',
    'subsidy': 'mean',
    'net_benefit': 'mean'
}).reset_index()

print("\n现行政策统计:")
print(current_stats)

print("\n优化方案统计:")
print(optimized_stats)

# ============================================================================
# 图1: 四政策对比 - 2x2子图
# ============================================================================
fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('现行政策 vs 优化方案 - 四维对比', fontsize=20, fontweight='bold', y=0.995)

x_pos = np.arange(5)
width = 0.35

# 子图1: 缴费额对比
ax1 = axes[0, 0]
bars1 = ax1.bar(x_pos - width/2, current_stats['contribution'], width, 
                label='现行政策', color='#FF6B6B', alpha=0.8)
bars2 = ax1.bar(x_pos + width/2, optimized_stats['contribution'], width,
                label='优化方案', color='#4ECDC4', alpha=0.8)

ax1.set_xlabel('收入组', fontsize=12, fontweight='bold')
ax1.set_ylabel('年缴费额 (元)', fontsize=12, fontweight='bold')
ax1.set_title('(1) 缴费额对比', fontsize=14, fontweight='bold', pad=15)
ax1.set_xticks(x_pos)
ax1.set_xticklabels(current_stats['income_group'])
ax1.legend(fontsize=11, loc='upper left')
ax1.grid(axis='y', alpha=0.3, linestyle='--')

# 添加数值标签
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'¥{int(height):,}',
                ha='center', va='bottom', fontsize=9)

# 子图2: T3税率对比
ax2 = axes[0, 1]
bars1 = ax2.bar(x_pos - width/2, current_stats['t3']*100, width,
                label='现行政策 (固定3%)', color='#FF6B6B', alpha=0.8)
bars2 = ax2.bar(x_pos + width/2, optimized_stats['t3']*100, width,
                label='优化方案 (0-14%)', color='#4ECDC4', alpha=0.8)

ax2.set_xlabel('收入组', fontsize=12, fontweight='bold')
ax2.set_ylabel('T3税率 (%)', fontsize=12, fontweight='bold')
ax2.set_title('(2) T3税率对比', fontsize=14, fontweight='bold', pad=15)
ax2.set_xticks(x_pos)
ax2.set_xticklabels(current_stats['income_group'])
ax2.legend(fontsize=11, loc='upper left')
ax2.grid(axis='y', alpha=0.3, linestyle='--')
ax2.axhline(y=3.0, color='red', linestyle='--', linewidth=2, alpha=0.5, label='现行固定3%')

# 添加数值标签
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2f}%',
                ha='center', va='bottom', fontsize=9)

# 子图3: 补贴对比
ax3 = axes[1, 0]
bars1 = ax3.bar(x_pos - width/2, [0]*5, width,
                label='现行政策 (无补贴)', color='#FF6B6B', alpha=0.8)
bars2 = ax3.bar(x_pos + width/2, optimized_stats['subsidy'], width,
                label='优化方案', color='#4ECDC4', alpha=0.8)

ax3.set_xlabel('收入组', fontsize=12, fontweight='bold')
ax3.set_ylabel('年补贴额 (元)', fontsize=12, fontweight='bold')
ax3.set_title('(3) 财政补贴对比', fontsize=14, fontweight='bold', pad=15)
ax3.set_xticks(x_pos)
ax3.set_xticklabels(current_stats['income_group'])
ax3.legend(fontsize=11, loc='upper right')
ax3.grid(axis='y', alpha=0.3, linestyle='--')

# 添加数值标签
for bar in bars2:
    height = bar.get_height()
    if height > 0:
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'¥{int(height):,}',
                ha='center', va='bottom', fontsize=9)

# 子图4: 净收益对比
ax4 = axes[1, 1]
bars1 = ax4.bar(x_pos - width/2, current_stats['net_benefit'], width,
                label='现行政策', color='#FF6B6B', alpha=0.8)
bars2 = ax4.bar(x_pos + width/2, optimized_stats['net_benefit'], width,
                label='优化方案', color='#4ECDC4', alpha=0.8)

ax4.set_xlabel('收入组', fontsize=12, fontweight='bold')
ax4.set_ylabel('终身净收益 (元)', fontsize=12, fontweight='bold')
ax4.set_title('(4) 终身净收益对比', fontsize=14, fontweight='bold', pad=15)
ax4.set_xticks(x_pos)
ax4.set_xticklabels(current_stats['income_group'])
ax4.legend(fontsize=11, loc='upper left')
ax4.grid(axis='y', alpha=0.3, linestyle='--')
ax4.axhline(y=0, color='black', linestyle='-', linewidth=1)

# 添加数值标签
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'¥{int(height):,}',
                ha='center', va='bottom' if height > 0 else 'top', fontsize=9)

plt.tight_layout()
plt.savefig('对比图1_四维政策对比.png', dpi=300, bbox_inches='tight')
print("\n✅ 已生成: 对比图1_四维政策对比.png")
plt.close()

# ============================================================================
# 图2: 净收益改善分析
# ============================================================================
fig, ax = plt.subplots(figsize=(14, 8))

improvement = optimized_stats['net_benefit'].values - current_stats['net_benefit'].values
colors = ['#2ECC71' if x > 0 else '#E74C3C' for x in improvement]

bars = ax.bar(x_pos, improvement, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

ax.set_xlabel('收入组', fontsize=14, fontweight='bold')
ax.set_ylabel('净收益改善额 (元)', fontsize=14, fontweight='bold')
ax.set_title('优化方案相对现行政策的净收益改善\n(正值=受益, 负值=受损)', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x_pos)
ax.set_xticklabels(current_stats['income_group'])
ax.axhline(y=0, color='black', linestyle='-', linewidth=2)
ax.grid(axis='y', alpha=0.3, linestyle='--')

# 添加数值标签和百分比
for i, (bar, improve, current_val) in enumerate(zip(bars, improvement, current_stats['net_benefit'])):
    height = bar.get_height()
    percentage = (improve / current_val * 100) if current_val != 0 else 0
    
    ax.text(bar.get_x() + bar.get_width()/2., height,
            f'¥{int(improve):+,}\n({percentage:+.1f}%)',
            ha='center', va='bottom' if height > 0 else 'top',
            fontsize=11, fontweight='bold')

# 添加总结文本
avg_improvement = improvement.mean()
ax.text(0.98, 0.97, f'平均改善: ¥{int(avg_improvement):+,}',
        transform=ax.transAxes, fontsize=13, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8),
        verticalalignment='top', horizontalalignment='right')

plt.tight_layout()
plt.savefig('对比图2_净收益改善分析.png', dpi=300, bbox_inches='tight')
print("✅ 已生成: 对比图2_净收益改善分析.png")
plt.close()

# ============================================================================
# 图3: 覆盖率与公平性对比
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

# 子图1: 覆盖率对比
coverage_current = (df_current['net_benefit'] > 0).mean() * 100
coverage_optimized = (df_optimized['net_benefit'] > 0).mean() * 100

coverage_data = [coverage_current, coverage_optimized]
bars = ax1.bar(['现行政策\n(¥12,000上限+3%T3)', '优化方案\n(动态上限+累进T3+补贴)'], 
               coverage_data, color=['#FF6B6B', '#4ECDC4'], alpha=0.8, 
               edgecolor='black', linewidth=2)

ax1.set_ylabel('覆盖率 (%)', fontsize=14, fontweight='bold')
ax1.set_title('(1) 理论有效覆盖范围对比', fontsize=15, fontweight='bold', pad=15)
ax1.set_ylim([0, 110])
ax1.grid(axis='y', alpha=0.3, linestyle='--')
ax1.axhline(y=100, color='green', linestyle='--', linewidth=2, alpha=0.5)

for bar, val in zip(bars, coverage_data):
    ax1.text(bar.get_x() + bar.get_width()/2., val + 2,
            f'{val:.1f}%',
            ha='center', va='bottom', fontsize=16, fontweight='bold')

improvement_pp = coverage_optimized - coverage_current
ax1.text(0.5, 0.5, f'提升: +{improvement_pp:.1f}个百分点',
        transform=ax1.transAxes, fontsize=13, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.8),
        ha='center')

# 子图2: Gini系数对比
def calculate_gini(values):
    sorted_values = np.sort(values[values > 0])
    n = len(sorted_values)
    if n == 0:
        return 0.0
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * sorted_values)) / (n * np.sum(sorted_values)) - (n + 1) / n

gini_current = calculate_gini(df_current['net_benefit'].values)
gini_optimized = calculate_gini(df_optimized['net_benefit'].values)

gini_data = [gini_current, gini_optimized]
bars = ax2.bar(['现行政策', '优化方案'], gini_data, 
               color=['#FF6B6B', '#4ECDC4'], alpha=0.8,
               edgecolor='black', linewidth=2)

ax2.set_ylabel('Gini系数', fontsize=14, fontweight='bold')
ax2.set_title('(2) 公平性对比 (Gini系数)', fontsize=15, fontweight='bold', pad=15)
ax2.set_ylim([0, 0.8])
ax2.grid(axis='y', alpha=0.3, linestyle='--')

for bar, val in zip(bars, gini_data):
    ax2.text(bar.get_x() + bar.get_width()/2., val + 0.02,
            f'{val:.3f}',
            ha='center', va='bottom', fontsize=16, fontweight='bold')

improvement_pct = (gini_current - gini_optimized) / gini_current * 100
ax2.text(0.5, 0.5, f'改善: -{improvement_pct:.1f}%\n(数值越小越公平)',
        transform=ax2.transAxes, fontsize=13, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.8),
        ha='center')

plt.suptitle('覆盖率与公平性对比分析', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('对比图3_覆盖率与公平性.png', dpi=300, bbox_inches='tight')
print("✅ 已生成: 对比图3_覆盖率与公平性.png")
plt.close()

# ============================================================================
# 图4: 收入-T3税率散点图对比
# ============================================================================
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 7))

# 现行政策
scatter1 = ax1.scatter(df_current['income']/10000, df_current['t3']*100,
                       c=df_current['t3']*100, cmap='Reds', alpha=0.6, s=50,
                       edgecolors='black', linewidth=0.5)
ax1.axhline(y=3.0, color='red', linestyle='--', linewidth=3, label='固定T3=3%')
ax1.set_xlabel('年收入 (万元)', fontsize=13, fontweight='bold')
ax1.set_ylabel('T3税率 (%)', fontsize=13, fontweight='bold')
ax1.set_title('现行政策: 固定T3税率=3%', fontsize=14, fontweight='bold', pad=15)
ax1.grid(alpha=0.3, linestyle='--')
ax1.legend(fontsize=12, loc='upper right')
cbar1 = plt.colorbar(scatter1, ax=ax1)
cbar1.set_label('T3税率 (%)', fontsize=11)

# 优化方案
scatter2 = ax2.scatter(df_optimized['income']/10000, df_optimized['t3']*100,
                       c=df_optimized['t3']*100, cmap='viridis', alpha=0.6, s=50,
                       edgecolors='black', linewidth=0.5)
ax2.set_xlabel('年收入 (万元)', fontsize=13, fontweight='bold')
ax2.set_ylabel('T3税率 (%)', fontsize=13, fontweight='bold')
ax2.set_title('优化方案: T3双逻辑函数(0-14%)', fontsize=14, fontweight='bold', pad=15)
ax2.grid(alpha=0.3, linestyle='--')
cbar2 = plt.colorbar(scatter2, ax=ax2)
cbar2.set_label('T3税率 (%)', fontsize=11)

# 添加参考线
for ax in [ax2]:
    ax.axhline(y=0, color='green', linestyle='--', linewidth=2, alpha=0.5, label='最低0%')
    ax.axhline(y=14, color='red', linestyle='--', linewidth=2, alpha=0.5, label='最高14%')
    ax.legend(fontsize=11, loc='upper left')

plt.suptitle('T3税率机制对比: 固定税率 vs 累进税率', fontsize=18, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('对比图4_T3税率机制对比.png', dpi=300, bbox_inches='tight')
print("✅ 已生成: 对比图4_T3税率机制对比.png")
plt.close()

# ============================================================================
# 图5: 财政成本对比
# ============================================================================
fig, ax = plt.subplots(figsize=(12, 8))

# 计算财政指标
subsidy_current = 0
subsidy_optimized = df_optimized['subsidy'].sum() * CONTRIBUTE_YEARS / 10000

tax_saving_current = df_current['tax_saving_pv'].sum() / 10000
tax_saving_optimized = df_optimized['tax_saving_pv'].sum() / 10000

t3_tax_current = df_current['tax_receive_pv'].sum() / 10000
t3_tax_optimized = df_optimized['tax_receive_pv'].sum() / 10000

net_cost_current = tax_saving_current - t3_tax_current
net_cost_optimized = subsidy_optimized + tax_saving_optimized - t3_tax_optimized

categories = ['补贴支出', '税优减收', 'T3税收', '净财政成本']
current_values = [subsidy_current, tax_saving_current, -t3_tax_current, net_cost_current]
optimized_values = [subsidy_optimized, tax_saving_optimized, -t3_tax_optimized, net_cost_optimized]

x_pos = np.arange(len(categories))
width = 0.35

bars1 = ax.bar(x_pos - width/2, current_values, width, label='现行政策',
               color='#FF6B6B', alpha=0.8, edgecolor='black', linewidth=1.5)
bars2 = ax.bar(x_pos + width/2, optimized_values, width, label='优化方案',
               color='#4ECDC4', alpha=0.8, edgecolor='black', linewidth=1.5)

ax.set_ylabel('金额 (万元)', fontsize=14, fontweight='bold')
ax.set_title('财政成本对比分析 (30年名义值)\n正值=支出, 负值=收入', 
             fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x_pos)
ax.set_xticklabels(categories, fontsize=12, fontweight='bold')
ax.axhline(y=0, color='black', linestyle='-', linewidth=2)
ax.legend(fontsize=13, loc='upper left')
ax.grid(axis='y', alpha=0.3, linestyle='--')

# 添加数值标签
for bars in [bars1, bars2]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'¥{height:+.0f}万',
                ha='center', va='bottom' if height > 0 else 'top',
                fontsize=10, fontweight='bold')

plt.tight_layout()
plt.savefig('对比图5_财政成本对比.png', dpi=300, bbox_inches='tight')
print("✅ 已生成: 对比图5_财政成本对比.png")
plt.close()

# ============================================================================
# 生成对比表格
# ============================================================================
print("\n" + "="*80)
print("综合对比表格")
print("="*80)

comparison_table = pd.DataFrame({
    '指标': [
        '平均缴费额 (元/年)',
        '平均T3税率 (%)',
        '平均补贴 (元/年)',
        '平均净收益 (元/终身)',
        '覆盖率 (%)',
        'Gini系数',
        '补贴支出 (万元/30年)',
        'T3税收 (万元/50年)',
        '净财政成本 (万元)'
    ],
    '现行政策': [
        f"{df_current['contribution'].mean():.0f}",
        f"{df_current['t3'].mean()*100:.2f}",
        "0",
        f"{df_current['net_benefit'].mean():.0f}",
        f"{coverage_current:.1f}",
        f"{gini_current:.3f}",
        f"{subsidy_current:.0f}",
        f"{t3_tax_current:.0f}",
        f"{net_cost_current:.0f}"
    ],
    '优化方案': [
        f"{df_optimized['contribution'].mean():.0f}",
        f"{df_optimized['t3'].mean()*100:.2f}",
        f"{df_optimized['subsidy'].mean():.0f}",
        f"{df_optimized['net_benefit'].mean():.0f}",
        f"{coverage_optimized:.1f}",
        f"{gini_optimized:.3f}",
        f"{subsidy_optimized:.0f}",
        f"{t3_tax_optimized:.0f}",
        f"{net_cost_optimized:.0f}"
    ],
    '改善幅度': [
        f"{(df_optimized['contribution'].mean() - df_current['contribution'].mean()):.0f}",
        f"{(df_optimized['t3'].mean() - df_current['t3'].mean())*100:+.2f}",
        f"+{df_optimized['subsidy'].mean():.0f}",
        f"{(df_optimized['net_benefit'].mean() - df_current['net_benefit'].mean()):.0f}",
        f"+{(coverage_optimized - coverage_current):.1f}",
        f"{(gini_optimized - gini_current):.3f}",
        f"+{subsidy_optimized:.0f}",
        f"{(t3_tax_optimized - t3_tax_current):.0f}",
        f"{(net_cost_optimized - net_cost_current):.0f}"
    ]
})

print(comparison_table.to_string(index=False))

# 保存表格
comparison_table.to_csv('对比表_政策综合对比.csv', index=False, encoding='utf-8-sig')
print("\n✅ 已生成: 对比表_政策综合对比.csv")

print("\n" + "="*80)
print("核心发现总结")
print("="*80)
print(f"\n1. 覆盖率提升: {coverage_current:.1f}% → {coverage_optimized:.1f}% (+{coverage_optimized-coverage_current:.1f}个百分点)")
print(f"2. 公平性改善: Gini {gini_current:.3f} → {gini_optimized:.3f} (改善{(gini_current-gini_optimized)/gini_current*100:.1f}%)")
print(f"3. 净收益提升: ¥{df_current['net_benefit'].mean():.0f} → ¥{df_optimized['net_benefit'].mean():.0f} (+¥{df_optimized['net_benefit'].mean()-df_current['net_benefit'].mean():.0f})")
print(f"4. T3税率: 固定3% → 累进0-14% (平均{df_optimized['t3'].mean()*100:.2f}%)")
print(f"5. 财政补贴: ¥0 → ¥{subsidy_optimized:.0f}万 (30年)")
print(f"6. 净财政成本: ¥{net_cost_current:.0f}万 → ¥{net_cost_optimized:.0f}万 (增加¥{net_cost_optimized-net_cost_current:.0f}万)")

print("\n✅ 所有对比图表生成完成！")
print("="*80)
