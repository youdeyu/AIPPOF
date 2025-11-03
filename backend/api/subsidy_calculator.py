"""
渐进式精准补贴计算模块 - 用于AIPPOF网页应用

实现养老金第三支柱的收入递减式补贴机制：
1. 默认参与设计，提升覆盖率
2. 双轨激励：低收入靠补贴，高收入靠税优
3. 平滑过渡：补贴随收入递减，避免悬崖效应
4. 两部制结构：固定补贴 + 分段配比

作者：养老金第三支柱优化研究组
版本：v1.0
更新：2025年11月3日
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class SubsidyParams:
    """精准补贴参数配置"""
    # 基础参数
    base_grant: float = 150.0          # 固定补贴（元）
    c_min: float = 200.0               # 最低缴费额（元）
    c0_ratio_of_wage: float = 0.02     # 第一档缴费基数比例（2%工资）
    
    # 匹配比例（两档）
    ratio_low: float = 0.30            # 低档匹配率（首档缴费）
    ratio_high: float = 0.06           # 高档匹配率（超额缴费）
    
    # 低收入倾斜
    uplift_low: float = 0.5            # 低收入加成比例（首档配比+50%）
    low_income_cut: float = 80000.0    # 低收入界定标准（元/年）
    
    # 补贴递减（平滑过渡）
    taper_mode: bool = True            # 启用收入递减
    taper_w_low: float = 40000.0       # 全额补贴上限（元/年）
    taper_w_high: float = 100000.0     # 补贴归零下限（元/年）
    
    # 默认参与
    default_enroll: bool = True        # 默认纳入补贴体系


def calculate_subsidy(
    annual_salary: float,
    contribution_amount: float,
    params: SubsidyParams = None
) -> Dict[str, Any]:
    """
    计算渐进式精准补贴
    
    参数:
        annual_salary: 年工资收入（元）
        contribution_amount: 计划缴费额（元）
        params: 补贴参数配置
        
    返回:
        {
            'subsidy': 补贴金额（元）,
            'c_effective': 实际生效缴费（元）,
            'ratio': 补贴率（%）,
            'triggered': 是否触发补贴（bool）,
            'breakdown': {  # 补贴明细
                'base_grant': 固定补贴（元）,
                'tier1_match': 首档配比补贴（元）,
                'tier2_match': 超额配比补贴（元）,
                'taper_factor': 收入递减因子（0-1）,
                'is_low_income': 是否享受低收入加成（bool）
            }
        }
    """
    if params is None:
        params = SubsidyParams()
    
    # 1. 默认参与检查
    if not params.default_enroll:
        return {
            'subsidy': 0.0,
            'c_effective': 0.0,
            'ratio': 0.0,
            'triggered': False,
            'breakdown': {}
        }
    
    # 2. 最低缴费门槛检查
    c_eff = float(contribution_amount)
    if c_eff < params.c_min:
        return {
            'subsidy': 0.0,
            'c_effective': c_eff,
            'ratio': 0.0,
            'triggered': False,
            'breakdown': {
                'reason': f'缴费额{c_eff:.0f}元低于最低门槛{params.c_min:.0f}元'
            }
        }
    
    # 3. 计算两档缴费
    wage = float(annual_salary)
    c0_threshold = params.c0_ratio_of_wage * wage  # 第一档上限
    c0 = min(c_eff, c0_threshold)  # 首档缴费
    c1 = max(0.0, c_eff - c0_threshold)  # 超额缴费
    
    # 4. 计算配比率（低收入加成）
    is_low_income = wage <= params.low_income_cut
    ratio_low_effective = params.ratio_low
    if is_low_income:
        ratio_low_effective *= (1.0 + params.uplift_low)
    
    # 5. 计算补贴组成
    base_grant = params.base_grant
    tier1_match = ratio_low_effective * c0
    tier2_match = params.ratio_high * c1
    subsidy_raw = base_grant + tier1_match + tier2_match
    
    # 6. 收入递减调整
    taper_factor = 1.0
    if params.taper_mode:
        if wage <= params.taper_w_low:
            taper_factor = 1.0  # 全额补贴
        elif wage >= params.taper_w_high:
            taper_factor = 0.0  # 补贴归零
        else:
            # 线性递减
            taper_factor = (params.taper_w_high - wage) / (
                params.taper_w_high - params.taper_w_low
            )
    
    subsidy_final = subsidy_raw * taper_factor
    
    # 7. 计算补贴率
    ratio = (subsidy_final / c_eff * 100) if c_eff > 0 else 0.0
    
    return {
        'subsidy': round(subsidy_final, 2),
        'c_effective': round(c_eff, 2),
        'ratio': round(ratio, 2),
        'triggered': True,
        'breakdown': {
            'base_grant': round(base_grant * taper_factor, 2),
            'tier1_match': round(tier1_match * taper_factor, 2),
            'tier2_match': round(tier2_match * taper_factor, 2),
            'taper_factor': round(taper_factor, 3),
            'is_low_income': is_low_income,
            'tier1_rate': round(ratio_low_effective * 100, 1),
            'tier2_rate': round(params.ratio_high * 100, 1),
            'c0_threshold': round(c0_threshold, 2),
            'c0_amount': round(c0, 2),
            'c1_amount': round(c1, 2)
        }
    }


def get_subsidy_explanation(result: Dict[str, Any], annual_salary: float) -> str:
    """
    生成补贴计算说明文本
    
    参数:
        result: calculate_subsidy返回的结果
        annual_salary: 年工资收入
        
    返回:
        补贴说明文本
    """
    if not result['triggered']:
        if 'reason' in result.get('breakdown', {}):
            return f"❌ 未获得补贴：{result['breakdown']['reason']}"
        return "❌ 未触发补贴条件"
    
    bd = result['breakdown']
    subsidy = result['subsidy']
    ratio = result['ratio']
    
    # 构建说明
    lines = []
    lines.append(f"✅ 补贴总额：¥{subsidy:.0f} 元（补贴率 {ratio:.1f}%）")
    
    # 收入分类
    if bd['is_low_income']:
        lines.append(f"📊 收入分类：低收入群体（≤¥80,000）- 享受加成优惠")
    elif annual_salary >= 100000:
        lines.append(f"📊 收入分类：高收入群体（≥¥100,000）- 补贴递减")
    else:
        lines.append(f"📊 收入分类：中等收入群体")
    
    # 补贴构成
    lines.append("\n💰 补贴构成：")
    if bd['taper_factor'] == 1.0:
        lines.append(f"  • 固定补贴：¥{bd['base_grant']:.0f}")
        lines.append(f"  • 首档配比（{bd['tier1_rate']:.0f}%）：¥{bd['tier1_match']:.0f}")
        if bd['tier2_match'] > 0:
            lines.append(f"  • 超额配比（{bd['tier2_rate']:.0f}%）：¥{bd['tier2_match']:.0f}")
    else:
        lines.append(f"  • 基础补贴小计：¥{(bd['base_grant'] + bd['tier1_match'] + bd['tier2_match']):.0f}")
        lines.append(f"  • 收入递减因子：{bd['taper_factor']:.1%}")
        lines.append(f"  • 最终补贴：¥{subsidy:.0f}")
    
    # 缴费档位说明
    if bd['c1_amount'] > 0:
        lines.append(f"\n📈 缴费档位：")
        lines.append(f"  • 首档（≤¥{bd['c0_threshold']:.0f}）：¥{bd['c0_amount']:.0f}")
        lines.append(f"  • 超额部分：¥{bd['c1_amount']:.0f}")
    
    return "\n".join(lines)


def get_subsidy_tier_info(annual_salary: float) -> Dict[str, Any]:
    """
    获取用户的补贴档位信息（用于前端显示）
    
    参数:
        annual_salary: 年工资收入
        
    返回:
        补贴档位信息字典
    """
    params = SubsidyParams()
    
    # 判断收入层次
    if annual_salary <= params.low_income_cut:
        tier = "低收入"
        description = "主要激励：高额财政补贴"
        base_rate = params.ratio_low * (1 + params.uplift_low) * 100
        advantages = [
            f"享受 {base_rate:.0f}% 首档配比率（含50%加成）",
            f"固定补贴 ¥{params.base_grant:.0f} 元",
            "补贴率可达 100%+ "
        ]
    elif annual_salary >= params.taper_w_high:
        tier = "高收入"
        description = "主要激励：税收优惠减免"
        advantages = [
            "补贴已递减至零（避免双重优惠）",
            "主要通过个税减免获益",
            "预计节税 500-2000 元/年"
        ]
    else:
        tier = "中等收入"
        description = "双轨激励：补贴与税优并重"
        if annual_salary < params.taper_w_low:
            taper_pct = 100
        else:
            taper_pct = (params.taper_w_high - annual_salary) / (
                params.taper_w_high - params.taper_w_low
            ) * 100
        advantages = [
            f"{params.ratio_low * 100:.0f}% 首档配比率",
            f"补贴递减比例：{taper_pct:.0f}%",
            "税收优惠与补贴双重受益"
        ]
    
    return {
        'tier': tier,
        'description': description,
        'advantages': advantages,
        'annual_salary': annual_salary,
        'is_eligible': True  # 默认参与模式下都符合条件
    }


# 测试代码
if __name__ == "__main__":
    # 测试案例
    test_cases = [
        {"salary": 30000, "contribution": 200, "name": "低收入最小缴费"},
        {"salary": 50000, "contribution": 1000, "name": "低收入正常缴费"},
        {"salary": 60000, "contribution": 5000, "name": "中等收入"},
        {"salary": 150000, "contribution": 12000, "name": "高收入"},
    ]
    
    print("=" * 60)
    print("渐进式精准补贴计算测试")
    print("=" * 60)
    
    for case in test_cases:
        print(f"\n【{case['name']}】")
        print(f"年工资：¥{case['salary']:,} | 缴费：¥{case['contribution']:,}")
        print("-" * 60)
        
        result = calculate_subsidy(case['salary'], case['contribution'])
        explanation = get_subsidy_explanation(result, case['salary'])
        print(explanation)
        
        tier_info = get_subsidy_tier_info(case['salary'])
        print(f"\n收入层次：{tier_info['tier']}")
        print(f"激励方式：{tier_info['description']}")
