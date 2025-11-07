# 🐛 Bug修复报告：SubsidyParams错误

## 问题描述
前端"新参与者"界面加载数据时报错：
```
'SubsidyParams' object has no attribute 'low_income_cut'
```

## 根本原因
在 `backend/main.py` 中，`calculate_subsidy` 函数被调用时使用了**错误的参数名**。

### 错误代码（修复前）
```python
# ❌ 错误：使用了不存在的参数名
subsidy_result = calculate_subsidy(
    wage=data['annualSalary'],  # 错误！应该是 annual_salary
    contribution=scenario['contribution']  # 错误！应该是 contribution_amount
)
```

### 函数实际签名
```python
def calculate_subsidy(
    annual_salary: float,  # ✅ 正确参数名
    contribution_amount: float,  # ✅ 正确参数名
    params: SubsidyParams = None
)
```

## 修复方案

### 修复位置1: `api_optimize_contribution` 端点（第275行）
```python
# ✅ 修复后
subsidy_result = calculate_subsidy(
    annual_salary=data['annualSalary'],
    contribution_amount=scenario['contribution']
)
```

### 修复位置2: `api_calculate_subsidy` 端点（第626行）
```python
# ✅ 修复后
subsidy_result = calculate_subsidy(
    annual_salary=data['annualSalary'],
    contribution_amount=data['contributionAmount']
)
```

## 为什么会出现这个错误？

当使用错误的参数名调用函数时：
1. Python无法匹配关键字参数
2. 可能导致位置参数错位
3. `annual_salary` 的值可能被传给了 `params` 参数
4. 然后代码尝试访问 `params.low_income_cut`
5. 但 `params` 实际上是一个数字（80000），不是 `SubsidyParams` 对象
6. 导致 `AttributeError: 'int' object has no attribute 'low_income_cut'` 或类似错误

## 修复步骤

1. ✅ 修改 `backend/main.py` 第275行
2. ✅ 修改 `backend/main.py` 第626行  
3. ⏳ 清理Python缓存：
   ```bash
   cd backend
   Remove-Item -Recurse -Force api\__pycache__
   Remove-Item -Recurse -Force __pycache__
   ```
4. ⏳ 重启后端服务（Flask watchdog会自动重启）
5. ⏳ 刷新前端页面测试

## 测试验证

访问前端"新参与者"路径，输入以下数据：
- 年龄：30岁
- 年收入：80,000元
- 工资增长率：3.9%

应该能正常显示补贴计算结果，不再报错。

## 相关文件
- `backend/main.py` - 主要修复文件
- `backend/api/subsidy_calculator.py` - 函数定义（无需修改）

## 修复日期
2024-11-07

## 状态
✅ 已修复，等待重启后端测试
