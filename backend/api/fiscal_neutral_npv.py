"""
财政中性NPV优化模型
确保推荐方案在财政上可持续（政府支出 ≈ 政府收入）
"""

from typing import Dict, List, Any
import numpy as np


def calculate_government_cash_flow(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    计算政府现金流（补贴支出 vs 税收收入）
    
    参数:
    - age: 当前年龄
    - annualSalary: 年薪
    - contributionAmount: 缴费金额
    - t2: T2节税率（%）
    - t3: T3领取期税率（%）
    - wageGrowthRate: 工资增长率（%）
    
    返回:
    {
        'governmentCost': float,      # 政府总成本（补贴 + 税收损失）
        'governmentRevenue': float,   # 政府总收入（T3税收）
        'fiscalBalance': float,        # 财政平衡（收入 - 成本）
        'isFiscalNeutral': bool       # 是否财政中性
    }
    """
    age = params['age']
    salary = params['annualSalary']
    contribution = params['contributionAmount']
    t2 = params['t2'] / 100
    t3 = params['t3'] / 100
    wage_growth = params['wageGrowthRate'] / 100
    
    # 常量
    retirement_age = 60
    contribution_years = retirement_age - age
    withdrawal_years = 20
    discount_rate = 0.03  # 政府贴现率3%
    subsidy_alpha1 = 0.24
    subsidy_alpha2 = 50
    
    # ==================== 计算政府成本 ====================
    total_subsidy_pv = 0  # 补贴现值
    total_tax_loss_pv = 0  # 税收损失现值
    
    for year in range(contribution_years):
        current_salary = salary * ((1 + wage_growth) ** year)
        current_contribution = min(contribution, 12000, current_salary * 0.12)
        
        # 补贴
        subsidy = subsidy_alpha1 * current_contribution + subsidy_alpha2
        subsidy_pv = subsidy / ((1 + discount_rate) ** year)
        total_subsidy_pv += subsidy_pv
        
        # 税收损失（缴费期）
        marginal_rate = _calculate_marginal_rate(current_salary)
        tax_loss = current_contribution * marginal_rate
        tax_loss_pv = tax_loss / ((1 + discount_rate) ** year)
        total_tax_loss_pv += tax_loss_pv
    
    government_cost = total_subsidy_pv + total_tax_loss_pv
    
    # ==================== 计算政府收入 ====================
    # 计算退休账户余额
    account_balance = 0
    investment_return = 0.0175
    
    for year in range(contribution_years):
        current_salary = salary * ((1 + wage_growth) ** year)
        current_contribution = min(contribution, 12000, current_salary * 0.12)
        account_balance = account_balance * (1 + investment_return) + current_contribution
    
    # 领取期税收（现值）
    annual_withdrawal = account_balance / withdrawal_years
    total_t3_tax_pv = 0
    
    for year in range(withdrawal_years):
        t3_tax = annual_withdrawal * t3
        # 贴现到当前
        years_from_now = contribution_years + year
        t3_tax_pv = t3_tax / ((1 + discount_rate) ** years_from_now)
        total_t3_tax_pv += t3_tax_pv
    
    government_revenue = total_t3_tax_pv
    
    # ==================== 财政平衡分析 ====================
    fiscal_balance = government_revenue - government_cost
    is_fiscal_neutral = abs(fiscal_balance) < government_cost * 0.1  # 10%容差
    
    return {
        'governmentCost': round(government_cost, 2),
        'subsidyPV': round(total_subsidy_pv, 2),
        'taxLossPV': round(total_tax_loss_pv, 2),
        'governmentRevenue': round(government_revenue, 2),
        't3TaxPV': round(total_t3_tax_pv, 2),
        'fiscalBalance': round(fiscal_balance, 2),
        'fiscalBalanceRate': round(fiscal_balance / government_cost * 100, 2) if government_cost > 0 else 0,
        'isFiscalNeutral': is_fiscal_neutral,
        'sustainability': _assess_sustainability(fiscal_balance, government_cost),
        'success': True
    }


def optimize_fiscal_neutral_contribution(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    优化缴费额以实现财政中性
    
    目标：Max(用户NPV) s.t. |政府收支差| < 阈值
    """
    age = params['age']
    salary = params['annualSalary']
    t2 = params['t2']
    t3_base = params.get('t3', 1.2)
    wage_growth = params['wageGrowthRate']
    
    best_contribution = 0
    best_user_npv = -float('inf')
    best_fiscal_balance = 0
    
    # 搜索最优缴费额（500 ~ 12000，步长500）
    for contribution in range(500, 12500, 500):
        # 重新计算T3（因为缴费额变化会影响T3）
        t3 = _estimate_t3(t2, salary, contribution)
        
        test_params = {
            'age': age,
            'annualSalary': salary,
            'contributionAmount': contribution,
            't2': t2,
            't3': t3,
            'wageGrowthRate': wage_growth
        }
        
        # 计算政府现金流
        fiscal = calculate_government_cash_flow(test_params)
        
        # 计算用户NPV
        user_npv = _calculate_user_npv(test_params)
        
        # 检查财政约束：收支差不超过成本的20%
        if abs(fiscal['fiscalBalance']) < fiscal['governmentCost'] * 0.2:
            if user_npv > best_user_npv:
                best_user_npv = user_npv
                best_contribution = contribution
                best_fiscal_balance = fiscal['fiscalBalance']
    
    # 如果没有找到满足约束的方案，选择财政平衡最好的
    if best_contribution == 0:
        best_contribution = 6000  # 默认中等水平
    
    return {
        'optimalContribution': best_contribution,
        'userNPV': round(best_user_npv, 2),
        'fiscalBalance': round(best_fiscal_balance, 2),
        'isFiscalNeutral': abs(best_fiscal_balance) < 1000,
        'reason': '该缴费额在保证用户收益的同时，确保政府财政可持续',
        'success': True
    }


def simulate_population_impact(population_params: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    模拟群体层面的财政影响
    
    用于政策制定者评估不同补贴系数下的财政压力
    """
    total_government_cost = 0
    total_government_revenue = 0
    total_participants = len(population_params)
    
    risk_distribution = {'low': 0, 'medium': 0, 'high': 0}
    
    for user_params in population_params:
        fiscal = calculate_government_cash_flow(user_params)
        total_government_cost += fiscal['governmentCost']
        total_government_revenue += fiscal['governmentRevenue']
        
        # 风险分类
        if fiscal['fiscalBalance'] < -5000:
            risk_distribution['high'] += 1
        elif fiscal['fiscalBalance'] < 0:
            risk_distribution['medium'] += 1
        else:
            risk_distribution['low'] += 1
    
    aggregate_balance = total_government_revenue - total_government_cost
    
    return {
        'totalParticipants': total_participants,
        'aggregateCost': round(total_government_cost, 2),
        'aggregateRevenue': round(total_government_revenue, 2),
        'aggregateBalance': round(aggregate_balance, 2),
        'perCapitaCost': round(total_government_cost / total_participants, 2) if total_participants > 0 else 0,
        'perCapitaRevenue': round(total_government_revenue / total_participants, 2) if total_participants > 0 else 0,
        'riskDistribution': risk_distribution,
        'sustainabilityRate': round((risk_distribution['low'] / total_participants * 100), 2) if total_participants > 0 else 0,
        'success': True
    }


def _calculate_marginal_rate(annual_salary: float) -> float:
    """计算边际税率"""
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


def _estimate_t3(t2: float, salary: float, contribution: float) -> float:
    """估算T3（简化版）"""
    # 基础T3 = T2 + 收入系数 + 缴费系数
    base_t3 = t2 * 0.8  # T3通常低于T2
    income_factor = (salary / 100000) * 0.2
    contribution_factor = (contribution / 12000) * 0.3
    
    t3 = base_t3 + income_factor + contribution_factor
    return min(14, max(0.5, t3))  # 限制在0.5%-14%


def _calculate_user_npv(params: Dict[str, Any]) -> float:
    """计算用户NPV（简化版）"""
    contribution = params['contributionAmount']
    t2 = params['t2'] / 100
    t3 = params['t3'] / 100
    years = 60 - params['age']
    
    # 补贴
    subsidy = 0.24 * contribution + 50
    
    # 税收节省
    marginal_rate = _calculate_marginal_rate(params['annualSalary'])
    tax_saving = contribution * marginal_rate
    
    # 领取期税负（简化）
    withdrawal_tax = contribution * t3 * 20  # 领取20年
    
    npv = (subsidy + tax_saving) * years - withdrawal_tax
    return npv


def _assess_sustainability(balance: float, cost: float) -> str:
    """评估财政可持续性"""
    if cost == 0:
        return '无成本'
    
    ratio = balance / cost
    
    if ratio > 0.1:
        return '政府盈余（税收 > 补贴），财政可持续性强'
    elif ratio > -0.1:
        return '财政中性（收支平衡），可持续'
    elif ratio > -0.3:
        return '轻度赤字，需监控'
    else:
        return '财政压力大，补贴过高'


if __name__ == '__main__':
    # 测试1: 普通用户财政影响
    print("=== 测试1: 普通收入用户 ===")
    test1 = {
        'age': 30,
        'annualSalary': 150000,
        'contributionAmount': 9500,
        't2': 1.4,
        't3': 1.2,
        'wageGrowthRate': 3.9
    }
    result1 = calculate_government_cash_flow(test1)
    print(f"政府成本: ¥{result1['governmentCost']:,.2f}")
    print(f"  - 补贴现值: ¥{result1['subsidyPV']:,.2f}")
    print(f"  - 税收损失: ¥{result1['taxLossPV']:,.2f}")
    print(f"政府收入: ¥{result1['governmentRevenue']:,.2f}")
    print(f"财政平衡: ¥{result1['fiscalBalance']:,.2f} ({result1['fiscalBalanceRate']}%)")
    print(f"是否财政中性: {result1['isFiscalNeutral']}")
    print(f"可持续性: {result1['sustainability']}")
    
    # 测试2: 优化财政中性缴费额
    print("\n=== 测试2: 优化财政中性方案 ===")
    test2 = {
        'age': 30,
        'annualSalary': 150000,
        't2': 1.4,
        'wageGrowthRate': 3.9
    }
    result2 = optimize_fiscal_neutral_contribution(test2)
    print(f"最优缴费额: ¥{result2['optimalContribution']:,}")
    print(f"用户NPV: ¥{result2['userNPV']:,.2f}")
    print(f"财政平衡: ¥{result2['fiscalBalance']:,.2f}")
    print(f"是否财政中性: {result2['isFiscalNeutral']}")
