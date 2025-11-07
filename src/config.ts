/**
 * API配置
 * 
 * 使用说明：
 * - 本地开发：npm run dev → 使用 localhost:8000
 * - 生产环境：npm run build → 使用环境变量 VITE_API_BASE_URL
 * - 环境变量在 .env.production 中配置
 */

// 优先使用环境变量，否则使用自动检测
const getApiBaseUrl = () => {
  // 1. 优先使用环境变量（构建时注入）
  if (import.meta.env.VITE_API_BASE_URL) {
    return import.meta.env.VITE_API_BASE_URL
  }
  
  // 2. 开发模式：自动检测当前访问地址
  const currentHost = window.location.hostname
  
  // 如果是通过域名或IP访问的，使用相同地址的8000端口
  if (currentHost !== 'localhost' && currentHost !== '127.0.0.1') {
    return `http://${currentHost}:8000`
  }
  
  // 3. 默认本地开发
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
console.log('🌍 Environment:', import.meta.env.MODE)

