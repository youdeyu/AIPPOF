"""
缴费上限计算模块
基于论文《AI驱动下的个人养老金税收优惠政策优化》中的混合动态上限模型（推荐策略）

核心公式（公式5-5）：
C_final(w, t₂) = min(C_dynamic, C_fixed_effective)

其中：
- C_dynamic = 0.08 × w（动态上限）
- C_fixed_effective = C_fixed_smooth(t₂) × τ(w)（有效固定上限）
- C_fixed_smooth(t₂)：S形平滑函数，节点12k→24k→48k→72k
- τ(w)：高收入递减因子，拐点200k
"""
import math
from typing import Optional


def _sigma(x: float) -> float:
    """
    Logistic σ函数（S型平滑函数）
    σ(x) = 1 / (1 + e^(-x))
    
    用于平滑过渡，避免阶梯突变
    """
    try:
        return 1.0 / (1.0 + math.exp(-x))
    except OverflowError:
        return 0.0 if x < 0 else 1.0


def dynamic_cap_from_wage(wage: float, cap_ratio: float = 0.08) -> float:
    """
    动态上限：C_dynamic = cap_ratio × wage
    
    公式5-3的基础版本，默认8%
    
    Args:
        wage: 年工资收入
        cap_ratio: 缴费比例（默认0.08，即8%）
        
    Returns:
        动态上限金额
    """
    return float(cap_ratio) * float(wage)


def fixed_cap_smooth(
    t2: float,
    nodes: tuple = (12000.0, 24000.0, 48000.0, 72000.0),
    thresholds: tuple = (0.03, 0.05, 0.10),
    k: float = 20.0
) -> float:
    """
    分层固定上限的平滑函数（S形连续过渡）
    
    公式：C_fixed(t₂) = base + Σ[Δᵢ × σ(k×(t₂ - thr_i))]
    
    设计思想：
    - 避免阶梯突变，使用Sigmoid函数平滑过渡
    - 节点：12k → 24k → 48k → 72k
    - t₂阈值：3%, 5%, 10%
    - k越大，过渡越陡峭（接近阶梯）
    
    Args:
        t2: T2平均节税率（百分比，如10.0表示10%）
        nodes: 四个固定节点 (12k, 24k, 48k, 72k)
        thresholds: 三个转折点t2值 (3%, 5%, 10%)
        k: S型函数斜率（默认20，平滑过渡）
        
    Returns:
        平滑固定上限金额
    """
    base, n2, n3, n4 = nodes
    deltas = (n2 - base, n3 - n2, n4 - n3)
    t = float(t2) / 100.0  # 转换为小数形式（10% → 0.10）
    
    val = base
    for delta, thr in zip(deltas, thresholds):
        val += delta * _sigma(float(k) * (t - float(thr)))
    
    return max(0.0, val)


def tau_of_wage(
    wage: float,
    tau_min: float = 0.5,
    w0_pivot: float = 200000.0,
    b_width: float = 100000.0
) -> float:
    """
    高收入递减因子 τ(w)（公式5-6）
    
    公式：τ(w) = τ_min + (1 - τ_min) × (1 - σ((w - w0)/b))
    
    设计思想：
    - 当w << w0_pivot时，τ ≈ 1（无递减）
    - 当w >> w0_pivot时，τ ≈ τ_min（最大递减50%）
    - 在w0_pivot附近平滑过渡
    - 控制超高收入群体的财政压力
    
    Args:
        wage: 年工资收入
        tau_min: 最低折扣（0~1），默认0.5表示最多递减50%
        w0_pivot: 收入递减起点（元），默认200,000元
        b_width: 递减平滑宽度（元），默认100,000元
        
    Returns:
        递减因子（0~1之间）
    """
    w = float(wage)
    x = (w - float(w0_pivot)) / float(b_width)
    return float(tau_min) + (1.0 - float(tau_min)) * (1.0 - _sigma(x))


def calculate_contribution_cap(annual_salary: float, t2_rate: Optional[float] = None) -> dict:
    """
    计算个性化缴费上限（混合动态上限模型，公式5-5）
    
    核心公式：
    C_final(w, t₂) = min(C_dynamic, C_fixed_effective)
    
    其中：
    - C_dynamic = 0.08 × w
    - C_fixed_smooth(t₂) = 12k + (24k-12k)×σ(20×(t₂-3%)) + (48k-24k)×σ(20×(t₂-5%)) + (72k-48k)×σ(20×(t₂-10%))
    - τ(w) = 0.5 + 0.5×(1 - σ((w-200k)/100k))
    - C_fixed_effective = C_fixed_smooth(t₂) × τ(w)
    
    Args:
        annual_salary: 年薪（税前）
        t2_rate: T2平均节税率 (%)，例如10.0表示10%
                如果为None，保守回退到纯动态比例
        
    Returns:
        dict: 上限详细信息
    """
    # 如果缺失t2，保守使用纯动态上限
    if t2_rate is None:
        dynamic_cap = dynamic_cap_from_wage(annual_salary, cap_ratio=0.08)
        return {
            'cap': round(dynamic_cap, 0),
            'strategy': 'dynamic_8p (fallback)',
            'formula': f"Cap = {annual_salary:,.0f} × 8% = {dynamic_cap:,.0f}元（无T2数据，使用保守策略）",
            'details': {
                'reason': '缺失T2，回退到纯动态比例',
                'dynamicCap': round(dynamic_cap, 0)
            }
        }
    
    # 1. 计算动态上限（公式5-3）
    dynamic_cap = dynamic_cap_from_wage(annual_salary, cap_ratio=0.08)
    
    # 2. 计算平滑固定上限（S形函数）
    fixed_raw = fixed_cap_smooth(
        t2_rate,
        nodes=(12000.0, 24000.0, 48000.0, 72000.0),
        thresholds=(0.03, 0.05, 0.10),
        k=20.0
    )
    
    # 3. 计算高收入递减因子（公式5-6）
    tau = tau_of_wage(
        annual_salary,
        tau_min=0.5,
        w0_pivot=200000.0,
        b_width=100000.0
    )
    
    # 4. 计算有效固定上限
    fixed_effective = fixed_raw * tau
    
    # 5. 取两者最小值（公式5-5核心）
    final_cap = min(dynamic_cap, fixed_effective)
    
    return {
        'cap': round(final_cap, 0),
        'strategy': 'min_dynamic_vs_fixed',
        'formula': f"Cap = min({dynamic_cap:,.0f}, {fixed_effective:,.0f}) = {final_cap:,.0f}元",
        'details': {
            't2': t2_rate,
            'dynamicCap': round(dynamic_cap, 0),
            'fixedRaw': round(fixed_raw, 0),
            'tau': round(tau, 3),
            'fixedEffective': round(fixed_effective, 0),
            'finalCap': round(final_cap, 0),
            'usedChannel': 'dynamic' if final_cap == dynamic_cap else 'fixed',
            'explanation': f"基于T2={t2_rate}%和年薪{annual_salary:,.0f}元，采用{'动态上限' if final_cap == dynamic_cap else '固定上限'}通道"
        }
    }


