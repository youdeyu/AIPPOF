"""
全周期可视化数据生成模块
生成缴费期（30年）和领取期（20年）的详细数据用于ECharts可视化
"""

import numpy as np
from typing import Dict, List, Any


def calculate_marginal_tax_rate(annual_salary: float) -> float:
    """
    根据年薪计算边际税率（中国个税税率表）
    """
    # 中国个税税率表（年度）
    brackets = [
        (36000, 0.03),
        (144000, 0.10),
        (300000, 0.20),
        (420000, 0.25),
        (660000, 0.30),
        (960000, 0.35),
        (float('inf'), 0.45)
    ]
    
    for threshold, rate in brackets:
        if annual_salary <= threshold:
            return rate
    return 0.45


def generate_lifecycle_data(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成全生命周期可视化数据
    
    参数:
    - age: 当前年龄
    - annualSalary: 当前年薪
    - contributionAmount: 缴费金额
    - t2: T2节税率（%）
    - t3: T3领取期税率（%）
    - wageGrowthRate: 工资增长率（%）
    
    返回:
    {
        'contributionPhase': {...},  # 缴费期数据（30年）
        'withdrawalPhase': {...},     # 领取期数据（20年）
        'summary': {...}               # 汇总统计
    }
    """
    age = params['age']
    salary = params['annualSalary']
    contribution = params['contributionAmount']
    t2 = params['t2'] / 100  # 转换为小数
    t3 = params['t3'] / 100
    wage_growth = params['wageGrowthRate'] / 100
    
    # 常量
    retirement_age = 60
    investment_return = 0.0175  # 1.75%
    subsidy_alpha1 = 0.24
    subsidy_alpha2 = 50
    
    # 缴费期年限
    contribution_years = retirement_age - age
    
    # ==================== 缴费期数据（30年） ====================
    contribution_phase = {
        'years': [],
        'ages': [],
        'salaries': [],
        'contributions': [],
        'taxSavings': [],
        'subsidies': [],
        'accountBalance': [],
        'cumulativeBenefit': []
    }
    
    account_balance = 0
    cumulative_benefit = 0
    
    for year in range(contribution_years):
        current_age = age + year
        current_salary = salary * ((1 + wage_growth) ** year)
        
        # 计算当年缴费额（可以根据收入动态调整）
        current_contribution = min(contribution, 12000, current_salary * 0.12)
        
        # 计算税收节省：ΔT = 缴费额 × 边际税率
        marginal_rate = calculate_marginal_tax_rate(current_salary)
        tax_saving = current_contribution * marginal_rate
        
        # 计算补贴：S = α1 × 缴费额 + α2
        subsidy = subsidy_alpha1 * current_contribution + subsidy_alpha2
        
        # 账户余额增长：本金 + 投资收益
        account_balance = account_balance * (1 + investment_return) + current_contribution
        
        # 累计收益 = 税收节省 + 补贴
        cumulative_benefit += (tax_saving + subsidy)
        
        contribution_phase['years'].append(2024 + year)
        contribution_phase['ages'].append(current_age)
        contribution_phase['salaries'].append(round(current_salary, 2))
        contribution_phase['contributions'].append(round(current_contribution, 2))
        contribution_phase['taxSavings'].append(round(tax_saving, 2))
        contribution_phase['subsidies'].append(round(subsidy, 2))
        contribution_phase['accountBalance'].append(round(account_balance, 2))
        contribution_phase['cumulativeBenefit'].append(round(cumulative_benefit, 2))
    
    # ==================== 领取期数据（20年） ====================
    withdrawal_years = 20
    withdrawal_phase = {
        'years': [],
        'ages': [],
        'withdrawalAmounts': [],
        'taxes': [],
        'netIncome': [],
        'accountBalance': []
    }
    
    # 计算年度领取金额（账户余额/20年）
    annual_withdrawal = account_balance / withdrawal_years
    
    for year in range(withdrawal_years):
        current_age = retirement_age + year
        
        # 计算领取税：领取额 × T3税率
        withdrawal_tax = annual_withdrawal * t3
        net_income = annual_withdrawal - withdrawal_tax
        
        # 账户余额递减
        account_balance -= annual_withdrawal
        
        withdrawal_phase['years'].append(2024 + contribution_years + year)
        withdrawal_phase['ages'].append(current_age)
        withdrawal_phase['withdrawalAmounts'].append(round(annual_withdrawal, 2))
        withdrawal_phase['taxes'].append(round(withdrawal_tax, 2))
        withdrawal_phase['netIncome'].append(round(net_income, 2))
        withdrawal_phase['accountBalance'].append(round(max(0, account_balance), 2))
    
    # ==================== 汇总统计 ====================
    total_contribution = sum(contribution_phase['contributions'])
    total_tax_savings = sum(contribution_phase['taxSavings'])
    total_subsidies = sum(contribution_phase['subsidies'])
    total_withdrawal_tax = sum(withdrawal_phase['taxes'])
    
    final_account = contribution_phase['accountBalance'][-1] if contribution_phase['accountBalance'] else 0
    total_net_income = sum(withdrawal_phase['netIncome'])
    
    # NPV计算
    npv = total_tax_savings + total_subsidies - total_withdrawal_tax
    
    summary = {
        'contributionPhase': {
            'years': contribution_years,
            'totalContribution': round(total_contribution, 2),
            'totalTaxSavings': round(total_tax_savings, 2),
            'totalSubsidies': round(total_subsidies, 2),
            'finalAccountBalance': round(final_account, 2)
        },
        'withdrawalPhase': {
            'years': withdrawal_years,
            'totalWithdrawal': round(final_account, 2),
            'totalTax': round(total_withdrawal_tax, 2),
            'totalNetIncome': round(total_net_income, 2)
        },
        'overall': {
            'npv': round(npv, 2),
            'roi': round((npv / total_contribution * 100) if total_contribution > 0 else 0, 2),
            'averageAnnualBenefit': round(npv / (contribution_years + withdrawal_years), 2)
        }
    }
    
    return {
        'contributionPhase': contribution_phase,
        'withdrawalPhase': withdrawal_phase,
        'summary': summary,
        'success': True
    }


def generate_comparison_scenarios(base_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    生成对比场景：不同缴费额的全周期对比
    
    返回:
    {
        'scenarios': [
            {'name': '¥4,000/年', 'data': {...}},
            {'name': '¥8,000/年', 'data': {...}},
            {'name': '¥12,000/年（推荐）', 'data': {...}}
        ]
    }
    """
    scenarios = []
    contribution_amounts = [4000, 8000, 12000]
    
    for amount in contribution_amounts:
        params = base_params.copy()
        params['contributionAmount'] = amount
        
        # 重新计算T2（可能随缴费额变化）
        # 这里简化处理，实际应调用T2计算模块
        
        data = generate_lifecycle_data(params)
        
        scenario_name = f'¥{amount:,}/年'
        if amount == 12000:
            scenario_name += '（推荐）'
        
        scenarios.append({
            'name': scenario_name,
            'amount': amount,
            'data': data
        })
    
    return {
        'scenarios': scenarios,
        'success': True
    }


def calculate_sensitivity_analysis(base_params: Dict[str, Any]) -> Dict[str, Any]:
    """
    敏感性分析：分析关键参数变化对NPV的影响
    
    分析维度：
    1. 工资增长率（2% ~ 6%）
    2. T3税率（0.5% ~ 3%）
    3. 投资回报率（1% ~ 3%）
    """
    sensitivity_data = {
        'wageGrowth': {'x': [], 'y': []},
        't3Rate': {'x': [], 'y': []},
        'investmentReturn': {'x': [], 'y': []}
    }
    
    # 1. 工资增长率敏感性
    for g in np.linspace(2, 6, 9):
        params = base_params.copy()
        params['wageGrowthRate'] = g
        result = generate_lifecycle_data(params)
        sensitivity_data['wageGrowth']['x'].append(round(g, 1))
        sensitivity_data['wageGrowth']['y'].append(result['summary']['overall']['npv'])
    
    # 2. T3税率敏感性
    for t3 in np.linspace(0.5, 3, 9):
        params = base_params.copy()
        params['t3'] = t3
        result = generate_lifecycle_data(params)
        sensitivity_data['t3Rate']['x'].append(round(t3, 1))
        sensitivity_data['t3Rate']['y'].append(result['summary']['overall']['npv'])
    
    return {
        'sensitivity': sensitivity_data,
        'success': True
    }


if __name__ == '__main__':
    # 测试数据生成
    test_params = {
        'age': 30,
        'annualSalary': 150000,
        'contributionAmount': 9500,
        't2': 1.4,
        't3': 1.2,
        'wageGrowthRate': 3.9
    }
    
    print("=== 测试全周期数据生成 ===")
    result = generate_lifecycle_data(test_params)
    print(f"缴费期总年数: {result['summary']['contributionPhase']['years']}")
    print(f"总缴费额: ¥{result['summary']['contributionPhase']['totalContribution']:,.2f}")
    print(f"总税收节省: ¥{result['summary']['contributionPhase']['totalTaxSavings']:,.2f}")
    print(f"总补贴: ¥{result['summary']['contributionPhase']['totalSubsidies']:,.2f}")
    print(f"退休账户余额: ¥{result['summary']['contributionPhase']['finalAccountBalance']:,.2f}")
    print(f"领取期总税负: ¥{result['summary']['withdrawalPhase']['totalTax']:,.2f}")
    print(f"总NPV: ¥{result['summary']['overall']['npv']:,.2f}")
    print(f"ROI: {result['summary']['overall']['roi']}%")
    
    print("\n=== 测试对比场景 ===")
    comparison = generate_comparison_scenarios(test_params)
    for scenario in comparison['scenarios']:
        print(f"{scenario['name']}: NPV = ¥{scenario['data']['summary']['overall']['npv']:,.2f}")
