"""
T3领取期税率计算模块
使用双逻辑斯蒂函数: t3 = f(T2, 收入, 年龄)
"""
import math


def calculate_t3(t2, annual_salary, age):
    """
    计算T3领取期累进税率（0%-14%）
    
    使用双逻辑斯蒂函数:
    t3 = L1 + (L2 - L1) / (1 + exp(-k1 * (T2 - T2_mid))) 
         + L3 / (1 + exp(-k2 * (w - w_high)))
    
    Args:
        t2: 当前T2值 (%)
        annual_salary: 年薪
        age: 年龄
        
    Returns:
        dict: 计算结果
        {
            't3': T3税率 (%),
            'formula': 使用的公式,
            'components': 组成部分详情
        }
    """
    # 参数验证
    if t2 < 0:
        raise ValueError("T2不能为负")
    
    if annual_salary <= 0:
        raise ValueError("年薪必须大于0")
    
    # 双逻辑斯蒂函数参数
    L1 = 0.0      # 最低税率
    L2 = 7.0      # 中档税率
    L3 = 7.0      # 高收入附加税率
    T2_mid = 5.0  # T2中值
    w_high = 500000  # 高收入阈值
    k1 = 2.0      # T2敏感度
    k2 = 0.00001  # 收入敏感度（非常小，使曲线平缓）
    
    # 第一部分：基于T2的逻辑斯蒂函数
    try:
        component1 = L1 + (L2 - L1) / (1 + math.exp(-k1 * (t2 - T2_mid)))
    except OverflowError:
        # 处理指数溢出
        if t2 > T2_mid:
            component1 = L1 + (L2 - L1)
        else:
            component1 = L1
    
    # 第二部分：基于收入的逻辑斯蒂函数
    try:
        component2 = L3 / (1 + math.exp(-k2 * (annual_salary - w_high)))
    except OverflowError:
        # 处理指数溢出
        if annual_salary > w_high:
            component2 = L3
        else:
            component2 = 0
    
    # 综合计算
    t3 = component1 + component2
    
    # 限制在0%-14%范围内
    t3 = max(0.0, min(14.0, t3))
    
    # 年龄调整（接近退休年龄可能有优惠）
    if age >= 55:
        age_discount = (60 - age) * 0.02  # 每年降低0.02%
        t3 = max(0, t3 - age_discount)
    
    return {
        't3': round(t3, 2),
        'formula': 'dual_logistic',
        'components': {
            'baseTax': round(component1, 2),
            'incomeAdjustment': round(component2, 2),
            'ageDiscount': round((60 - age) * 0.02 if age >= 55 else 0, 2),
            'finalRate': round(t3, 2)
        },
        'details': {
            'parameters': {
                'L1': L1,
                'L2': L2,
                'L3': L3,
                'T2_mid': T2_mid,
                'w_high': w_high,
                'k1': k1,
                'k2': k2
            },
            'inputs': {
                't2': t2,
                'annualSalary': annual_salary,
                'age': age
            }
        }
    }


# 测试函数
if __name__ == '__main__':
    # 测试用例
    test_cases = [
        {'t2': 1.4, 'annual_salary': 150000, 'age': 30},
        {'t2': 3.0, 'annual_salary': 80000, 'age': 25},
        {'t2': 5.5, 'annual_salary': 300000, 'age': 40},
        {'t2': 8.0, 'annual_salary': 600000, 'age': 50},
        {'t2': 2.0, 'annual_salary': 120000, 'age': 58},  # 接近退休
    ]
    
    print("T3领取期税率计算测试\n" + "="*60)
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n测试用例 {i}:")
        print(f"输入: T2={case['t2']}%, 年薪={case['annual_salary']}, 年龄={case['age']}")
        result = calculate_t3(**case)
        print(f"T3 = {result['t3']}%")
        print(f"基础税率: {result['components']['baseTax']}%")
        print(f"收入调整: {result['components']['incomeAdjustment']}%")
        if result['components']['ageDiscount'] > 0:
            print(f"年龄优惠: -{result['components']['ageDiscount']}%")
