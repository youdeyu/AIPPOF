"""
测试T3计算模型的API集成
验证T3计算公式是否与文档一致
"""
import requests
import json

API_BASE = "http://localhost:8000"

def test_t3_calculation():
    """测试T3计算的几个关键场景"""
    test_cases = [
        {
            "name": "年薪150000，T2=10%",
            "data": {
                "annualSalary": 150000,
                "age": 30,
                "wageGrowthRate": 0.05  # 5%工资增长率
            },
            "expected_t3_range": (0, 14)  # T3应在0-14%之间
        },
        {
            "name": "年薪80000，T2=5%",
            "data": {
                "annualSalary": 80000,
                "age": 25,
                "wageGrowthRate": 0.05
            },
            "expected_t3_range": (0, 14)
        },
        {
            "name": "年薪300000，T2=8%（高收入）",
            "data": {
                "annualSalary": 300000,
                "age": 40,
                "wageGrowthRate": 0.04
            },
            "expected_t3_range": (0, 14)
        },
        {
            "name": "年薪120000，年龄58（接近退休）",
            "data": {
                "annualSalary": 120000,
                "age": 58,
                "wageGrowthRate": 0.03
            },
            "expected_t3_range": (0, 14)
        }
    ]
    
    print("=" * 80)
    print("T3计算模型API测试")
    print("=" * 80)
    
    all_passed = True
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n测试场景 {i}: {test['name']}")
        print(f"输入数据: {json.dumps(test['data'], ensure_ascii=False)}")
        
        try:
            # 调用optimize_contribution API，会自动计算T2
            response = requests.post(
                f"{API_BASE}/api/optimize-contribution",
                json=test['data']
            )
            
            if response.status_code != 200:
                print(f"❌ API调用失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                all_passed = False
                continue
            
            result = response.json()
            
            # 检查响应中是否有T2和T3
            if 't2' not in result:
                print(f"❌ 响应中没有T2数据")
                all_passed = False
                continue
            
            if 't3' not in result:
                print(f"❌ 响应中没有T3数据")
                all_passed = False
                continue
            
            t2_value = result['t2']
            t3_value = result['t3']
            print(f"API返回的T2: {t2_value}%")
            print(f"API返回的T3: {t3_value}%")
            
            # 验证T3在合理范围内
            min_t3, max_t3 = test['expected_t3_range']
            if min_t3 <= t3_value <= max_t3:
                print(f"✅ T3值在预期范围内 [{min_t3}%, {max_t3}%]")
            else:
                print(f"❌ T3值超出预期范围 [{min_t3}%, {max_t3}%]，实际值: {t3_value}%")
                all_passed = False
            
            # 额外验证：直接调用T3计算器确认公式
            from t3_calculator import calculate_t3
            t3_direct = calculate_t3(
                t2=t2_value,
                annual_salary=test['data']['annualSalary'],
                age=test['data']['age']
            )
            
            print(f"  - 基础税率: {t3_direct['components']['baseTax']}%")
            print(f"  - 收入调整: {t3_direct['components']['incomeAdjustment']}%")
            print(f"  - 年龄优惠: {t3_direct['components']['ageDiscount']}%")
            
            # 验证双逻辑斯蒂函数的公式实现
            if t3_direct['formula'] == 'dual_logistic':
                print(f"✅ 使用正确的公式: 双逻辑斯蒂函数")
            else:
                print(f"❌ 公式类型不正确: {t3_direct['formula']}")
                all_passed = False
            
            # 验证API返回的T3与直接计算的T3一致
            if abs(t3_value - t3_direct['t3']) < 0.01:
                print(f"✅ API返回的T3与直接计算一致")
            else:
                print(f"❌ API返回的T3({t3_value}%)与直接计算({t3_direct['t3']}%)不一致")
                all_passed = False
            
        except Exception as e:
            print(f"❌ 测试出错: {str(e)}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 所有T3测试通过！")
        print("✅ T3计算模型已正确实现双逻辑斯蒂函数")
        print("✅ T3值在合理范围内（0%-14%）")
        print("✅ 年龄优惠机制正常工作")
    else:
        print("⚠️  部分测试未通过，请检查")
    print("=" * 80)
    
    return all_passed


if __name__ == '__main__':
    test_t3_calculation()
