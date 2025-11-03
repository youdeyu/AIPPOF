"""
AI增强的缴费策略诊断模块
基于效率评分、历史数据、T2/T3分析，提供个性化优化建议
"""
import sys
import os
from typing import Dict, List, Any

# 添加父目录到路径以支持独立测试
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.subsidy_calculator import calculate_subsidy
from api.t2_calculator import calculate_t2_for_contribution
from api.cap_calculator import calculate_contribution_cap


def generate_ai_suggestions(diagnosis_result: Dict[str, Any], current_age: int) -> Dict[str, Any]:
    """
    基于诊断结果生成AI优化建议
    
    Args:
        diagnosis_result: history_diagnosis.diagnose_history() 的返回结果
        current_age: 当前年龄
        
    Returns:
        {
            'priority': 优先级 (high/medium/low),
            'suggestions': [建议列表],
            'actionPlan': {具体行动计划},
            'riskWarnings': [风险提示],
            'expectedBenefit': 预期收益
        }
    """
    score = diagnosis_result['efficiencyScore']
    t2 = diagnosis_result['cumulativeT2']
    total_subsidy = diagnosis_result['totalSubsidy']
    recommended_amount = diagnosis_result['recommendedAmount']
    potential_gain = diagnosis_result['potentialGain']
    npv_improvement = diagnosis_result['npvImprovement']
    
    hist_details = diagnosis_result['historicalDetails']
    avg_salary = hist_details['averageSalary']
    avg_contribution = hist_details['averageContribution']
    
    # 初始化建议列表
    suggestions = []
    risk_warnings = []
    action_plan = {}
    
    # ==================== 评分等级诊断 ====================
    
    if score >= 90:
        priority = 'low'
        suggestions.append({
            'type': 'maintain',
            'icon': '✅',
            'title': '保持优秀策略',
            'description': f'您的缴费效率评分{score}分,处于优秀水平。当前策略已充分利用税优和补贴,建议继续保持。',
            'action': '每年审查一次缴费额,根据收入变化微调即可'
        })
    
    elif score >= 70:
        priority = 'medium'
        suggestions.append({
            'type': 'optimize',
            'icon': '📊',
            'title': '可进一步优化',
            'description': f'您的缴费效率评分{score}分,良好但仍有提升空间。',
            'action': f'建议调整缴费额至¥{recommended_amount:,}/年,预期可提升NPV约{abs(npv_improvement):.1f}%'
        })
    
    elif score >= 50:
        priority = 'high'
        suggestions.append({
            'type': 'improve',
            'icon': '⚠️',
            'title': '需要改进策略',
            'description': f'您的缴费效率评分{score}分,存在明显优化空间。',
            'action': f'强烈建议调整缴费额至¥{recommended_amount:,}/年,可额外获得¥{potential_gain:,.0f}元收益'
        })
    
    else:
        priority = 'high'
        suggestions.append({
            'type': 'urgent',
            'icon': '🚨',
            'title': '亟需调整策略',
            'description': f'您的缴费效率评分{score}分,当前策略未能有效利用税优和补贴。',
            'action': f'请立即调整缴费额至¥{recommended_amount:,}/年,并咨询专业顾问'
        })
    
    # ==================== T2合理性诊断 ====================
    
    # T2合理区间根据年薪动态调整
    if avg_salary <= 60000:
        # 低收入：T2合理区间 0.5%-3%
        t2_low, t2_high = 0.5, 3.0
    elif avg_salary <= 120000:
        # 中等收入：T2合理区间 1%-5%
        t2_low, t2_high = 1.0, 5.0
    elif avg_salary <= 200000:
        # 中高收入：T2合理区间 5%-15% (高税率区间)
        t2_low, t2_high = 5.0, 15.0
    else:
        # 高收入：T2合理区间 10%-20% (最高税率区间)
        t2_low, t2_high = 10.0, 20.0
    
    if t2 < t2_low:
        suggestions.append({
            'type': 'tax_efficiency',
            'icon': '💰',
            'title': 'T2过低 - 税优利用不足',
            'description': f'您的累积T2仅{t2:.2f}%,低于年薪¥{avg_salary:,.0f}的合理区间({t2_low}%-{t2_high}%),税收节约效果不佳。',
            'action': '原因可能是缴费额过低或收入不匹配,建议增加缴费至最优区间'
        })
        
        # 计算建议缴费额
        if avg_salary > 0:
            optimal_contrib = min(12000, avg_salary * 0.08)
            action_plan['increaseContribution'] = {
                'from': avg_contribution,
                'to': optimal_contrib,
                'reason': '提高缴费额以充分利用税收优惠'
            }
    
    elif t2 > t2_high:
        suggestions.append({
            'type': 'tax_efficiency',
            'icon': '📉',
            'title': 'T2过高 - 可能过度缴费',
            'description': f'您的累积T2高达{t2:.2f}%,超出年薪¥{avg_salary:,.0f}的合理区间({t2_low}%-{t2_high}%),可能存在过度缴费。',
            'action': '建议减少缴费额,避免资金过度锁定'
        })
        
        action_plan['decreaseContribution'] = {
            'from': avg_contribution,
            'to': recommended_amount,
            'reason': '避免过度缴费,提高资金灵活性'
        }
    
    elif t2_low <= t2 <= t2_high:
        suggestions.append({
            'type': 'tax_efficiency',
            'icon': '✨',
            'title': 'T2处于最优区间',
            'description': f'您的累积T2为{t2:.2f}%,在年薪¥{avg_salary:,.0f}的合理区间({t2_low}%-{t2_high}%)内,税收优惠利用充分。',
            'action': '继续保持当前缴费水平'
        })
    
    # ==================== 补贴利用诊断 ====================
    
    years_count = len(hist_details['subsidyByYear'])
    avg_subsidy = total_subsidy / years_count if years_count > 0 else 0
    
    # ✅ 修正补贴计算逻辑:严格遵守150k截断点
    # 补贴公式: S = 固定补贴150 + 缴费额 × 匹配率 × 衰减系数
    # 匹配率: 低收入(≤40k)为50%, 中等收入(40k-100k)为30%
    # 衰减系数: (150,000 - 年薪) / 50,000, 年薪≥150k时为0
    
    if avg_salary >= 150000:
        # 年薪≥150k,完全无补贴
        max_possible_subsidy = 0
        suggestions.append({
            'type': 'subsidy',
            'icon': 'ℹ️',
            'title': '高收入者无补贴(年薪≥¥150k)',
            'description': f'您的年薪¥{avg_salary:,.0f}达到或超过补贴截断点(¥150,000),根据精准补贴机制不享受财政补贴。',
            'action': '您的优势在于高税率带来的税收优惠,应着重优化T2节税效果'
        })
    elif avg_salary >= 100000:
        # 100k-150k区间,线性衰减
        taper_factor = (150000 - avg_salary) / 50000
        if avg_salary <= 40000:
            match_rate = 0.50
        else:
            match_rate = 0.30
        max_possible_subsidy = 150 + 12000 * match_rate * taper_factor
        
        if avg_subsidy < max_possible_subsidy * 0.5:
            suggestions.append({
                'type': 'subsidy',
                'icon': '💸',
                'title': '补贴利用率较低(中高收入过渡区)',
                'description': f'您处于补贴衰减区(¥100k-¥150k),年均补贴¥{avg_subsidy:.0f},理论最大¥{max_possible_subsidy:.0f}(衰减系数{taper_factor:.2f})。',
                'action': f'建议调整缴费至¥{recommended_amount:,}/年以优化补贴-税优平衡'
            })
        else:
            suggestions.append({
                'type': 'subsidy',
                'icon': '🎁',
                'title': '补贴利用合理(过渡区)',
                'description': f'您处于补贴衰减区,年均获得¥{avg_subsidy:.0f}补贴,利用率{(avg_subsidy/max_possible_subsidy*100):.1f}%。',
                'action': '继续保持,关注收入变化对补贴的影响'
            })
    elif avg_salary <= 40000:
        # 低收入,50%匹配率
        max_possible_subsidy = 150 + 12000 * 0.50
        subsidy_utilization = (avg_subsidy / max_possible_subsidy) * 100
        
        if subsidy_utilization < 50:
            suggestions.append({
                'type': 'subsidy',
                'icon': '💸',
                'title': '补贴利用率低(低收入高匹配)',
                'description': f'您享受50%匹配率,但补贴利用率仅{subsidy_utilization:.1f}%,年均¥{avg_subsidy:.0f},最大可获¥{max_possible_subsidy:.0f}。',
                'action': f'建议增加缴费至¥{recommended_amount:,}/年以获取更多补贴'
            })
            action_plan['maxSubsidy'] = {
                'current': avg_subsidy,
                'potential': max_possible_subsidy,
                'gap': max_possible_subsidy - avg_subsidy
            }
        else:
            suggestions.append({
                'type': 'subsidy',
                'icon': '🎁',
                'title': '补贴利用充分(50%匹配)',
                'description': f'您享受50%高匹配率,补贴利用率{subsidy_utilization:.1f}%,年均获得¥{avg_subsidy:.0f}。',
                'action': '继续保持,充分利用低收入补贴优势'
            })
    else:
        # 中等收入(40k-100k),30%匹配率
        max_possible_subsidy = 150 + 12000 * 0.30
        subsidy_utilization = (avg_subsidy / max_possible_subsidy) * 100
        
        if subsidy_utilization < 50:
            suggestions.append({
                'type': 'subsidy',
                'icon': '💸',
                'title': '补贴利用率低(中等收入)',
                'description': f'您享受30%匹配率,补贴利用率{subsidy_utilization:.1f}%,年均¥{avg_subsidy:.0f},最大可获¥{max_possible_subsidy:.0f}。',
                'action': f'建议增加缴费至¥{recommended_amount:,}/年以获取更多补贴'
            })
            action_plan['maxSubsidy'] = {
                'current': avg_subsidy,
                'potential': max_possible_subsidy,
                'gap': max_possible_subsidy - avg_subsidy
            }
        else:
            suggestions.append({
                'type': 'subsidy',
                'icon': '🎁',
                'title': '补贴利用充分(30%匹配)',
                'description': f'您享受30%匹配率,补贴利用率{subsidy_utilization:.1f}%,年均获得¥{avg_subsidy:.0f}。',
                'action': '继续保持当前缴费水平'
            })
    
    # ==================== 缴费上限利用诊断 ====================
    
    # 计算建议缴费额对应的上限
    cap_result = calculate_contribution_cap(
        annual_salary=avg_salary,
        t2_rate=t2
    )
    
    cap_utilization = (avg_contribution / cap_result['cap']) * 100 if cap_result['cap'] > 0 else 0
    
    if cap_utilization < 40:
        suggestions.append({
            'type': 'cap_utilization',
            'icon': '📈',
            'title': '缴费上限利用率低',
            'description': f'您的缴费额仅为上限的{cap_utilization:.1f}% (¥{avg_contribution:,.0f} / ¥{cap_result["cap"]:,.0f}),仍有很大提升空间。',
            'action': '可以安全增加缴费额而不触及上限'
        })
    
    elif cap_utilization > 90:
        risk_warnings.append({
            'type': 'warning',
            'icon': '⚠️',
            'title': '接近缴费上限',
            'description': f'您的缴费已达上限的{cap_utilization:.1f}%,继续增加可能超限。',
            'action': '谨慎调整,避免超出法定上限导致超额部分无法享受优惠'
        })
    
    # ==================== 年龄阶段建议 ====================
    
    if current_age < 30:
        suggestions.append({
            'type': 'age_strategy',
            'icon': '🌱',
            'title': '青年阶段策略',
            'description': '您处于职业生涯早期,收入增长空间大。',
            'action': '建议采用渐进式缴费策略,随收入增长逐年提高缴费额,复利效应更佳'
        })
    
    elif 30 <= current_age < 45:
        suggestions.append({
            'type': 'age_strategy',
            'icon': '💼',
            'title': '中年黄金期策略',
            'description': '您处于收入高峰期,税收优惠价值最大。',
            'action': '建议最大化缴费额(在上限内),充分利用高税率下的节税效果'
        })
    
    elif 45 <= current_age < 55:
        suggestions.append({
            'type': 'age_strategy',
            'icon': '🎯',
            'title': '退休准备期策略',
            'description': '距离退休不足15年,需要平衡积累与流动性。',
            'action': '建议稳定缴费,同时关注T3领取税率,为退休后规划做准备'
        })
    
    else:
        suggestions.append({
            'type': 'age_strategy',
            'icon': '🏖️',
            'title': '临退休阶段策略',
            'description': '接近退休,应重点关注领取期规划。',
            'action': '维持当前缴费,开始研究最优领取策略以降低T3税负'
        })
    
    # ==================== 计算预期收益 ====================
    
    years_to_retirement = max(0, 60 - current_age)
    
    # 生成格式化的预期收益字符串（前端期望字符串格式）
    if potential_gain > 0:
        annual_gain = potential_gain / years_to_retirement if years_to_retirement > 0 else 0
        expected_benefit_text = (
            f"若采纳AI建议调整缴费策略，预计未来{years_to_retirement}年内可额外获得"
            f"¥{potential_gain:,.0f}元收益（年均¥{annual_gain:,.0f}），"
            f"全周期NPV提升{abs(npv_improvement):.1f}%"
        )
    else:
        expected_benefit_text = (
            f"当前缴费策略已接近最优，继续保持并关注政策变化即可。"
            f"未来{years_to_retirement}年预计稳定获益。"
        )
    
    # 同时保留结构化数据供高级分析使用
    expected_benefit_details = {
        'annualGain': potential_gain / years_to_retirement if years_to_retirement > 0 else 0,
        'lifetimeGain': potential_gain,
        'npvImprovement': npv_improvement,
        'timeHorizon': years_to_retirement
    }
    
    # ==================== 生成行动计划 ====================
    
    if not action_plan:
        action_plan = {
            'maintain': {
                'action': '保持当前策略',
                'reviewFrequency': '每年一次',
                'nextReviewDate': f'{2025 + 1}-01-01'
            }
        }
    
    # 确保所有建议都有priority字段
    for suggestion in suggestions:
        if 'priority' not in suggestion:
            # 根据type推断priority
            if suggestion.get('type') in ['urgent', 'improve']:
                suggestion['priority'] = 'high'
            elif suggestion.get('type') in ['optimize', 'tax_efficiency']:
                suggestion['priority'] = 'medium'
            else:
                suggestion['priority'] = 'low'
    
    return {
        'priority': priority,
        'suggestions': suggestions,
        'actionPlan': action_plan,
        'riskWarnings': risk_warnings,
        'expectedBenefit': expected_benefit_text,  # 前端期望的字符串格式
        'expectedBenefitDetails': expected_benefit_details,  # 结构化数据
        'summary': {
            'totalSuggestions': len(suggestions),
            'criticalIssues': len([s for s in suggestions if s.get('type') in ['urgent', 'improve']]),
            'optimizationPotential': 'high' if npv_improvement > 10 else 'medium' if npv_improvement > 5 else 'low'
        }
    }


