"""
T2平均节税率计算模块
实现蓝浩歌模型核心公式: T2 = 节税额 / 缴费额
"""
import math


# 中国个人所得税税率表（综合所得年度税率）
TAX_BRACKETS = [
    (36000, 0.03),      # 0-36,000: 3%
    (144000, 0.10),     # 36,000-144,000: 10%
    (300000, 0.20),     # 144,000-300,000: 20%
    (420000, 0.25),     # 300,000-420,000: 25%
    (660000, 0.30),     # 420,000-660,000: 30%
    (960000, 0.35),     # 660,000-960,000: 35%
    (float('inf'), 0.45) # 960,000以上: 45%
]


def get_marginal_tax_rate(annual_salary):
    """
    根据年薪计算边际税率 t1
    
    Args:
        annual_salary: 年薪（税前）
        
    Returns:
        float: 边际税率 (%)
    """
    # 减去基本扣除额60,000元
    taxable_income = max(0, annual_salary - 60000)
    
    for threshold, rate in TAX_BRACKETS:
        if taxable_income <= threshold:
            return rate * 100  # 转换为百分比
    
    return 45.0  # 默认最高税率


def calculate_tax_from_taxable_income(taxable_income):
    """
    根据应纳税所得额计算个人所得税（超额累进）
    
    Args:
        taxable_income: 应纳税所得额
        
    Returns:
        float: 应纳税额
    """
    if taxable_income <= 0:
        return 0
    
    # 使用超额累进税率表计算
    accumulated_tax = 0
    remaining_income = taxable_income
    
    prev_threshold = 0
    for threshold, rate in TAX_BRACKETS:
        if threshold == float('inf'):
            # 最高档：剩余全部收入
            accumulated_tax += remaining_income * rate
            break
        else:
            # 计算本档应税金额
            bracket_width = threshold - prev_threshold
            taxable_in_bracket = min(remaining_income, bracket_width)
            accumulated_tax += taxable_in_bracket * rate
            remaining_income -= taxable_in_bracket
            prev_threshold = threshold
        
        if remaining_income <= 0:
            break
    
    return accumulated_tax


def calculate_t2_for_contribution(annual_salary, contribution_amount):
    """
    根据缴费额计算对应的T2平均节税率（蓝浩歌模型核心公式）
    
    平均节税率 T2 = 节税额 / 缴费额
    
    其中：
    - 节税额 = 不缴养老金的税 - 缴养老金后的税
    - 缴费额 = 个人养老金缴费金额
    
    Args:
        annual_salary: 年薪（税前）
        contribution_amount: 缴费额
        
    Returns:
        dict: 包含T2及详细信息
    """
    # 确保缴费不超过上限12000
    contribution_amount = min(contribution_amount, 12000)
    
    if contribution_amount == 0:
        return {
            't2': 0,
            'taxSaving': 0,
            'realCost': 0,
            'marginalRate': get_marginal_tax_rate(annual_salary),
            'details': {
                'contributionAmount': 0,
                'taxNoPension': 0,
                'taxWithPension': 0,
                'taxableNoPension': 0,
                'taxableWithPension': 0
            }
        }
    
    # 场景1：不缴养老金
    taxable_no_pension = max(0, annual_salary - 60000)
    tax_no_pension = calculate_tax_from_taxable_income(taxable_no_pension)
    
    # 场景2：缴纳养老金（税前扣除）
    taxable_with_pension = max(0, annual_salary - 60000 - contribution_amount)
    tax_with_pension = calculate_tax_from_taxable_income(taxable_with_pension)
    
    # 节税额
    tax_saving = tax_no_pension - tax_with_pension
    
    # 平均节税率（核心指标）
    t2 = (tax_saving / contribution_amount * 100) if contribution_amount > 0 else 0
    
    # 边际税率
    marginal_rate = get_marginal_tax_rate(annual_salary) 
    
    # 实际成本
    real_cost = contribution_amount - tax_saving
    
    return {
        't2': round(t2, 2),
        'taxSaving': round(tax_saving, 2),
        'realCost': round(real_cost, 2),
        'marginalRate': round(marginal_rate, 1),
        'details': {
            'contributionAmount': contribution_amount,
            'taxNoPension': round(tax_no_pension, 2),
            'taxWithPension': round(tax_with_pension, 2),
            'taxableNoPension': taxable_no_pension,
            'taxableWithPension': taxable_with_pension
        }
    }


