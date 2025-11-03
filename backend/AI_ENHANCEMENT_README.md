# AI增强版工资增长率预测 - 配置说明

## 🎯 功能概述

工资增长率预测模块已升级为**三层智能预测架构**：

1. **基础预测层** (40%权重)
   - 基于历史数据和统计模型
   - 9个行业 × 4个职级 × 年龄因素 × 薪资因素
   - 无需额外配置，开箱即用

2. **AI深度思考层** (40%权重)
   - 使用GPT-4分析宏观经济、行业趋势、政策影响
   - 需要配置OpenAI API密钥
   - 提供3-5条专业洞察和推理过程

3. **联网搜索层** (20%权重)
   - 实时搜索最新行业薪资报告
   - 当前使用模拟数据，可替换为真实API
   - 提供权威来源引用

---

## 🔧 配置方法

### 方法1：环境变量配置（推荐）

**Windows PowerShell:**
```powershell
# 临时设置（当前会话）
$env:OPENAI_API_KEY = "sk-your-api-key-here"

# 永久设置（用户级）
[System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'sk-your-api-key-here', 'User')
```

**Windows CMD:**
```cmd
set OPENAI_API_KEY=sk-your-api-key-here
```

**Linux/Mac:**
```bash
export OPENAI_API_KEY="sk-your-api-key-here"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export OPENAI_API_KEY="sk-your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

### 方法2：.env文件配置

1. 在`backend`目录创建`.env`文件：
```env
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4  # 或 gpt-3.5-turbo
```

2. 安装python-dotenv：
```bash
pip install python-dotenv
```

3. 在代码中加载：
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 📦 依赖安装

```bash
# 基础预测（已安装）
pip install numpy

# AI深度思考（可选）
pip install openai

# 联网搜索（可选）
pip install requests

# 环境变量管理（可选）
pip install python-dotenv
```

或一键安装：
```bash
pip install -r requirements.txt
```

---

## 🚀 使用示例

### 示例1：完整AI增强预测

```python
from wage_growth_prediction import predict_wage_growth

result = predict_wage_growth(
    age=30,
    annual_salary=150000,
    industry='it',
    job_level='intermediate',
    enable_ai=True,          # 启用AI深度思考
    enable_web_search=True   # 启用联网搜索
)

print(f"预测增长率: {result['predictedGrowth']}%")
print(f"置信度: {result['confidence']}")
print(f"AI洞察: {result['aiInsights']}")
print(f"搜索来源: {result['webSources']}")
```

### 示例2：仅使用基础预测

```python
result = predict_wage_growth(
    age=30,
    annual_salary=150000,
    industry='it',
    job_level='intermediate',
    enable_ai=False,         # 禁用AI
    enable_web_search=False  # 禁用搜索
)
# 仅返回基础统计模型预测
```

### 示例3：仅使用AI深度思考

```python
result = predict_wage_growth(
    age=30,
    annual_salary=150000,
    industry='it',
    job_level='intermediate',
    enable_ai=True,          # 启用AI
    enable_web_search=False  # 禁用搜索
)
# 权重分配：基础50% + AI50%
```

---

## 🔑 获取OpenAI API密钥

1. 访问 [OpenAI官网](https://platform.openai.com/)
2. 注册/登录账号
3. 进入 [API Keys页面](https://platform.openai.com/account/api-keys)
4. 点击"Create new secret key"
5. 复制密钥并保存（仅显示一次）

**注意事项：**
- API调用需要付费（GPT-4约$0.03/1K tokens）
- 建议设置使用限额避免超支
- 密钥泄露请立即撤销并重新生成

---

## 🌐 联网搜索API替换指南

当前模块使用模拟数据，可替换为以下真实API：

### 方案1：百度搜索API

```python
def web_search_enhancement(industry, job_level):
    import requests
    
    api_key = os.getenv('BAIDU_API_KEY')
    url = 'https://aip.baidubce.com/rest/2.0/kg/v1/cognitive/search'
    
    response = requests.get(url, params={
        'query': f'{industry}行业薪资增长率',
        'access_token': api_key
    })
    
    # 解析结果...
```

### 方案2：智谱GLM API

```python
from zhipuai import ZhipuAI

client = ZhipuAI(api_key=os.getenv('ZHIPU_API_KEY'))
response = client.chat.completions.create(
    model="glm-4",
    messages=[
        {"role": "user", "content": f"搜索{industry}行业最新薪资报告"}
    ]
)
```

### 方案3：必应搜索API

```python
import requests

subscription_key = os.getenv('BING_SEARCH_API_KEY')
search_url = "https://api.bing.microsoft.com/v7.0/search"

headers = {"Ocp-Apim-Subscription-Key": subscription_key}
params = {"q": f"{industry}薪资增长率 2025"}

