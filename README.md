# AIPPOF - AI驱动个人养老金优化框架 Web应用

## 项目简介

基于AIPPOF（AI-driven Personal Pension Optimization Framework）学术模型，打造的智能化个人养老金缴费决策支持系统。

## 核心功能

### 路径A：新参与者 - 方案预测
- **智能预测**：基于年龄、年薪、性别、职业、职级预测工资增长率g
- **T2计算**：计算个人化平均节税率 T2 = t1 / (1+r/g)^n
- **AI建议**：给出最优缴费额建议（考虑补贴最大化+T3税负优化）
- **NPV对比**：展示"采纳AI建议" vs "维持现状"的净现值差异

### 路径B：已参与者 - 方案诊断
- **历史分析**：解析历史缴费记录，计算累积加权平均T2
- **效率诊断**：识别过度缴费或缴费不足问题
- **优化建议**：调整未来缴费策略

### T3领取期税率计算
- **渐进税率**：基于T2、收入、年龄计算0%-14%累进税率
- **双逻辑斯蒂函数**：t3 = f(T2, 收入, 年龄)
- **可视化展示**：预测领取期税负

### 行为助推（Nudge）
- **A/B测试**：损失厌恶框架（"损失¥680" vs "额外赚取¥680"）
- **动态对比表**：实时展示采纳/不采纳的差异
- **数据收集**：跟踪用户选择转化率

## 技术架构

### 前端
- **框架**：Vue 3 + TypeScript
- **样式**：Tailwind CSS
- **图表**：ECharts / Chart.js
- **UI设计**：深紫-深蓝渐变主题（参考YouTube Dubbing风格）
  - 背景渐变：#2C2A4A → #1A3A52
  - 玻璃态卡片：backdrop-blur + 柔和阴影
  - 圆角设计：border-radius: 16px
  - 紫色高亮按钮：#7C3AED

### 后端
- **API框架**：Node.js / Python Flask
- **数据库**：MySQL / PostgreSQL
- **OCR**：百度OCR / Google Cloud Vision（截图识别）
- **核心算法**：
  - 工资增长率预测模型
  - T2计算引擎
  - T3累进税率计算
  - NPV优化算法
  - 财政中性约束模型

### 部署
- **云服务器**：阿里云 / 腾讯云
- **HTTPS**：SSL证书配置
- **CDN**：静态资源加速

## 项目结构

```
08_AIPPOF网页应用/
├── frontend/                 # 前端项目
│   ├── src/
│   │   ├── views/           # 页面组件
│   │   │   ├── Welcome.vue  # 欢迎/分流页
│   │   │   ├── PathA/       # 新参与者路径
│   │   │   │   ├── InputForm.vue
│   │   │   │   └── Report.vue
│   │   │   └── PathB/       # 已参与者路径
│   │   │       ├── InputForm.vue
│   │   │       └── Report.vue
│   │   ├── components/      # 复用组件
│   │   │   ├── ComparisonTable.vue  # 对比表
│   │   │   ├── NudgeModule.vue      # 助推模块
│   │   │   └── Dashboard.vue        # 可视化仪表盘
│   │   ├── utils/           # 工具函数
│   │   ├── api/             # API调用
│   │   └── styles/          # 样式文件
│   ├── public/
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                  # 后端项目
│   ├── api/
│   │   ├── wage_growth_prediction.py  # 工资增长预测
│   │   ├── t2_calculator.py           # T2计算
│   │   ├── t3_calculator.py           # T3计算
│   │   ├── npv_optimizer.py           # NPV优化
│   │   └── subsidy_calculator.py      # 补贴计算
│   ├── models/              # 数据模型
│   ├── database/            # 数据库配置
│   ├── requirements.txt
│   └── main.py
│
├── docs/                     # 文档
│   ├── API文档.md
│   ├── 用户手册.md
│   └── 技术方案.md
│
└── README.md
```

## 核心算法公式

