"""
测试AI诊断建议API
"""
import requests
import json

API_BASE = "http://localhost:8000"

def test_ai_suggestions():
    """测试AI诊断建议API"""
    print("="*70)
    print("测试 /api/ai-suggestions API")
    print("="*70)
    
    # 测试用例1: 中等效率场景
    test_data_1 = {
        "historyData": [
            {"year": 2022, "salary": 120000, "contribution": 8000},
            {"year": 2023, "salary": 135000, "contribution": 10000},
            {"year": 2024, "salary": 150000, "contribution": 12000}
        ],
        "age": 35
    }
    
    print("\n📊 测试用例1: 中等效率场景")
    print(f"   历史数据: 3年,年薪12-15万,缴费8k-12k")
    print(f"   当前年龄: 35岁")
    
    response = requests.post(
        f"{API_BASE}/api/ai-suggestions",
        json=test_data_1,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ API调用成功")
        print(f"   优先级: {result['priority'].upper()}")
        print(f"   建议数量: {result['summary']['totalSuggestions']}条")
        print(f"   关键问题: {result['summary']['criticalIssues']}个")
        print(f"   优化潜力: {result['summary']['optimizationPotential'].upper()}")
        
        print(f"\n📋 详细建议:")
        for i, suggestion in enumerate(result['suggestions'][:3], 1):  # 只显示前3条
            print(f"   {i}. {suggestion['icon']} {suggestion['title']}")
            print(f"      {suggestion['description'][:60]}...")
        
        if result['riskWarnings']:
            print(f"\n⚠️  风险提示: {len(result['riskWarnings'])}个")
            for warning in result['riskWarnings']:
                print(f"   {warning['icon']} {warning['title']}")
        
        print(f"\n💰 预期收益:")
        benefit = result['expectedBenefit']
        print(f"   年均收益: ¥{benefit['annualGain']:,.0f}")
        print(f"   终身收益: ¥{benefit['lifetimeGain']:,.0f}")
        print(f"   NPV提升: {benefit['npvImprovement']:.1f}%")
    else:
        print(f"❌ API调用失败: {response.status_code}")
        print(f"   错误信息: {response.text}")
    
    # 测试用例2: 低效率场景
    print("\n" + "="*70)
    print("📊 测试用例2: 低效率场景")
    
    test_data_2 = {
        "historyData": [
            {"year": 2022, "salary": 80000, "contribution": 3000},
            {"year": 2023, "salary": 85000, "contribution": 3500},
            {"year": 2024, "salary": 90000, "contribution": 4000}
        ],
        "age": 28
    }
    
    print(f"   历史数据: 3年,年薪8-9万,缴费3k-4k(偏低)")
    print(f"   当前年龄: 28岁")
    
    response = requests.post(
        f"{API_BASE}/api/ai-suggestions",
        json=test_data_2,
        headers={'Content-Type': 'application/json'}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✅ API调用成功")
        print(f"   优先级: {result['priority'].upper()}")
        print(f"   建议数量: {result['summary']['totalSuggestions']}条")
        print(f"   优化潜力: {result['summary']['optimizationPotential'].upper()}")
        
        print(f"\n📋 关键建议:")
        for suggestion in result['suggestions'][:2]:
            print(f"   {suggestion['icon']} {suggestion['title']}")
            print(f"      💡 {suggestion['action']}")
    else:
        print(f"❌ API调用失败: {response.status_code}")
    
    print("\n" + "="*70)
    print("测试完成")
    print("="*70)


if __name__ == '__main__':
    try:
        test_ai_suggestions()
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到后端服务器")
        print("   请确保后端服务器正在运行: python main.py")
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
