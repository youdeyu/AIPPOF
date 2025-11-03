from t2_calculator import calculate_t2_for_contribution

# 测试税阶边界情况
salary = 100000  # 应纳税所得额 = 40000（第一档内）
print(f"年薪: ¥{salary:,} (应纳税所得额 = ¥40,000，在第二档10%)")
print("-" * 60)

for contrib in [0, 4000, 8000, 12000]:
    result = calculate_t2_for_contribution(salary, contrib)
    print(f"缴费 ¥{contrib:,}:")
    print(f"  T2 = {result['t2']}%")
    print(f"  节税额 = ¥{result['taxSaving']}")
    print(f"  缴后应纳税所得额 = ¥{result['details']['taxableWithPension']:,}")
    print(f"  边际税率 = {result['marginalRate']}%")
    print()
