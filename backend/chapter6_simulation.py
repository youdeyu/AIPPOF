"""
第六章 模拟实验验证脚本
基于文档：11.4AI驱动下的个人养老金税收优惠政策优化^7一个智能化决策框架的理论构想 (2).docx
完整重现第六章中的所有图表和数值实验
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import rcParams
import seaborn as sns
from scipy import stats

# 设置中文字体
rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'Arial Unicode MS']
rcParams['axes.unicode_minus'] = False
rcParams['figure.dpi'] = 300

print("="*80)
print("第六章 模拟实验验证")
print("="*80)

# ==================== 第一部分：参数设置 ====================
print("\n【第一部分：参数设置】")

# 样本规模
N_SAMPLE = 10000
print(f"样本规模: {N_SAMPLE:,}个虚拟个体")

# 生命周期参数
AGE_START = 30        # 开始缴费年龄
AGE_RETIRE = 60       # 退休年龄
AGE_END = 80          # 预期寿命
CONTRIBUTE_YEARS = AGE_RETIRE - AGE_START  # 缴费年限30年
RECEIVE_YEARS = AGE_END - AGE_RETIRE        # 领取年限20年

# 经济参数
R_INVEST = 0.0175     # 投资回报率1.75%
G_WAGE_CONSERVATIVE = 0.03  # 保守工资增长率3%
G_WAGE_NEUTRAL = 0.05       # 中性工资增长率5%
G_WAGE_OPTIMISTIC = 0.07    # 乐观工资增长率7%

# 收入分布参数（对数正态分布）
MU_INCOME = np.log(50000)    # 对数均值（对应中位数5万）
SIGMA_INCOME = 0.8           # 对数标准差

# 缴费意愿分布
RATIO_CONSERVATIVE = 0.30    # 保守型占比30%
RATIO_STABLE = 0.50          # 稳健型占比50%
RATIO_AGGRESSIVE = 0.20      # 积极型占比20%

# 缴费比例
CONTRIB_RATE_CONSERVATIVE = 0.02  # 保守型2%
CONTRIB_RATE_STABLE = 0.05        # 稳健型5%
CONTRIB_RATE_AGGRESSIVE = 0.08    # 积极型8%

print(f"\n生命周期设置:")
print(f"  缴费期: {AGE_START}-{AGE_RETIRE}岁 ({CONTRIBUTE_YEARS}年)")
print(f"  领取期: {AGE_RETIRE}-{AGE_END}岁 ({RECEIVE_YEARS}年)")
print(f"  投资回报率: {R_INVEST*100:.2f}%")
print(f"  工资增长率: {G_WAGE_NEUTRAL*100:.1f}% (中性)")

# ==================== 现行政策参数 ====================
print(f"\n现行政策参数:")

# 固定上限
CAP_CURRENT = 12000
print(f"  固定上限: ¥{CAP_CURRENT:,}/年")

# 个税起征点和税率表
TAX_THRESHOLD = 60000
TAX_BRACKETS = [
    (36000, 0.03, 0),
    (144000, 0.10, 2520),
    (300000, 0.20, 16920),
    (420000, 0.25, 31920),
    (660000, 0.30, 52920),
    (960000, 0.35, 85920),
    (float('inf'), 0.45, 181920)
]

# T3固定税率
T3_CURRENT = 0.03  # 现行3%固定税率
print(f"  T3固定税率: {T3_CURRENT*100:.1f}%")

# 无补贴
SUBSIDY_CURRENT = 0
print(f"  财政补贴: ¥{SUBSIDY_CURRENT}")

# ==================== 优化方案参数 ====================
print(f"\n优化方案参数:")

# 个性化上限参数
CAP_LAYERS = [
    (60000, 0.06),     # 低收入层6%
    (120000, 0.08),    # 中低收入层8%
    (240000, 0.10),    # 中等收入层10%
    (float('inf'), 0.12)  # 高收入层12%
]
print(f"  个性化上限: 分层比例6%-12%")

# T3双逻辑函数参数
L1 = 0.0    # 最低税率0%
L2 = 0.07   # 中档税率7%
L3 = 0.07   # 高档附加7%
T2_MID = 0.05  # T2中点5%
K1 = 2.0    # T2灵敏度
W_HIGH = 500000  # 高收入阈值50万
K2 = 0.00001  # 收入灵敏度

print(f"  T3范围: {L1*100:.1f}%-{(L2+L3)*100:.1f}% (双逻辑函数)")

# 补贴参数（两段式）
SUBSIDY_BASE = 150        # 固定补贴150元
SUBSIDY_RATIO_LOW = 0.45  # 低收入档45%配比
SUBSIDY_RATIO_MID = 0.30  # 中收入档30%配比
SUBSIDY_RATIO_HIGH = 0.06 # 超额档6%配比
SUBSIDY_INCOME_LOW = 40000   # 低收入界定4万
SUBSIDY_INCOME_HIGH = 100000  # 补贴归零10万

print(f"  补贴配比: 低收入45% → 中收入30% → 超额6%")
print(f"  补贴归零: 年薪≥¥{SUBSIDY_INCOME_HIGH:,}")

# ==================== 第二部分：生成虚拟人群 ====================
print(f"\n{'='*80}")
print("【第二部分：生成虚拟人群】")

np.random.seed(42)  # 设置随机种子以保证可重复性

# 生成收入分布
incomes = np.random.lognormal(MU_INCOME, SIGMA_INCOME, N_SAMPLE)
incomes = np.clip(incomes, 20000, 300000)  # 限制在2万-30万区间

print(f"\n收入分布统计:")
print(f"  平均值: ¥{incomes.mean():,.0f}")
print(f"  中位数: ¥{np.median(incomes):,.0f}")
print(f"  标准差: ¥{incomes.std():,.0f}")
print(f"  范围: ¥{incomes.min():,.0f} - ¥{incomes.max():,.0f}")

# 按收入五等分
income_quintiles = np.percentile(incomes, [0, 20, 40, 60, 80, 100])
print(f"\n收入五等分:")
for i in range(5):
    print(f"  Q{i+1}: ¥{income_quintiles[i]:,.0f} - ¥{income_quintiles[i+1]:,.0f}")

# 分配缴费类型
contrib_types = np.random.choice(
    ['conservative', 'stable', 'aggressive'],
    size=N_SAMPLE,
    p=[RATIO_CONSERVATIVE, RATIO_STABLE, RATIO_AGGRESSIVE]
)

contrib_rates = np.where(
    contrib_types == 'conservative', CONTRIB_RATE_CONSERVATIVE,
    np.where(contrib_types == 'stable', CONTRIB_RATE_STABLE, CONTRIB_RATE_AGGRESSIVE)
)

print(f"\n缴费类型分布:")
print(f"  保守型(2%): {(contrib_types=='conservative').sum():,}人 ({(contrib_types=='conservative').sum()/N_SAMPLE*100:.1f}%)")
print(f"  稳健型(5%): {(contrib_types=='stable').sum():,}人 ({(contrib_types=='stable').sum()/N_SAMPLE*100:.1f}%)")
print(f"  积极型(8%): {(contrib_types=='aggressive').sum():,}人 ({(contrib_types=='aggressive').sum()/N_SAMPLE*100:.1f}%)")

# ==================== 第三部分：核心计算函数 ====================
print(f"\n{'='*80}")
print("【第三部分：核心计算函数】")

def calculate_marginal_tax_rate(taxable_income):
    """计算边际税率"""
    if taxable_income <= 0:
        return 0.0
    
    for threshold, rate, deduction in TAX_BRACKETS:
        if taxable_income <= threshold:
            return rate
    return TAX_BRACKETS[-1][1]

def calculate_tax(taxable_income):
    """计算个人所得税"""
    if taxable_income <= 0:
        return 0.0
    
    for threshold, rate, deduction in TAX_BRACKETS:
        if taxable_income <= threshold:
            return taxable_income * rate - deduction
    
    # 最高档
    return taxable_income * TAX_BRACKETS[-1][1] - TAX_BRACKETS[-1][2]

def calculate_t2_蓝浩歌(income, contribution, years=30, r=R_INVEST, g=G_WAGE_NEUTRAL):
    """
    计算T2平均节税率（蓝浩歌公式）
    """
    total_tax_saving = 0.0
    total_contribution_pv = 0.0
    
    for t in range(years):
        # 第t年的收入（考虑工资增长）
        income_t = income * (1 + g) ** t
        
        # 第t年的缴费额
        contrib_t = contribution * (1 + g) ** t
        
        # 应税收入
        taxable_t = income_t - TAX_THRESHOLD
        
        # 边际税率
        marginal_rate = calculate_marginal_tax_rate(taxable_t)
        
        # 当年税收节约
        tax_saving_t = contrib_t * marginal_rate
        
        # 折现到领取期初
        discount_factor = (1 + r) ** (years - t)
        total_tax_saving += tax_saving_t * discount_factor
        total_contribution_pv += contrib_t * discount_factor
    
    # T2 = 总节税现值 / 总缴费现值
    if total_contribution_pv > 0:
        t2 = total_tax_saving / total_contribution_pv
    else:
        t2 = 0.0
    
    return t2

def calculate_t3_dual_logistic(t2, income):
    """
    计算T3双逻辑函数税率
    """
    # 第一部分：基于T2的逻辑函数
    f1 = L2 / (1 + np.exp(-K1 * (t2 - T2_MID)))
    
    # 第二部分：基于收入的逻辑函数
    f2 = L3 / (1 + np.exp(-K2 * (income - W_HIGH)))
    
    # 合计
    t3 = L1 + f1 + f2
    
    # 限制在[0, 14%]
    t3 = np.clip(t3, 0.0, 0.14)
    
    return t3

def calculate_cap_optimized(income, t2):
    """
    计算优化方案的个性化上限
    """
    # 基础上限（分层比例）
    for threshold, ratio in CAP_LAYERS:
        if income <= threshold:
            cap_base = income * ratio
            break
    
    # 高收入递减因子（简化版）
    if income > 200000:
        decay_factor = 1.0 - 0.3 * (income - 200000) / 300000
        decay_factor = max(0.7, decay_factor)
    else:
        decay_factor = 1.0
    
    cap_final = cap_base * decay_factor
    
    # 限制最低和最高
    cap_final = max(2000, min(15000, cap_final))
    
    return cap_final

def calculate_subsidy_optimized(income, contribution):
    """
    计算优化方案的精准补贴（两段式）
    """
    # 判断是否触发补贴（收入<10万）
    if income >= SUBSIDY_INCOME_HIGH:
        return 0.0
    
    # 首档上限（2%工资）
    c0 = income * 0.02
    
    # 分段计算
    if contribution <= c0:
        # 第一段
        if income < SUBSIDY_INCOME_LOW:
            # 低收入45%
            subsidy_match = contribution * SUBSIDY_RATIO_LOW
        else:
            # 中收入30%
            subsidy_match = contribution * SUBSIDY_RATIO_MID
    else:
        # 第二段：首档 + 超额
        if income < SUBSIDY_INCOME_LOW:
            tier1 = c0 * SUBSIDY_RATIO_LOW
        else:
            tier1 = c0 * SUBSIDY_RATIO_MID
        
        tier2 = (contribution - c0) * SUBSIDY_RATIO_HIGH
        subsidy_match = tier1 + tier2
    
    # 加上固定补贴
    subsidy_total = SUBSIDY_BASE + subsidy_match
    
    # 收入递减因子
    if income <= SUBSIDY_INCOME_LOW:
        taper = 1.0
    elif income < SUBSIDY_INCOME_HIGH:
        taper = (SUBSIDY_INCOME_HIGH - income) / (SUBSIDY_INCOME_HIGH - SUBSIDY_INCOME_LOW)
    else:
        taper = 0.0
    
    subsidy_final = subsidy_total * taper
    
    return subsidy_final

# ==================== 第四部分：现行政策模拟 ====================
print(f"\n{'='*80}")
print("【第四部分：现行政策模拟】")

# 初始化结果数组
results_current = []

for i in range(N_SAMPLE):
    income = incomes[i]
    contrib_rate = contrib_rates[i]
    
    # 缴费额（受12000上限约束）
    contribution_desired = income * contrib_rate
    contribution_actual = min(contribution_desired, CAP_CURRENT)
    
    # 计算T2
    t2 = calculate_t2_蓝浩歌(income, contribution_actual, years=CONTRIBUTE_YEARS)
    
    # T3固定3%
    t3 = T3_CURRENT
    
    # 无补贴
    subsidy = 0.0
    
    # 缴费期现值（税收节约）
    tax_saving_pv = 0.0
    for t in range(CONTRIBUTE_YEARS):
        income_t = income * (1 + G_WAGE_NEUTRAL) ** t
        contrib_t = contribution_actual * (1 + G_WAGE_NEUTRAL) ** t
        taxable_t = income_t - TAX_THRESHOLD
        marginal_rate = calculate_marginal_tax_rate(taxable_t)
        tax_saving_t = contrib_t * marginal_rate
        discount_factor = (1 + R_INVEST) ** t
        tax_saving_pv += tax_saving_t / discount_factor
    
    # 领取期账户余额
    account_balance = 0.0
    for t in range(CONTRIBUTE_YEARS):
        contrib_t = contribution_actual * (1 + G_WAGE_NEUTRAL) ** t
        years_to_retire = CONTRIBUTE_YEARS - t
        account_balance += contrib_t * (1 + R_INVEST) ** years_to_retire
    
    # 领取期税负现值
    annual_withdrawal = account_balance / RECEIVE_YEARS
    tax_receive_pv = 0.0
    for t in range(RECEIVE_YEARS):
        tax_t = annual_withdrawal * t3
        discount_factor = (1 + R_INVEST) ** (CONTRIBUTE_YEARS + t)
        tax_receive_pv += tax_t / discount_factor
    
    # 净收益 = 税收节约 + 补贴 - 领取期税
    net_benefit = tax_saving_pv + subsidy * CONTRIBUTE_YEARS - tax_receive_pv
    
    results_current.append({
        'income': income,
        'contribution': contribution_actual,
        'cap': CAP_CURRENT,
        't2': t2,
        't3': t3,
        'subsidy': subsidy,
        'tax_saving_pv': tax_saving_pv,
        'tax_receive_pv': tax_receive_pv,
        'net_benefit': net_benefit
    })

df_current = pd.DataFrame(results_current)

print(f"\n现行政策模拟结果:")
print(f"  平均缴费额: ¥{df_current['contribution'].mean():,.0f}")
print(f"  平均T2: {df_current['t2'].mean()*100:.2f}%")
print(f"  平均T3: {df_current['t3'].mean()*100:.2f}%")
print(f"  平均净收益: ¥{df_current['net_benefit'].mean():,.0f}")
print(f"  覆盖率: {(df_current['net_benefit'] > 0).mean()*100:.1f}%")

# ==================== 第五部分：优化方案模拟 ====================
print(f"\n{'='*80}")
print("【第五部分：优化方案模拟】")

results_optimized = []

for i in range(N_SAMPLE):
    income = incomes[i]
    contrib_rate = contrib_rates[i]
    
    # 计算个性化上限
    t2_estimate = calculate_t2_蓝浩歌(income, income * contrib_rate, years=CONTRIBUTE_YEARS)
    cap_individual = calculate_cap_optimized(income, t2_estimate)
    
    # 缴费额（受个性化上限约束）
    contribution_desired = income * contrib_rate
    contribution_actual = min(contribution_desired, cap_individual)
    
    # 重新计算T2
    t2 = calculate_t2_蓝浩歌(income, contribution_actual, years=CONTRIBUTE_YEARS)
    
    # T3双逻辑函数
    t3 = calculate_t3_dual_logistic(t2, income)
    
    # 精准补贴
    subsidy = calculate_subsidy_optimized(income, contribution_actual)
    
    # 缴费期现值（税收节约 + 补贴）
    tax_saving_pv = 0.0
    subsidy_pv = 0.0
    for t in range(CONTRIBUTE_YEARS):
        income_t = income * (1 + G_WAGE_NEUTRAL) ** t
        contrib_t = contribution_actual * (1 + G_WAGE_NEUTRAL) ** t
        taxable_t = income_t - TAX_THRESHOLD
        marginal_rate = calculate_marginal_tax_rate(taxable_t)
        tax_saving_t = contrib_t * marginal_rate
        discount_factor = (1 + R_INVEST) ** t
        tax_saving_pv += tax_saving_t / discount_factor
        subsidy_pv += subsidy / discount_factor
    
    # 领取期账户余额（含补贴）
    account_balance = 0.0
    for t in range(CONTRIBUTE_YEARS):
        contrib_t = contribution_actual * (1 + G_WAGE_NEUTRAL) ** t
        subsidy_t = subsidy
        years_to_retire = CONTRIBUTE_YEARS - t
        account_balance += (contrib_t + subsidy_t) * (1 + R_INVEST) ** years_to_retire
    
    # 领取期税负现值
    annual_withdrawal = account_balance / RECEIVE_YEARS
    tax_receive_pv = 0.0
    for t in range(RECEIVE_YEARS):
        tax_t = annual_withdrawal * t3
        discount_factor = (1 + R_INVEST) ** (CONTRIBUTE_YEARS + t)
        tax_receive_pv += tax_t / discount_factor
    
    # 净收益
    net_benefit = tax_saving_pv + subsidy_pv - tax_receive_pv
    
    results_optimized.append({
        'income': income,
        'contribution': contribution_actual,
        'cap': cap_individual,
        't2': t2,
        't3': t3,
        'subsidy': subsidy,
        'tax_saving_pv': tax_saving_pv,
        'tax_receive_pv': tax_receive_pv,
        'net_benefit': net_benefit
    })

df_optimized = pd.DataFrame(results_optimized)

print(f"\n优化方案模拟结果:")
print(f"  平均缴费额: ¥{df_optimized['contribution'].mean():,.0f}")
print(f"  平均T2: {df_optimized['t2'].mean()*100:.2f}%")
print(f"  平均T3: {df_optimized['t3'].mean()*100:.2f}%")
print(f"  平均补贴: ¥{df_optimized['subsidy'].mean():,.0f}")
print(f"  平均净收益: ¥{df_optimized['net_benefit'].mean():,.0f}")
print(f"  覆盖率: {(df_optimized['net_benefit'] > 0).mean()*100:.1f}%")

print(f"\n程序执行完成！即将生成图表...")
print("="*80)
