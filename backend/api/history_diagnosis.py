"""
历史数据诊断模块
解析历史缴费记录，计算累积T2，诊断缴费效率
"""
import sys
import os

# 添加父目录到路径以支持独立测试
if __name__ == '__main__':
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.t2_calculator import calculate_t2, get_marginal_tax_rate, calculate_t2_for_contribution
from api.t3_calculator import calculate_t3
from api.subsidy_calculator import calculate_subsidy  # 使用正确的补贴计算器
from api.cap_calculator import calculate_contribution_cap  # 动态上限计算器


def diagnose_history(history_data, age):
    """
    诊断历史缴费数据
    
    Args:
        history_data: 历史数据列表
            [
                {"year": 2022, "salary": 120000, "contribution": 8000},
                {"year": 2023, "salary": 135000, "contribution": 10000},
                ...
            ]
        age: 当前年龄
        
    Returns:
        dict: 诊断结果
    """
    if not history_data or len(history_data) == 0:
        raise ValueError("历史数据不能为空")
    
    # 排序历史数据（按年份）
    sorted_data = sorted(history_data, key=lambda x: x['year'])
    
    # ==================== 数据验证和清洗（使用动态上限） ====================
    
    cap_warnings = []  # 存储上限警告
    for record in sorted_data:
        salary = record['salary']
        contribution = record['contribution']
        year = record['year']
        
        # 先计算该年的T2（用于确定动态上限）
        temp_t2_result = calculate_t2_for_contribution(salary, contribution)
        temp_t2 = temp_t2_result['t2']
        
        # 计算该年薪和T2对应的动态上限
        cap_result = calculate_contribution_cap(
            annual_salary=salary,
            t2_rate=temp_t2
        )
        dynamic_cap = cap_result['cap']  # 修复字段名：使用'cap'而非'recommended_cap'
        
        # 检查是否超出动态上限
        if contribution > dynamic_cap:
            cap_warnings.append({
                'year': year,
                'salary': salary,
                'contribution': contribution,
                'dynamic_cap': dynamic_cap,
                'excess': contribution - dynamic_cap
            })
            print(f"⚠️ {year}年: 缴费¥{contribution:,}超出动态上限¥{dynamic_cap:,.0f} (超出¥{contribution - dynamic_cap:,.0f})")
    
    # ==================== 计算累积加权平均T2 ====================
    
    total_weighted_t2 = 0
    total_contribution = 0
    t2_values = []
    
    for record in sorted_data:
        salary = record['salary']
        contribution = record['contribution']
        year = record['year']
        
        # ✅ 使用蓝浩歌公式：T2 = 实际税收节约 / 缴费额
        t2_result = calculate_t2_for_contribution(salary, contribution)
        t2_year = t2_result['t2']  # 这是真实的税收节约率(已经是百分比)
        
        t2_values.append({
            'year': year,
            't2': round(t2_year, 2),
            'contribution': contribution,
            'salary': salary
        })
        
        # 加权累加
        total_weighted_t2 += t2_year * contribution
        total_contribution += contribution
    
    # 累积加权平均T2
    if total_contribution > 0:
        cumulative_t2 = total_weighted_t2 / total_contribution
    else:
        cumulative_t2 = 0
    
    # ==================== 计算总补贴及每年明细 ====================
    
    total_subsidy = 0
    subsidy_by_year = []
    for record in sorted_data:
        # 调用正确的补贴计算器（参数顺序：salary, contribution）
        subsidy_result = calculate_subsidy(record['salary'], record['contribution'])
        subsidy_amount = subsidy_result['subsidy']
        total_subsidy += subsidy_amount
        subsidy_by_year.append({
            'year': record['year'],
            'subsidy': round(subsidy_amount, 2),
            'contribution': record['contribution'],
            'salary': record['salary']
        })
    
    # ==================== 效率评分（0-100分） ====================
    
    # 评分标准（根据年薪动态调整）:
    # 1. T2合理性（40分）: T2应该在合理区间内（区间根据年薪动态调整）
    # 2. 缴费额合理性（30分）: 不过度缴费，不缴费不足
    # 3. 补贴利用率（30分）: 充分利用补贴（高收入无补贴改为T3优化评分）
    
    score = 0
    
    # 计算平均值
    avg_contribution = total_contribution / len(sorted_data)
    avg_salary = sum(r['salary'] for r in sorted_data) / len(sorted_data)
    
    # 1. T2合理性评分（根据年薪动态调整）
    if avg_salary <= 60000:
        t2_optimal_low, t2_optimal_high = 0.5, 3.0
    elif avg_salary <= 120000:
        t2_optimal_low, t2_optimal_high = 1.0, 5.0
    elif avg_salary <= 200000:
        t2_optimal_low, t2_optimal_high = 5.0, 15.0
    else:
        t2_optimal_low, t2_optimal_high = 10.0, 20.0
    
    if t2_optimal_low <= cumulative_t2 <= t2_optimal_high:
        score += 40  # 完美区间
    elif (t2_optimal_low * 0.5) <= cumulative_t2 < t2_optimal_low:
        score += 30  # 略低
    elif t2_optimal_high < cumulative_t2 <= (t2_optimal_high * 1.5):
        score += 30  # 略高
    else:
        score += 20  # 偏离较远
    
    # 2. 缴费额合理性评分（根据年薪动态调整）
    # 使用动态上限替代硬编码12k
    if avg_salary <= 40000:
        optimal_contrib = 6000
    elif avg_salary <= 100000:
        optimal_contrib = 8000
    else:
        # 高收入：使用动态上限模型
        cap_result_for_eval = calculate_contribution_cap(
            annual_salary=avg_salary,
            t2_rate=cumulative_t2
        )
        optimal_contrib = cap_result_for_eval['cap']
    
    contrib_ratio = avg_contribution / optimal_contrib
    
    if 0.8 <= contrib_ratio <= 1.2:
        score += 30  # 完美匹配
    elif 0.5 <= contrib_ratio < 0.8 or 1.2 < contrib_ratio <= 1.5:
        score += 20  # 可接受
    else:
        score += 10  # 偏离较多
    
    # 3. 补贴/税优利用率评分（高收入改为T3优化评分）
    if avg_salary >= 150000:
        # 高收入无补贴，改为评估T3控制（先计算T3）
        latest_record = sorted_data[-1]
        temp_predicted_t3_result = calculate_t3(
            t2=cumulative_t2,
            annual_salary=latest_record['salary'],
            age=age
        )
        temp_predicted_t3 = temp_predicted_t3_result['t3']
        
        if temp_predicted_t3 <= 3.0:
            score += 30  # T3低于现行税率，优秀
        elif temp_predicted_t3 <= 5.0:
            score += 20  # T3略高但可接受
        else:
            score += 10  # T3过高需优化
    else:
        # 中低收入评估补贴利用率
        avg_subsidy = total_subsidy / len(sorted_data)
        if avg_salary <= 40000:
            max_possible_subsidy = 150 + 12000 * 0.50  # 低收入50%匹配率
        else:
            max_possible_subsidy = 150 + 12000 * 0.30  # 中等收入30%匹配率
        
        if max_possible_subsidy > 0:
            subsidy_utilization = avg_subsidy / max_possible_subsidy
            score += int(subsidy_utilization * 30)
        else:
            score += 15  # 无法计算补贴利用率时给中等分
    
    # ==================== 诊断问题（基于动态上限） ====================
    
    diagnosis = {
        'overContribution': False,
        'underContribution': False,
        'exceedsDynamicCap': len(cap_warnings) > 0,  # 新增：是否超出动态上限
        'capWarnings': cap_warnings,  # 新增：详细警告列表
        'message': ''
    }
    
    # 使用动态上限判断过度缴费
    if len(cap_warnings) >= 2:
        diagnosis['overContribution'] = True
        years_str = ', '.join(str(w['year']) for w in cap_warnings)
        avg_excess = sum(w['excess'] for w in cap_warnings) / len(cap_warnings)
        diagnosis['message'] = (
            f"在{years_str}年缴费超出动态上限，"
            f"平均超出¥{avg_excess:,.0f}。"
            f"建议根据年薪和T2调整缴费策略"
        )
    elif len(cap_warnings) == 1:
        w = cap_warnings[0]
        diagnosis['message'] = (
            f"{w['year']}年缴费¥{w['contribution']:,}超出动态上限¥{w['dynamic_cap']:,.0f}，"
            f"但整体策略合理"
        )
    
    # 检查缴费不足（根据年薪动态调整）
    under_contrib_years = []
    for r in sorted_data:
        # 年薪>8万但缴费<5000视为不足
        if r['salary'] > 80000 and r['contribution'] < 5000:
            under_contrib_years.append(r['year'])
    
    if len(under_contrib_years) >= 2:
        diagnosis['underContribution'] = True
        diagnosis['message'] += f" 在{', '.join(map(str, under_contrib_years))}年缴费不足，未充分利用税收优惠"
    
    if not diagnosis['overContribution'] and not diagnosis['underContribution']:
        if avg_salary >= 150000:
            diagnosis['message'] = "缴费策略合理。作为高收入者，您的优势在于高税率带来的节税效果"
        elif avg_salary <= 40000:
            diagnosis['message'] = "缴费策略合理。建议保持当前缴费并充分利用财政补贴"
        else:
            diagnosis['message'] = "缴费策略整体合理，继续保持"
    
    # ==================== 预测T3 ====================
    
    latest_record = sorted_data[-1]
    predicted_t3_result = calculate_t3(
        t2=cumulative_t2,
        annual_salary=latest_record['salary'],
        age=age
    )
    predicted_t3 = predicted_t3_result['t3']
    
    # ==================== 潜在优化空间 ====================
    
    # 当前策略下的年度收益
    current_annual_benefit = (total_subsidy / len(sorted_data)) + (avg_contribution * cumulative_t2 / 100)
    
    # 智能推荐缴费额（根据年薪分段）
    if avg_salary <= 40000:
        # 低收入：补贴全额，推荐适度缴费
        recommended_amount = 6000
    elif avg_salary <= 100000:
        # 中等收入：补贴递减区间，推荐8000避免过度缴费
        recommended_amount = 8000
    else:
        # 高收入：使用动态上限模型（替代固定12k）
        cap_result_for_recommend = calculate_contribution_cap(
            annual_salary=avg_salary,
            t2_rate=cumulative_t2
        )
        recommended_amount = int(cap_result_for_recommend['cap'])
    
    # 优化策略下的年度收益（假设采纳推荐缴费额）
    optimized_subsidy_result = calculate_subsidy(avg_salary, recommended_amount)
    optimized_subsidy = optimized_subsidy_result['subsidy']
    optimized_tax_save = recommended_amount * (cumulative_t2 / 100)
    optimized_annual_benefit = optimized_subsidy + optimized_tax_save
    
    potential_gain = (optimized_annual_benefit - current_annual_benefit) * (60 - age)
    
    # NPV提升百分比
    if current_annual_benefit > 0:
        npv_improvement = ((optimized_annual_benefit - current_annual_benefit) / current_annual_benefit) * 100
    else:
        npv_improvement = 0
    
    return {
        'cumulativeT2': round(cumulative_t2, 2),
        'efficiencyScore': min(100, score),
        'totalSubsidy': round(total_subsidy, 2),
        'diagnosis': diagnosis,
        'predictedT3': predicted_t3,
        'potentialGain': round(max(0, potential_gain), 2),
        'npvImprovement': round(npv_improvement, 2),
        'recommendedAmount': recommended_amount,
        'historicalDetails': {
            't2ByYear': t2_values,
            'subsidyByYear': subsidy_by_year,  # 每年补贴明细
            'averageContribution': round(avg_contribution, 2),
            'averageSalary': round(avg_salary, 2),
            'totalContribution': round(total_contribution, 2)
        }
    }


