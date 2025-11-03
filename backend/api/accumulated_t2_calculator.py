"""
累计T2计算模块（已参与者专用）
基于历史缴费记录计算累计的平均节税率

公式（蓝浩歌论文式(5)）：
t2_accumulated = Σ[ΔTk·(1+r)^(N−k+1)] / Σ[Pk·(1+r)^(N−k+1)]

其中：
- ΔTk = 第k年的节税额（税前收入wk缴费前后的个税差）
- Pk = 第k年的缴费额
- r = 贴现率（默认1.75%）
- N = 总缴费年数
- k = 年份索引（从1开始）
"""
from typing import List, Dict


# 中国个人所得税税率表（综合所得年度税率）
TAX_BRACKETS = [
    (36000, 0.03, 0),           # 0-36,000: 3%
    (144000, 0.10, 2520),       # 36,000-144,000: 10%
    (300000, 0.20, 16920),      # 144,000-300,000: 20%
    (420000, 0.25, 31920),      # 300,000-420,000: 25%
    (660000, 0.30, 52920),      # 420,000-660,000: 30%
    (960000, 0.35, 85920),      # 660,000-960,000: 35%
    (float('inf'), 0.45, 181920) # 960,000以上: 45%
]


def calculate_annual_tax(taxable_income):
    """
    计算年度个人所得税（超额累进）
    
    Args:
        taxable_income: 应纳税所得额（已扣除起征点60000）
        
    Returns:
        float: 应纳税额
    """
    if taxable_income <= 0:
        return 0.0
    
    t = max(0.0, float(taxable_income))
    for threshold, rate, quick_deduction in TAX_BRACKETS:
        if t <= threshold:
            return t * rate - quick_deduction
    
    # 最高档
    return t * 0.45 - 181920


def calculate_delta_t(annual_salary, contribution, deduction=60000):
    """
    计算单年的节税额 ΔT
    
    ΔT = 不缴费时的税 - 缴费后的税
    
    Args:
        annual_salary: 年薪（税前，已扣五险一金）
        contribution: 个人养老金缴费额
        deduction: 个人所得税起征点（默认60000）
        
    Returns:
        float: 节税额
    """
    # 不缴费时的应纳税所得额
    taxable_without = annual_salary - deduction
    tax_without = calculate_annual_tax(taxable_without)
    
    # 缴费后的应纳税所得额（缴费可抵扣）
    taxable_with = max(0, annual_salary - contribution) - deduction
    tax_with = calculate_annual_tax(taxable_with)
    
    # 节税额
    delta_t = tax_without - tax_with
    
    return delta_t


def calculate_accumulated_t2(history_records, discount_rate=0.0175):
    """
    计算累计T2平均节税率（基于历史缴费记录）
    
    使用蓝浩歌论文公式(5)：
    t2 = Σ[ΔTk·(1+r)^(N−k+1)] / Σ[Pk·(1+r)^(N−k+1)]
    
    Args:
        history_records: 历史缴费记录数组
            [
                {"year": 2022, "salary": 100000, "contribution": 8000},
                {"year": 2023, "salary": 110000, "contribution": 10000},
                {"year": 2024, "salary": 120000, "contribution": 12000}
            ]
        discount_rate: 贴现率（默认1.75%）
        
    Returns:
        dict: 累计T2结果
        {
            "accumulatedT2": 累计T2值（%）,
            "totalTaxSaving": 累计节税总额（元）,
            "totalContribution": 累计缴费总额（元）,
            "yearlyDetails": [年度明细],
            "averageT2": 简单平均T2（不考虑折现）,
            "discountRate": 使用的贴现率
        }
    """
    if not history_records or len(history_records) == 0:
        return {
            "accumulatedT2": 0.0,
            "totalTaxSaving": 0.0,
            "totalContribution": 0.0,
            "yearlyDetails": [],
            "averageT2": 0.0,
            "discountRate": discount_rate
        }
    
    # 按年份排序
    sorted_records = sorted(history_records, key=lambda x: x['year'])
    N = len(sorted_records)
    
    # 累计计算（带折现）
    numerator = 0.0  # Σ[ΔTk·(1+r)^(N−k+1)]
    denominator = 0.0  # Σ[Pk·(1+r)^(N−k+1)]
    
    # 简单累计（不带折现）
    total_tax_saving_simple = 0.0
    total_contribution_simple = 0.0
    
    yearly_details = []
    
    for k, record in enumerate(sorted_records, start=1):
        year = record['year']
        salary = record['salary']
        contribution = record['contribution']
        
        # 计算该年的节税额
        delta_t = calculate_delta_t(salary, contribution)
        
        # 计算折现因子 (1+r)^(N-k+1)
        discount_factor = (1 + discount_rate) ** (N - k + 1)
        
        # 累加到分子和分母
        numerator += delta_t * discount_factor
        denominator += contribution * discount_factor
        
        # 简单累计（用于辅助分析）
        total_tax_saving_simple += delta_t
        total_contribution_simple += contribution
        
        # 该年的单独T2（用于趋势分析）
        yearly_t2 = (delta_t / contribution * 100) if contribution > 0 else 0
        
        yearly_details.append({
            "year": year,
            "salary": salary,
            "contribution": contribution,
            "taxSaving": round(delta_t, 2),
            "t2": round(yearly_t2, 2),
            "discountFactor": round(discount_factor, 4)
        })
    
    # 计算累计T2（带折现）
    accumulated_t2 = (numerator / denominator * 100) if denominator > 0 else 0
    
    # 计算简单平均T2（不带折现）
    average_t2_simple = (total_tax_saving_simple / total_contribution_simple * 100) if total_contribution_simple > 0 else 0
    
    return {
        "accumulatedT2": round(accumulated_t2, 2),  # %
        "totalTaxSaving": round(total_tax_saving_simple, 2),  # 元（简单累加）
        "totalContribution": round(total_contribution_simple, 2),  # 元
        "yearlyDetails": yearly_details,
        "averageT2": round(average_t2_simple, 2),  # %（简单平均）
        "discountRate": discount_rate,
        "yearsCount": N
    }


