/**
 * API配置
 * 
 * 使用说明：
 * - 本地开发：使用 localhost
 * - 局域网共享：使用本机IP地址（10.32.124.16）
 * - 生产环境：使用实际服务器地址
 */

// 自动检测：如果访问地址不是localhost，则使用当前host的IP
const getApiBaseUrl = () => {
  const currentHost = window.location.hostname
  
  // 如果是通过IP访问的，使用相同的IP访问API
  if (currentHost !== 'localhost' && currentHost !== '127.0.0.1') {
    return `http://${currentHost}:8000`
  }
  
  // 默认使用localhost
  return 'http://localhost:8000'
}

export const API_BASE_URL = getApiBaseUrl()

export const API_ENDPOINTS = {
  // PathA 相关
  predictWageGrowth: `${API_BASE_URL}/api/predict-wage-growth`,
  optimizeContribution: `${API_BASE_URL}/api/optimize-contribution`,
  lifecycleData: `${API_BASE_URL}/api/lifecycle-data`,
  comparisonScenarios: `${API_BASE_URL}/api/comparison-scenarios`,
  
  // PathB 相关
  diagnoseHistory: `${API_BASE_URL}/api/diagnose-history`,
  aiSuggestions: `${API_BASE_URL}/api/ai-suggestions`,
  fiveTierSuggestions: `${API_BASE_URL}/api/5tier-suggestions`,
}

// 打印当前API地址（便于调试）
console.log('🔧 API Base URL:', API_BASE_URL)
