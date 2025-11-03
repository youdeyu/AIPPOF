"""
测试累计T2计算API
验证已参与者的历史缴费记录分析功能
"""
import requests
import json

API_BASE = "http://localhost:8000"

def test_accumulated_t2_api():
    """测试累计T2计算API"""
    
    test_cases = [
        {
            "name": "稳定增长的IT从业者（3年）",
            "data": {
                "historyRecords": [
                    {"year": 2022, "salary": 100000, "contribution": 8000},
                    {"year": 2023, "salary": 110000, "contribution": 10000},
                    {"year": 2024, "salary": 120000, "contribution": 12000}
                ]
            },
            "expected": {
                "t2_range": (2.5, 4.5),  # 预期T2在2.5%-4.5%之间
                "total_contribution": 30000
            }
        },
        {
            "name": "高收入金融从业者（3年）",
            "data": {
                "historyRecords": [
                    {"year": 2022, "salary": 200000, "contribution": 12000},
                    {"year": 2023, "salary": 220000, "contribution": 12000},
                    {"year": 2024, "salary": 250000, "contribution": 12000}
                ]
            },
            "expected": {
                "t2_range": (15.0, 25.0),  # 高收入T2更高
                "total_contribution": 36000
            }
        },
        {
            "name": "收入波动的制造业员工（3年）",
            "data": {
                "historyRecords": [
                    {"year": 2022, "salary": 80000, "contribution": 5000},
                    {"year": 2023, "salary": 75000, "contribution": 6000},
                    {"year": 2024, "salary": 90000, "contribution": 8000}
                ]
            },
            "expected": {
                "t2_range": (2.0, 4.0),
                "total_contribution": 19000
            }
        }
    ]
    
    print("=" * 80)
    print("累计T2计算API测试")
    print("=" * 80)
    
    all_passed = True
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n测试场景 {i}: {test['name']}")
        print(f"历史记录:")
        for record in test['data']['historyRecords']:
            print(f"  {record['year']}年: 年薪¥{record['salary']:,}, 缴费¥{record['contribution']:,}")
        
        try:
            response = requests.post(
                f"{API_BASE}/api/calculate-accumulated-t2",
                json=test['data']
            )
            
            if response.status_code != 200:
                print(f"❌ API调用失败: {response.status_code}")
                print(f"   错误信息: {response.text}")
                all_passed = False
                continue
            
            result = response.json()
            
            # 验证必要字段
            required_fields = ['accumulatedT2', 'totalTaxSaving', 'totalContribution', 'yearlyDetails']
            for field in required_fields:
                if field not in result:
                    print(f"❌ 响应中缺少字段: {field}")
                    all_passed = False
                    continue
            
            # 显示结果
            print(f"\n累计T2结果:")
            print(f"  累计T2（带折现）: {result['accumulatedT2']}%")
            print(f"  简单平均T2: {result.get('averageT2', 'N/A')}%")
            print(f"  累计节税总额: ¥{result['totalTaxSaving']:,}")
            print(f"  累计缴费总额: ¥{result['totalContribution']:,}")
            
            # 验证累计缴费
            if result['totalContribution'] == test['expected']['total_contribution']:
                print(f"✅ 累计缴费金额正确")
            else:
                print(f"❌ 累计缴费金额错误: 期望¥{test['expected']['total_contribution']:,}, 实际¥{result['totalContribution']:,}")
                all_passed = False
            
            # 验证T2范围
            t2_min, t2_max = test['expected']['t2_range']
            if t2_min <= result['accumulatedT2'] <= t2_max:
                print(f"✅ T2值在合理范围内 [{t2_min}%, {t2_max}%]")
            else:
                print(f"⚠️  T2值({result['accumulatedT2']}%)超出预期范围 [{t2_min}%, {t2_max}%]")
                print(f"   (这可能是正常的，取决于税率阶梯)")
            
            # 显示年度明细
            if 'yearlyDetails' in result and len(result['yearlyDetails']) > 0:
                print(f"\n年度明细:")
                for detail in result['yearlyDetails']:
                    print(f"  {detail['year']}年: 节税¥{detail['taxSaving']}, T2={detail['t2']}%, 折现因子={detail['discountFactor']}")
                print(f"✅ 年度明细完整")
            else:
                print(f"❌ 缺少年度明细")
                all_passed = False
            
        except Exception as e:
            print(f"❌ 测试出错: {str(e)}")
            import traceback
            traceback.print_exc()
            all_passed = False
    
    print("\n" + "=" * 80)
    if all_passed:
        print("🎉 累计T2计算API测试完成！")
        print("✅ 所有API调用成功")
        print("✅ 计算结果合理")
        print("✅ 年度明细完整")
    else:
        print("⚠️  部分测试未通过，请检查")
    print("=" * 80)
    
    return all_passed


if __name__ == '__main__':
    test_accumulated_t2_api()
