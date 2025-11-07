from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

# 导入计算模块
from api.wage_growth_prediction import predict_wage_growth
from api.t2_calculator import calculate_t2
from api.policy_utils import calculate_t3
from api.cap_calculator import calculate_contribution_cap
from api.contribution_optimizer import optimize_contribution
from api.npv_calculator import calculate_npv
from api.history_diagnosis import diagnose_history
from api.ai_diagnosis import generate_ai_suggestions
from api.contribution_suggestions import generate_5tier_suggestions
from api.lifecycle_visualization import generate_lifecycle_data, generate_comparison_scenarios
from api.risk_monitoring import assess_t3_risk, calculate_optimal_cap
from api.fiscal_neutral_npv import calculate_government_cash_flow, optimize_fiscal_neutral_contribution
from api.subsidy_calculator import calculate_subsidy, get_subsidy_explanation, get_subsidy_tier_info
from api.accumulated_t2_calculator import calculate_accumulated_t2

# 加载环境变量
load_dotenv()

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-aippof-2024')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'True') == 'True'


# ==================== 路由定义 ====================

@app.route('/')
def index():
    """API根路径"""
    return jsonify({
        'name': 'AIPPOF Backend API',
        'version': '0.1.0',
        'description': 'AI-driven Personal Pension Optimization Framework',
        'endpoints': [
            '/api/predict-wage-growth',
            '/api/calculate-t2',
            '/api/calculate-t3',
            '/api/optimize-contribution',
            '/api/calculate-npv',
            '/api/diagnose-history',
            '/api/ai-suggestions',
            '/api/5tier-suggestions',
            '/api/lifecycle-data',
            '/api/comparison-scenarios',
            '/api/risk-assessment',
            '/api/optimal-cap',
            '/api/fiscal-analysis',
            '/api/fiscal-optimize'
        ]
    })


@app.route('/health')
def health():
    """健康检查"""
    return jsonify({'status': 'healthy'})


@app.route('/api/predict-wage-growth', methods=['POST'])
def api_predict_wage_growth():
    """
    工资增长率预测API
    
    请求体:
    {
        "age": 30,
        "annualSalary": 150000,
        "industry": "it",
        "jobLevel": "intermediate"
    }
    """
    try:
        data = request.get_json()
        
        # 参数验证
        required_fields = ['age', 'annualSalary', 'industry', 'jobLevel']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        # 调用预测函数
        result = predict_wage_growth(
            age=data['age'],
            annual_salary=data['annualSalary'],
            industry=data['industry'],
            job_level=data['jobLevel']
        )
        
        # 规范化响应字段名
        response = {
            'predicted_growth_rate': result['predictedGrowth'],
            'confidence': result['confidence'],
            'industry_average': result['industryAverage'],
            'methodology': result['methodology'],
            'factors': {
                'base_growth': result['baseGrowth'],
                'ai_adjusted_growth': result['aiAdjustedGrowth'],
                'web_search_growth': result['webSearchGrowth']
            },
            'ai_insights': result['aiInsights'],
            'web_sources': result['webSources'],
            'details': result['details']
        }
        
        return jsonify(response)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/calculate-t2', methods=['POST'])
