"""
测试动态上限超额检测功能
"""
import sys
sys.path.insert(0, '.')

from api.history_diagnosis import diagnose_history

print("="*70)
print("测试案例：用户缴费超出动态上限")
print("="*70)

# 测试案例：年薪24万，T2=20%时，动态上限≈19,200
# 如果用户缴费1.5万，应该被检测为合理
# 如果用户缴费3万，应该被检测为超限

test_cases = [
    {
        'name': '案例1: 缴费在动态上限内',
        'data': [
            {'year': 2024, 'salary': 240000, 'contribution': 15000}  # 15k < 19.2k
        ],
        'expected': '不应超限'
    },
    {
        'name': '案例2: 缴费超出动态上限',
        'data': [
            {'year': 2024, 'salary': 240000, 'contribution': 30000}  # 30k > 19.2k
        ],
        'expected': '应检测到超限'
    },
    {
        'name': '案例3: 低T2时缴费接近上限',
        'data': [
            {'year': 2024, 'salary': 100000, 'contribution': 8000}  # 8k vs ~8k
        ],
        'expected': '应合理'
    }
]

for case in test_cases:
    print(f"\n{case['name']}")
    print("-" * 70)
    print(f"预期结果: {case['expected']}")
    
    result = diagnose_history(case['data'], age=30)
    
    # 输出关键信息
    print(f"\n诊断结果:")
    print(f"  累积T2: {result['cumulativeT2']:.2f}%")  # 使用camelCase字段名
    
    if 'exceedsDynamicCap' in result['diagnosis']:
        exceeds = result['diagnosis']['exceedsDynamicCap']
        print(f"  超出动态上限: {'是' if exceeds else '否'}")
        
        if exceeds and 'capWarnings' in result['diagnosis']:
            warnings = result['diagnosis']['capWarnings']
            print(f"  超限记录数: {len(warnings)}条")
            for warning in warnings:
                print(f"    {warning['year']}年: 缴费¥{warning['contribution']:,} > "
                      f"动态上限¥{warning['dynamic_cap']:,.0f}, "
                      f"超出¥{warning['excess']:,.0f}")
    
    print(f"  诊断消息: {result['diagnosis'].get('message', '无')}")

print("\n" + "="*70)
print("测试完成")
print("="*70)
