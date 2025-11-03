"""
测试所有新增API端点
"""
import requests
import json

BASE_URL = 'http://localhost:8000'

def test_lifecycle_data():
    """测试全生命周期数据生成"""
    print("\n" + "="*60)
    print("测试1: 全生命周期数据生成 API")
    print("="*60)
    
    data = {
        'age': 30,
        'annualSalary': 150000,
        'contributionAmount': 9500,
        't2': 1.4,
        't3': 1.2,
        'wageGrowthRate': 3.9
    }
    
    response = requests.post(f'{BASE_URL}/api/lifecycle-data', json=data)
    result = response.json()
    
    if result.get('success'):
        print("✅ API调用成功")
        print(f"缴费期年数: {result['summary']['contributionPhase']['years']}")
        print(f"总缴费额: ¥{result['summary']['contributionPhase']['totalContribution']:,.2f}")
        print(f"总税收节省: ¥{result['summary']['contributionPhase']['totalTaxSavings']:,.2f}")
        print(f"总补贴: ¥{result['summary']['contributionPhase']['totalSubsidies']:,.2f}")
        print(f"退休账户: ¥{result['summary']['contributionPhase']['finalAccountBalance']:,.2f}")
        print(f"领取期税负: ¥{result['summary']['withdrawalPhase']['totalTax']:,.2f}")
        print(f"NPV: ¥{result['summary']['overall']['npv']:,.2f}")
        print(f"ROI: {result['summary']['overall']['roi']}%")
    else:
        print(f"❌ API调用失败: {result.get('error')}")


def test_comparison_scenarios():
    """测试缴费额对比场景"""
    print("\n" + "="*60)
    print("测试2: 缴费额对比场景 API")
    print("="*60)
    
    data = {
        'age': 30,
        'annualSalary': 150000,
        't2': 1.4,
        't3': 1.2,
        'wageGrowthRate': 3.9
    }
    
    response = requests.post(f'{BASE_URL}/api/comparison-scenarios', json=data)
    result = response.json()
    
    if result.get('success'):
        print("✅ API调用成功")
        for scenario in result['scenarios']:
            print(f"{scenario['name']}: NPV = ¥{scenario['data']['summary']['overall']['npv']:,.2f}")
    else:
        print(f"❌ API调用失败: {result.get('error')}")


def test_risk_assessment():
    """测试T3风险评估"""
    print("\n" + "="*60)
    print("测试3: T3风险评估 API")
    print("="*60)
    
    # 测试普通用户
    data1 = {
        'annualSalary': 150000,
        't2': 1.4,
        't3': 1.2,
        'contributionAmount': 9500,
        'age': 30
    }
    
    response1 = requests.post(f'{BASE_URL}/api/risk-assessment', json=data1)
    result1 = response1.json()
    
    if result1.get('success'):
        print("✅ 普通用户风险评估:")
        print(f"   风险等级: {result1['riskLabel']} ({result1['riskScore']}分)")
        print(f"   退出概率: {result1['exitProbability']}%")
        print(f"   警告数量: {len(result1['warnings'])}")
    
    # 测试高风险用户
    data2 = {
        'annualSalary': 600000,
        't2': 8.0,
        't3': 12.5,
        'contributionAmount': 12000,
        'age': 45
    }
    
    response2 = requests.post(f'{BASE_URL}/api/risk-assessment', json=data2)
    result2 = response2.json()
    
    if result2.get('success'):
        print("\n✅ 高收入用户风险评估:")
        print(f"   风险等级: {result2['riskLabel']} ({result2['riskScore']}分)")
        print(f"   退出概率: {result2['exitProbability']}%")
        print(f"   警告数量: {len(result2['warnings'])}")
        for i, warning in enumerate(result2['warnings'][:3], 1):
            print(f"   [{warning['type']}] {warning['message']}")


