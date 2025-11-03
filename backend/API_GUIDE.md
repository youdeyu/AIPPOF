# AIPPOF API 使用指南

## 📚 目录

1. [快速开始](#快速开始)
2. [PathA API - 新参与者](#patha-api---新参与者)
3. [PathB API - 已参与者](#pathb-api---已参与者)
4. [核心计算API](#核心计算api)
5. [错误处理](#错误处理)
6. [最佳实践](#最佳实践)

---

## 快速开始

### 基础信息

- **Base URL**: `http://localhost:8000`
- **Content-Type**: `application/json`
- **认证**: 暂无需要

### 健康检查

```bash
curl http://localhost:8000/health
```

**响应**:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-03T10:45:00Z"
}
```

---

## PathA API - 新参与者

### 完整流程示例

#### 步骤1: 预测工资增长率

```bash
curl -X POST http://localhost:8000/api/predict-wage-growth \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "annualSalary": 150000,
    "industry": "it",
    "jobLevel": "intermediate"
  }'
```

**响应**:
```json
{
  "predicted_growth_rate": 5.65,
  "confidence": 0.85,
  "industry_average": 5.0,
  "methodology": "base+ai+web",
  "factors": {
    "base_growth": 5.2,
    "ai_adjusted_growth": 6.1,
    "web_search_growth": 5.5
  },
  "ai_insights": [
    "IT行业持续高增长趋势",
    "中级岗位晋升空间较大"
  ]
}
```

#### 步骤2: 获取优化方案

```bash
curl -X POST http://localhost:8000/api/optimize-contribution \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "annualSalary": 150000,
    "wageGrowthRate": 5.65
  }'
```

**响应**:
```json
{
  "scenarios": [
    {
      "name": "保守型",
      "contribution": 7200,
      "predictedT2": 10.0,
      "subsidy": 0,
      "npv": 37176.67
    },
    {
      "name": "均衡型",
      "contribution": 9600,
      "predictedT2": 10.0,
      "subsidy": 0,
      "npv": 49568.90,
      "recommended": true
    },
    {
      "name": "激进型",
      "contribution": 12000,
      "predictedT2": 10.0,
      "subsidy": 0,
      "npv": 61961.12
    }
  ],
  "t2": 10.0,
  "t3": 7.2,
  "cap": 12000,
  "subsidyTierInfo": {
    "tier": "high_income",
    "subsidy": 0,
    "reason": "年薪超过15万,补贴归零"
  }
}
```

### Python示例

```python
import requests

# 1. 预测工资增长
response = requests.post(
    'http://localhost:8000/api/predict-wage-growth',
    json={
        'age': 30,
        'annualSalary': 150000,
        'industry': 'it',
        'jobLevel': 'intermediate'
    }
)
growth_data = response.json()
growth_rate = growth_data['predicted_growth_rate']

# 2. 获取优化方案
response = requests.post(
    'http://localhost:8000/api/optimize-contribution',
    json={
        'age': 30,
        'annualSalary': 150000,
        'wageGrowthRate': growth_rate
    }
)
scenarios = response.json()

# 3. 选择推荐方案
recommended = next(s for s in scenarios['scenarios'] if s.get('recommended'))
print(f"推荐缴费: ¥{recommended['contribution']:,}")
print(f"预期NPV: ¥{recommended['npv']:,.2f}")
```

### JavaScript示例

```javascript
// 使用 fetch API
async function getOptimizedPlan(age, salary, industry, jobLevel) {
  // 1. 预测工资增长
  const growthResponse = await fetch('http://localhost:8000/api/predict-wage-growth', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ age, annualSalary: salary, industry, jobLevel })
  });
  const growthData = await growthResponse.json();
  
  // 2. 获取优化方案
  const optimizeResponse = await fetch('http://localhost:8000/api/optimize-contribution', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      age,
      annualSalary: salary,
      wageGrowthRate: growthData.predicted_growth_rate
    })
  });
  const scenarios = await optimizeResponse.json();
  
  return scenarios;
}

