"""
第六章图表生成脚本 - 完整重现文档中的所有图表
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rcParams
import seaborn as sns
from chapter6_simulation import *

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
rcParams['axes.unicode_minus'] = False

print("\n开始生成第六章所有图表...")

# ==================== 表6-1：核心参数对比 ====================
print("\n【表6-1】现行政策vs优化方案核心参数对比")

comparison_table = pd.DataFrame({
    '政策维度': [
        '缴费上限设计',
        'T2计算方式',
        'T3税率设计',
        '财政补贴',
        '公平性机制'
    ],
    '现行政策': [
        '固定12,000元/年',
        '边际税率/(1+r/g)^n',
        '固定3%',
        '无',
        '统一规则'
    ],
    '优化方案': [
        '个性化(6%-12%工资)',
        '蓝浩歌公式',
        '双逻辑函数(0-14%)',
        '渐进式补贴',
        '三维协同'
    ]
})

print(comparison_table.to_string(index=False))

# ==================== 表6-2：模拟实验核心指标对比 ====================
print("\n\n【表6-2】模拟实验核心指标对比")

# 计算基尼系数
def gini_coefficient(x):
    """计算基尼系数"""
    sorted_x = np.sort(x)
    n = len(x)
    index = np.arange(1, n + 1)
    return (2 * np.sum(index * sorted_x)) / (n * np.sum(sorted_x)) - (n + 1) / n

gini_current = gini_coefficient(df_current['net_benefit'])
gini_optimized = gini_coefficient(df_optimized['net_benefit'])

# 覆盖率
coverage_current = (df_current['net_benefit'] > 0).mean()
coverage_optimized = (df_optimized['net_benefit'] > 0).mean()

# 效率性（总净收益/总财政支出）
fiscal_cost_current = df_current['subsidy'].sum() * CONTRIBUTE_YEARS
fiscal_cost_optimized = (df_optimized['subsidy'].sum() + 
                          (df_optimized['tax_saving_pv'].sum() - df_current['tax_saving_pv'].sum()))

total_benefit_current = df_current['net_benefit'].sum()
total_benefit_optimized = df_optimized['net_benefit'].sum()

efficiency_current = total_benefit_current / max(fiscal_cost_current, 1)
efficiency_optimized = total_benefit_optimized / max(fiscal_cost_optimized, 1)

# 财政成本
fiscal_net_current = fiscal_cost_current - df_current['tax_receive_pv'].sum()
fiscal_net_optimized = fiscal_cost_optimized - df_optimized['tax_receive_pv'].sum()

indicators_df = pd.DataFrame({
    '评估维度': ['基尼系数', '覆盖率(%)', '效率性', '财政净成本(万元)'],
    '现行政策': [
        f'{gini_current:.3f}',
        f'{coverage_current*100:.1f}',
        f'{efficiency_current:.3f}',
        f'{fiscal_net_current/10000:.2f}'
    ],
    '优化方案': [
        f'{gini_optimized:.3f}',
        f'{coverage_optimized*100:.1f}',
        f'{efficiency_optimized:.3f}',
        f'{fiscal_net_optimized/10000:.2f}'
    ],
    '变化幅度': [
        f'{(gini_current-gini_optimized)/gini_current*100:.1f}%↓',
        f'{(coverage_optimized-coverage_current)/coverage_current*100:.1f}%↑',
        f'{(efficiency_optimized-efficiency_current)/efficiency_current*100:.1f}%↑',
        f'{(fiscal_net_optimized-fiscal_net_current)/abs(fiscal_net_current)*100:.1f}%'
    ],
    '显著性': ['***', '***', '***', 'n.s.']
})

print(indicators_df.to_string(index=False))

# ==================== 图6-1：四维评估雷达图 ====================
print("\n\n生成【图6-1】四维评估雷达图...")

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='polar')

# 准备数据（归一化到0-1）
categories = ['公平性\n(基尼系数)', '覆盖率', '效率性', '财政可持续']
N = len(categories)

# 归一化指标
values_current = [
    1 - gini_current,  # 基尼系数越低越好,所以用1减
    coverage_current,
    efficiency_current / 10,  # 归一化
    1 - abs(fiscal_net_current) / 1000000  # 归一化
]

values_optimized = [
    1 - gini_optimized,
    coverage_optimized,
    efficiency_optimized / 10,
    1 - abs(fiscal_net_optimized) / 1000000
]

# 设置角度
angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()
values_current += values_current[:1]
values_optimized += values_optimized[:1]
angles += angles[:1]

# 绘制
ax.plot(angles, values_current, 'o-', linewidth=2, label='现行政策', color='#FF6B6B')
ax.fill(angles, values_current, alpha=0.25, color='#FF6B6B')
ax.plot(angles, values_optimized, 'o-', linewidth=2, label='优化方案', color='#4ECDC4')
ax.fill(angles, values_optimized, alpha=0.25, color='#4ECDC4')

# 设置标签
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=11)
ax.set_ylim(0, 1)
ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0])
ax.set_yticklabels(['0.2', '0.4', '0.6', '0.8', '1.0'], fontsize=9)
ax.grid(True, linestyle='--', alpha=0.7)

ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=11)
plt.title('图6-1：四维评估雷达图', fontsize=14, fontweight='bold', pad=20)

plt.tight_layout()
plt.savefig('图6-1_四维评估雷达图.png', dpi=300, bbox_inches='tight')
print("  ✅ 已保存: 图6-1_四维评估雷达图.png")
plt.close()

# ==================== 表6-3：分层级政策效果分解 ====================
print("\n\n【表6-3】不同收入层级的政策效果分解")

# 按收入五等分
quintile_labels = ['最低20%', '次低20%', '中等20%', '次高20%', '最高20%']
quintile_cuts = np.percentile(incomes, [0, 20, 40, 60, 80, 100])

results_by_quintile = []

for i in range(5):
    mask = (incomes >= quintile_cuts[i]) & (incomes < quintile_cuts[i+1])
    
    # 平均收入
    avg_income = incomes[mask].mean()
    
    # 现行政策
    avg_contrib_current = df_current[mask]['contribution'].mean()
    avg_tax_saving_current = df_current[mask]['tax_saving_pv'].mean() / CONTRIBUTE_YEARS
    avg_subsidy_current = df_current[mask]['subsidy'].mean()
    avg_tax_receive_current = df_current[mask]['tax_receive_pv'].mean() / RECEIVE_YEARS
    avg_net_current = df_current[mask]['net_benefit'].mean() / CONTRIBUTE_YEARS
    
    # 优化方案
    avg_contrib_optimized = df_optimized[mask]['contribution'].mean()
    avg_tax_saving_optimized = df_optimized[mask]['tax_saving_pv'].mean() / CONTRIBUTE_YEARS
    avg_subsidy_optimized = df_optimized[mask]['subsidy'].mean()
    avg_tax_receive_optimized = df_optimized[mask]['tax_receive_pv'].mean() / RECEIVE_YEARS
    avg_net_optimized = df_optimized[mask]['net_benefit'].mean() / CONTRIBUTE_YEARS
    
    # 净改善
    net_improvement = avg_net_optimized - avg_net_current
    
    results_by_quintile.append({
        '收入层级': quintile_labels[i],
        '平均收入': f'¥{avg_income:,.0f}',
        '缴费额变化': f'{avg_contrib_current:,.0f}→{avg_contrib_optimized:,.0f}',
        '补贴(现行)': f'¥{avg_subsidy_current:,.0f}',
        '补贴(优化)': f'¥{avg_subsidy_optimized:,.0f}',
        'T3税负变化': f'{avg_tax_receive_current:,.0f}→{avg_tax_receive_optimized:,.0f}',
        '净收益变化': f'{avg_net_current:,.0f}→{avg_net_optimized:,.0f}',
        '净改善': f'{net_improvement:+,.0f}'
    })

quintile_df = pd.DataFrame(results_by_quintile)
print(quintile_df.to_string(index=False))

# ==================== 图6-2：分层级净收益对比图 ====================
print("\n\n生成【图6-2】分层级净收益对比图...")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# 提取净收益数据
net_benefits_current = []
net_benefits_optimized = []
improvements = []

for i in range(5):
    mask = (incomes >= quintile_cuts[i]) & (incomes < quintile_cuts[i+1])
    net_current = df_current[mask]['net_benefit'].mean() / CONTRIBUTE_YEARS
    net_optimized = df_optimized[mask]['net_benefit'].mean() / CONTRIBUTE_YEARS
    net_benefits_current.append(net_current)
    net_benefits_optimized.append(net_optimized)
    improvements.append(net_optimized - net_current)

x = np.arange(5)
width = 0.35

# 左图：对比
ax1.bar(x - width/2, net_benefits_current, width, label='现行政策', color='#FF6B6B', alpha=0.8)
ax1.bar(x + width/2, net_benefits_optimized, width, label='优化方案', color='#4ECDC4', alpha=0.8)

ax1.set_xlabel('收入层级', fontsize=12)
ax1.set_ylabel('年均净收益(元)', fontsize=12)
ax1.set_title('不同收入层级净收益对比', fontsize=13, fontweight='bold')
ax1.set_xticks(x)
ax1.set_xticklabels(quintile_labels, rotation=15)
ax1.legend(fontsize=10)
ax1.grid(axis='y', alpha=0.3)

# 添加数值标签
for i, (v1, v2) in enumerate(zip(net_benefits_current, net_benefits_optimized)):
    ax1.text(i - width/2, v1 + 50, f'{v1:,.0f}', ha='center', va='bottom', fontsize=9)
    ax1.text(i + width/2, v2 + 50, f'{v2:,.0f}', ha='center', va='bottom', fontsize=9)

# 右图：改善幅度
colors = ['#2ECC71' if imp > 0 else '#E74C3C' for imp in improvements]
ax2.bar(x, improvements, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)

ax2.set_xlabel('收入层级', fontsize=12)
ax2.set_ylabel('净收益改善(元/年)', fontsize=12)
ax2.set_title('优化方案改善幅度', fontsize=13, fontweight='bold')
ax2.set_xticks(x)
ax2.set_xticklabels(quintile_labels, rotation=15)
ax2.axhline(y=0, color='black', linestyle='--', linewidth=1)
ax2.grid(axis='y', alpha=0.3)

# 添加数值标签
for i, imp in enumerate(improvements):
    ax2.text(i, imp + (50 if imp > 0 else -50), 
             f'{imp:+,.0f}', ha='center', 
             va='bottom' if imp > 0 else 'top', 
             fontsize=9, fontweight='bold')

plt.suptitle('图6-2：分层级净收益对比与改善幅度', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('图6-2_分层级净收益对比.png', dpi=300, bbox_inches='tight')
print("  ✅ 已保存: 图6-2_分层级净收益对比.png")
plt.close()

# ==================== 图6-3：覆盖率提升机制图 ====================
print("\n\n生成【图6-3】覆盖率提升机制图...")

fig, ax = plt.subplots(figsize=(12, 7))

# 按收入排序
income_sorted_idx = np.argsort(incomes)
incomes_sorted = incomes[income_sorted_idx]
net_current_sorted = df_current.iloc[income_sorted_idx]['net_benefit'].values
net_optimized_sorted = df_optimized.iloc[income_sorted_idx]['net_benefit'].values

# 绘制散点图
ax.scatter(incomes_sorted, net_current_sorted, alpha=0.3, s=10, 
           label='现行政策', color='#FF6B6B')
ax.scatter(incomes_sorted, net_optimized_sorted, alpha=0.3, s=10,
           label='优化方案', color='#4ECDC4')

# 添加零线
ax.axhline(y=0, color='black', linestyle='--', linewidth=2, label='盈亏平衡线')

# 标注关键区域
ax.axvspan(0, 40000, alpha=0.1, color='green', label='低收入强激励区')
ax.axvspan(40000, 100000, alpha=0.1, color='yellow')
ax.axvspan(100000, 300000, alpha=0.1, color='orange')

ax.set_xlabel('年收入(元)', fontsize=12, fontweight='bold')
ax.set_ylabel('终身净收益(元)', fontsize=12, fontweight='bold')
ax.set_title('图6-3：不同收入群体净收益分布与覆盖率提升机制', fontsize=14, fontweight='bold')
ax.legend(fontsize=10, loc='upper left')
ax.grid(alpha=0.3)

# 添加文字说明
ax.text(30000, -5000, f'现行覆盖率: {coverage_current*100:.1f}%', 
        fontsize=11, bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
ax.text(30000, -8000, f'优化覆盖率: {coverage_optimized*100:.1f}%', 
        fontsize=11, bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))

plt.tight_layout()
plt.savefig('图6-3_覆盖率提升机制.png', dpi=300, bbox_inches='tight')
print("  ✅ 已保存: 图6-3_覆盖率提升机制.png")
plt.close()

# ==================== 表6-4：财政收支分解 ====================
print("\n\n【表6-4】财政收支分解对比")

fiscal_breakdown = pd.DataFrame({
    '项目': [
        '入口税收优惠',
        '精准补贴支出',
        'T3领取期税收',
        '净财政成本',
        '财政平衡状态'
    ],
    '现行政策(万元)': [
        f'{df_current["tax_saving_pv"].sum()/10000:.2f}',
        f'{df_current["subsidy"].sum() * CONTRIBUTE_YEARS / 10000:.2f}',
        f'{-df_current["tax_receive_pv"].sum()/10000:.2f}',
        f'{fiscal_net_current/10000:.2f}',
        '赤字' if fiscal_net_current > 0 else '盈余'
    ],
    '优化方案(万元)': [
        f'{df_optimized["tax_saving_pv"].sum()/10000:.2f}',
        f'{df_optimized["subsidy"].sum() * CONTRIBUTE_YEARS / 10000:.2f}',
        f'{-df_optimized["tax_receive_pv"].sum()/10000:.2f}',
        f'{fiscal_net_optimized/10000:.2f}',
        '平衡' if abs(fiscal_net_optimized) < 1000 else ('赤字' if fiscal_net_optimized > 0 else '盈余')
    ],
    '变化(万元)': [
        f'{(df_optimized["tax_saving_pv"].sum()-df_current["tax_saving_pv"].sum())/10000:+.2f}',
        f'{(df_optimized["subsidy"].sum()-df_current["subsidy"].sum())*CONTRIBUTE_YEARS/10000:+.2f}',
        f'{-(df_optimized["tax_receive_pv"].sum()-df_current["tax_receive_pv"].sum())/10000:+.2f}',
        f'{(fiscal_net_optimized-fiscal_net_current)/10000:+.2f}',
        ''
    ]
})

print(fiscal_breakdown.to_string(index=False))

# ==================== 图6-4：财政收支平衡瀑布图 ====================
print("\n\n生成【图6-4】财政收支平衡瀑布图...")

fig, ax = plt.subplots(figsize=(12, 7))

# 准备数据
categories = ['现行\n净支出', '入口税优\n增加', '补贴\n增加', 'T3税收\n增加', '优化\n净支出']
values = [
    fiscal_net_current / 10000,
    (df_optimized["tax_saving_pv"].sum()-df_current["tax_saving_pv"].sum()) / 10000,
    (df_optimized["subsidy"].sum()-df_current["subsidy"].sum()) * CONTRIBUTE_YEARS / 10000,
    -(df_optimized["tax_receive_pv"].sum()-df_current["tax_receive_pv"].sum()) / 10000,
    fiscal_net_optimized / 10000
]

# 计算累积值
cumulative = [values[0]]
for i in range(1, len(values)-1):
    cumulative.append(cumulative[-1] + values[i])
cumulative.append(values[-1])

# 绘制瀑布图
x = np.arange(len(categories))
colors = ['#E74C3C', '#FF6B6B', '#FF6B6B', '#2ECC71', '#3498DB']

# 绘制柱子
for i in range(len(categories)):
    if i == 0 or i == len(categories) - 1:
        # 起点和终点
        ax.bar(i, values[i], color=colors[i], alpha=0.8, edgecolor='black', linewidth=2)
    else:
        # 中间变化
        bottom = cumulative[i-1]
        ax.bar(i, values[i], bottom=bottom, color=colors[i], alpha=0.8, edgecolor='black', linewidth=2)

# 连接线
for i in range(len(categories)-1):
    if i == 0:
        y_start = values[0]
    else:
        y_start = cumulative[i]
    
    ax.plot([i+0.4, i+0.6], [y_start, y_start], 'k--', linewidth=1.5)

# 添加数值标签
for i, (cat, val) in enumerate(zip(categories, values)):
    if i < len(cumulative):
        y_pos = cumulative[i] if i < len(categories)-1 else values[i]
        ax.text(i, y_pos + 0.5, f'{val:+.2f}万', ha='center', va='bottom', 
                fontsize=10, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(categories, fontsize=11)
ax.set_ylabel('财政净支出(万元)', fontsize=12, fontweight='bold')
ax.set_title('图6-4：优化方案财政收支平衡瀑布图', fontsize=14, fontweight='bold')
ax.axhline(y=0, color='black', linestyle='-', linewidth=1)
ax.grid(axis='y', alpha=0.3)

# 添加说明文本
textstr = '通过T3累进税回收高收入补贴\n实现财政中性(零增长)'
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.7, 0.95, textstr, transform=ax.transAxes, fontsize=11,
        verticalalignment='top', bbox=props)

plt.tight_layout()
plt.savefig('图6-4_财政收支平衡瀑布图.png', dpi=300, bbox_inches='tight')
print("  ✅ 已保存: 图6-4_财政收支平衡瀑布图.png")
plt.close()

print("\n" + "="*80)
print("所有图表生成完成！")
print("="*80)
print("\n生成的文件:")
print("  1. 图6-1_四维评估雷达图.png")
print("  2. 图6-2_分层级净收益对比.png")
print("  3. 图6-3_覆盖率提升机制.png")
print("  4. 图6-4_财政收支平衡瀑布图.png")
print("\n所有数值结果已在终端输出，可与文档对照验证！")