# 测试函数
if __name__ == '__main__':
    print("=" * 80)
    print("累计T2计算测试（已参与者）")
    print("=" * 80)
    
    # 测试用例1: 稳定增长的IT从业者
    test_case_1 = [
        {"year": 2022, "salary": 100000, "contribution": 8000},
        {"year": 2023, "salary": 110000, "contribution": 10000},
        {"year": 2024, "salary": 120000, "contribution": 12000}
    ]
    
    print("\n测试用例1: 稳定增长的IT从业者")
    print("历史记录:")
    for record in test_case_1:
        print(f"  {record['year']}年: 年薪¥{record['salary']:,}, 缴费¥{record['contribution']:,}")
    
    result_1 = calculate_accumulated_t2(test_case_1)
    print(f"\n累计T2结果:")
    print(f"  累计T2（带折现）: {result_1['accumulatedT2']}%")
    print(f"  简单平均T2: {result_1['averageT2']}%")
    print(f"  累计节税总额: ¥{result_1['totalTaxSaving']:,}")
    print(f"  累计缴费总额: ¥{result_1['totalContribution']:,}")
    print(f"  年度明细:")
    for detail in result_1['yearlyDetails']:
        print(f"    {detail['year']}年: 节税¥{detail['taxSaving']}, T2={detail['t2']}%, 折现因子={detail['discountFactor']}")
    
    # 测试用例2: 高收入金融从业者
    test_case_2 = [
        {"year": 2022, "salary": 200000, "contribution": 12000},
        {"year": 2023, "salary": 220000, "contribution": 12000},
        {"year": 2024, "salary": 250000, "contribution": 12000}
    ]
    
    print("\n" + "=" * 80)
    print("测试用例2: 高收入金融从业者")
    print("历史记录:")
    for record in test_case_2:
        print(f"  {record['year']}年: 年薪¥{record['salary']:,}, 缴费¥{record['contribution']:,}")
    
    result_2 = calculate_accumulated_t2(test_case_2)
    print(f"\n累计T2结果:")
    print(f"  累计T2（带折现）: {result_2['accumulatedT2']}%")
    print(f"  简单平均T2: {result_2['averageT2']}%")
    print(f"  累计节税总额: ¥{result_2['totalTaxSaving']:,}")
    print(f"  累计缴费总额: ¥{result_2['totalContribution']:,}")
    
    # 测试用例3: 收入波动的制造业员工
    test_case_3 = [
        {"year": 2022, "salary": 80000, "contribution": 5000},
        {"year": 2023, "salary": 75000, "contribution": 6000},
        {"year": 2024, "salary": 90000, "contribution": 8000}
    ]
    
    print("\n" + "=" * 80)
    print("测试用例3: 收入波动的制造业员工")
    print("历史记录:")
    for record in test_case_3:
        print(f"  {record['year']}年: 年薪¥{record['salary']:,}, 缴费¥{record['contribution']:,}")
    
    result_3 = calculate_accumulated_t2(test_case_3)
    print(f"\n累计T2结果:")
    print(f"  累计T2（带折现）: {result_3['accumulatedT2']}%")
    print(f"  简单平均T2: {result_3['averageT2']}%")
    print(f"  累计节税总额: ¥{result_3['totalTaxSaving']:,}")
    print(f"  累计缴费总额: ¥{result_3['totalContribution']:,}")
    
    print("\n" + "=" * 80)
    print("测试完成！")
    print("=" * 80)