// 使用
getOptimizedPlan(30, 150000, 'it', 'intermediate')
  .then(data => {
    console.log('T2:', data.t2);
    console.log('T3:', data.t3);
    console.log('上限:', data.cap);
    console.log('方案:', data.scenarios);
  });
```

---

## PathB API - 已参与者

### 完整流程示例

#### 步骤1: 历史诊断

```bash
curl -X POST http://localhost:8000/api/diagnose-history \
  -H "Content-Type: application/json" \
  -d '{
    "historyData": [
      {"year": 2022, "salary": 120000, "contribution": 8000},
      {"year": 2023, "salary": 135000, "contribution": 10000},
      {"year": 2024, "salary": 150000, "contribution": 12000}
    ],
    "age": 35
  }'
```

**响应**:
```json
{
  "efficiencyScore": 75,
  "cumulativeT2": 2.5,
  "totalSubsidy": 0,
  "predictedT3": 5.2,
  "historicalDetails": [
    {
      "year": 2022,
      "salary": 120000,
      "contribution": 8000,
      "t2": 2.3,
      "subsidy": 0,
      "efficiency": 72
    },
    {
      "year": 2023,
      "salary": 135000,
      "contribution": 10000,
      "t2": 2.5,
      "subsidy": 0,
      "efficiency": 76
    },
    {
      "year": 2024,
      "salary": 150000,
      "contribution": 12000,
      "t2": 2.7,
      "subsidy": 0,
      "efficiency": 78
    }
  ]
}
```

#### 步骤2: AI建议

```bash
curl -X POST http://localhost:8000/api/ai-suggestions \
  -H "Content-Type: application/json" \
  -d '{
    "historyData": [
      {"year": 2022, "salary": 120000, "contribution": 8000},
      {"year": 2023, "salary": 135000, "contribution": 10000},
      {"year": 2024, "salary": 150000, "contribution": 12000}
    ],
    "currentAge": 35
  }'
```

**响应**:
```json
{
  "priority": "medium",
  "suggestions": [
    {
      "type": "optimize",
      "priority": "medium",
      "icon": "📊",
      "title": "可进一步优化",
      "description": "您的缴费效率评分75分,良好但仍有提升空间",
      "action": "建议调整缴费额至¥11,000/年,预期可提升NPV约8.5%"
    },
    {
      "type": "tax_efficiency",
      "priority": "medium",
      "icon": "💰",
      "title": "优化税优利用",
      "description": "当前T2为2.5%,可进一步提升至3.0%",
      "action": "适当增加缴费额以充分利用税收优惠"
    }
  ],
  "actionPlan": {
    "increaseContribution": {
      "from": 10000,
      "to": 11000,
      "reason": "提高缴费额以充分利用税收优惠"
    }
  },
  "riskWarnings": [
    "注意流动性风险,确保有足够应急资金"
  ],
  "expectedBenefit": {
    "annualGain": 1200,
    "lifetimeGain": 30000,
    "npvImprovement": 8.5,
    "timeHorizon": 25
  }
}
```

#### 步骤3: 5档方案

```bash
curl -X POST http://localhost:8000/api/5tier-suggestions \
  -H "Content-Type: application/json" \
  -d '{
    "currentAge": 35,
    "annualSalary": 150000,
    "currentContribution": 10000
  }'