def test_optimal_cap():
    """测试最优缴费上限"""
    print("\n" + "="*60)
    print("测试4: 最优缴费上限 API")
    print("="*60)
    
    test_cases = [
        {'annualSalary': 150000, 't2': 1.4, 'age': 30, 'label': '普通收入'},
        {'annualSalary': 500000, 't2': 8.0, 'age': 45, 'label': '高收入'},
        {'annualSalary': 1000000, 't2': 12.0, 'age': 50, 'label': '超高收入'}
    ]
    
    for case in test_cases:
        response = requests.post(f'{BASE_URL}/api/optimal-cap', json=case)
        result = response.json()
        
        if result.get('success'):
            print(f"\n✅ {case['label']} (年薪¥{case['annualSalary']:,}):")
            print(f"   最优上限: ¥{result['optimalCap']:,}")
            print(f"   预估T3: {result['estimatedT3']}%")
            print(f"   理由: {result['reason']}")


def test_fiscal_analysis():
    """测试财政影响分析"""
    print("\n" + "="*60)
    print("测试5: 财政影响分析 API")
    print("="*60)
    
    data = {
        'age': 30,
        'annualSalary': 150000,
        'contributionAmount': 9500,
        't2': 1.4,
        't3': 1.2,
        'wageGrowthRate': 3.9
    }
    
    response = requests.post(f'{BASE_URL}/api/fiscal-analysis', json=data)
    result = response.json()
    
    if result.get('success'):
        print("✅ API调用成功")
        print(f"政府成本: ¥{result['governmentCost']:,.2f}")
        print(f"  - 补贴现值: ¥{result['subsidyPV']:,.2f}")
        print(f"  - 税收损失: ¥{result['taxLossPV']:,.2f}")
        print(f"政府收入: ¥{result['governmentRevenue']:,.2f}")
        print(f"财政平衡: ¥{result['fiscalBalance']:,.2f} ({result['fiscalBalanceRate']}%)")
        print(f"是否财政中性: {'✅ 是' if result['isFiscalNeutral'] else '❌ 否'}")
        print(f"可持续性: {result['sustainability']}")


def test_fiscal_optimize():
    """测试财政中性优化"""
    print("\n" + "="*60)
    print("测试6: 财政中性优化 API")
    print("="*60)
    
    data = {
        'age': 30,
        'annualSalary': 150000,
        't2': 1.4,
        'wageGrowthRate': 3.9
    }
    
    response = requests.post(f'{BASE_URL}/api/fiscal-optimize', json=data)
    result = response.json()
    
    if result.get('success'):
        print("✅ API调用成功")
        print(f"最优缴费额: ¥{result['optimalContribution']:,}")
        print(f"用户NPV: ¥{result['userNPV']:,.2f}")
        print(f"财政平衡: ¥{result['fiscalBalance']:,.2f}")
        print(f"是否财政中性: {'✅ 是' if result['isFiscalNeutral'] else '❌ 否'}")
        print(f"优化理由: {result['reason']}")


def main():
    print("\n" + "🚀"*30)
    print("AIPPOF 新增API端点测试")
    print("🚀"*30)
    
    try:
        # 测试服务器连接
        response = requests.get(f'{BASE_URL}/')
        if response.status_code == 200:
            print("✅ 后端服务器连接成功")
            api_info = response.json()
            print(f"API版本: {api_info['version']}")
            print(f"端点数量: {len(api_info['endpoints'])}")
        else:
            print("❌ 后端服务器连接失败")
            return
    except Exception as e:
        print(f"❌ 无法连接到后端服务器: {e}")
        return
    
    # 运行所有测试
    test_lifecycle_data()
    test_comparison_scenarios()
    test_risk_assessment()
    test_optimal_cap()
    test_fiscal_analysis()
    test_fiscal_optimize()
    
    print("\n" + "="*60)
    print("✅ 所有API测试完成!")
    print("="*60 + "\n")


if __name__ == '__main__':
    main()
