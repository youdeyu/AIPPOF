# AIPPOF Backend API

基于Python Flask的后端API服务，提供养老金优化计算引擎。

## 功能模块

### 核心计算API
1. **工资增长率预测** - `/api/predict-wage-growth`
2. **T2节税率计算** - `/api/calculate-t2`
3. **T3领取期税率计算** - `/api/calculate-t3`
4. **推荐缴费额计算** - `/api/optimize-contribution`
5. **NPV净现值计算** - `/api/calculate-npv`
6. **历史数据诊断** - `/api/diagnose-history`

## 技术栈

- **框架**: Flask + Flask-CORS
- **计算库**: NumPy, SciPy
- **数据处理**: Pandas
- **API文档**: Flask-RESTful

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行服务器

```bash
python main.py
```

服务器运行在 `http://localhost:8000`

## API文档

### 1. 工资增长率预测
**POST** `/api/predict-wage-growth`

**请求体:**
```json
{
  "age": 30,
  "annualSalary": 150000,
  "industry": "it",
  "jobLevel": "intermediate"
}
```

**响应:**
```json
{
  "predictedGrowth": 3.9,
  "confidence": 0.85,
  "industryAverage": 4.2
}
```

### 2. T2节税率计算
**POST** `/api/calculate-t2`

**请求体:**
```json
{
  "age": 30,
  "annualSalary": 150000,
  "wageGrowthRate": 3.9
}
```

**响应:**
```json
{
  "t2": 1.4,
  "t1": 10.0,
  "n": 30,
  "details": {
    "contributionYears": 30,
    "returnRate": 1.75,
    "marginalTaxRate": 10.0
  }
}
```

### 3. T3领取期税率计算
**POST** `/api/calculate-t3`

**请求体:**
```json
{
  "t2": 1.4,
  "annualSalary": 150000,
  "age": 30
}
```

**响应:**
```json
{
  "t3": 1.2,
  "formula": "dual_logistic",
  "components": {
    "baseTax": 0.8,
    "incomeAdjustment": 0.4
  }
}
```

### 4. 推荐缴费额计算
**POST** `/api/optimize-contribution`

**请求体:**
```json
{
  "age": 30,
  "annualSalary": 150000,
  "t2": 1.4,
  "t3": 1.2,
  "wageGrowthRate": 3.9
}
```

**响应:**
```json
{
  "recommendedAmount": 9500,
  "subsidy": 680,
  "npvOptimized": 125300,
  "reasons": [
    "补贴最大化：可获得¥680补贴",
    "规避边际递减：避免40k-100k递减区间",
    "T3税负优化：领取期税率仅1.2%"
  ]
}
```

### 5. NPV净现值计算
**POST** `/api/calculate-npv`

**请求体:**
```json
{
  "age": 30,
  "annualSalary": 150000,
  "contributionAmount": 9500,
  "t2": 1.4,
  "t3": 1.2,
  "wageGrowthRate": 3.9
}
```

**响应:**
```json
{
  "npv": 125300,
  "totalSubsidy": 20400,
  "totalTaxSave": 42000,
  "totalT3Tax": 15600,
  "breakdown": {
    "contributionPhase": 62400,
    "withdrawalPhase": 62900
  }
}
```

### 6. 历史数据诊断
**POST** `/api/diagnose-history`

**请求体:**
```json
{
  "historyData": [
    {"year": 2022, "salary": 120000, "contribution": 8000},
    {"year": 2023, "salary": 135000, "contribution": 10000},
    {"year": 2024, "salary": 150000, "contribution": 12000}
  ],
  "age": 30
}
```

**响应:**
```json
{
  "cumulativeT2": 2.1,
  "efficiencyScore": 78,
  "totalSubsidy": 1850,
  "diagnosis": {
    "overContribution": true,
    "message": "2023-2024年存在过度缴费"
  },
  "predictedT3": 2.8,
  "potentialGain": 1200,
  "recommendedAmount": 9500
}
```

## 核心算法说明

### T2计算公式
```
T2 = t1 / (1 + r/g)^n

其中：
- t1 = 边际税率（基于年薪）
- r = 1.75%（养老金账户收益率）
- g = 工资增长率
- n = 缴费年限（60 - age）
```

### T3计算公式（双逻辑斯蒂函数）
```python
t3 = L1 + (L2 - L1) / (1 + exp(-k1 * (T2 - T2_mid))) + L3 / (1 + exp(-k2 * (w - w_high)))

参数：
- L1 = 0% (最低税率)
- L2 = 7% (中档税率)
- L3 = 7% (高收入附加)
- T2_mid = 5% (T2中值)
- w_high = 500000 (高收入阈值)
- k1 = 2.0 (T2敏感度)
- k2 = 0.00001 (收入敏感度)
```

### 补贴计算公式（优化模型）
```python
# 基础补贴
base_subsidy = 150

# 缴费匹配补贴
if income <= 40000:
    match_subsidy = contribution * 0.30
elif income <= 100000:
    # 线性递减
    taper = (100000 - income) / 60000
    match_subsidy = contribution * (0.06 + 0.24 * taper)
else:
    match_subsidy = contribution * 0.06

total_subsidy = base_subsidy + match_subsidy
```

## 测试

```bash
# 运行单元测试
python -m pytest tests/

# 测试单个模块
python -m pytest tests/test_t2_calculator.py -v
```

## 部署

### 开发环境
```bash
python main.py
```

### 生产环境（使用Gunicorn）
```bash
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

## 环境变量

创建 `.env` 文件：
```
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:pass@localhost/aippof
```

## 错误码

- `400` - 请求参数错误
- `404` - 资源不存在
- `500` - 服务器内部错误

## 更新日志

### v0.1.0 (2024-11-02)
- ✅ 初始化项目结构
- ✅ 实现工资增长率预测
- ✅ 实现T2/T3计算引擎
- ✅ 实现推荐缴费额优化
- ✅ 实现NPV计算
- ✅ 实现历史数据诊断