```

**响应**:
```json
{
  "tiers": [
    {
      "tier": "conservative",
      "name": "保守型",
      "icon": "🛡️",
      "contribution": 3600,
      "capUtilization": 30,
      "npv": {"total_npv": 8443.78, "years_to_retirement": 25},
      "characteristics": ["低风险、低收益", "资金灵活度高"],
      "suitableFor": "风险厌恶、需要高流动性者",
      "riskLevel": "低",
      "annualBenefit": 337.75
    },
    {
      "tier": "stable",
      "name": "稳健型",
      "icon": "📊",
      "contribution": 6000,
      "capUtilization": 50,
      "npv": {"total_npv": 14072.97, "years_to_retirement": 25},
      "riskLevel": "中低",
      "annualBenefit": 562.92
    },
    {
      "tier": "balanced",
      "name": "均衡型",
      "icon": "⚖️",
      "contribution": 8400,
      "capUtilization": 70,
      "npv": {"total_npv": 19702.16, "years_to_retirement": 25},
      "riskLevel": "中",
      "annualBenefit": 788.09,
      "recommended": true
    },
    {
      "tier": "aggressive",
      "name": "积极型",
      "icon": "📈",
      "contribution": 10200,
      "capUtilization": 85,
      "npv": {"total_npv": 23924.05, "years_to_retirement": 25},
      "riskLevel": "中高",
      "annualBenefit": 956.96
    },
    {
      "tier": "maximum",
      "name": "激进型",
      "icon": "🚀",
      "contribution": 11400,
      "capUtilization": 95,
      "npv": {"total_npv": 26738.65, "years_to_retirement": 25},
      "riskLevel": "高",
      "annualBenefit": 1069.55
    }
  ],
  "recommended": "balanced"
}
```

### Python完整流程

```python
import requests

class AIPPOFClient:
    def __init__(self, base_url='http://localhost:8000'):
        self.base_url = base_url
    
    def diagnose_pathb(self, history_data, age):
        """PathB完整诊断流程"""
        # 1. 历史诊断
        diagnosis = requests.post(
            f'{self.base_url}/api/diagnose-history',
            json={'historyData': history_data, 'age': age}
        ).json()
        
        print(f"📊 效率评分: {diagnosis['efficiencyScore']}分")
        print(f"📈 累积T2: {diagnosis['cumulativeT2']}%")
        
        # 2. AI建议
        suggestions = requests.post(
            f'{self.base_url}/api/ai-suggestions',
            json={'historyData': history_data, 'currentAge': age}
        ).json()
        
        print(f"\n💡 AI建议 ({len(suggestions['suggestions'])}条):")
        for s in suggestions['suggestions']:
            print(f"  {s['icon']} {s['title']}")
        
        # 3. 5档方案
        current_salary = history_data[-1]['salary']
        tiers = requests.post(
            f'{self.base_url}/api/5tier-suggestions',
            json={'currentAge': age, 'annualSalary': current_salary}
        ).json()
        
        print(f"\n📊 5档方案:")
        for tier in tiers['tiers']:
            npv = tier['npv']['total_npv']
            print(f"  {tier['icon']} {tier['name']}: ¥{tier['contribution']:,} → NPV ¥{npv:,.2f}")
        
        return {
            'diagnosis': diagnosis,
            'suggestions': suggestions,
            'tiers': tiers
        }

# 使用示例
client = AIPPOFClient()
result = client.diagnose_pathb(
    history_data=[
        {"year": 2022, "salary": 120000, "contribution": 8000},
        {"year": 2023, "salary": 135000, "contribution": 10000},
        {"year": 2024, "salary": 150000, "contribution": 12000}
    ],
    age=35
)
```

---

## 核心计算API

### T2计算

```bash
curl -X POST http://localhost:8000/api/calculate-t2 \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "annualSalary": 150000,
    "wageGrowthRate": 4.5
  }'
```

**响应**:
```json
{
  "t2": 10.0,
  "t1": 20.0,
  "n": 30,
  "formula": "T2 = 12000.00 / 12000 * 100% = 10.00%",
  "details": {
    "contributionYears": 30,
    "returnRate": 1.75,
    "wageGrowthRate": 4.5,
    "marginalTaxRate": 20.0,
    "taxSaving": 12000.0
  }
}
```

### T3计算

```bash
curl -X POST http://localhost:8000/api/calculate-t3 \
  -H "Content-Type: application/json" \
  -d '{
    "t2": 10.0,
    "annualSalary": 150000,
    "age": 30
  }'
```

### 补贴计算

```bash
# 低收入案例
curl -X POST http://localhost:8000/api/calculate-subsidy \
  -H "Content-Type: application/json" \
  -d '{
    "annualSalary": 60000,
    "contributionAmount": 5000
  }'

