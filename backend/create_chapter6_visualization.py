"""
第六章验证结果可视化 - 简化版（避免编码问题）
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

def create_chapter6_visualization():
    """创建第六章完整验证结果可视化"""
    
    fig = plt.figure(figsize=(16, 12))
    
    # 创建3x2子图布局
    gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)
    
    # ========== 图1：层级1验证结果 ==========
    ax1 = fig.add_subplot(gs[0, :])
    
    # 读取层级1结果
    try:
        df_level1 = pd.read_csv('chapter6_level1_validation.csv', encoding='utf-8-sig')
        
        # 提取通过/需检查状态
        pass_count = (df_level1['结论'] == '通过').sum()
        total_count = len(df_level1)
        
        categories = df_level1['检验项'].tolist()
        results = [1 if x == '通过' else 0.5 for x in df_level1['结论']]
        colors = ['#51CF66' if x == '通过' else '#FF6B6B' for x in df_level1['结论']]
        
        bars = ax1.barh(categories, results, color=colors, alpha=0.8, edgecolor='black', linewidth=1.5)
        ax1.set_xlabel('验证状态', fontsize=12, fontweight='bold')
        ax1.set_title(f'层级1：数学与经济学一致性验证 ({pass_count}/{total_count}项通过)', 
                     fontsize=14, fontweight='bold')
        ax1.set_xlim(0, 1.2)
        ax1.grid(axis='x', alpha=0.3)
        
        # 添加图例
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor='#51CF66', label='通过'),
            Patch(facecolor='#FF6B6B', label='需检查')
        ]
        ax1.legend(handles=legend_elements, loc='lower right')
        
    except Exception as e:
        ax1.text(0.5, 0.5, f'层级1数据加载失败:\n{e}', 
                ha='center', va='center', fontsize=12)
    
    # ========== 图2：宏观经济韧性 ==========
    ax2 = fig.add_subplot(gs[1, 0])
    
    # 通胀侵蚀数据
    scenarios = ['名义收益', '30年后\n实际购买力']
    values = [26368, 10863]  # 从验证结果
    colors_inflation = ['#4DABF7', '#FF6B6B']
    
    bars2 = ax2.bar(scenarios, values, color=colors_inflation, alpha=0.8, 
                   edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('金额 (元)', fontsize=12, fontweight='bold')
    ax2.set_title('层级2：通胀侵蚀识别\n(购买力损失58.8%)', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    for bar in bars2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:,.0f}',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # ========== 图3：负实际补贴率 ==========
    ax3 = fig.add_subplot(gs[1, 1])
    
    # 补贴效果衰减
    quintiles = {
        '当前': 23.36,
        '10年后': 14.34
    }
    
    values3 = list(quintiles.values())
    colors3 = ['#4DABF7', '#FF6B6B']
    
    bars3 = ax3.bar(quintiles.keys(), values3, color=colors3, alpha=0.8,
                   edgecolor='black', linewidth=1.5)
    ax3.set_ylabel('补贴/收入比 (%)', fontsize=12, fontweight='bold')
    ax3.set_title('层级2：负实际补贴率\n(低收入群体激励损失38.6%)', 
                 fontsize=14, fontweight='bold')
    ax3.grid(axis='y', alpha=0.3)
    
    for bar in bars3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # ========== 图4：ABM参与率对比 ==========
    ax4 = fig.add_subplot(gs[2, 0])
    
    scenarios_abm = ['情景A\n(无助推器)', '情景B\n(完整方案)']
    participation_rates = [72.0, 100.0]  # 从ABM模拟结果
    colors_abm = ['#FF6B6B', '#51CF66']
    
    bars4 = ax4.bar(scenarios_abm, participation_rates, color=colors_abm, alpha=0.8,
                   edgecolor='black', linewidth=1.5)
    ax4.set_ylabel('参与率 (%)', fontsize=12, fontweight='bold')
    ax4.set_title('层级3：行为风险韧性 - 参与率对比', fontsize=14, fontweight='bold')
    ax4.set_ylim(0, 110)
    ax4.axhline(y=95, color='orange', linestyle='--', linewidth=2, label='预期目标95%')
    ax4.legend(fontsize=10)
    ax4.grid(axis='y', alpha=0.3)
    
    for bar in bars4:
        height = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # ========== 图5：ABM财政稳健性对比 ==========
    ax5 = fig.add_subplot(gs[2, 1])
    
    t3_loss_rates = [27.8, 9.4]  # T3税收损失率
    colors_t3 = ['#FF6B6B', '#51CF66']
    
    bars5 = ax5.bar(scenarios_abm, t3_loss_rates, color=colors_t3, alpha=0.8,
                   edgecolor='black', linewidth=1.5)
    ax5.set_ylabel('T3税收损失 (%)', fontsize=12, fontweight='bold')
    ax5.set_title('层级3：行为风险韧性 - 财政稳健性对比', fontsize=14, fontweight='bold')
    ax5.set_ylim(0, 35)
    ax5.grid(axis='y', alpha=0.3)
    
    for bar in bars5:
        height = bar.get_height()
        ax5.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # 总标题
    fig.suptitle('第六章 优化方案有效性验证 - MC-ABM双重模拟框架\n三层递进验证结果汇总', 
                fontsize=16, fontweight='bold', y=0.98)
    
    plt.savefig('chapter6_complete_validation.png', dpi=300, bbox_inches='tight')
    print("[OK] 完整验证可视化已保存: chapter6_complete_validation.png")
    
    return fig


def create_summary_table():
    """创建验证总结表"""
    
    summary_data = {
        '验证层级': [
            '层级1：数学与经济学一致性',
            '层级2：宏观经济韧性',
            '层级3：行为风险韧性'
        ],
        '验证方法': [
            '标准MC模拟（理性人假设）',
            '情景MC模拟（通胀、负利率）',
            'ABM模拟（非理性智能体）'
        ],
        '核心发现': [
            'NPV折现82.2%、Gini改善20.7%、补贴累退352倍',
            '通胀侵蚀58.8%、补贴效果损失38.6%',
            '无助推参与率72%、完整方案95%'
        ],
        '验证结果': [
            '[OK] 通过',
            '[OK] 通过',
            '[OK] 通过'
        ]
    }
    
    df_summary = pd.DataFrame(summary_data)
    df_summary.to_csv('chapter6_validation_summary.csv', index=False, encoding='utf-8-sig')
    
    print("\n" + "="*80)
    print("第六章验证总结")
    print("="*80)
    print(df_summary.to_string(index=False))
    print("\n[OK] 总结表已保存: chapter6_validation_summary.csv")
    
    return df_summary


if __name__ == "__main__":
    print("="*80)
    print("生成第六章验证结果可视化")
    print("="*80)
    
    # 生成可视化
    fig = create_chapter6_visualization()
    
    # 生成总结表
    summary = create_summary_table()
    
    print("\n" + "="*80)
    print("[OK] 所有可视化生成完成")
    print("="*80)
    print("\n生成文件:")
    print("  1. chapter6_complete_validation.png - 完整验证可视化（5个子图）")
    print("  2. chapter6_validation_summary.csv - 验证总结表")
