"""T3 计算接口（兼容）

此模块仍保留原函数名，但将实现委托给 `api.policy_utils.calculate_t3`，
以便集中维护 T3 的新逻辑并保证向后兼容。
"""
from api.policy_utils import calculate_t3 as _calculate_t3


def calculate_t3(t2, annual_salary, age):
    """兼容旧签名的包装，返回和旧实现相同格式的 dict。"""
    return _calculate_t3(t2, annual_salary, age)


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