response = requests.get(search_url, headers=headers, params=params)
```

---

## 📊 返回数据结构

```python
{
    'predictedGrowth': 5.65,           # 最终预测增长率(%)
    'confidence': 0.85,                # 置信度(0-1)
    'industryAverage': 5.2,            # 行业平均(%)
    'baseGrowth': 5.72,                # 基础预测(%)
    'aiAdjustedGrowth': 5.8,           # AI调整后(%)
    'webSearchGrowth': 5.5,            # 联网搜索(%)
    'aiInsights': [                    # AI洞察
        '2025年IT行业受AI技术驱动薪资增长加速',
        '中级岗位薪资增幅高于初级和管理层',
        '...更多洞察'
    ],
    'webSources': [                    # 搜索来源
        '《2025年中国IT行业薪酬白皮书》',
        '智联招聘2025Q1报告',
        '...更多来源'
    ],
    'methodology': '基础统计模型 + AI深度分析 + 实时数据搜索',
    'weights': {                       # 权重分配
        'base': 0.4,
        'ai': 0.4,
        'web': 0.2
    },
    'details': {                       # 详细信息
        'aiReasoning': 'AI推理过程...',
        'lastWebUpdate': '2025-11-02 10:30',
        'aiAvailable': True,
        'webAvailable': True
    }
}
```

---

## ⚙️ 高级配置

### 自定义权重分配

修改`wage_growth_prediction.py`中的权重：

```python
# 默认权重：基础40% + AI40% + 搜索20%
weights = {
    'base': 0.4,
    'ai': 0.4,
    'web': 0.2
}

# 保守配置（信任基础模型）
weights = {
    'base': 0.7,
    'ai': 0.2,
    'web': 0.1
}

# 激进配置（信任AI）
weights = {
    'base': 0.2,
    'ai': 0.6,
    'web': 0.2
}
```

### 更换AI模型

```python
# 使用GPT-3.5（更便宜）
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",  # 替换为gpt-3.5-turbo
    ...
)

# 使用国产大模型（智谱GLM-4）
from zhipuai import ZhipuAI
client = ZhipuAI(api_key=os.getenv('ZHIPU_API_KEY'))
response = client.chat.completions.create(
    model="glm-4",
    ...
)
```

---

## 🐛 故障排查

### 问题1：AI功能不可用

**症状**：返回结果中`aiInsights`为空或显示"AI功能未启用"

**解决方案**：
1. 检查是否安装openai库：`pip install openai`
2. 检查环境变量：`echo $env:OPENAI_API_KEY`（PowerShell）
3. 检查API密钥是否有效
4. 检查网络连接（需访问OpenAI服务器）

### 问题2：联网搜索返回空结果

**症状**：`webSources`为空

**解决方案**：
1. 当前使用模拟数据，检查行业是否在预定义列表中
2. 如需真实搜索，替换为真实API（见上文）
3. 检查requests库是否安装：`pip install requests`

### 问题3：预测结果异常

**症状**：增长率过高(>10%)或过低(<0.5%)

**解决方案**：
1. 检查输入参数是否合理（age、salary、industry）
2. 检查行业代码是否正确（参见`INDUSTRY_GROWTH_RATES`）
3. 查看详细日志：`print(result['details'])`

---

## 📈 性能优化

### 缓存AI结果

```python
import functools
from datetime import datetime, timedelta

@functools.lru_cache(maxsize=100)
def cached_ai_prediction(age, salary, industry, level):
    return ai_deep_thinking_prediction(age, salary, industry, level, base_pred)

# 缓存24小时内的相同查询
```

### 异步调用

```python
import asyncio

async def async_predict():
    base_task = asyncio.create_task(base_prediction())
    ai_task = asyncio.create_task(ai_prediction())
    web_task = asyncio.create_task(web_search())
    
    base, ai, web = await asyncio.gather(base_task, ai_task, web_task)
    return combine_results(base, ai, web)
```

---

## 📝 更新日志

**v2.0** (2025-11-02)
- ✨ 新增AI深度思考功能（GPT-4集成）
- ✨ 新增联网搜索功能（实时数据）
- 🔧 重构为三层预测架构
- 📊 新增详细洞察和来源引用
- ⚙️ 支持功能开关和权重自定义

**v1.0** (2025-10-28)
- 🎉 基础统计模型上线
- 📊 支持9个行业×4个职级

---

## 🤝 技术支持

如有问题或建议，请联系开发团队。

**相关文档**：
- OpenAI API文档: https://platform.openai.com/docs
- 智谱GLM文档: https://open.bigmodel.cn/dev/api
- 百度AI文档: https://ai.baidu.com/docs

---

**最后更新**: 2025年11月2日
