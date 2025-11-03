#!/usr/bin/env python3
"""
端到端测试套件 - PathA和PathB完整流程验证
"""

import sys
import time
import requests
import json
from typing import Dict, List, Any
from colorama import init, Fore, Style

# 初始化colorama
init(autoreset=True)

class E2ETestSuite:
    """端到端测试套件"""
    
    def __init__(self, base_url: str = 'http://localhost:8000'):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.passed = 0
        self.failed = 0
        self.results = []
        
    def print_header(self, text: str):
        """打印测试标题"""
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}{text}")
        print(f"{Fore.CYAN}{'='*80}")
        
    def print_test(self, name: str):
        """打印测试名称"""
        print(f"\n{Fore.YELLOW}▶ {name}...")
        
    def assert_success(self, condition: bool, message: str):
        """断言成功"""
        if condition:
            print(f"{Fore.GREEN}  ✓ {message}")
            self.passed += 1
            self.results.append({'test': message, 'status': 'PASS'})
        else:
            print(f"{Fore.RED}  ✗ {message}")
            self.failed += 1
            self.results.append({'test': message, 'status': 'FAIL'})
            
    def print_summary(self):
        """打印测试总结"""
        total = self.passed + self.failed
        pass_rate = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n{Fore.CYAN}{'='*80}")
        print(f"{Fore.CYAN}测试总结")
        print(f"{Fore.CYAN}{'='*80}")
        print(f"总测试数: {total}")
        print(f"{Fore.GREEN}通过: {self.passed} ({pass_rate:.1f}%)")
        print(f"{Fore.RED}失败: {self.failed}")
        
        if self.failed > 0:
            print(f"\n{Fore.RED}❌ 失败的测试:")
            for result in self.results:
                if result['status'] == 'FAIL':
                    print(f"  - {result['test']}")
        
        return self.failed == 0

    # ============== PathA 测试 ==============
    
    def test_patha_wage_growth_prediction(self):
        """测试PathA: 工资增长预测"""
        self.print_test("PathA - 工资增长预测")
        
        try:
            response = requests.post(
                f"{self.api_url}/predict-wage-growth",
                json={
                    "age": 30,
                    "annualSalary": 150000,
                    "industry": "it",
                    "jobLevel": "intermediate"
                },
                timeout=10
            )
            
            self.assert_success(response.status_code == 200, "API响应状态码200")
            
            data = response.json()
            self.assert_success('predicted_growth_rate' in data, "返回预测增长率")
            self.assert_success(data['predicted_growth_rate'] > 0, "增长率大于0")
            self.assert_success(data['predicted_growth_rate'] < 20, "增长率小于20% (合理范围)")
            self.assert_success('factors' in data, "返回计算因子")
            
            print(f"  📊 预测增长率: {data['predicted_growth_rate']:.2f}%")
            
        except Exception as e:
            self.assert_success(False, f"工资增长预测失败: {str(e)}")
            
    def test_patha_contribution_optimization(self):
        """测试PathA: 缴费方案优化"""
        self.print_test("PathA - 缴费方案优化")
        
        try:
            response = requests.post(
                f"{self.api_url}/optimize-contribution",
                json={
                    "age": 30,
                    "annualSalary": 150000,
                    "wageGrowthRate": 4.5
                },
                timeout=10
            )
            
            self.assert_success(response.status_code == 200, "API响应状态码200")
            
            data = response.json()
            self.assert_success('scenarios' in data, "返回多方案")
            self.assert_success(len(data['scenarios']) == 3, "返回3个方案")
            self.assert_success('t2' in data, "返回T2值")
            self.assert_success('t3' in data, "返回T3值")
            self.assert_success('cap' in data, "返回缴费上限")
            self.assert_success('subsidyTierInfo' in data, "返回补贴档位信息")
            
            # 验证方案1
            scenario1 = data['scenarios'][0]
            self.assert_success('contribution' in scenario1, "方案1包含缴费额")
            self.assert_success('predictedT2' in scenario1, "方案1包含T2")
            self.assert_success('subsidy' in scenario1, "方案1包含补贴")
            self.assert_success('npv' in scenario1, "方案1包含NPV")
            
            print(f"  💰 推荐缴费: ¥{scenario1['contribution']:,}")
            print(f"  📈 T2: {data['t2']:.1f}%, T3: {data['t3']*100:.1f}%")
            print(f"  🎁 补贴: ¥{scenario1['subsidy']:.0f}")
            print(f"  💎 NPV: ¥{scenario1['npv']:,}")
            
        except Exception as e:
            self.assert_success(False, f"缴费方案优化失败: {str(e)}")
            
    def test_patha_t2_calculation(self):
        """测试PathA: T2计算"""
        self.print_test("PathA - T2税收优惠计算")
        
        try:
            response = requests.post(
                f"{self.api_url}/calculate-t2",
                json={
                    "age": 30,
                    "annualSalary": 150000,
                    "wageGrowthRate": 4.5
                },
                timeout=10
            )
            
            self.assert_success(response.status_code == 200, "API响应状态码200")
            
            data = response.json()
            self.assert_success('t2' in data, "返回T2值")
            self.assert_success(data['t2'] >= 0, "T2非负")
            self.assert_success(data['t2'] <= 45, "T2不超过最高边际税率")
            self.assert_success('formula' in data, "返回公式说明")
            
            print(f"  📊 T2税收优惠率: {data['t2']:.2f}%")
            
        except Exception as e:
            self.assert_success(False, f"T2计算失败: {str(e)}")
            
    def test_patha_t3_calculation(self):
        """测试PathA: T3计算"""
        self.print_test("PathA - T3领取期税率计算")
        
        try:
            response = requests.post(
                f"{self.api_url}/calculate-t3",
                json={
                    "t2": 10.0,
                    "annualSalary": 150000,
                    "age": 30
                },
                timeout=10
            )
            
            self.assert_success(response.status_code == 200, "API响应状态码200")
            
            data = response.json()
            self.assert_success('t3' in data, "返回T3值")
            self.assert_success(data['t3'] >= 0, "T3非负")
            self.assert_success(data['t3'] <= 14, "T3不超过14% (双逻辑函数上限)")
            self.assert_success('formula' in data, "返回公式说明")
            
            print(f"  📊 T3领取期税率: {data['t3']:.2f}%")
            
        except Exception as e:
            self.assert_success(False, f"T3计算失败: {str(e)}")
            
    def test_patha_subsidy_calculation(self):
        """测试PathA: 补贴计算"""
        self.print_test("PathA - 精准补贴计算")
        
        try:
            # 测试案例1: 低收入应有补贴
            response1 = requests.post(
                f"{self.api_url}/calculate-subsidy",
                json={"annualSalary": 60000, "contributionAmount": 5000},
                timeout=10
            )
            data1 = response1.json()
            self.assert_success(data1['subsidy'] > 0, "低收入(6万)应获得补贴")
            
            # 测试案例2: 高收入应无补贴
            response2 = requests.post(
                f"{self.api_url}/calculate-subsidy",
                json={"annualSalary": 150000, "contributionAmount": 12000},
                timeout=10
            )
            data2 = response2.json()
            self.assert_success(data2['subsidy'] == 0, "高收入(15万)补贴归零")
            
            print(f"  🎁 低收入补贴: ¥{data1['subsidy']:.0f}")
            print(f"  🎁 高收入补贴: ¥{data2['subsidy']:.0f}")
            
        except Exception as e:
            self.assert_success(False, f"补贴计算失败: {str(e)}")
            
    def test_patha_cap_calculation(self):
        """测试PathA: 缴费上限计算"""
        self.print_test("PathA - 缴费上限计算")
        
        try:
            response = requests.post(
                f"{self.api_url}/calculate-cap",
                json={
                    "annualSalary": 150000,
                    "t2Rate": 10.0
                },
                timeout=10
            )
            
            self.assert_success(response.status_code == 200, "API响应状态码200")
            
            data = response.json()
            self.assert_success('cap' in data, "返回上限值")
            self.assert_success(data['cap'] > 0, "上限大于0")
            self.assert_success('strategy' in data, "返回策略说明")
            self.assert_success('details' in data, "返回详细信息")
            
            print(f"  🔒 缴费上限: ¥{data['cap']:,.0f}")
            print(f"  📋 策略: {data['strategy']}")
            
        except Exception as e:
            self.assert_success(False, f"缴费上限计算失败: {str(e)}")

    # ============== PathB 测试 ==============
    
    def test_pathb_history_diagnosis(self):
        """测试PathB: 历史诊断"""
        self.print_test("PathB - 历史缴费诊断")
        
        history_data = [
            {"year": 2022, "salary": 120000, "contribution": 8000},
            {"year": 2023, "salary": 135000, "contribution": 10000},
            {"year": 2024, "salary": 150000, "contribution": 12000}
        ]
        
        try:
            response = requests.post(
                f"{self.api_url}/diagnose-history",
                json={
                    "historyData": history_data,
                    "age": 30
                },
                timeout=10
            )
            
            self.assert_success(response.status_code == 200, "API响应状态码200")
            
            data = response.json()
            self.assert_success('efficiencyScore' in data, "返回效率评分")
            self.assert_success(data['efficiencyScore'] >= 0, "效率评分非负")
            self.assert_success(data['efficiencyScore'] <= 100, "效率评分不超过100")
            self.assert_success('cumulativeT2' in data, "返回累积T2")
            self.assert_success('totalSubsidy' in data, "返回累计补贴")
            self.assert_success('predictedT3' in data, "返回预测T3")
            self.assert_success('historicalDetails' in data, "返回历史详情")
            
            print(f"  📊 效率评分: {data['efficiencyScore']:.0f}分")
            print(f"  📈 累积T2: {data['cumulativeT2']:.2f}%")
            print(f"  💰 累计补贴: ¥{data['totalSubsidy']:.0f}")
            print(f"  🔮 预测T3: {data['predictedT3']:.2f}%")
            
        except Exception as e:
            self.assert_success(False, f"历史诊断失败: {str(e)}")
            
    def test_pathb_ai_suggestions(self):
        """测试PathB: AI诊断建议"""
        self.print_test("PathB - AI个性化建议")
        
        # 先获取诊断结果
        history_data = [
            {"year": 2022, "salary": 120000, "contribution": 8000},
            {"year": 2023, "salary": 135000, "contribution": 10000},
            {"year": 2024, "salary": 150000, "contribution": 12000}
        ]
        
        try:
            # 步骤1: 获取诊断
            diagnosis_response = requests.post(
                f"{self.api_url}/diagnose-history",
                json={"historyData": history_data, "age": 30},
                timeout=10
            )
            diagnosis_data = diagnosis_response.json()
            
            # 步骤2: 获取AI建议
            ai_response = requests.post(
                f"{self.api_url}/ai-suggestions",
                json={
                    "diagnosisResult": diagnosis_data,
                    "currentAge": 30
                },
                timeout=10
            )
            
            self.assert_success(ai_response.status_code == 200, "API响应状态码200")
            
            ai_data = ai_response.json()
            self.assert_success('suggestions' in ai_data, "返回建议列表")
            self.assert_success(len(ai_data['suggestions']) > 0, "至少有1条建议")
            self.assert_success('actionPlan' in ai_data, "返回行动计划")
            self.assert_success('expectedBenefit' in ai_data, "返回预期收益")
            
            # 验证建议结构
            if len(ai_data['suggestions']) > 0:
                suggestion = ai_data['suggestions'][0]
                self.assert_success('title' in suggestion, "建议包含标题")
                self.assert_success('description' in suggestion, "建议包含描述")
                self.assert_success('priority' in suggestion, "建议包含优先级")
            
            print(f"  💡 建议数量: {len(ai_data['suggestions'])}条")
            print(f"  📋 行动计划: {len(ai_data.get('actionPlan', []))}步")
            print(f"  💰 预期收益: {ai_data['expectedBenefit']}")
            
        except Exception as e:
            self.assert_success(False, f"AI建议失败: {str(e)}")
            
    def test_pathb_5tier_suggestions(self):
        """测试PathB: 5档方案"""
        self.print_test("PathB - 五档缴费方案")
        
        try:
            response = requests.post(
                f"{self.api_url}/5tier-suggestions",
                json={
                    "currentAge": 30,
                    "annualSalary": 150000
                },
                timeout=10
            )
            
            self.assert_success(response.status_code == 200, "API响应状态码200")
            
            data = response.json()
            self.assert_success('tiers' in data, "返回档位列表")
            self.assert_success(len(data['tiers']) == 5, "返回5个档位")
            
            # 验证档位结构
            for i, tier in enumerate(data['tiers']):
                self.assert_success('name' in tier, f"档位{i+1}包含名称")
                self.assert_success('contribution' in tier, f"档位{i+1}包含缴费额")
                self.assert_success('npv' in tier, f"档位{i+1}包含NPV")
                self.assert_success('riskLevel' in tier, f"档位{i+1}包含风险等级")
            
            # 验证NPV递增
            npvs = [tier['npv']['total_npv'] if isinstance(tier['npv'], dict) else tier['npv'] for tier in data['tiers']]
            self.assert_success(npvs == sorted(npvs), "NPV递增(保守→激进)")
            
            print(f"  📊 5档方案:")
            for tier in data['tiers']:
                npv_value = tier['npv']['total_npv'] if isinstance(tier['npv'], dict) else tier['npv']
                print(f"    {tier['icon']} {tier['name']}: ¥{tier['contribution']:,} → NPV ¥{npv_value:,}")
            
        except Exception as e:
            self.assert_success(False, f"5档方案失败: {str(e)}")

    # ============== 综合测试 ==============
    
    def test_complete_patha_flow(self):
        """测试PathA完整流程"""
        self.print_test("PathA - 完整流程测试")
        
        try:
            # 1. 工资预测
            growth_response = requests.post(
                f"{self.api_url}/predict-wage-growth",
                json={"age": 30, "annualSalary": 150000, "industry": "it", "jobLevel": "intermediate"},
                timeout=10
            )
            growth_data = growth_response.json()
            predicted_growth = growth_data['predicted_growth_rate']
            
            # 2. 方案优化
            optimize_response = requests.post(
                f"{self.api_url}/optimize-contribution",
                json={"age": 30, "annualSalary": 150000, "wageGrowthRate": predicted_growth},
                timeout=10
            )
            optimize_data = optimize_response.json()
            
            self.assert_success(
                optimize_response.status_code == 200 and len(optimize_data['scenarios']) == 3,
                "PathA完整流程: 工资预测 → 方案优化"
            )
            
            print(f"  ✓ 流程完成: {predicted_growth:.1f}% 增长率 → ¥{optimize_data['scenarios'][0]['contribution']:,} 推荐缴费")
            
        except Exception as e:
            self.assert_success(False, f"PathA完整流程失败: {str(e)}")
            
    def test_complete_pathb_flow(self):
        """测试PathB完整流程"""
        self.print_test("PathB - 完整流程测试")
        
        history_data = [
            {"year": 2022, "salary": 120000, "contribution": 8000},
            {"year": 2023, "salary": 135000, "contribution": 10000},
            {"year": 2024, "salary": 150000, "contribution": 12000}
        ]
        
        try:
            # 1. 历史诊断
            diagnosis_response = requests.post(
                f"{self.api_url}/diagnose-history",
                json={"historyData": history_data, "age": 30},
                timeout=10
            )
            diagnosis_data = diagnosis_response.json()
            
            # 2. AI建议
            ai_response = requests.post(
                f"{self.api_url}/ai-suggestions",
                json={"diagnosisResult": diagnosis_data, "currentAge": 30},
                timeout=10
            )
            ai_data = ai_response.json()
            
            # 3. 5档方案
            tier_response = requests.post(
                f"{self.api_url}/5tier-suggestions",
                json={"currentAge": 30, "annualSalary": 150000},
                timeout=10
            )
            tier_data = tier_response.json()
            
            self.assert_success(
                all([r.status_code == 200 for r in [diagnosis_response, ai_response, tier_response]]),
                "PathB完整流程: 历史诊断 → AI建议 → 5档方案"
            )
            
            print(f"  ✓ 流程完成: {diagnosis_data['efficiencyScore']:.0f}分效率 → {len(ai_data['suggestions'])}条建议 → 5档方案")
            
        except Exception as e:
            self.assert_success(False, f"PathB完整流程失败: {str(e)}")

    def run_all_tests(self):
        """运行所有测试"""
        self.print_header("AIPPOF 端到端测试套件")
        print(f"测试服务器: {self.base_url}")
        
        # PathA测试
        self.print_header("PathA 测试 (新参与者路径)")
        self.test_patha_wage_growth_prediction()
        self.test_patha_t2_calculation()
        self.test_patha_t3_calculation()
        self.test_patha_subsidy_calculation()
        self.test_patha_cap_calculation()
        self.test_patha_contribution_optimization()
        self.test_complete_patha_flow()
        
        # PathB测试
        self.print_header("PathB 测试 (已参与者路径)")
        self.test_pathb_history_diagnosis()
        self.test_pathb_ai_suggestions()
        self.test_pathb_5tier_suggestions()
        self.test_complete_pathb_flow()
        
        # 打印总结
        return self.print_summary()


if __name__ == '__main__':
    print(f"{Fore.CYAN}AIPPOF 端到端测试")
    print(f"{Fore.CYAN}测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查服务器
    suite = E2ETestSuite()
    try:
        response = requests.get(f"{suite.base_url}/health", timeout=5)
        if response.status_code != 200:
            print(f"{Fore.RED}❌ 后端服务未启动!")
            print(f"{Fore.YELLOW}请先运行: python main.py")
            sys.exit(1)
    except Exception as e:
        print(f"{Fore.RED}❌ 无法连接到后端服务: {e}")
        print(f"{Fore.YELLOW}请先运行: python main.py")
        sys.exit(1)
    
    # 运行测试
    success = suite.run_all_tests()
    
    # 退出码
    sys.exit(0 if success else 1)