# 高收入案例 (补贴归零)
curl -X POST http://localhost:8000/api/calculate-subsidy \
  -H "Content-Type: application/json" \
  -d '{
    "annualSalary": 150000,
    "contributionAmount": 12000
  }'
```

**响应** (低收入):
```json
{
  "subsidy": 612.0,
  "tier": "low_income",
  "match_rate": 50.0,
  "taper_factor": 0.245
}
```

**响应** (高收入):
```json
{
  "subsidy": 0,
  "tier": "high_income",
  "match_rate": 0,
  "taper_factor": 0
}
```

### 上限计算

```bash
curl -X POST http://localhost:8000/api/calculate-cap \
  -H "Content-Type: application/json" \
  -d '{
    "annualSalary": 150000,
    "t2Rate": 10.0
  }'
```

---

## 错误处理

### 常见错误

#### 400 - 参数错误

```json
{
  "error": "缺少必填字段: age"
}
```

#### 500 - 服务器错误

```json
{
  "error": "计算错误: division by zero"
}
```

### 错误处理示例

```python
import requests

try:
    response = requests.post(
        'http://localhost:8000/api/calculate-t2',
        json={'age': 30, 'annualSalary': 150000}  # 缺少wageGrowthRate
    )
    response.raise_for_status()
    data = response.json()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 400:
        error = e.response.json()
        print(f"参数错误: {error['error']}")
    else:
        print(f"服务器错误: {e}")
except Exception as e:
    print(f"请求失败: {e}")
```

---

## 最佳实践

### 1. 参数验证

```python
def validate_age(age):
    if not isinstance(age, int):
        raise ValueError("年龄必须是整数")
    if age < 18 or age > 65:
        raise ValueError("年龄必须在18-65之间")
    return age

def validate_salary(salary):
    if salary < 0:
        raise ValueError("年薪不能为负数")
    return salary
```

### 2. 超时处理

```python
import requests

response = requests.post(
    'http://localhost:8000/api/predict-wage-growth',
    json=data,
    timeout=10  # 10秒超时
)
```

### 3. 重试机制

```python
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(
    total=3,
    backoff_factor=0.3,
    status_forcelist=[500, 502, 503, 504]
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)

response = session.post('http://localhost:8000/api/calculate-t2', json=data)
```

### 4. 批量处理

```python
def batch_optimize(users):
    """批量优化多个用户"""
    results = []
    for user in users:
        try:
            response = requests.post(
                'http://localhost:8000/api/optimize-contribution',
                json=user
            )
            results.append({
                'user_id': user['id'],
                'status': 'success',
                'data': response.json()
            })
        except Exception as e:
            results.append({
                'user_id': user['id'],
                'status': 'error',
                'error': str(e)
            })
    return results
```

---

## 附录

### API端点一览

| 端点 | 方法 | 用途 | 路径 |
|------|------|------|------|
| 健康检查 | GET | 服务状态 | PathA/PathB |
| 工资预测 | POST | 增长率预测 | PathA |
| T2计算 | POST | 税优计算 | 核心 |
| T3计算 | POST | 领取期税率 | 核心 |
| 补贴计算 | POST | 精准补贴 | 核心 |
| 上限计算 | POST | 缴费上限 | 核心 |
| 方案优化 | POST | 3档方案 | PathA |
| 历史诊断 | POST | 效率评分 | PathB |
| AI建议 | POST | 个性化建议 | PathB |
| 5档方案 | POST | NPV对比 | PathB |

### 数据范围

| 参数 | 最小值 | 最大值 | 单位 |
|------|--------|--------|------|
| age | 18 | 65 | 岁 |
| annualSalary | 0 | - | 元 |
| wageGrowthRate | 0 | 20 | % |
| contributionAmount | 0 | 12000 | 元 |
| t2 | 0 | 45 | % |
| t3 | 0 | 14 | % |

---

**文档版本**: v1.0  
**最后更新**: 2025-11-03  
**联系方式**: support@aippof.com