def api_calculate_t2():
    """
    T2平均节税率计算API
    
    请求体:
    {
        "age": 30,
        "annualSalary": 150000,
        "wageGrowthRate": 3.9
    }
    """
    try:
        data = request.get_json()
        
        # 参数验证
        required_fields = ['age', 'annualSalary', 'wageGrowthRate']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        # 调用计算函数
        result = calculate_t2(
            age=data['age'],
            annual_salary=data['annualSalary'],
            wage_growth_rate=data['wageGrowthRate']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/calculate-cap', methods=['POST'])
def api_calculate_cap():
    """
    缴费上限计算API
    
    请求体:
    {
        "annualSalary": 150000,
        "t2Rate": 10.0
    }
    """
    try:
        data = request.get_json()
        
        # 参数验证
        required_fields = ['annualSalary', 't2Rate']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        # 调用计算函数
        result = calculate_contribution_cap(
            annual_salary=data['annualSalary'],
            t2_rate=data['t2Rate']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/calculate-t3', methods=['POST'])
def api_calculate_t3():
    """
    T3领取期税率计算API
    
    请求体:
    {
        "t2": 1.4,
        "annualSalary": 150000,
        "age": 30
    }
    """
    try:
        data = request.get_json()
        
        # 参数验证
        required_fields = ['t2', 'annualSalary', 'age']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        # 调用计算函数
        result = calculate_t3(
            t2=data['t2'],
            annual_salary=data['annualSalary'],
            age=data['age']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/optimize-contribution', methods=['POST'])
def api_optimize_contribution():
    """
    推荐缴费额优化API - 返回多方案含T2
    
    请求体:
    {
        "age": 30,
        "annualSalary": 150000,
        "wageGrowthRate": 3.9
    }
    
    注意：不再需要t2和t3作为输入，会自动计算
    """
    try:
        data = request.get_json()
        
        # 参数验证
        required_fields = ['age', 'annualSalary', 'wageGrowthRate']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        # 1. 计算T2（基于个人属性）
        t2_result = calculate_t2(
            age=data['age'],
            annual_salary=data['annualSalary'],
            wage_growth_rate=data['wageGrowthRate']
        )
        t2 = t2_result['t2']
        
        # 2. 计算T3（基于个人属性）
        t3_result = calculate_t3(
            t2=t2,
            annual_salary=data['annualSalary'],
            age=data['age']
        )
        # T3计算器返回的是百分比数值（例如0.21表示0.21%）
        # 需要转换为小数形式（0.0021）以便前端使用
        t3 = t3_result['t3'] / 100.0
        
        # 3. 调用优化函数获取多方案
        optimization_result = optimize_contribution(
            age=data['age'],
            annual_salary=data['annualSalary'],
            t2=t2,
            t3=t3,
            wage_growth_rate=data['wageGrowthRate']
        )
        
        # 4. 为每个方案添加T2和精准补贴计算
        for scenario in optimization_result['scenarios']:
            scenario['predictedT2'] = t2
            
            # 计算精准补贴
            subsidy_result = calculate_subsidy(
                annual_salary=data['annualSalary'],
                contribution_amount=scenario['contribution']
            )
            scenario['subsidy'] = subsidy_result['subsidy']
            scenario['subsidyRatio'] = subsidy_result['ratio']
            scenario['subsidyTriggered'] = subsidy_result['triggered']
            scenario['subsidyBreakdown'] = subsidy_result['breakdown']
        
        # 5. 添加全局T2、T3和补贴档位信息到结果中
        optimization_result['t2'] = t2
        optimization_result['t3'] = t3
        optimization_result['subsidyTierInfo'] = get_subsidy_tier_info(data['annualSalary'])
        
        return jsonify(optimization_result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/calculate-npv', methods=['POST'])
def api_calculate_npv():
    """
    NPV净现值计算API
    
    请求体:
    {
        "age": 30,
        "annualSalary": 150000,
        "contributionAmount": 9500,
        "t2": 1.4,
        "t3": 1.2,
        "wageGrowthRate": 3.9
    }
    """
    try:
        data = request.get_json()
        
        # 参数验证
        required_fields = ['age', 'annualSalary', 'contributionAmount', 't2', 't3', 'wageGrowthRate']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        # 调用计算函数
        result = calculate_npv(
            age=data['age'],
            annual_salary=data['annualSalary'],
            contribution_amount=data['contributionAmount'],
            t2=data['t2'],
            t3=data['t3'],
            wage_growth_rate=data['wageGrowthRate']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/diagnose-history', methods=['POST'])
def api_diagnose_history():
    """
    历史数据诊断API
    
    请求体:
    {
        "historyData": [
            {"year": 2022, "salary": 120000, "contribution": 8000},
            {"year": 2023, "salary": 135000, "contribution": 10000},
            {"year": 2024, "salary": 150000, "contribution": 12000}
        ],
        "age": 30
    }
    """
    try:
        data = request.get_json()
        
        # 参数验证
        if 'historyData' not in data or 'age' not in data:
            return jsonify({'error': '缺少必填字段: historyData 或 age'}), 400
        
        # 调用诊断函数
        result = diagnose_history(
            history_data=data['historyData'],
            age=data['age']
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/ai-suggestions', methods=['POST'])
def api_ai_suggestions():
    """
    AI诊断建议API
    
    请求体:
    {
        "diagnosisResult": {...},  // 可选,如果未提供则从historyData计算
        "currentAge": 35
    }
    或者
    {
        "historyData": [
            {"year": 2022, "salary": 120000, "contribution": 8000}
        ],
        "currentAge": 35
    }
    """
    try:
        data = request.get_json()
        
        # 参数验证
        if 'currentAge' not in data:
            return jsonify({'error': '缺少必填字段: currentAge'}), 400
        
        # 获取或计算诊断结果
        if 'diagnosisResult' in data:
            diagnosis_result = data['diagnosisResult']
        elif 'historyData' in data:
            # 从历史数据计算诊断结果
            diagnosis_result = diagnose_history(
                history_data=data['historyData'],
                age=data['currentAge']
            )
        else:
            return jsonify({'error': '需要提供 diagnosisResult 或 historyData'}), 400
        
        # 生成AI建议
        ai_suggestions = generate_ai_suggestions(
            diagnosis_result=diagnosis_result,
            current_age=data['currentAge']
        )
        
        return jsonify(ai_suggestions)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/5tier-suggestions', methods=['POST'])
def api_5tier_suggestions():
    """
    5档缴费方案建议API
    
    请求体:
    {
        "currentSalary": 120000,
        "currentAge": 35,
        "currentContribution": 8000,  // 可选
        "t2Rate": 10.0,  // 可选
        "wageGrowthRate": 4.0  // 可选,默认3.5
    }
    
    返回:
    {
        "tiers": [
            {
                "tier": "conservative/stable/balanced/aggressive/maximum",
                "name": "保守型/稳健型/均衡型/积极型/激进型",
                "icon": "🛡️/📊/⚖️/📈/🚀",
                "contribution": 缴费额,
                "cap_utilization": 上限利用率%,
                "npv": {NPV详情},
                "characteristics": [特点列表],
                "suitable_for": "适合人群",
                "risk_level": "风险等级",
                "annual_benefit": 年均收益,
                "recommended": true/false  // 仅均衡型为true
            }
        ],
        "recommended": "balanced",
        "comparison": {对比分析},
        "parameters": {输入参数}
    }
    """
    try:
        data = request.get_json()
        
        # 参数验证 - 支持多种参数名
        current_age = data.get('currentAge') or data.get('age')
        annual_salary = data.get('annualSalary') or data.get('currentSalary')
        
        if not current_age or not annual_salary:
            return jsonify({'error': '缺少必填字段: currentAge/age 和 annualSalary/currentSalary'}), 400
        
        # 生成5档方案
        result = generate_5tier_suggestions(
            current_salary=annual_salary,
            current_age=current_age,
            current_contribution=data.get('currentContribution'),
            t2_rate=data.get('t2Rate'),
            wage_growth_rate=data.get('wageGrowthRate', 3.5)
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/lifecycle-data', methods=['POST'])
def api_lifecycle_data():
    """
    全生命周期数据生成API
    
    请求体:
    {
        "age": 30,
        "annualSalary": 150000,
        "contributionAmount": 9500,
        "t2": 1.4,
        "t3": 1.2,
        "wageGrowthRate": 3.9
    }
    """
    try:
        data = request.get_json()
        result = generate_lifecycle_data(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/comparison-scenarios', methods=['POST'])
def api_comparison_scenarios():
    """
    缴费额对比场景API
    
    请求体: 同上
    """
    try:
        data = request.get_json()
        result = generate_comparison_scenarios(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/risk-assessment', methods=['POST'])
def api_risk_assessment():
    """
    T3风险评估API
    
    请求体:
    {
        "annualSalary": 150000,
        "t2": 1.4,
        "t3": 1.2,
        "contributionAmount": 9500,
        "age": 30
    }
    """
    try:
        data = request.get_json()
        result = assess_t3_risk(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/optimal-cap', methods=['POST'])
def api_optimal_cap():
    """
    最优缴费上限API
    
    请求体:
    {
        "annualSalary": 150000,
        "t2": 1.4,
        "age": 30
    }
    """
    try:
        data = request.get_json()
        result = calculate_optimal_cap(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/fiscal-analysis', methods=['POST'])
def api_fiscal_analysis():
    """
    财政影响分析API
    
    请求体: 同lifecycle-data
    """
    try:
        data = request.get_json()
        result = calculate_government_cash_flow(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/fiscal-optimize', methods=['POST'])
def api_fiscal_optimize():
    """
    财政中性优化API
    
    请求体:
    {
        "age": 30,
        "annualSalary": 150000,
        "t2": 1.4,
        "wageGrowthRate": 3.9
    }
    """
    try:
        data = request.get_json()
        result = optimize_fiscal_neutral_contribution(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/calculate-subsidy', methods=['POST'])
def api_calculate_subsidy():
    """
    精准补贴计算API
    
    请求体:
    {
        "annualSalary": 150000,
        "contributionAmount": 12000
    }
    
    返回:
    {
        "subsidy": 补贴金额,
        "ratio": 补贴率,
        "triggered": 是否触发补贴,
        "breakdown": 补贴明细,
        "explanation": 补贴说明文本,
        "tierInfo": 补贴档位信息
    }
    """
    try:
        data = request.get_json()
        
        # 参数验证
        required_fields = ['annualSalary', 'contributionAmount']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'缺少必填字段: {field}'}), 400
        
        # 计算补贴
        subsidy_result = calculate_subsidy(
            annual_salary=data['annualSalary'],
            contribution_amount=data['contributionAmount']
        )
        
        # 生成说明文本
        explanation = get_subsidy_explanation(
            subsidy_result,
            data['annualSalary']
        )
        
        # 获取档位信息
        tier_info = get_subsidy_tier_info(data['annualSalary'])
        
        # 组合返回结果
        result = {
            **subsidy_result,
            'explanation': explanation,
            'tierInfo': tier_info
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/calculate-accumulated-t2', methods=['POST'])
def api_calculate_accumulated_t2():
    """
    累计T2计算API（已参与者专用）
    
    请求体:
    {
        "historyRecords": [
            {"year": 2022, "salary": 100000, "contribution": 8000},
            {"year": 2023, "salary": 110000, "contribution": 10000},
            {"year": 2024, "salary": 120000, "contribution": 12000}
        ],
        "discountRate": 0.0175  // 可选，默认1.75%
    }
    """
    try:
        data = request.get_json()
        
        # 参数验证
        if 'historyRecords' not in data:
            return jsonify({'error': '缺少必填字段: historyRecords'}), 400
        
        history_records = data['historyRecords']
        
        if not isinstance(history_records, list) or len(history_records) == 0:
            return jsonify({'error': 'historyRecords必须是非空数组'}), 400
        
        # 验证每条记录的必要字段
        for i, record in enumerate(history_records):
            if 'year' not in record or 'salary' not in record or 'contribution' not in record:
                return jsonify({'error': f'第{i+1}条记录缺少必要字段'}), 400
        
        # 可选参数
        discount_rate = data.get('discountRate', 0.0175)
        
        # 调用计算函数
        result = calculate_accumulated_t2(
            history_records=history_records,
            discount_rate=discount_rate
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ==================== 错误处理 ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': '资源不存在'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': '服务器内部错误'}), 500


# ==================== 主程序 ====================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
