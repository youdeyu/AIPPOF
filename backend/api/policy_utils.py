"""
兼容策略工具：为 legacy 调用提供向后兼容的 calculate_t3 包装。

目标：统一后端各处对 T3 的调用签名并保持老代码（t2, annual_salary, age）可用。
输出与原来后端期望一致：返回 dict，字段 't3' 为百分比（例如 7.25 表示 7.25%）。
"""
import os
import json
import math

# 尝试加载仓库根目录下的最优参数（如果存在）以驱动默认行为
DEFAULT_PARAMS = {}
try:
    root = os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..', 'final'))
    root_params = os.path.join(root, 'optimal_parameters.json')
    if os.path.exists(root_params):
        with open(root_params, 'r', encoding='utf-8') as f:
            DEFAULT_PARAMS = json.load(f)
except Exception:
    DEFAULT_PARAMS = {}


def _compute_t3_decimal(t2, w, params=None):
    """内部计算，返回小数形式的税率（0-1）。

    t2: 以小数表示的有效缴费期税率或以相容形式的数值（如果 t2 大于1，会视为百分比除以100）。
    w: 年收入
    params: 参数字典
    """
    if params is None:
        params = DEFAULT_PARAMS or {}

    # 允许外部以百分比形式传入 t2（例如 10 表示 10%），如果 t2>1 则除以100
    t2_val = float(t2)
    if t2_val > 1.5:
        t2_val = t2_val / 100.0

    L1 = params.get('L1', 0.0)
    L2 = params.get('L2', 0.10)
    L3 = params.get('L3', 0.05)
    T2_mid = params.get('T2_mid', 0.10)
    w_high = params.get('w_high', 300000.0)
    k1 = params.get('k1', 20.0)
    k2 = params.get('k2', 30.0)

    try:
        S_t2 = L2 / (1.0 + math.exp(-k1 * (t2_val - T2_mid)))
    except OverflowError:
        S_t2 = L2 if (t2_val - T2_mid) > 0 else 0.0

    xw = (w - w_high) / max(w_high, 1.0)
    try:
        S_w = L3 / (1.0 + math.exp(-k2 * xw))
    except OverflowError:
        S_w = L3 if xw > 0 else 0.0

    t3 = L1 + S_t2 + S_w
    # 边界
    t3 = min(max(t3, L1), L1 + L2 + L3)
    # 强制 t3 不超过 t2（小数形式）以保证一致性
    t3 = min(t3, t2_val)
    t3 = max(t3, 0.0)
    return float(t3)


def calculate_t3(t2, annual_salary=None, age=None, params=None):
    """兼容包装：接受旧签名 (t2, annual_salary, age) 或新签名 (t2, w, params)

    返回 dict 与旧后端模块兼容：{'t3': <percent>, 'formula':..., 'components': {...}}
    """
    # 解析参数优先级：显式 params > 文件中默认参数
    merged_params = DEFAULT_PARAMS.copy() if isinstance(DEFAULT_PARAMS, dict) else {}
    if isinstance(params, dict):
        merged_params.update(params)

    # 如果 annual_salary 被传为 None，而 params 中存在 w_high 等，我们允许把第二个参数视为 t3_max_rate（旧兼容），
    # 但在后端中大部分调用都会传入年收入，因此这里优先把 annual_salary 作为收入
    w = annual_salary if annual_salary is not None else merged_params.get('w_high', 300000.0)

    # 计算小数形式 t3
    t3_decimal = _compute_t3_decimal(t2, w, merged_params)

    # 将小数转为百分比以兼容后端现有显示和计算（例如 0.07 -> 7.0）
    t3_percent = round(t3_decimal * 100.0, 2)

    # 构建组件信息（供 debug/前端展示）
    # 为了避免复杂内联表达式导致语法问题，先单独计算各组件
    base_tax_pct = round((merged_params.get('L1', 0.0)) * 100.0, 2)
    try:
        t2_input = t2 if t2 <= 1.5 else t2 / 100.0
        t2_comp = merged_params.get('L2', 0.10)
        k1_val = merged_params.get('k1', 20.0)
        T2_mid_val = merged_params.get('T2_mid', 0.1)
        t2_component_pct = round((t2_comp / (1.0 + math.exp(-k1_val * (t2_input - T2_mid_val)))) * 100.0, 2)
    except Exception:
        t2_component_pct = 0.0

    try:
        l3 = merged_params.get('L3', 0.05)
        k2_val = merged_params.get('k2', 30.0)
        w_high_val = merged_params.get('w_high', 300000.0)
        income_adj_pct = round((l3 / (1.0 + math.exp(-k2_val * ((w - w_high_val) / max(w_high_val, 1.0))))) * 100.0, 2)
    except Exception:
        income_adj_pct = 0.0

    components = {
        'baseTax': base_tax_pct,
        't2Component': t2_component_pct,
        'incomeAdjustment': income_adj_pct,
        'ageDiscount': 0.0,
        'finalRate': t3_percent
    }

    if age is not None and age >= 55:
        # 与旧实现保持小幅年龄折扣（每年0.02%）
        age_discount = round(max(0.0, (60 - age) * 0.02), 2)
        components['ageDiscount'] = age_discount
        components['finalRate'] = round(max(0.0, components['finalRate'] - age_discount), 2)
        t3_percent = components['finalRate']

    return {
        't3': t3_percent,
        'formula': 'dual_logistic_compatible',
        'components': components,
        'details': {
            'params_used': merged_params,
            'inputs': {'t2': t2, 'annual_salary': w, 'age': age}
        }
    }