# 测试函数
if __name__ == '__main__':
    # 模拟诊断结果
    from api.history_diagnosis import diagnose_history
    
    test_history = [
        {"year": 2022, "salary": 120000, "contribution": 8000},
        {"year": 2023, "salary": 135000, "contribution": 10000},
        {"year": 2024, "salary": 150000, "contribution": 12000}
    ]
    
    test_age = 35
    
    print("AI诊断建议测试\n" + "="*70)
    
    # 第一步：历史诊断
    diagnosis = diagnose_history(test_history, test_age)
    print(f"步骤1: 基础诊断完成")
    print(f"  效率评分: {diagnosis['efficiencyScore']}分")
    print(f"  累积T2: {diagnosis['cumulativeT2']}%")
    print(f"  累计补贴: ¥{diagnosis['totalSubsidy']:,.2f}")
    
    # 第二步：AI建议
    ai_suggestions = generate_ai_suggestions(diagnosis, test_age)
    
    print(f"\n步骤2: AI建议生成")
    print(f"  优先级: {ai_suggestions['priority'].upper()}")
    print(f"  建议数量: {ai_suggestions['summary']['totalSuggestions']}条")
    print(f"  关键问题: {ai_suggestions['summary']['criticalIssues']}个")
    print(f"  优化潜力: {ai_suggestions['summary']['optimizationPotential'].upper()}")
    
    print(f"\n详细建议:")
    for i, suggestion in enumerate(ai_suggestions['suggestions'], 1):
        print(f"\n  {i}. {suggestion['icon']} {suggestion['title']}")
        print(f"     {suggestion['description']}")
        print(f"     💡 行动: {suggestion['action']}")
    
    if ai_suggestions['riskWarnings']:
        print(f"\n⚠️  风险提示:")
        for warning in ai_suggestions['riskWarnings']:
            print(f"  {warning['icon']} {warning['title']}: {warning['description']}")
    
    print(f"\n📊 预期收益:")
    benefit = ai_suggestions['expectedBenefit']
    print(f"  年均收益: ¥{benefit['annualGain']:,.0f}")
    print(f"  终身收益: ¥{benefit['lifetimeGain']:,.0f}")
    print(f"  NPV提升: {benefit['npvImprovement']:.1f}%")
    print(f"  时间跨度: {benefit['timeHorizon']}年")
