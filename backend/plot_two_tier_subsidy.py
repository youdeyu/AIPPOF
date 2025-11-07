"""
绘制两段式补贴模型示意图
展示AIPPOF网页应用实际采用的补贴计算方式
"""
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib import rcParams

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False

# 补贴参数
base_grant = 150  # 固定补贴
ratio_low = 0.30   # 低档配比（首档30%）
ratio_high = 0.06  # 高档配比（超额6%）
uplift_low = 0.5   # 低收入加成（+50%）
c0_threshold = 1600  # 首档上限（假设年薪8万×2%）
low_income_cut = 80000  # 低收入界定

# 创建缴费额序列
contribution = np.linspace(0, 12000, 1000)

# 计算补贴（普通收入）
def calc_subsidy_normal(C):
    """普通收入群体补贴（年薪>8万）"""
    subsidy = np.zeros_like(C)
    
    for i, c in enumerate(C):
        if c < 200:  # 最低门槛
            subsidy[i] = 0
        elif c <= c0_threshold:
            # 第一段：30%配比
            match = c * ratio_low
            subsidy[i] = base_grant + match
        else:
            # 第二段：首档30% + 超额6%
            tier1 = c0_threshold * ratio_low
            tier2 = (c - c0_threshold) * ratio_high
            subsidy[i] = base_grant + tier1 + tier2
    
    # 收入递减（假设年薪8万，递减因子0.333）
    taper_factor = 0.333
    subsidy = subsidy * taper_factor
    
    return subsidy

# 计算补贴（低收入）
def calc_subsidy_low_income(C):
    """低收入群体补贴（年薪≤8万）"""
    subsidy = np.zeros_like(C)
    
    for i, c in enumerate(C):
        if c < 200:
            subsidy[i] = 0
        elif c <= c0_threshold:
            # 第一段：30% × (1+50%) = 45%配比
            match = c * ratio_low * (1 + uplift_low)
            subsidy[i] = base_grant + match
        else:
            # 第二段：首档45% + 超额6%
            tier1 = c0_threshold * ratio_low * (1 + uplift_low)
            tier2 = (c - c0_threshold) * ratio_high
            subsidy[i] = base_grant + tier1 + tier2
    
    # 收入递减（假设年薪8万，递减因子0.333）
    taper_factor = 0.333
    subsidy = subsidy * taper_factor
    
    return subsidy

# 计算两种补贴
subsidy_normal = calc_subsidy_normal(contribution)
subsidy_low = calc_subsidy_low_income(contribution)

# ==================== 创建图表 ====================
fig = plt.figure(figsize=(16, 10))

# 图1: 两段式补贴曲线对比
ax1 = plt.subplot(2, 2, 1)
ax1.plot(contribution, subsidy_normal, 'b-', linewidth=2.5, label='普通收入（30%+6%）')
ax1.plot(contribution, subsidy_low, 'r-', linewidth=2.5, label='低收入加成（45%+6%）')
ax1.axvline(c0_threshold, color='gray', linestyle='--', alpha=0.5, label=f'首档上限 ¥{c0_threshold}')
ax1.axvline(200, color='orange', linestyle=':', alpha=0.5, label='最低门槛 ¥200')

ax1.set_xlabel('年度缴费额（元）', fontsize=12, fontweight='bold')
ax1.set_ylabel('补贴金额（元）', fontsize=12, fontweight='bold')
ax1.set_title('两段式补贴模型：缴费-补贴关系', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10, loc='upper left')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0, 12000)
ax1.set_ylim(0, max(subsidy_low)*1.1)

# 添加注释
ax1.annotate('第一段：30%配比\n（低收入45%）', 
             xy=(800, calc_subsidy_low_income(np.array([800]))[0]), 
             xytext=(2000, 350),
             arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
             fontsize=10, color='red', weight='bold')

ax1.annotate('第二段：6%配比', 
             xy=(8000, calc_subsidy_normal(np.array([8000]))[0]), 
             xytext=(9000, 150),
             arrowprops=dict(arrowstyle='->', color='blue', lw=1.5),
             fontsize=10, color='blue', weight='bold')

# 图2: 补贴率曲线
ax2 = plt.subplot(2, 2, 2)
subsidy_rate_normal = (subsidy_normal / contribution) * 100
subsidy_rate_low = (subsidy_low / contribution) * 100

# 处理无穷大值
subsidy_rate_normal[contribution < 200] = 0
subsidy_rate_low[contribution < 200] = 0

ax2.plot(contribution, subsidy_rate_normal, 'b-', linewidth=2.5, label='普通收入补贴率')
ax2.plot(contribution, subsidy_rate_low, 'r-', linewidth=2.5, label='低收入补贴率')
ax2.axvline(c0_threshold, color='gray', linestyle='--', alpha=0.5)

