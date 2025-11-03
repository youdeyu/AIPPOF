"""
推荐缴费额优化模块
基于NPV最大化、补贴最大化、规避边际递减的综合优化
整合混合动态上限模型（公式5-5）
"""
import numpy as np

try:
    from .t2_calculator import calculate_t2_for_contribution
    from .cap_calculator import calculate_contribution_cap
except ImportError:
    from t2_calculator import calculate_t2_for_contribution
    from cap_calculator import calculate_contribution_cap


def calculate_subsidy(contribution, annual_salary):
    """
    计算财政补贴
    
    补贴公式:
    - 基础补贴: 150元
    - 缴费匹配补贴:
      * 收入 <= 40,000: 30%
      * 40,000 < 收入 <= 100,000: 线性递减 (30% -> 6%)
      * 收入 > 100,000: 6%
    
    Args:
        contribution: 缴费额
        annual_salary: 年薪
        
    Returns:
        float: 补贴金额
    """
    base_subsidy = 150
    
    if annual_salary <= 40000:
        match_rate = 0.30
    elif annual_salary <= 100000:
        # 线性递减: y = 0.30 - (0.24 * (x - 40000) / 60000)
        taper = (annual_salary - 40000) / 60000
        match_rate = 0.30 - (0.24 * taper)
    else:
        match_rate = 0.06
    
    match_subsidy = contribution * match_rate
    total_subsidy = base_subsidy + match_subsidy
    
    return round(total_subsidy, 2)


def calculate_tax_save(contribution, t2):
    """
    计算税收节省
    
    Args:
        contribution: 缴费额
        t2: 平均节税率 (%)
        
    Returns:
        float: 税收节省金额
    """
    return round(contribution * (t2 / 100), 2)


def optimize_contribution(age, annual_salary, t2, t3, wage_growth_rate):
    """
    优化推荐缴费额 - 返回3个推荐方案（整合混合动态上限）
    
    核心改进：
    1. 使用混合动态上限模型（公式5-5）计算个性化上限
    2. 为每个方案计算真实T2（基于实际缴费额）
    3. 返回3个最优方案（而非5个）
    4. 提供详细推荐理由
    
    Args:
        age: 年龄
        annual_salary: 年薪
        t2: T2节税率 (%)（用于上限计算）
        t3: T3领取期税率 (%)
        wage_growth_rate: 工资增长率 (%)
        
    Returns:
        dict: 包含3个推荐方案的优化结果
    """
    # **核心改进1**: 计算个性化缴费上限（混合动态模型）
    cap_result = calculate_contribution_cap(annual_salary, t2)
    personal_cap = min(cap_result['cap'], 12000)  # 当前系统最高12000元
    
    # 缴费额候选范围（500到个性化上限，步长500）
    max_candidate = int(min(personal_cap, 12000))
    candidates = np.arange(500, max_candidate + 1, 500)
    
    # 如果上限不是500的倍数，添加上限值
    if max_candidate not in candidates and max_candidate >= 500:
        candidates = np.append(candidates, max_candidate)
    
    # 存储所有候选方案
    all_scenarios = []
    
    # 遍历所有候选缴费额
    for contrib in candidates:
        # 计算年度补贴
        subsidy = calculate_subsidy(contrib, annual_salary)
        
        # **核心改进2**: 计算此缴费额对应的真实T2
        t2_result = calculate_t2_for_contribution(annual_salary, contrib)
        real_t2 = t2_result['t2']
        
        # 计算年度税收节省（使用真实T2）
        tax_save = calculate_tax_save(contrib, real_t2)
        
        # 估算T3税负（假设账户余额按1.75%增长）
        n = 60 - age  # 缴费年限
        r = 0.0175    # 账户收益率
        
        # 账户余额估算（简化为等额缴费）
        account_balance = contrib * ((1 + r) ** n - 1) / r
        
        # 领取期总税负估算（20年领取期）
        withdrawal_years = 20
        annual_withdrawal = account_balance / withdrawal_years
        annual_t3_tax = annual_withdrawal * (t3 / 100)
        total_t3_tax = annual_t3_tax * withdrawal_years
        
        # 贴现到现在（简化处理）
        discount_rate = 0.03
        discounted_t3_tax = total_t3_tax / ((1 + discount_rate) ** n)
        
        # 计算NPV（30年缴费期 + 贴现后的T3税负）
        npv_contribution = (subsidy + tax_save) * n - discounted_t3_tax
        
        # 检查是否在补贴递减区间（避免过度缴费）
        if 40000 < annual_salary <= 100000:
            # 在递减区间，适当降低高缴费额的评分
            if contrib > 10000:
                npv_contribution *= 0.95
        
        # 存储此方案
        all_scenarios.append({
            'contribution': int(contrib),
            'subsidy': round(subsidy, 2),
            'taxSave': round(tax_save, 2),
            'npv': round(npv_contribution, 2),
            'accountBalance': round(account_balance, 2),
            'predictedT2': round(real_t2, 2),  # 真实T2
            'taxSaving': t2_result['taxSaving']
        })
    
    # 按NPV排序，获取前3个最优方案
    all_scenarios.sort(key=lambda x: x['npv'], reverse=True)
    top_scenarios = all_scenarios[:3]  # **改为3个方案**
    
    # **核心改进3**: 为每个方案生成详细推荐理由
    for idx, scenario in enumerate(top_scenarios):
        contrib = scenario['contribution']
        subsidy = scenario['subsidy']
        npv = scenario['npv']
        pred_t2 = scenario['predictedT2']
        
        reasons = []
        
        if idx == 0:
            # 方案1: NPV最大化
            reasons.append(f"🏆 NPV最大化：全生命周期净收益¥{npv:,.0f}元，为所有方案中最高")
            reasons.append(f"💰 高节税效率：T2节税率{pred_t2:.1f}%，年省税¥{scenario['taxSave']:,.0f}元")
            reasons.append(f"🎁 补贴奖励：每年获补贴¥{subsidy:,.0f}元，{60-age}年累计¥{subsidy*(60-age):,.0f}元")
            reasons.append(f"✅ 在您的个性化上限¥{personal_cap:,.0f}元内，合规安全")
        elif idx == 1:
            # 方案2: 平衡方案
            reasons.append(f"⚖️ 收益与流动性平衡：NPV¥{npv:,.0f}元，兼顾长期收益与短期可支配")
            reasons.append(f"💡 适中缴费：缴费额¥{contrib:,.0f}元，不会过度占用现金流")
            reasons.append(f"📈 稳健节税：T2={pred_t2:.1f}%，持续享受税收优惠")
            reasons.append(f"🎯 适合稳健型投资者，风险与收益兼顾")
        else:
            # 方案3: 保守方案
            reasons.append(f"🛡️ 保守低压力：缴费额¥{contrib:,.0f}元，减轻财务负担")
            reasons.append(f"💵 高补贴率：补贴占缴费比{(subsidy/contrib*100):.1f}%，财政支持明显")
            reasons.append(f"🌱 灵活起步：先以较低额度参与，未来可根据收入调整")
            reasons.append(f"👍 适合初次参与或收入波动较大的人群")
        
        scenario['reasons'] = reasons
        scenario['label'] = ['NPV最优', '平衡方案', '保守方案'][idx]
    
    # 返回结构（包含上限信息）
    best_scenario = top_scenarios[0]
    
    return {
        'recommendedAmount': best_scenario['contribution'],
        'subsidy': best_scenario['subsidy'],
        'taxSave': best_scenario['taxSave'],
        'npvOptimized': best_scenario['npv'],
        'reasons': best_scenario['reasons'],
        'scenarios': top_scenarios,  # 3个推荐方案
        'cap': {  # 新增：上限信息
            'personalCap': int(personal_cap),
            'strategy': cap_result['strategy'],
            'formula': cap_result['formula'],
            'details': cap_result.get('details', {})
        },
        'details': {
            'contributionYears': 60 - age,
            'withdrawalYears': 20,
            'estimatedAccountBalance': best_scenario['accountBalance'],
            't2': t2,
            't3': t3,
            'wageGrowthRate': wage_growth_rate
        }
    }