# 测试函数
if __name__ == '__main__':
    print("="*80)
    print("缴费上限计算测试（混合动态上限模型 - 公式5-5）")
    print("="*80)
    
    # 测试用例（覆盖不同收入和t2组合）
    test_cases = [
        {'salary': 50000, 't2': 5.0, 'desc': '低收入+低t2'},
        {'salary': 80000, 't2': 8.0, 'desc': '中低收入+中t2'},
        {'salary': 120000, 't2': 12.0, 'desc': '中等收入+高t2'},
        {'salary': 200000, 't2': 18.0, 'desc': '高收入（拐点）+高t2'},
        {'salary': 300000, 't2': 25.0, 'desc': '高收入+超高t2'},
        {'salary': 500000, 't2': 30.0, 'desc': '超高收入+超高t2'},
    ]
    
    print(f"\n{'描述':<20} {'年薪':<12} {'T2':<8} {'动态上限':<12} {'固定上限':<12} {'τ(w)':<8} {'最终上限':<12} {'通道'}")
    print("-" * 110)
    
    for case in test_cases:
        result = calculate_contribution_cap(case['salary'], case['t2'])
        details = result['details']
        
        print(f"{case['desc']:<20} ¥{case['salary']:<11,} {case['t2']:<7.1f}% "
              f"¥{details['dynamicCap']:<11,.0f} ¥{details['fixedEffective']:<11,.0f} "
              f"{details['tau']:<7.3f} ¥{result['cap']:<11,.0f} {details['usedChannel']}")
    
    print("\n" + "="*80)
    print("关键特征验证")
    print("="*80)
    
    # 验证1: t2阈值平滑过渡
    print("\n1. T2阈值平滑过渡（工资12万，t2从0%到15%）:")
    for t2 in [0, 3, 5, 8, 10, 12, 15]:
        result = calculate_contribution_cap(120000, float(t2))
        print(f"   T2={t2:2}%: 上限¥{result['cap']:,.0f}元")
    
    # 验证2: 高收入递减效应
    print("\n2. 高收入递减效应（t2=15%，工资从10万到50万）:")
    for salary in [100000, 150000, 200000, 250000, 300000, 400000, 500000]:
        result = calculate_contribution_cap(salary, 15.0)
        tau = result['details']['tau']
        print(f"   工资¥{salary:,}: τ(w)={tau:.3f}, 上限¥{result['cap']:,.0f}元")
    
    # 验证3: 动态vs固定通道切换
    print("\n3. 动态vs固定通道切换（t2=10%）:")
    for salary in [60000, 100000, 150000, 200000, 300000]:
        result = calculate_contribution_cap(salary, 10.0)
        channel = result['details']['usedChannel']
        print(f"   工资¥{salary:,}: {channel}通道, 上限¥{result['cap']:,.0f}元")
    
    print("\n" + "="*80)
    print("公式验证（与论文对比）")
    print("="*80)
    
    # 典型案例：年薪12万，t2=10%
    salary_test = 120000
    t2_test = 10.0
    result = calculate_contribution_cap(salary_test, t2_test)
    
    print(f"\n典型案例：年薪¥{salary_test:,}，T2={t2_test}%")
    print(f"  动态上限: {salary_test} × 8% = ¥{result['details']['dynamicCap']:,.0f}")
    print(f"  平滑固定上限: ¥{result['details']['fixedRaw']:,.0f}（基于t2={t2_test}%）")
    print(f"  高收入递减因子: τ(w) = {result['details']['tau']:.3f}")
    print(f"  有效固定上限: {result['details']['fixedRaw']:.0f} × {result['details']['tau']:.3f} = ¥{result['details']['fixedEffective']:,.0f}")
    print(f"  最终上限: min({result['details']['dynamicCap']:,.0f}, {result['details']['fixedEffective']:,.0f}) = ¥{result['cap']:,.0f}")
    print(f"  选用通道: {result['details']['usedChannel']}")

