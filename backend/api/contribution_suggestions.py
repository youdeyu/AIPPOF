"""
5档缴费方案建议模块
基于AI预测和当前状态,生成保守/稳健/均衡/积极/激进五档缴费方案
每档方案包含NPV对比、风险评估、适用人群
"""
import sys
import os
from typing import Dict, List, Any

# 添加父目录到路径以支持独立测试
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.subsidy_calculator import calculate_subsidy
from api.t2_calculator import calculate_t2_for_contribution
from api.t3_calculator import calculate_t3
from api.cap_calculator import calculate_contribution_cap


def calculate_npv_simple(
    annual_contribution: float,
    annual_salary: float,
    t2_rate: float,
    t3_rate: float,
    current_age: int,
    wage_growth_rate: float = 3.5,
    discount_rate: float = 3.0
) -> Dict[str, float]:
    """
    简化NPV计算（用于快速方案对比）
    
    Args:
        annual_contribution: 年缴费额
        annual_salary: 当前年薪
        t2_rate: T2税率 (%)
        t3_rate: T3税率 (%)
        current_age: 当前年龄
        wage_growth_rate: 工资增长率 (%)
        discount_rate: 折现率 (%)
        
    Returns:
        {
            'contribution_phase_npv': 缴费期NPV,
            'withdrawal_phase_npv': 领取期NPV,
            'total_npv': 总NPV,
            'total_contribution': 累计缴费,
            'total_subsidy': 累计补贴,
            'total_tax_save': 累计税收节约
        }
    """
    # 缴费期: current_age -> 60岁
    years_to_retirement = max(0, 60 - current_age)
    
    total_contribution = 0
    total_subsidy = 0
    total_tax_save = 0
    contribution_npv = 0
    
    salary = annual_salary
    for year in range(years_to_retirement):
        # 计算当年补贴
        subsidy_result = calculate_subsidy(salary, annual_contribution)
        subsidy = subsidy_result['subsidy']
        
        # 计算当年税收节约
        tax_save = annual_contribution * (t2_rate / 100)
        
        # 折现到当前
        discount_factor = (1 + discount_rate/100) ** year
        contribution_npv += (subsidy + tax_save) / discount_factor
        
        total_contribution += annual_contribution
        total_subsidy += subsidy
        total_tax_save += tax_save
        
        # 工资增长
        salary *= (1 + wage_growth_rate/100)
    
    # 领取期: 60岁 -> 80岁
    withdrawal_years = 20
    total_accumulated = total_contribution  # 简化:忽略投资收益
    
    annual_withdrawal = total_accumulated / withdrawal_years
    withdrawal_tax_per_year = annual_withdrawal * (t3_rate / 100)
    
    withdrawal_npv = 0
    for year in range(withdrawal_years):
        discount_factor = (1 + discount_rate/100) ** (years_to_retirement + year)
        withdrawal_npv -= withdrawal_tax_per_year / discount_factor
    
    total_npv = contribution_npv + withdrawal_npv
    
    return {
        'contribution_phase_npv': round(contribution_npv, 2),
        'withdrawal_phase_npv': round(withdrawal_npv, 2),
        'total_npv': round(total_npv, 2),
        'total_contribution': round(total_contribution, 2),
        'total_subsidy': round(total_subsidy, 2),
        'total_tax_save': round(total_tax_save, 2),
        'years_to_retirement': years_to_retirement
    }


