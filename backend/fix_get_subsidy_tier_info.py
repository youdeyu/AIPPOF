"""
修复 subsidy_calculator.py 中的 get_subsidy_tier_info 函数
将旧的两档模型改为新的三段式模型
"""
import re

file_path = 'api/subsidy_calculator.py'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 定义新的 get_subsidy_tier_info 函数
new_function = '''def get_subsidy_tier_info(annual_salary: float) -> Dict[str, Any]:
    """
    获取用户的补贴档位信息（用于前端显示）
    
    参数:
        annual_salary: 年工资收入
        
    返回:
        补贴档位信息字典
    """
    params = SubsidyParams()
    
    # 判断收入层次（基于taper机制）
    low_income_threshold = params.taper_w_low  # 40000元
    high_income_threshold = params.taper_w_high  # 100000元
    
    if annual_salary <= low_income_threshold:
        tier = "低收入"
        description = "主要激励：高额财政补贴"
        advantages = [
            f"享受 {params.alpha_1 * 100:.0f}% 首档配比率（最高档）",
            f"固定补贴 ¥{params.base_grant:.0f} 元",
            "全额补贴，无递减"
        ]
    elif annual_salary >= high_income_threshold:
        tier = "高收入"
        description = "主要激励：税收优惠减免"
        advantages = [
            "补贴已递减至零（避免双重优惠）",
            "主要通过个税减免获益",
            "预计节税 500-2000 元/年"
        ]
    else:
        tier = "中等收入"
        description = "双轨激励：补贴与税优并重"
        taper_pct = (high_income_threshold - annual_salary) / (
            high_income_threshold - low_income_threshold
        ) * 100
        advantages = [
            f"三段式补贴：{params.alpha_1*100:.0f}% / {params.alpha_2*100:.0f}% / {params.alpha_3*100:.0f}%",
            f"补贴递减比例：{taper_pct:.0f}%",
            "税收优惠与补贴双重受益"
        ]
    
    return {
        'tier': tier,
        'description': description,
        'advantages': advantages,
        'annual_salary': annual_salary,
        'is_eligible': True  # 默认参与模式下都符合条件
    }
'''

# 找到函数定义的开始和结束位置
pattern = r'def get_subsidy_tier_info\(annual_salary: float\).*?(?=\n\ndef |\n\nif __name__|$)'
match = re.search(pattern, content, re.DOTALL)

if match:
    # 替换函数
    new_content = content[:match.start()] + new_function + content[match.end():]
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print("✅ 成功修复 get_subsidy_tier_info 函数！")
    print(f"\n修改的位置：字符 {match.start()} 到 {match.end()}")
    print(f"原函数长度：{match.end() - match.start()} 字符")
    print(f"新函数长度：{len(new_function)} 字符")
else:
    print("❌ 未找到函数定义")
