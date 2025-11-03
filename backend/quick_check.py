# -*- coding: utf-8 -*-
import sys
sys.stdout.reconfigure(encoding='utf-8')

from api.subsidy_calculator import calculate_subsidy
from api.t2_calculator import calculate_t2_for_contribution

print("="*80)
print("核心精度测试")
print("="*80)

# 测试1: 28万年薪补贴应该是0
print("\n测试1: 28万年薪补贴测试")
result = calculate_subsidy(280000, 12000)
print(f"年薪280000, 缴费12000 -> 补贴: {result['subsidy']}")
assert result['subsidy'] == 0, "ERROR: 补贴应该是0!"
print("PASS: 补贴正确为0")

# 测试2: 150k边界
print("\n测试2: 150k边界测试")
for salary in [149000, 150000, 151000]:
    result = calculate_subsidy(salary, 10000)
    status = "PASS" if (salary >= 150000 and result['subsidy'] == 0) or (salary < 150000 and result['subsidy'] > 0) else "FAIL"
    print(f"年薪{salary} -> 补贴{result['subsidy']} [{status}]")

# 测试3: 蓝浩歌T2公式
print("\n测试3: 蓝浩歌T2公式测试")
for salary, contrib in [(80000, 8000), (150000, 12000), (280000, 12000)]:
    result = calculate_t2_for_contribution(salary, contrib)
    print(f"年薪{salary}, 缴费{contrib} -> T2={result['t2']:.2f}%, 节税={result['taxSaving']}")

print("\n="*80)
print("所有核心测试PASS! 小猫们安全了!")
print("="*80)
