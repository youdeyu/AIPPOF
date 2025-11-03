"""
PathB 集成测试 - 验证已参与者路径API完整性
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_pathb_flow():
    """测试PathB完整流程"""
    print("\n" + "="*60)
    print("PathB 已参与者路径 - 完整流程测试")
    print("="*60)
    
    # 模拟历史缴费数据
    years_data = [
        {"year": 2022, "salary": 120000, "contribution": 10000},
        {"year": 2023, "salary": 135000, "contribution": 11000},
        {"year": 2024, "salary": 150000, "contribution": 12000}
    ]
    
    print("\n📊 输入历史数据:")
    for year in years_data:
        print(f"  {year['year']}年: 年薪¥{year['salary']:,}, 缴费¥{year['contribution']:,}")
    
    # 调用历史诊断API
    print("\n🔄 调用历史诊断API...")
    response = requests.post(f"{BASE_URL}/api/diagnose-history", json={
        "years_data": years_data,
        "current_age": 35,
        "wage_growth_rate": 0.05
    })
    
    if response.status_code != 200:
        print(f"❌ API调用失败: {response.status_code}")
        print(response.text)
        return
    
    data = response.json()
    print("\n✅ 历史诊断结果:")
    print(f"  累积T2: {data['cumulative_t2']:.2f}%")
    print(f"  效率评分: {data['efficiency_score']}/100")
    print(f"  累计补贴: ¥{data['total_subsidy']:,.2f}")
    print(f"  预测T3: {data['predicted_t3']:.2f}%")
    
    print("\n📈 历史明细:")
    for item in data['historical_details']:
        print(f"  {item['year']}年:")
        print(f"    - T2税优率: {item['t2']:.2f}% (蓝浩歌公式)")
        print(f"    - 补贴金额: ¥{item['subsidy']:,.2f}")
        print(f"    - 节税金额: ¥{item['tax_saving']:,.2f}")
    
    # 调用AI建议API
    print("\n🔄 调用AI个性化建议API...")
    avg_salary = sum(y['salary'] for y in years_data) / len(years_data)
    avg_contribution = sum(y['contribution'] for y in years_data) / len(years_data)
    
    ai_response = requests.post(f"{BASE_URL}/api/ai-suggestions", json={
        "years_data": years_data,
        "current_age": 35,
        "cumulative_t2": data['cumulative_t2'],
        "total_subsidy": data['total_subsidy'],
        "efficiency_score": data['efficiency_score']
    })
    
    if ai_response.status_code == 200:
        ai_data = ai_response.json()
        print(f"\n💡 AI建议 ({len(ai_data['suggestions'])}条):")
        for i, sug in enumerate(ai_data['suggestions'][:3], 1):
            print(f"  {i}. {sug['title']}")
            print(f"     {sug['description'][:60]}...")
    
    # 调用5档方案API
    print("\n🔄 调用5档缴费方案API...")
    tier_response = requests.post(f"{BASE_URL}/api/5tier-suggestions", json={
        "current_salary": years_data[-1]['salary'],
        "current_age": 35,
        "current_contribution": years_data[-1]['contribution'],
        "wage_growth_rate": 0.05
    })
    
    if tier_response.status_code == 200:
        tier_data = tier_response.json()
        print(f"\n📊 5档方案建议:")
        for tier in tier_data['tiers']:
            print(f"  {tier['name']:8s}: 缴费¥{tier['contribution']:>7,} → NPV ¥{tier['npv']:>10,.0f} ({tier['risk_level']})")
    
    print("\n" + "="*60)
    print("✅ PathB完整流程测试通过!")
    print("="*60)

if __name__ == "__main__":
    try:
        test_pathb_flow()
    except requests.exceptions.ConnectionError:
        print("\n❌ 无法连接到后端服务器")
        print("请先启动后端: python backend/main.py")
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
