"""
测试 /api/diagnose-history 端点
"""
import requests
import json

# 测试数据 (使用后端期望的字段名)
test_payload = {
    "historyData": [
        {"year": 2022, "salary": 120000, "contribution": 10000},
        {"year": 2023, "salary": 135000, "contribution": 11000},
        {"year": 2024, "salary": 150000, "contribution": 12000}
    ],
    "age": 35
}

print("🔍 测试 PathB 历史诊断API")
print("="*50)
print(f"请求数据: {json.dumps(test_payload, indent=2, ensure_ascii=False)}")
print("="*50)

try:
    response = requests.post(
        'http://localhost:8000/api/diagnose-history',
        json=test_payload,
        timeout=10
    )
    
    print(f"✅ HTTP状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("\n📊 API响应数据:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
        
        print("\n" + "="*50)
        print("核心指标验证:")
        print(f"  累积T2: {data.get('cumulative_t2', 'N/A')}%")
        print(f"  效率评分: {data.get('efficiency_score', 'N/A')}")
        print(f"  总补贴: ¥{data.get('total_subsidy', 'N/A')}")
        print(f"  预测T3: {data.get('predicted_t3', 'N/A')}%")
        print(f"  潜在收益: ¥{data.get('potential_gain', 'N/A')}")
        print(f"  NPV提升: {data.get('npv_improvement', 'N/A')}%")
        print(f"  推荐缴费额: ¥{data.get('recommended_amount', 'N/A')}")
        
        print("\n历史明细数据:")
        if 'historical_details' in data:
            for item in data['historical_details']:
                print(f"  {item['year']}年: 年薪¥{item['salary']:,}, 缴费¥{item['contribution']:,}, T2={item['t2']}%, 补贴¥{item['subsidy']}")
        
        print("\n✅ API测试成功!")
    else:
        print(f"❌ API返回错误: {response.text}")
        
except requests.exceptions.ConnectionError:
    print("❌ 无法连接到后端服务器 (http://localhost:8000)")
    print("   请确保后端服务正在运行: python backend/main.py")
except Exception as e:
    print(f"❌ 测试失败: {str(e)}")