# 测试函数
if __name__ == '__main__':
    # 测试用例
    test_cases = [
        {
            'age': 30,
            'annual_salary': 150000,
            't2': 1.4,
            't3': 1.2,
            'wage_growth_rate': 3.9
        },
        {
            'age': 25,
            'annual_salary': 80000,
            't2': 2.0,
            't3': 1.5,
            'wage_growth_rate': 5.0
        },
        {
            'age': 40,
            'annual_salary': 300000,
            't2': 3.5,
            't3': 4.2,
            'wage_growth_rate': 3.0
        }
    ]
    
    print("推荐缴费额优化测试\n" + "="*70)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n{'='*70}")
        print(f"测试用例 {i}:")
        print(f"输入: 年龄={case['age']}, 年薪={case['annual_salary']}, T2={case['t2']}%, T3={case['t3']}%")
        result = optimize_contribution(**case)
        print(f"\n推荐缴费额: ¥{result['recommendedAmount']}")
        print(f"年度补贴: ¥{result['subsidy']}")
        print(f"年度税收节省: ¥{result['taxSave']}")
        print(f"优化NPV: ¥{result['npvOptimized']:.2f}")
        
        # 打印所有方案的T2
        print(f"\n所有推荐方案（含预测T2）:")
        print(f"{'方案':<6} {'缴费额':<10} {'T2(%)':<10} {'补贴':<10} {'NPV':<12}")
        print("-" * 60)
        for idx, scenario in enumerate(result['scenarios'], 1):
            print(f"{idx:<6} ¥{scenario['contribution']:<9} "
                  f"{scenario.get('predictedT2', 'N/A'):<10} "
                  f"¥{scenario['subsidy']:<9} "
                  f"¥{scenario['npv']:<11.2f}")
        print(f"\n推荐理由:")
        for j, reason in enumerate(result['reasons'], 1):
            print(f"  {j}. {reason}")