ax2.set_xlabel('年度缴费额（元）', fontsize=12, fontweight='bold')
ax2.set_ylabel('补贴率（%）', fontsize=12, fontweight='bold')
ax2.set_title('补贴率随缴费额变化', fontsize=14, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(0, 12000)
ax2.set_ylim(0, 20)

# 图3: 分段明细堆叠图（低收入）
ax3 = plt.subplot(2, 2, 3)

# 计算各部分
C_values = np.array([500, 1000, 1600, 3000, 6000, 9000, 12000])
base_parts = []
tier1_parts = []
tier2_parts = []

for c in C_values:
    if c <= c0_threshold:
        tier1 = c * ratio_low * (1 + uplift_low) * 0.333
        tier2 = 0
    else:
        tier1 = c0_threshold * ratio_low * (1 + uplift_low) * 0.333
        tier2 = (c - c0_threshold) * ratio_high * 0.333
    
    base_parts.append(base_grant * 0.333)
    tier1_parts.append(tier1)
    tier2_parts.append(tier2)

x_pos = np.arange(len(C_values))
width = 0.6

p1 = ax3.bar(x_pos, base_parts, width, label='固定补贴（¥150×33.3%）', color='#FFD700')
p2 = ax3.bar(x_pos, tier1_parts, width, bottom=base_parts, label='首档配比（45%）', color='#FF6B6B')
p3 = ax3.bar(x_pos, tier2_parts, width, bottom=np.array(base_parts)+np.array(tier1_parts), 
             label='超额配比（6%）', color='#4ECDC4')

ax3.set_xlabel('缴费额（元）', fontsize=12, fontweight='bold')
ax3.set_ylabel('补贴金额（元）', fontsize=12, fontweight='bold')
ax3.set_title('低收入群体补贴构成（三部分叠加）', fontsize=14, fontweight='bold')
ax3.set_xticks(x_pos)
ax3.set_xticklabels([f'¥{int(c)}' for c in C_values], rotation=45)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3, axis='y')

# 添加数值标签
for i, (c, total) in enumerate(zip(C_values, np.array(base_parts)+np.array(tier1_parts)+np.array(tier2_parts))):
    ax3.text(i, total + 10, f'¥{total:.0f}', ha='center', fontsize=9, weight='bold')

# 图4: 公式流程图（文字说明）
ax4 = plt.subplot(2, 2, 4)
ax4.axis('off')

formula_text = """
【两段式补贴模型公式】

1️⃣ 参数设定：
   • 固定补贴：G₀ = ¥150
   • 首档缴费基数：C₀ = 2%工资
   • 首档配比率：γ₁ = 30%（普通）或 45%（低收入）
   • 超额配比率：γ₂ = 6%
   • 低收入界定：≤ ¥80,000/年
   • 收入递减区间：¥40,000 ~ ¥100,000

2️⃣ 补贴计算公式：

   当 C ≤ C₀ 时（第一段）：
   S = (G₀ + C × γ₁) × λ(w)
   
   当 C > C₀ 时（第二段）：
   S = (G₀ + C₀ × γ₁ + (C - C₀) × γ₂) × λ(w)

3️⃣ 低收入加成：
   若 w ≤ ¥80,000：
   γ₁ = 30% × (1 + 50%) = 45%

4️⃣ 收入递减因子 λ(w)：
   • w ≤ ¥40,000：λ = 1.0（全额）
   • ¥40,000 < w < ¥100,000：λ = (100k-w)/(100k-40k)
   • w ≥ ¥100,000：λ = 0.0（补贴归零）

【示例】年薪¥80,000，缴费¥6,000：
   C₀ = 80,000 × 2% = ¥1,600
   γ₁ = 45%（低收入加成）
   λ = (100,000-80,000)/(100,000-40,000) = 0.333
   
   S = (150 + 1,600×45% + (6,000-1,600)×6%) × 0.333
     = (150 + 720 + 264) × 0.333
     = 1,134 × 0.333
     = ¥378
"""

ax4.text(0.05, 0.95, formula_text, transform=ax4.transAxes,
         fontsize=10, verticalalignment='top', family='monospace',
         bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3))

plt.suptitle('AIPPOF两段式补贴模型完整解析', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout(rect=[0, 0, 1, 0.96])

# 保存图片
output_file = '两段式补贴模型示意图.png'
plt.savefig(output_file, dpi=300, bbox_inches='tight')
print(f"✅ 图表已保存: {output_file}")

plt.show()

# ==================== 输出详细说明 ====================
print("\n" + "="*80)
print("【两段式补贴模型说明】")
print("="*80)
print("\n📊 模型结构：")
print("   第一段：0 < C ≤ C₀（首档缴费）")
print("   第二段：C > C₀（超额缴费）")
print("\n💰 配比率：")
print("   • 普通收入：首档30% + 超额6%")
print("   • 低收入：  首档45% + 超额6%（含50%加成）")
print("\n🎯 关键特点：")
print("   1. 固定补贴：所有人享受¥150基础补贴")
print("   2. 分段配比：激励低额缴费（30%/45%），超额递减（6%）")
print("   3. 收入递减：高收入补贴逐步归零（4万-10万区间）")
print("   4. 低收入倾斜：年薪≤8万享受50%加成（30%→45%）")
print("\n✅ 与论文三段式的等价性：")
print("   论文：α₁=45%, α₂=30%, α₃=6%（三个独立参数）")
print("   代码：γ₁=30%×(1+50%)=45%, γ₂=6%（通过加成实现）")
print("   结果：实质等价，低收入首档均为45%，超额均为6%")
print("\n" + "="*80)
