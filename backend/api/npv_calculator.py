"""
NPV净现值计算模块
计算公式: NPV = Σ(补贴S + 税收节省ΔT1) - 领取期税负T3
"""
import numpy as np


def calculate_npv(age, annual_salary, contribution_amount, t2, t3, wage_growth_rate):
    """
    计算全生命周期净现值NPV
    
    NPV = 缴费期收益NPV - 领取期税负NPV
    
    缴费期收益 = 每年补贴 + 每年税收节省
    领取期税负 = 每年领取金额 * T3税率
    
    Args:
        age: 当前年龄
        annual_salary: 当前年薪
        contribution_amount: 缴费额
        t2: T2节税率 (%)
        t3: T3领取期税率 (%)
        wage_growth_rate: 工资增长率 (%)
        
    Returns:
        dict: NPV计算结果
    """
    # 基本参数
    contribution_years = 60 - age  # 缴费年限
    withdrawal_years = 20          # 领取年限（假设60-80岁）
    account_return_rate = 0.0175   # 账户收益率 1.75%
    discount_rate = 0.03           # 贴现率 3%
    
    # ==================== 缴费期计算 ====================
    
    total_subsidy = 0
    total_tax_save = 0
    contribution_phase_npv = 0
    
    current_salary = annual_salary
    
    for year in range(contribution_years):
        # 计算当年补贴
        if current_salary <= 40000:
            match_rate = 0.30
        elif current_salary <= 100000:
            taper = (current_salary - 40000) / 60000
            match_rate = 0.30 - (0.24 * taper)
        else:
            match_rate = 0.06
        
        annual_subsidy = 150 + contribution_amount * match_rate
        
        # 计算当年税收节省
        annual_tax_save = contribution_amount * (t2 / 100)
        
        # 当年总收益
        annual_benefit = annual_subsidy + annual_tax_save
        
        # 贴现到现在
        present_value = annual_benefit / ((1 + discount_rate) ** year)
        contribution_phase_npv += present_value
        
        # 累计总额
        total_subsidy += annual_subsidy
        total_tax_save += annual_tax_save
        
        # 更新下一年工资
        current_salary *= (1 + wage_growth_rate / 100)
    
    # ==================== 账户余额计算 ====================
    
    # 假设等额缴费，计算60岁时账户余额
    # FV = C * [(1+r)^n - 1] / r
    account_balance = contribution_amount * (((1 + account_return_rate) ** contribution_years - 1) / account_return_rate)
    
    # ==================== 领取期计算 ====================
    
    # 每年领取金额（平均分配）
    annual_withdrawal = account_balance / withdrawal_years
    
    # 每年T3税负
    annual_t3_tax = annual_withdrawal * (t3 / 100)
    
    # 总T3税负
    total_t3_tax = 0
    for year in range(withdrawal_years):
        # 贴现到现在（从第contribution_years年开始）
        present_value = annual_t3_tax / ((1 + discount_rate) ** (contribution_years + year))
        total_t3_tax += present_value
    
    # ==================== 计算NPV ====================
    
    npv = contribution_phase_npv - total_t3_tax
    
    # ==================== 对比维持现状（0缴费或固定4000元） ====================
    
    # 计算固定4000元缴费的NPV作为对比
    comparison_contribution = 4000
    comparison_npv = 0
    comparison_salary = annual_salary
    
    for year in range(contribution_years):
        if comparison_salary <= 40000:
            match_rate = 0.30
        elif comparison_salary <= 100000:
            taper = (comparison_salary - 40000) / 60000
            match_rate = 0.30 - (0.24 * taper)
        else:
            match_rate = 0.06
        
        comp_subsidy = 150 + comparison_contribution * match_rate
        comp_tax_save = comparison_contribution * (t2 / 100)
        comp_benefit = comp_subsidy + comp_tax_save
        
        comparison_npv += comp_benefit / ((1 + discount_rate) ** year)
        comparison_salary *= (1 + wage_growth_rate / 100)
    
    # 对比方案的T3税负
    comp_balance = comparison_contribution * (((1 + account_return_rate) ** contribution_years - 1) / account_return_rate)
    comp_withdrawal = comp_balance / withdrawal_years
    comp_t3_tax = 0
    
    for year in range(withdrawal_years):
        annual_comp_tax = comp_withdrawal * (t3 / 100)
        comp_t3_tax += annual_comp_tax / ((1 + discount_rate) ** (contribution_years + year))
    
    comparison_npv -= comp_t3_tax
    
    # NPV差异
    npv_advantage = npv - comparison_npv
    
    return {
        'npv': round(npv, 2),
        'totalSubsidy': round(total_subsidy, 2),
        'totalTaxSave': round(total_tax_save, 2),
        'totalT3Tax': round(total_t3_tax * withdrawal_years, 2),  # 名义总额（未贴现）
        'accountBalance': round(account_balance, 2),
        'annualWithdrawal': round(annual_withdrawal, 2),
        'breakdown': {
            'contributionPhaseNPV': round(contribution_phase_npv, 2),
            'withdrawalPhaseCost': round(total_t3_tax, 2),
            'netNPV': round(npv, 2)
        },
        'comparison': {
            'comparisonAmount': comparison_contribution,
            'comparisonNPV': round(comparison_npv, 2),
            'npvAdvantage': round(npv_advantage, 2),
            'percentageGain': round((npv_advantage / max(comparison_npv, 1)) * 100, 2)
        },
        'details': {
            'contributionYears': contribution_years,
            'withdrawalYears': withdrawal_years,
            'accountReturnRate': account_return_rate * 100,
            'discountRate': discount_rate * 100
        }
    }


# 测试函数
if __name__ == '__main__':
    # 测试用例
    test_case = {
        'age': 30,
        'annual_salary': 150000,
        'contribution_amount': 9500,
        't2': 1.4,
        't3': 1.2,
        'wage_growth_rate': 3.9
    }
    
    print("NPV净现值计算测试\n" + "="*70)
    print(f"输入参数:")
    print(f"  年龄: {test_case['age']}")
    print(f"  年薪: ¥{test_case['annual_salary']:,}")
    print(f"  缴费额: ¥{test_case['contribution_amount']:,}")
    print(f"  T2: {test_case['t2']}%")
    print(f"  T3: {test_case['t3']}%")
    print(f"  工资增长率: {test_case['wage_growth_rate']}%")
    
    result = calculate_npv(**test_case)
    
    print(f"\n计算结果:")
    print(f"  全生命周期NPV: ¥{result['npv']:,.2f}")
    print(f"  30年累计补贴: ¥{result['totalSubsidy']:,.2f}")
    print(f"  30年累计税收节省: ¥{result['totalTaxSave']:,.2f}")
    print(f"  20年领取期税负: ¥{result['totalT3Tax']:,.2f}")
    print(f"  60岁账户余额: ¥{result['accountBalance']:,.2f}")
    print(f"  年领取金额: ¥{result['annualWithdrawal']:,.2f}")
    
    print(f"\n与固定4000元缴费对比:")
    print(f"  对比方案NPV: ¥{result['comparison']['comparisonNPV']:,.2f}")
    print(f"  NPV优势: ¥{result['comparison']['npvAdvantage']:,.2f}")
    print(f"  提升比例: {result['comparison']['percentageGain']}%")