### T2平均节税率
```
T2 = t1 / (1 + r/g)^n
其中：
- t1 = 边际税率（基于当前收入）
- r = 1.75%（养老金账户收益率）
- g = 工资增长率（AI预测）
- n = 缴费年限（60 - 当前年龄）
```

### T3领取期税率（双逻辑斯蒂函数）
```
t3 = L1 + (L2 - L1) / (1 + exp(-k1(T2 - T2_mid))) + L3 / (1 + exp(-k2(w - w_high)))
其中：
- L1 = 0%（最低税率）
- L2 = 7%（中档税率）
- L3 = 7%（高收入附加）
- T2_mid = 5%（T2中值）
- w_high = 500,000（高收入阈值）
```

### NPV净现值
```
NPV = Σ(补贴S + 税收节省ΔT1) - 领取期税负T3
```

### 优化目标
```
Maximize: NPV(Subsidy_S) + NPV(TaxSave_t2) - NPV(TaxCost_t3)
Subject to: 财政中性约束
```

## 快速开始

### 前端开发

```powershell
cd frontend
npm install
npm run dev
```

访问 http://localhost:5173

### 后端开发

```powershell
cd backend
pip install -r requirements.txt
python main.py
```

API运行在 http://localhost:8000

## 数据流向

```
用户输入（年龄/年薪/职业）
    ↓
[前端] 数据验证 → 发送API请求
    ↓
[后端] 工资增长预测模型 → g值
    ↓
[后端] T2计算引擎 → T2值
    ↓
[后端] NPV优化算法 → 最优缴费额C*
    ↓
[后端] T3计算引擎 → 预测领取期税率
    ↓
[前端] Dashboard可视化展示
    ↓
[前端] Nudge模块引导用户决策
    ↓
[数据库] 记录用户选择（用于A/B测试分析）
```

## A/B测试设计

### 话术A（损失厌恶框架）
> ⚠️ **警告**：维持现状将直接损失 ¥680 补贴

### 话术B（获得感框架）
> ✅ **机会**：立即采纳将额外赚取 ¥680 补贴

### 数据收集
- 用户ID
- 分配组别（A/B）
- 最终决策（采纳/拒绝）
- 决策时间
- 计算转化率差异

## 关键特性

✅ **个性化预测**：基于真实行业数据的工资增长率预测  
✅ **精准计算**：符合学术论文公式的T2/T3计算引擎  
✅ **智能优化**：考虑补贴最大化+边际递减+T3税负的综合NPV优化  
✅ **行为助推**：基于损失厌恶理论的A/B测试框架  
✅ **全周期可视化**：缴费期+领取期50年现金流动态图表  
✅ **多端适配**：PC/平板/手机响应式布局  
✅ **数据驱动**：滚动迭代模拟，持续优化模型参数  

## 后续迭代计划

### 第一阶段（MVP）
- [x] 项目初始化
- [ ] 欢迎页 + 分流逻辑
- [ ] 路径A基础功能（输入表单 + T2计算 + 报告展示）
- [ ] 简化版对比表
- [ ] 基础UI主题

### 第二阶段
- [ ] 路径B完整功能（OCR识别 + 历史数据诊断）
- [ ] T3计算模块
- [ ] 全周期Dashboard
- [ ] A/B测试Nudge模块
- [ ] 数据导出功能

### 第三阶段
- [ ] 后端AI模型优化（工资增长预测）
- [ ] 高收入T3风险监测
- [ ] 财政中性NPV模型
- [ ] 滚动迭代模拟（Evolution Loop）
- [ ] 云端部署

## 参考文献

- AIPPOF框架蓝图（图1-图6）
- UI设计参考（图7 YouTube Dubbing风格）
- 优化政策学术论文（T2/T3计算公式）

## 联系方式

项目负责人：[待补充]  
技术支持：[待补充]  
反馈邮箱：[待补充]

---

**License**: MIT  
**Version**: 0.1.0 (MVP开发中)