def generate_5tier_suggestions(
    current_salary: float,
    current_age: int,
    current_contribution: float = None,
    t2_rate: float = None,
    wage_growth_rate: float = 3.5
) -> Dict[str, Any]:
    """
    生成5档缴费方案建议
    
    Args:
        current_salary: 当前年薪
        current_age: 当前年龄
        current_contribution: 当前缴费额（可选）
        t2_rate: 当前T2税率（可选）
        wage_growth_rate: 工资增长率预测
        
    Returns:
        {
            'tiers': [5档方案列表],
            'recommended': 推荐档位,
            'comparison': 对比分析
        }
    """
    # 计算缴费上限
    if t2_rate is None:
        # 估算T2（基于收入）
        if current_salary <= 60000:
            t2_rate = 3.0
        elif current_salary <= 120000:
            t2_rate = 10.0
        elif current_salary <= 200000:
            t2_rate = 15.0
        else:
            t2_rate = 20.0
    
    cap_result = calculate_contribution_cap(current_salary, t2_rate)
    max_cap = cap_result['cap']
    
    # 计算T3（估算）
    t3_result = calculate_t3(t2_rate, current_salary, current_age)
    t3_rate = t3_result['t3']
    
    # 定义5档方案
    tiers = []
    
    # 1. 保守型 (Conservative) - 30%上限
    conservative_amount = max_cap * 0.30  # 移除固定6000上限，使用动态上限
    conservative_npv = calculate_npv_simple(
        conservative_amount, current_salary, t2_rate, t3_rate,
        current_age, wage_growth_rate
    )
    tiers.append({
        'tier': 'conservative',
        'name': '保守型',
        'icon': '🛡️',
        'contribution': round(conservative_amount, 0),
        'cap_utilization': round((conservative_amount / max_cap) * 100, 1),
        'npv': conservative_npv,
        'characteristics': [
            '低风险、低收益',
            '资金灵活性高',
            '适合收入不稳定者'
        ],
        'suitable_for': '初入职场、收入波动大、对养老金第三支柱不太了解的人群',
        'risk_level': 'low',
        'annual_benefit': round(conservative_npv['total_npv'] / conservative_npv['years_to_retirement'], 0) if conservative_npv['years_to_retirement'] > 0 else 0
    })
    
    # 2. 稳健型 (Stable) - 50%上限
    stable_amount = max_cap * 0.50  # 移除固定8000上限，使用动态上限
    stable_npv = calculate_npv_simple(
        stable_amount, current_salary, t2_rate, t3_rate,
        current_age, wage_growth_rate
    )
    tiers.append({
        'tier': 'stable',
        'name': '稳健型',
        'icon': '📊',
        'contribution': round(stable_amount, 0),
        'cap_utilization': round((stable_amount / max_cap) * 100, 1),
        'npv': stable_npv,
        'characteristics': [
            '中低风险、稳定收益',
            '平衡补贴与税优',
            '适合普通工薪族'
        ],
        'suitable_for': '收入稳定、追求长期稳健增值、对风险偏保守的中产阶层',
        'risk_level': 'low-medium',
        'annual_benefit': round(stable_npv['total_npv'] / stable_npv['years_to_retirement'], 0) if stable_npv['years_to_retirement'] > 0 else 0
    })
    
    # 3. 均衡型 (Balanced) - 70%上限 (推荐)
    balanced_amount = max_cap * 0.70  # 移除固定9500上限，使用动态上限
    balanced_npv = calculate_npv_simple(
        balanced_amount, current_salary, t2_rate, t3_rate,
        current_age, wage_growth_rate
    )
    tiers.append({
        'tier': 'balanced',
        'name': '均衡型',
        'icon': '⚖️',
        'contribution': round(balanced_amount, 0),
        'cap_utilization': round((balanced_amount / max_cap) * 100, 1),
        'npv': balanced_npv,
        'characteristics': [
            '中等风险、较高收益',
            '充分利用补贴和税优',
            '风险收益最优平衡'
        ],
        'suitable_for': '【推荐】大多数参与者的最佳选择，收入中等偏上、追求性价比',
        'risk_level': 'medium',
        'annual_benefit': round(balanced_npv['total_npv'] / balanced_npv['years_to_retirement'], 0) if balanced_npv['years_to_retirement'] > 0 else 0,
        'recommended': True
    })
    
    # 4. 积极型 (Aggressive) - 85%上限
    aggressive_amount = max_cap * 0.85  # 移除固定11000上限，使用动态上限
    aggressive_npv = calculate_npv_simple(
        aggressive_amount, current_salary, t2_rate, t3_rate,
        current_age, wage_growth_rate
    )
    tiers.append({
        'tier': 'aggressive',
        'name': '积极型',
        'icon': '📈',
        'contribution': round(aggressive_amount, 0),
        'cap_utilization': round((aggressive_amount / max_cap) * 100, 1),
        'npv': aggressive_npv,
        'characteristics': [
            '中高风险、高收益',
            '最大化税收优惠',
            '适合高收入群体'
        ],
        'suitable_for': '高收入、税率高、追求最大节税效果、资金充裕的人群',
        'risk_level': 'medium-high',
        'annual_benefit': round(aggressive_npv['total_npv'] / aggressive_npv['years_to_retirement'], 0) if aggressive_npv['years_to_retirement'] > 0 else 0
    })
    
    # 5. 激进型 (Maximum) - 95%上限
    maximum_amount = max_cap * 0.95  # 已经使用动态上限的95%
    maximum_npv = calculate_npv_simple(
        maximum_amount, current_salary, t2_rate, t3_rate,
        current_age, wage_growth_rate
    )
    tiers.append({
        'tier': 'maximum',
        'name': '激进型',
        'icon': '🚀',
        'contribution': round(maximum_amount, 0),
        'cap_utilization': round((maximum_amount / max_cap) * 100, 1),
        'npv': maximum_npv,
        'characteristics': [
            '高风险、最高收益',
            '接近上限边界',
            '资金锁定度高'
        ],
        'suitable_for': '超高收入、追求极致节税、退休储蓄意识强、资金非常充裕者',
        'risk_level': 'high',
        'annual_benefit': round(maximum_npv['total_npv'] / maximum_npv['years_to_retirement'], 0) if maximum_npv['years_to_retirement'] > 0 else 0
    })
    
    # 对比分析
    npv_values = [tier['npv']['total_npv'] for tier in tiers]
    best_npv_tier = tiers[npv_values.index(max(npv_values))]
    
    # 如果有当前缴费额,计算相对提升
    current_tier_name = None
    if current_contribution:
        for tier in tiers:
            if abs(tier['contribution'] - current_contribution) < 1000:
                current_tier_name = tier['name']
                break
    
    comparison = {
        'best_npv_tier': best_npv_tier['tier'],
        'best_npv_value': best_npv_tier['npv']['total_npv'],
        'npv_range': {
            'min': min(npv_values),
            'max': max(npv_values),
            'spread': max(npv_values) - min(npv_values)
        },
        'current_tier': current_tier_name,
        'contribution_range': {
            'min': tiers[0]['contribution'],
            'max': tiers[-1]['contribution'],
            'recommended': tiers[2]['contribution']  # 均衡型
        }
    }
    
    # 规范化字段名 - 添加驼峰式别名
    for tier in tiers:
        tier['riskLevel'] = tier.get('risk_level', 'low')
        tier['capUtilization'] = tier.get('cap_utilization', 0)
        tier['annualBenefit'] = tier.get('annual_benefit', 0)
        tier['suitableFor'] = tier.get('suitable_for', '')
    
    return {
        'tiers': tiers,
        'recommended': 'balanced',  # 默认推荐均衡型
        'comparison': comparison,
        'parameters': {
            'current_salary': current_salary,
            'current_age': current_age,
            'max_cap': max_cap,
            't2_rate': t2_rate,
            't3_rate': t3_rate,
            'wage_growth_rate': wage_growth_rate
        }
    }