def calculate_t2(age, annual_salary, wage_growth_rate):
    """
    计算T2平均节税率（简化版，假设固定缴费12000）
    
    此函数为兼容旧代码保留，新代码应使用calculate_t2_for_contribution
    
    Args:
        age: 当前年龄
        annual_salary: 年薪
        wage_growth_rate: 工资增长率 (%)
        
    Returns:
        dict: 计算结果
    """
    # 参数验证
    if age < 18 or age >= 60:
        raise ValueError("年龄必须在18-59之间")
    
    if annual_salary <= 0:
        raise ValueError("年薪必须大于0")
    
    if wage_growth_rate < 0:
        raise ValueError("工资增长率不能为负")
    
    # 使用12000元作为默认缴费额计算T2
    result = calculate_t2_for_contribution(annual_salary, 12000)
    t2 = result['t2']
    t1 = result['marginalRate']
    
    # 计算缴费年限 n（到60岁退休）
    n = 60 - age
    
    # 养老金账户收益率 r
    r = 1.75
    
    return {
        't2': round(t2, 2),
        't1': round(t1, 1),
        'n': n,
        'formula': f"T2 = {result['taxSaving']:.2f} / 12000 * 100% = {t2:.2f}%",
        'details': {
            'contributionYears': n,
            'returnRate': r,
            'wageGrowthRate': wage_growth_rate,
            'marginalTaxRate': round(t1, 1),
            'taxableIncome': annual_salary - 60000,
            'taxSaving': result['taxSaving'],
            'formula': f"T2 = {result['taxSaving']:.2f} / 12000 * 100% = {t2:.2f}%"
        }
    }


# 测试函数
if __name__ == '__main__':
    # 测试用例1：测试不同缴费额的T2
    print("="*70)
    print("测试用例1：不同缴费额对T2的影响")
    print("="*70)
    
    annual_salary = 150000
    contributions = [6000, 8000, 10000, 12000]
    
    print(f"\n年薪: ¥{annual_salary:,}")
    print(f"{'缴费额':<10} {'T2 (%)':<10} {'节税额':<12} {'实际成本':<12} {'边际税率 (%)'}")
    print("-" * 70)
    
    for contrib in contributions:
        result = calculate_t2_for_contribution(annual_salary, contrib)
        print(f"¥{contrib:<9,} {result['t2']:<10.2f} ¥{result['taxSaving']:<11.2f} "
              f"¥{result['realCost']:<11.2f} {result['marginalRate']:<10.1f}")
    
    # 测试用例2：不同收入水平的T2
    print("\n" + "="*70)
    print("测试用例2：不同收入水平对T2的影响（固定缴费¥12,000）")
    print("="*70)
    
    salaries = [80000, 150000, 300000, 500000]
    
    print(f"\n{'年薪':<12} {'T2 (%)':<10} {'节税额':<12} {'实际成本':<12} {'边际税率 (%)'}")
    print("-" * 70)
    
    for salary in salaries:
        result = calculate_t2_for_contribution(salary, 12000)
        print(f"¥{salary:<11,} {result['t2']:<10.2f} ¥{result['taxSaving']:<11.2f} "
              f"¥{result['realCost']:<11.2f} {result['marginalRate']:<10.1f}")
    
    # 测试用例3：验证与旧函数的兼容性
    print("\n" + "="*70)
    print("测试用例3：验证calculate_t2()函数兼容性")
    print("="*70)
    
    test_cases = [
        {'age': 30, 'annual_salary': 150000, 'wage_growth_rate': 3.9},
        {'age': 25, 'annual_salary': 80000, 'wage_growth_rate': 5.0},
        {'age': 40, 'annual_salary': 300000, 'wage_growth_rate': 3.0},
    ]
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n测试 {i}: 年龄={case['age']}, 年薪=¥{case['annual_salary']:,}, "
              f"增长率={case['wage_growth_rate']}%")
        result = calculate_t2(**case)
        print(f"T2 = {result['t2']}%")
        print(f"边际税率 t1 = {result['t1']}%")
        print(f"缴费年限 n = {result['n']}年")
        print(f"公式: {result['details']['formula']}")
