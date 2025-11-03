"""
高收入群体T3风险监测模块
识别高风险用户并提供预警
"""

from typing import Dict, List, Any
import math


def assess_t3_risk(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    评估T3税率风险
    
    参数:
    - annualSalary: 年薪
    - t2: T2节税率（%）
    - t3: T3领取期税率（%）
    - contributionAmount: 缴费金额
    - age: 当前年龄
    
    返回:
    {
        'riskLevel': 'low' | 'medium' | 'high' | 'critical',
        'riskScore': 0-100,
        'warnings': [...],
        'recommendations': [...],
        'isHighRisk': bool
    }
    """
    salary = params['annualSalary']
    t2 = params['t2']
    t3 = params['t3']
    contribution = params['contributionAmount']
    age = params['age']
    
    risk_factors = []
    warnings = []
    recommendations = []
    risk_score = 0
    
    # ==================== 风险因素1: T3税率过高 ====================
    if t3 >= 12:
        risk_factors.append('t3_critical')
        risk_score += 40
        warnings.append({
            'type': 'critical',
            'message': f'领取期税率高达{t3}%，超过临界值12%，可能导致净收益为负',
            'impact': '严重影响退休后实际收入'
        })
        recommendations.append({
            'priority': 'high',
            'action': '建议降低缴费额至¥6,000以下，避免T3税率过高',
            'expectedEffect': f'可将T3降至约{max(0.5, t3 * 0.6):.1f}%'
        })
    elif t3 >= 8:
        risk_factors.append('t3_high')
        risk_score += 25
        warnings.append({
            'type': 'warning',
            'message': f'领取期税率为{t3}%，处于较高水平（8%-12%）',
            'impact': '中等风险，建议优化缴费策略'
        })
        recommendations.append({
            'priority': 'medium',
            'action': '建议适度降低缴费额或分散投资',
            'expectedEffect': f'优化后可降至{max(0.5, t3 * 0.75):.1f}%左右'
        })
    elif t3 >= 3:
        risk_factors.append('t3_moderate')
        risk_score += 10
        warnings.append({
            'type': 'info',
            'message': f'领取期税率为{t3}%，处于合理区间（3%-8%）',
            'impact': '风险可控，继续监测'
        })
    
    # ==================== 风险因素2: 高收入高缴费 ====================
    if salary >= 500000 and contribution >= 10000:
        risk_factors.append('high_income_high_contribution')
        risk_score += 20
        warnings.append({
            'type': 'warning',
            'message': '年薪超50万且缴费额超¥10,000，属于高收入高缴费群体',
            'impact': '退休后领取金额大，可能触发高T3税率'
        })
        recommendations.append({
            'priority': 'medium',
            'action': '考虑分散养老投资：个人养老金 + 商业保险 + 其他理财',
            'expectedEffect': '降低单一账户集中度，规避高税率风险'
        })
    
    # ==================== 风险因素3: T2-T3税率倒挂 ====================
    if t3 > t2:
        tax_inversion = t3 - t2
        risk_factors.append('tax_inversion')
        risk_score += 15
        warnings.append({
            'type': 'critical',
            'message': f'税率倒挂：领取期税率({t3}%)高于缴费期节税率({t2}%)',
            'impact': f'净税负增加{tax_inversion:.1f}%，存在亏损风险'
        })
        recommendations.append({
            'priority': 'high',
            'action': '紧急调整缴费策略，降低缴费额以平衡T2和T3',
            'expectedEffect': '避免"交税反而更多"的情况'
        })
    
    # ==================== 风险因素4: 年轻人过度缴费 ====================
    if age < 35 and contribution > salary * 0.10:
        risk_factors.append('young_overcontribution')
        risk_score += 12
        warnings.append({
            'type': 'info',
            'message': f'{age}岁缴费占收入比例{contribution/salary*100:.1f}%，可能过度锁定流动性',
            'impact': '养老金要到60岁才能领取，可能影响短期财务灵活性'
        })
        recommendations.append({
            'priority': 'low',
            'action': '年轻人建议平衡养老储蓄与短期投资',
            'expectedEffect': '保留更多流动资金用于购房、教育等需求'
        })
    
    # ==================== 风险因素5: 缴费额接近上限 ====================
    if contribution >= 11000:
        risk_factors.append('near_cap')
        risk_score += 8
        warnings.append({
            'type': 'info',
            'message': f'缴费额¥{contribution:,}接近年度上限¥12,000',
            'impact': '已充分利用税收优惠，但需注意领取期税负'
        })
    
    # ==================== 计算综合风险等级 ====================
    if risk_score >= 60:
        risk_level = 'critical'
        risk_label = '高危'
        risk_color = '#ef4444'
    elif risk_score >= 35:
        risk_level = 'high'
        risk_label = '较高'
        risk_color = '#f97316'
    elif risk_score >= 15:
        risk_level = 'medium'
        risk_label = '中等'
        risk_color = '#eab308'
    else:
        risk_level = 'low'
        risk_label = '低'
        risk_color = '#22c55e'
    
    # ==================== 计算退出概率（基于T3） ====================
    # 使用逻辑回归模型预测退出概率
    # P(退出) = 1 / (1 + e^(-β0 - β1*t3))
    # 假设 β0=-3, β1=0.5 (基于理论假设，实际需用真实数据拟合)
    exit_probability = 1 / (1 + math.exp(-(-3 + 0.5 * t3)))
    
    return {
        'riskLevel': risk_level,
        'riskLabel': risk_label,
        'riskColor': risk_color,
        'riskScore': min(100, risk_score),
        'riskFactors': risk_factors,
        'warnings': warnings,
        'recommendations': recommendations,
        'isHighRisk': risk_level in ['high', 'critical'],
        'exitProbability': round(exit_probability * 100, 2),
        'monitoring': {
            't2': t2,
            't3': t3,
            'taxGap': round(t3 - t2, 2),
            'contributionRatio': round(contribution / salary * 100, 2)
        },
        'success': True
    }


def batch_risk_screening(users: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    批量筛选高风险用户
    
    用于后台监测系统，识别需要干预的用户
    """
    high_risk_users = []
    risk_distribution = {'low': 0, 'medium': 0, 'high': 0, 'critical': 0}
    
    for user in users:
        assessment = assess_t3_risk(user)
        risk_distribution[assessment['riskLevel']] += 1
        
        if assessment['isHighRisk']:
            high_risk_users.append({
                'userId': user.get('userId', 'unknown'),
                'salary': user['annualSalary'],
                't3': user['t3'],
                'riskLevel': assessment['riskLevel'],
                'riskScore': assessment['riskScore'],
                'exitProbability': assessment['exitProbability']
            })
    
    # 按风险评分排序
    high_risk_users.sort(key=lambda x: x['riskScore'], reverse=True)
    
    return {
        'totalUsers': len(users),
        'highRiskUsers': high_risk_users,
        'highRiskCount': len(high_risk_users),
        'riskDistribution': risk_distribution,
        'highRiskRate': round(len(high_risk_users) / len(users) * 100, 2) if users else 0,
        'success': True
    }


def calculate_optimal_cap(params: Dict[str, Any]) -> Dict[str, Any]:
    """
    计算最优缴费上限（避免T3风险）
    
    目标：找到使 NPV > 0 且 T3 <= 3% 的最大缴费额
    """
    salary = params['annualSalary']
    t2 = params['t2']
    age = params['age']
    
    # 简化算法：根据收入水平设定安全上限
    if salary >= 1000000:
        safe_cap = 6000  # 百万年薪，保守缴费
        reason = '超高收入群体，需严格控制T3风险'
    elif salary >= 500000:
        safe_cap = 8000  # 50万年薪，适度缴费
        reason = '高收入群体，平衡税收优惠与T3税负'
    elif salary >= 200000:
        safe_cap = 10000  # 20万年薪，积极缴费
        reason = '中高收入群体，充分利用税收优惠'
    else:
        safe_cap = 12000  # 普通收入，上限缴费
        reason = '普通收入群体，T3风险较低'
    
    return {
        'optimalCap': safe_cap,
        'reason': reason,
        'estimatedT3': round(0.5 + (salary / 100000) * 0.3, 1),  # 简化估算
        'safetyMargin': 12000 - safe_cap,
        'success': True
    }


if __name__ == '__main__':
    # 测试1: 低风险用户
    print("=== 测试1: 普通收入用户 ===")
    test1 = {
        'annualSalary': 150000,
        't2': 1.4,
        't3': 1.2,
        'contributionAmount': 9500,
        'age': 30
    }
    result1 = assess_t3_risk(test1)
    print(f"风险等级: {result1['riskLabel']} ({result1['riskScore']}分)")
    print(f"退出概率: {result1['exitProbability']}%")
    print(f"警告数量: {len(result1['warnings'])}")
    
    # 测试2: 高风险用户
    print("\n=== 测试2: 高收入高T3用户 ===")
    test2 = {
        'annualSalary': 600000,
        't2': 8.0,
        't3': 12.5,
        'contributionAmount': 12000,
        'age': 45
    }
    result2 = assess_t3_risk(test2)
    print(f"风险等级: {result2['riskLabel']} ({result2['riskScore']}分)")
    print(f"退出概率: {result2['exitProbability']}%")
    print(f"警告数量: {len(result2['warnings'])}")
    for warning in result2['warnings']:
        print(f"  - [{warning['type']}] {warning['message']}")
    
    # 测试3: 税率倒挂
    print("\n=== 测试3: 税率倒挂用户 ===")
    test3 = {
        'annualSalary': 80000,
        't2': 0.8,
        't3': 2.5,
        'contributionAmount': 12000,
        'age': 28
    }
    result3 = assess_t3_risk(test3)
    print(f"风险等级: {result3['riskLabel']} ({result3['riskScore']}分)")
    print(f"税率倒挂: T3({result3['monitoring']['t3']}%) > T2({result3['monitoring']['t2']}%)")
