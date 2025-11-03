from api.subsidy_calculator import calculate_subsidy
from api.t2_calculator import calculate_t2_for_contribution

# 检查补贴计算
print("补贴计算详情:")
r1 = calculate_subsidy(30000, 6000)
print(f"年薪3万缴费6000: 补贴={r1['subsidy']}")
print(f"  详情: {r1['breakdown']}")

r2 = calculate_subsidy(70000, 8000)
print(f"\n年薪7万缴费8000: 补贴={r2['subsidy']}")
print(f"  详情: {r2['breakdown']}")

# 检查T2计算
print("\n\nT2计算详情:")
t1 = calculate_t2_for_contribution(200000, 12000)
print(f"年薪20万缴费12000: T2={t1['t2']}%")
print(f"  详情: {t1}")