# 测试函数
if __name__ == '__main__':
    print("="*70)
    print("5档缴费方案建议测试")
    print("="*70)
    
    # 测试场景1: 中等收入,35岁
    print("\n📊 场景1: 中等收入参与者")
    print("-"*70)
    result1 = generate_5tier_suggestions(
        current_salary=120000,
        current_age=35,
        current_contribution=8000,
        wage_growth_rate=4.0
    )
    
    print(f"当前状况: 年薪¥{result1['parameters']['current_salary']:,}, {result1['parameters']['current_age']}岁")
    print(f"上限: ¥{result1['parameters']['max_cap']:,.0f}, T2={result1['parameters']['t2_rate']:.1f}%, T3={result1['parameters']['t3_rate']:.2f}%")
    print(f"\n推荐档位: {result1['recommended'].upper()}")
    
    print(f"\n{'档位':<12} {'缴费额':<12} {'上限利用率':<12} {'年均收益':<12} {'总NPV':<12} {'风险等级'}")
    print("-"*70)
    for tier in result1['tiers']:
        is_recommended = '★' if tier.get('recommended', False) else ' '
        print(f"{is_recommended} {tier['icon']} {tier['name']:<8} "
              f"¥{tier['contribution']:<10,.0f} {tier['cap_utilization']:<10.1f}% "
              f"¥{tier['annual_benefit']:<10,.0f} ¥{tier['npv']['total_npv']:<10,.0f} "
              f"{tier['risk_level']}")
    
    print(f"\n对比分析:")
    print(f"  NPV最高档位: {result1['comparison']['best_npv_tier'].upper()} (¥{result1['comparison']['best_npv_value']:,.0f})")
    print(f"  NPV范围: ¥{result1['comparison']['npv_range']['min']:,.0f} ~ ¥{result1['comparison']['npv_range']['max']:,.0f}")
    print(f"  差距: ¥{result1['comparison']['npv_range']['spread']:,.0f}")
    
    # 测试场景2: 高收入,45岁
    print("\n" + "="*70)
    print("📊 场景2: 高收入参与者")
    print("-"*70)
    result2 = generate_5tier_suggestions(
        current_salary=250000,
        current_age=45,
        wage_growth_rate=3.0
    )
    
    print(f"当前状况: 年薪¥{result2['parameters']['current_salary']:,}, {result2['parameters']['current_age']}岁")
    print(f"上限: ¥{result2['parameters']['max_cap']:,.0f}")
    
    print(f"\n{'档位':<12} {'缴费额':<12} {'累计补贴':<12} {'累计节税':<12} {'总NPV'}")
    print("-"*70)
    for tier in result2['tiers']:
        is_recommended = '★' if tier.get('recommended', False) else ' '
        print(f"{is_recommended} {tier['icon']} {tier['name']:<8} "
              f"¥{tier['contribution']:<10,.0f} "
              f"¥{tier['npv']['total_subsidy']:<10,.0f} "
              f"¥{tier['npv']['total_tax_save']:<10,.0f} "
              f"¥{tier['npv']['total_npv']:<10,.0f}")
    
    print("\n" + "="*70)
    print("详细方案特征（均衡型 - 推荐）:")
    print("="*70)
    balanced = [t for t in result1['tiers'] if t['tier'] == 'balanced'][0]
    print(f"\n{balanced['icon']} {balanced['name']}")
    print(f"  缴费额: ¥{balanced['contribution']:,.0f}/年")
    print(f"  上限利用率: {balanced['cap_utilization']:.1f}%")
    print(f"  风险等级: {balanced['risk_level']}")
    print(f"\n  特点:")
    for char in balanced['characteristics']:
        print(f"    • {char}")
    print(f"\n  适合人群:")
    print(f"    {balanced['suitable_for']}")
    print(f"\n  预期收益:")
    print(f"    总NPV: ¥{balanced['npv']['total_npv']:,.0f}")
    print(f"    累计补贴: ¥{balanced['npv']['total_subsidy']:,.0f}")
    print(f"    累计节税: ¥{balanced['npv']['total_tax_save']:,.0f}")
    print(f"    年均收益: ¥{balanced['annual_benefit']:,.0f}")
