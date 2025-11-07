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
    """精准补贴参数配置 - 三段式补贴模型"""
    # 基础参数
    base_grant: float = 150.0          # 固定补贴（元）
    c_min: float = 200.0               # 最低缴费额（元）
    
    # 三段式分段点（对应论文中的 C̅₁ 和 C̅₂）
    c_bar_1: float = 1600.0            # 第一分段点（首档上限，约2%×80k）
    c_bar_2: float = 6000.0            # 第二分段点（超额上限）
    
    # 三段式匹配比例（对应论文中的 α₁, α₂, α₃）
    alpha_1: float = 0.45              # 第一段配比率（0 < C ≤ C̅₁）
    alpha_2: float = 0.30              # 第二段配比率（C̅₁ < C ≤ C̅₂）
    alpha_3: float = 0.06              # 第三段配比率（C > C̅₂）
    
    # T2触发阈值（对应论文中的 τ₀）
    t2_threshold: float = 0.05         # T2 ≤ 5% 时触发补贴
    
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
    计算渐进式精准补贴 - 三段式模型（符合论文公式5-12）
    
    公式:
         ⎧ α₁C,                                    0 < C ≤ C̅₁
    S = ⎨ α₁C̅₁ + α₂(C - C̅₁),                   C̅₁ < C ≤ C̅₂  
         ⎩ α₁C̅₁ + α₂(C̅₂ - C̅₁) + α₃(C - C̅₂),   C > C̅₂
    
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
                'tier1_subsidy': 第一段补贴（元）,
                'tier2_subsidy': 第二段补贴（元）,
                'tier3_subsidy': 第三段补贴（元）,
                'taper_factor': 收入递减因子（0-1）,
                'segment': 所属段数（1/2/3）
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
    
    wage = float(annual_salary)
    
    # 3. 三段式补贴计算（论文公式5-12）
    tier1_subsidy = 0.0
    tier2_subsidy = 0.0
    tier3_subsidy = 0.0
    segment = 0
    
    if c_eff <= params.c_bar_1:
        # 第一段：0 < C ≤ C̅₁，配比率 α₁ = 45%
        tier1_subsidy = params.alpha_1 * c_eff
        segment = 1
    elif c_eff <= params.c_bar_2:
        # 第二段：C̅₁ < C ≤ C̅₂，配比率 α₂ = 30%
        tier1_subsidy = params.alpha_1 * params.c_bar_1
        tier2_subsidy = params.alpha_2 * (c_eff - params.c_bar_1)
        segment = 2
    else:
        # 第三段：C > C̅₂，配比率 α₃ = 6%
        tier1_subsidy = params.alpha_1 * params.c_bar_1
        tier2_subsidy = params.alpha_2 * (params.c_bar_2 - params.c_bar_1)
        tier3_subsidy = params.alpha_3 * (c_eff - params.c_bar_2)
        segment = 3
    
    # 配比补贴总额
    match_subsidy = tier1_subsidy + tier2_subsidy + tier3_subsidy
    
    # 4. 固定补贴 + 配比补贴
    subsidy_raw = params.base_grant + match_subsidy
    
    # 5. 收入递减调整
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
    
    # 6. 计算补贴率
    ratio = (subsidy_final / c_eff * 100) if c_eff > 0 else 0.0
    
    return {
        'subsidy': round(subsidy_final, 2),
        'c_effective': round(c_eff, 2),
        'ratio': round(ratio, 2),
        'triggered': True,
        'breakdown': {
            'base_grant': round(params.base_grant * taper_factor, 2),
            'tier1_subsidy': round(tier1_subsidy * taper_factor, 2),
            'tier2_subsidy': round(tier2_subsidy * taper_factor, 2),
            'tier3_subsidy': round(tier3_subsidy * taper_factor, 2),
            'taper_factor': round(taper_factor, 3),
            'segment': segment,
            'alpha_1': params.alpha_1,
            'alpha_2': params.alpha_2,
            'alpha_3': params.alpha_3,
            'c_bar_1': params.c_bar_1,
            'c_bar_2': params.c_bar_2
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
    
    # 判断收入层次（基于taper机制）
    low_income_threshold = params.taper_w_low  # 40000元
    high_income_threshold = params.taper_w_high  # 100000元
    
    if annual_salary <= low_income_threshold:
        tier = "低收入"
        description = "主要激励：高额财政补贴"
        advantages = [
            f"享受 {params.alpha_1 * 100:.0f}% 首档配比率（最高档）",
            f"固定补贴 ¥{params.base_grant:.0f} 元",
            "全额补贴，无递减"
        ]
    elif annual_salary >= high_income_threshold:
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
        taper_pct = (high_income_threshold - annual_salary) / (
            high_income_threshold - low_income_threshold
        ) * 100
        advantages = [
            f"三段式补贴：{params.alpha_1*100:.0f}% / {params.alpha_2*100:.0f}% / {params.alpha_3*100:.0f}%",
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

