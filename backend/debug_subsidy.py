"""
模拟前端请求，调试 calculate_subsidy 错误
"""
import sys
sys.path.append('.')

from api.subsidy_calculator import calculate_subsidy, SubsidyParams, get_subsidy_tier_info

print("="*70)
print("测试 1: 直接调用 calculate_subsidy（正常情况）")
print("="*70)
try:
    result = calculate_subsidy(
        annual_salary=80000,
        contribution_amount=10000
    )
    print("✅ 成功！")
    print(f"补贴: {result['subsidy']}")
    print(f"触发: {result['triggered']}")
except Exception as e:
    print(f"❌ 失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("测试 2: 调用 get_subsidy_tier_info")
print("="*70)
try:
    tier_info = get_subsidy_tier_info(80000)
    print("✅ 成功！")
    print(f"档位: {tier_info['tier']}")
    print(f"说明: {tier_info['description']}")
except Exception as e:
    print(f"❌ 失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("测试 3: 检查 SubsidyParams 属性")
print("="*70)
try:
    params = SubsidyParams()
    print(f"✅ SubsidyParams 创建成功")
    print(f"low_income_cut = {params.low_income_cut}")
    print(f"ratio_low = {params.ratio_low}")
    print(f"base_grant = {params.base_grant}")
    
    # 检查所有属性
    print("\n所有属性:")
    for attr in dir(params):
        if not attr.startswith('_'):
            print(f"  {attr} = {getattr(params, attr)}")
            
except Exception as e:
    print(f"❌ 失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("测试 4: 模拟API调用场景（dict参数）")
print("="*70)
try:
    # 模拟前端可能发送的数据
    data = {
        'annualSalary': 80000,
        'contributionAmount': 10000
    }
    
    result = calculate_subsidy(
        annual_salary=data['annualSalary'],
        contribution_amount=data['contributionAmount']
    )
    
    print("✅ 成功！")
    print(f"补贴: {result['subsidy']}")
    
    # 模拟scenario循环
    scenarios = [
        {'contribution': 6000},
        {'contribution': 10000},
        {'contribution': 12000}
    ]
    
    for i, scenario in enumerate(scenarios):
        subsidy_result = calculate_subsidy(
            annual_salary=data['annualSalary'],
            contribution_amount=scenario['contribution']
        )
        print(f"\nScenario {i+1} (缴费¥{scenario['contribution']}): 补贴¥{subsidy_result['subsidy']}")
        
except Exception as e:
    print(f"❌ 失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("所有测试完成！")
print("="*70)