# 测试函数
if __name__ == '__main__':
    # 测试用例
    test_history = [
        {"year": 2022, "salary": 120000, "contribution": 8000},
        {"year": 2023, "salary": 135000, "contribution": 10000},
        {"year": 2024, "salary": 150000, "contribution": 12000}
    ]
    
    test_age = 30
    
    print("历史数据诊断测试\n" + "="*70)
    print("历史缴费记录:")
    for record in test_history:
        print(f"  {record['year']}年: 年薪¥{record['salary']:,}, 缴费¥{record['contribution']:,}")
    print(f"当前年龄: {test_age}")
    
    result = diagnose_history(test_history, test_age)
    
    print(f"\n诊断结果:")
    print(f"  累积加权平均T2: {result['cumulativeT2']}%")
    print(f"  缴费效率评分: {result['efficiencyScore']}分")
    print(f"  累计获得补贴: ¥{result['totalSubsidy']:,.2f}")
    print(f"  预测领取期T3: {result['predictedT3']}%")
    print(f"  潜在优化收益: ¥{result['potentialGain']:,.2f}")
    print(f"  NPV提升空间: {result['npvImprovement']}%")
    print(f"  推荐未来缴费额: ¥{result['recommendedAmount']:,}")
    
    print(f"\n诊断意见:")
    print(f"  {result['diagnosis']['message']}")
    
    print(f"\n历年T2详情:")
    for item in result['historicalDetails']['t2ByYear']:
        print(f"  {item['year']}年: T2={item['t2']}%, 缴费¥{item['contribution']:,}")
    
    print(f"\n历年补贴明细:")
    for item in result['historicalDetails']['subsidyByYear']:
        print(f"  {item['year']}年: 补贴¥{item['subsidy']:,.2f}, 缴费¥{item['contribution']:,}, 年薪¥{item['salary']:,}")

