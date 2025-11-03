#!/usr/bin/env python3
"""
检查T3在高T2时的值
"""

import sys
sys.path.append('.')

from api.t3_calculator import calculate_t3

# 测试T3在T2=20%时的值
print("\n=== T3计算测试 (T2=20%) ===")
result = calculate_t3(t2=20.0, annual_salary=300000, age=40)
print(f"T2=20%, 年薪30万, 年龄40:")
print(f"  T3 = {result['t3']:.2f}%")
print(f"  详情: {result}")

# 测试不同T2下的T3变化
print("\n=== T3随T2变化 ===")
for t2 in [2, 5, 10, 15, 20, 25, 30]:
    result = calculate_t3(t2=float(t2), annual_salary=200000, age=35)
    print(f"T2={t2:2d}% → T3={result['t3']:5.2f}%")
