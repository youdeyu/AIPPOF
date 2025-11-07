<template>
  <div class="report-page min-h-screen p-8">
    <div class="container max-w-6xl mx-auto">
      <!-- 返回按钮 -->
      <button @click="goBack" class="mb-6 text-white/70 hover:text-white flex items-center transition-colors">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        返回输入页
      </button>

      <!-- 页面标题 -->
      <div class="text-center mb-8 fade-in">
        <h1 class="text-4xl font-bold mb-3 text-white">AI预测分析报告</h1>
        <p class="text-white/70">基于您的个人信息，AI为您生成以下优化建议</p>
      </div>

      <!-- 加载状态 -->
      <div v-if="isLoading" class="glass-card p-12 text-center mb-8">
        <div class="inline-block animate-spin rounded-full h-16 w-16 border-t-2 border-b-2 border-accent-purple mb-4"></div>
        <p class="text-white text-lg">🤖 AI正在分析您的数据...</p>
        <p class="text-white/60 text-sm mt-2">预测工资增长率 → 计算最优缴费方案 → 生成个性化建议</p>
      </div>

      <!-- 错误提示 -->
      <div v-if="!isLoading && errorMessage" class="glass-card p-8 mb-8 bg-red-500/10 border border-red-500/30">
        <div class="flex items-center mb-4">
          <svg class="w-8 h-8 text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="text-xl font-bold text-red-400">数据加载失败</h3>
        </div>
        <p class="text-white mb-4">{{ errorMessage }}</p>
        <p class="text-white/70 text-sm mb-4">已使用降级数据显示示例报告，数据仅供参考。</p>
        <button @click="loadPredictionData" class="btn-primary">
          🔄 重新加载
        </button>
      </div>

      <!-- 报告内容（仅在数据加载成功或有降级数据时显示） -->
      <div v-if="!isLoading && reportData.scenarios.length > 0">
      <!-- 核心指标卡片 -->
      <div class="grid md:grid-cols-2 gap-6 mb-8">
        <!-- AI预测工资增长率 -->
        <div class="glass-card p-6 slide-in-left">
          <div class="text-white/60 text-sm mb-2">AI预测工资增长率 (g)</div>
          <div class="text-4xl font-bold text-blue-400 mb-2">{{ reportData.predictedGrowth }}%</div>
          <div class="text-white/50 text-xs">基于行业与职级深度学习预测</div>
        </div>

        <!-- AI推荐最优方案 -->
        <div class="glass-card p-6 slide-in-right">
          <div class="text-white/60 text-sm mb-2">AI推荐最优缴费额</div>
          <div class="text-4xl font-bold text-green-400 mb-2">¥{{ reportData.recommendedAmount.toLocaleString() }}</div>
          <div class="text-white/50 text-xs">多方案对比优选结果</div>
        </div>
      </div>

      <!-- 精准补贴档位信息卡片 -->
      <div v-if="reportData.subsidyTierInfo" class="glass-card p-6 mb-8 fade-in">
        <div class="flex items-center mb-4">
          <svg class="w-6 h-6 mr-3 text-yellow-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <h3 class="text-xl font-bold text-white">
            💰 您的补贴档位：{{ reportData.subsidyTierInfo.tier }}
          </h3>
        </div>
        
        <div class="mb-4">
          <p class="text-white/80 text-sm mb-2">
            <strong>激励方式：</strong>{{ reportData.subsidyTierInfo.description }}
          </p>
        </div>
        
        <div class="bg-black/20 rounded-lg p-4">
          <div class="text-white/70 text-sm mb-2 font-semibold">✨ 您享受的优惠政策：</div>
          <ul class="space-y-2 text-white/80 text-sm">
            <li v-for="(advantage, idx) in reportData.subsidyTierInfo.advantages" :key="idx" class="flex items-start">
              <span class="text-green-400 mr-2">✓</span>
              <span>{{ advantage }}</span>
            </li>
          </ul>
        </div>
        
        <div class="mt-4 text-white/60 text-xs text-center">
          💡 补贴计算基于渐进式精准补贴机制，随收入平滑过渡，确保公平性
        </div>
      </div>

      <!-- 多方案推荐对比卡片 -->
      <div class="glass-card p-8 mb-8 fade-in">
        <h2 class="text-2xl font-bold mb-6 text-white flex items-center">
          <svg class="w-6 h-6 mr-3 text-accent-purple" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                  d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
          </svg>
          AI推荐的3个最优缴费方案
        </h2>
        
        <!-- 个性化缴费上限提示 -->
        <div v-if="reportData.cap" class="mb-6 p-4 bg-purple-500/10 border border-purple-500/30 rounded-lg">
          <p class="text-white/80 text-sm">
            💎 <strong>您的个性化缴费上限</strong>：¥{{ reportData.cap.personalCap.toLocaleString() }}元
            （基于混合动态上限模型，年薪¥{{ formData.annualSalary.toLocaleString() }}）
          </p>
        </div>
        
        <div class="grid md:grid-cols-3 gap-6">
          <div v-for="(scenario, index) in reportData.scenarios" :key="index" 
               :ref="el => { if (el) scenarioRefs[index] = el as HTMLElement }"
               class="border rounded-lg p-6 hover:border-accent-purple transition-all hover:shadow-lg"
               :class="index === 0 ? 'border-accent-purple bg-accent-purple/10' : 'border-white/20'">
            <div class="mb-4">
              <!-- 方案标签 -->
              <div class="mb-3 text-center">
                <span v-if="index === 0" class="px-3 py-1 bg-accent-purple/30 text-accent-purple rounded-full text-xs font-bold">
                  🏆 NPV最优
                </span>
                <span v-else-if="index === 1" class="px-3 py-1 bg-blue-500/30 text-blue-400 rounded-full text-xs font-bold">
                  ⚖️ 平衡方案
                </span>
                <span v-else class="px-3 py-1 bg-green-500/30 text-green-400 rounded-full text-xs font-bold">
                  🛡️ 保守方案
                </span>
              </div>
              
              <!-- 缴费额 -->
              <div class="text-3xl font-bold text-white mb-4">¥{{ scenario.contribution.toLocaleString() }}</div>
              
              <!-- 核心指标 -->
              <div class="space-y-3 text-sm mb-4">
                <div class="flex justify-between items-center">
                  <span class="text-white/60">预测 T2:</span>
                  <span class="text-blue-400 font-bold text-lg">{{ scenario.predictedT2 }}%</span>
                </div>
                <div class="flex justify-between">
                  <span class="text-white/60">💰 年度补贴:</span>
                  <div class="text-right">
                    <span class="text-green-400 font-semibold">¥{{ scenario.subsidy.toLocaleString() }}</span>
                    <div v-if="scenario.subsidyRatio" class="text-xs text-green-300/70">
                      补贴率 {{ scenario.subsidyRatio.toFixed(1) }}%
                    </div>
                  </div>
                </div>
                <div class="flex justify-between">
                  <span class="text-white/60">📉 年度节税:</span>
                  <span class="text-blue-400 font-semibold">¥{{ scenario.taxSave.toLocaleString() }}</span>
                </div>
                <div class="flex justify-between border-t border-white/10 pt-2">
                  <span class="text-white/60">全周期NPV:</span>
                  <span class="text-accent-purple font-bold">¥{{ scenario.npv.toLocaleString() }}</span>
                </div>
              </div>
              
              <!-- 推荐理由 -->
              <div class="text-left space-y-2 text-xs text-white/70 bg-black/20 rounded p-3 mb-4">
                <div v-for="(reason, idx) in scenario.reasons" :key="idx" class="leading-relaxed">
                  {{ reason }}
                </div>
              </div>
              
              <!-- 操作按钮 -->
              <div class="flex gap-2">
                <button 
                  @click="selectScenario(scenario, index)"
                  :class="[
                    'flex-1 py-2 px-4 rounded-lg font-semibold transition-all',
                    index === 0 
                      ? 'bg-accent-purple text-white hover:bg-accent-purple/80' 
                      : 'bg-white/10 text-white hover:bg-white/20'
                  ]"
                >
                  {{ index === 0 ? '✓ 采纳方案1（最优）' : `选择方案${index + 1}` }}
                </button>
                
                <button 
                  @click="exportScenarioAsImage(scenario, index)"
                  class="px-4 py-2 rounded-lg font-semibold transition-all bg-blue-500/20 text-blue-300 hover:bg-blue-500/30 border border-blue-500/30"
                  title="导出为图片"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
        
        <div class="mt-6 p-4 bg-blue-500/10 border border-blue-500/30 rounded-lg">
          <p class="text-white/80 text-sm">
            💡 <strong>重要说明</strong>：以上3个方案均基于混合动态上限模型（公式5-5）计算。
            <strong>预测T2</strong>是根据您的实际缴费额计算的真实节税率（超额累进税率效应）。
            缴费额越高，跨越的税阶越多，平均T2可能降低。推荐优先选择<strong>方案1（NPV最优）</strong>。
          </p>
        </div>
      </div>

      <!-- 核心公式详解 -->
      <div class="glass-card p-8 mb-8 fade-in">
        <FormulaExplanation
          :title="'📐 核心公式详解 - 了解您的方案计算依据'"
          :showT2="true"
          :showT3="true"
          :showSubsidy="true"
          :showCap="true"
          :showNPV="true"
          :t2="reportData.scenarios[0]?.predictedT2 || 0"
          :t3="parseFloat(reportData.predictedT3) || 0"
          :subsidy="reportData.scenarios[0]?.subsidy || 0"
          :subsidyBreakdown="reportData.scenarios[0]?.subsidyBreakdown"
          :cap="reportData.cap?.personalCap || 0"
          :capBreakdown="reportData.cap"
          :npv="reportData.scenarios[0]?.npv || 0"
          :annualSalary="formData.annualSalary"
          :contribution="reportData.scenarios[0]?.contribution || 0"
          :age="formData.age"
          :wageGrowth="reportData.predictedGrowth"
        />
      </div>

      <!-- 决策对比表（方案1 vs 方案2） -->
      <div class="glass-card p-8 mb-8 fade-in">
        <h2 class="text-2xl font-bold mb-6 text-white text-center">方案深度对比</h2>
        <div class="overflow-x-auto">
          <table class="w-full text-white">
            <thead>
              <tr class="border-b border-white/20">
                <th class="py-4 px-4 text-left">对比维度</th>
                <th class="py-4 px-4 text-center bg-accent-purple/10">
                  <div class="flex flex-col items-center">
                    <span class="text-accent-purple font-bold">推荐方案 1</span>
                    <span class="text-sm text-white/70">¥{{ reportData.scenarios[0].contribution.toLocaleString() }}/年</span>
                  </div>
                </th>
                <th class="py-4 px-4 text-center">
                  <div class="flex flex-col items-center">
                    <span class="text-white/80">推荐方案 2</span>
                    <span class="text-sm text-white/70">¥{{ reportData.scenarios[1].contribution.toLocaleString() }}/年</span>
                  </div>
                </th>
              </tr>
            </thead>
            <tbody>
              <tr class="border-b border-white/10">
                <td class="py-4 px-4">预测平均节税率 (T2)</td>
                <td class="py-4 px-4 text-center bg-accent-purple/5 font-semibold text-blue-400">{{ reportData.scenarios[0].predictedT2 }}%</td>
                <td class="py-4 px-4 text-center text-white/60">{{ reportData.scenarios[1].predictedT2 }}%</td>
              </tr>
              <tr class="border-b border-white/10">
                <td class="py-4 px-4">年度财政补贴 (S)</td>
                <td class="py-4 px-4 text-center bg-accent-purple/5 font-semibold text-green-400">¥{{ reportData.scenarios[0].subsidy.toLocaleString() }}</td>
                <td class="py-4 px-4 text-center text-white/60">¥{{ reportData.scenarios[1].subsidy.toLocaleString() }}</td>
              </tr>
              <tr class="border-b border-white/10">
                <td class="py-4 px-4">领取期税率 (T3)</td>
                <td class="py-4 px-4 text-center bg-accent-purple/5 font-semibold text-green-400">{{ reportData.predictedT3 }}%</td>
                <td class="py-4 px-4 text-center text-white/60">{{ reportData.predictedT3 }}%</td>
              </tr>
              <tr class="border-b border-white/10 bg-yellow-500/10">
                <td class="py-4 px-4 font-semibold">全生命周期NPV</td>
                <td class="py-4 px-4 text-center bg-accent-purple/10 font-bold text-2xl text-accent-purple">
                  ¥{{ reportData.scenarios[0].npv.toLocaleString() }}
                </td>
                <td class="py-4 px-4 text-center font-semibold text-white/60">¥{{ reportData.scenarios[1].npv.toLocaleString() }}</td>
              </tr>
              <tr>
                <td class="py-4 px-4 font-bold text-accent-purple">AIPPOF建议</td>
                <td class="py-4 px-4 text-center bg-accent-purple/10">
                  <span class="inline-block bg-accent-purple text-white px-4 py-2 rounded-lg font-semibold">
                    ✓ 强烈推荐
                  </span>
                </td>
                <td class="py-4 px-4 text-center text-white/60">次优选择</td>
              </tr>
            </tbody>
          </table>
        </div>
        <div class="mt-4 p-3 bg-accent-purple/10 border border-accent-purple/30 rounded-lg">
          <p class="text-white/80 text-sm text-center">
            💡 两个方案的T2税率不同，因为缴费额会影响您未来的平均节税率
          </p>
        </div>
      </div>

      <!-- A/B测试 Nudge区域 -->
      <div class="glass-card p-8 mb-8 fade-in">
        <h2 class="text-2xl font-bold mb-6 text-white text-center">立即做出选择</h2>
        
        <!-- 根据A/B分组显示不同话术 -->
        <div v-if="nudgeGroup === 'A'" class="bg-red-500/10 border border-red-500/30 rounded-lg p-6 mb-6">
          <div class="flex items-center mb-3">
            <svg class="w-8 h-8 text-red-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <h3 class="text-xl font-bold text-red-400">选择次优方案的代价</h3>
          </div>
          <p class="text-white text-lg">
            选择方案2将<span class="text-red-400 font-bold text-2xl">少获得 ¥{{ (reportData.scenarios[0].subsidy - reportData.scenarios[1].subsidy).toFixed(0) }}</span> 补贴，且全周期NPV减少 <span class="text-red-400 font-bold text-2xl">¥{{ (reportData.scenarios[0].npv - reportData.scenarios[1].npv).toLocaleString() }}</span>
          </p>
        </div>

        <div v-else class="bg-green-500/10 border border-green-500/30 rounded-lg p-6 mb-6">
          <div class="flex items-center mb-3">
            <svg class="w-8 h-8 text-green-400 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <h3 class="text-xl font-bold text-green-400">选择最优方案的收益</h3>
          </div>
          <p class="text-white text-lg">
            选择方案1将<span class="text-green-400 font-bold text-2xl">多赚取 ¥{{ (reportData.scenarios[0].subsidy - reportData.scenarios[1].subsidy).toFixed(0) }}</span> 补贴，且全周期NPV增加 <span class="text-green-400 font-bold text-2xl">¥{{ (reportData.scenarios[0].npv - reportData.scenarios[1].npv).toLocaleString() }}</span>
          </p>
        </div>

        <div class="flex justify-center gap-6">
          <button @click="handleAccept" class="btn-primary text-lg px-10 py-4">
            ✓ 采纳方案1（最优）
          </button>
          <button @click="handleReject" class="btn-secondary text-lg px-10 py-4">
            选择方案2
          </button>
        </div>
      </div>

      <!-- 底部说明 -->
      <div class="text-center text-white/50 text-sm fade-in">
        <p>* 以上数据基于AI模型预测，实际收益可能因市场变化而波动</p>
        <p class="mt-2">本系统采用财政中性NPV优化模型，确保建议方案可持续</p>
      </div>
      
      </div> <!-- 关闭报告内容容器 -->
    </div>
    
    <!-- Toast 通知 -->
    <Toast 
      :show="toast.show"
      :type="toast.type"
      :title="toast.title"
      :message="toast.message"
      :duration="toast.duration"
      @close="toast.show = false"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import { API_BASE_URL } from '@/config'
import FormulaExplanation from '@/components/FormulaExplanation.vue'
import Toast from '@/components/Toast.vue'
import html2canvas from 'html2canvas'

const router = useRouter()
const route = useRoute()

// A/B测试分组（随机分配）
const nudgeGroup = ref<'A' | 'B'>(Math.random() > 0.5 ? 'A' : 'B')

// 从URL获取表单数据
const formData = ref({
  age: parseInt(route.query.age as string) || 30,
  annualSalary: parseInt(route.query.salary as string) || 150000,
  industry: route.query.industry as string || 'it',
  jobLevel: route.query.level as string || 'intermediate'
})

// 加载状态
const isLoading = ref(true)
const errorMessage = ref('')
const scenarioRefs = ref<HTMLElement[]>([])

// Toast 通知状态
const toast = ref({
  show: false,
  type: 'info' as 'success' | 'error' | 'warning' | 'info',
  title: '',
  message: '',
  duration: 3000
})

// 显示通知
const showToast = (type: 'success' | 'error' | 'warning' | 'info', title: string, message: string, duration = 3000) => {
  toast.value = {
    show: true,
    type,
    title,
    message,
    duration
  }
}

// 报告数据（从后端API获取）
const reportData = ref({
  predictedGrowth: 0,
  recommendedAmount: 0,
  subsidyAmount: 0,
  predictedT3: 3.0, // 固定领取期税率
  age: formData.value.age,
  annualSalary: formData.value.annualSalary,
  cap: null as any,
  scenarios: [] as any[],
  subsidyTierInfo: null as any // 补贴档位信息
})

// 全生命周期可视化参数
const lifecycleParams = computed(() => ({
  age: reportData.value.age,
  annualSalary: reportData.value.annualSalary,
  contributionAmount: reportData.value.recommendedAmount,
  t2: reportData.value.scenarios[0]?.predictedT2 || 0,
  t3: reportData.value.predictedT3,
  wageGrowthRate: reportData.value.predictedGrowth
}))

// 加载数据函数
const loadPredictionData = async () => {
  isLoading.value = true
  errorMessage.value = ''
  
  try {
    // 第1步：调用工资预测API
    const growthResponse = await axios.post(`${API_BASE_URL}/api/predict-wage-growth`, {
      age: formData.value.age,
      annualSalary: formData.value.annualSalary,
      industry: formData.value.industry,
      jobLevel: formData.value.jobLevel
    })
    
    const growthData = growthResponse.data
    reportData.value.predictedGrowth = parseFloat(growthData.predicted_growth_rate.toFixed(2))
    
    // 第2步：调用缴费方案优化API
    const optimizeResponse = await axios.post(`${API_BASE_URL}/api/optimize-contribution`, {
      age: formData.value.age,
      annualSalary: formData.value.annualSalary,
      wageGrowthRate: reportData.value.predictedGrowth / 100 // 转换为小数
    })
    
    const optimizeData = optimizeResponse.data
    
    // 更新报告数据
    reportData.value.scenarios = optimizeData.scenarios.map((s: any) => ({
      contribution: s.contribution,
      predictedT2: s.predictedT2,
      subsidy: s.subsidy || 0,
      subsidyRatio: s.subsidyRatio || 0,
      taxSave: s.taxSave || 0,
      npv: s.npv,
      label: s.label || '',
      reasons: s.reasons || []
    }))
    
    // 设置推荐金额为第一个方案
    if (reportData.value.scenarios.length > 0) {
      reportData.value.recommendedAmount = reportData.value.scenarios[0].contribution
      reportData.value.subsidyAmount = reportData.value.scenarios[0].subsidy
    }
    
    // 保存上限信息、T2/T3和补贴档位信息
    reportData.value.cap = optimizeData.cap
    reportData.value.predictedT3 = (optimizeData.t3 * 100).toFixed(1)
    reportData.value.subsidyTierInfo = optimizeData.subsidyTierInfo || null
    
    console.log('✅ 数据加载成功:', reportData.value)
    
  } catch (error: any) {
    console.error('❌ 数据加载失败:', error)
    errorMessage.value = error.response?.data?.error || '数据加载失败，请检查后端服务是否启动'
    
    // 使用降级数据（简化版模拟数据）
    reportData.value.predictedGrowth = 4.5
    reportData.value.recommendedAmount = 12000
    reportData.value.scenarios = [
      {
        contribution: 12000,
        predictedT2: 10.0,
        subsidy: 870,
        taxSave: 3600,
        npv: 59785,
        label: 'NPV最优',
        reasons: ['🏆 NPV最大化', '💰 补贴最高', '📊 T2平衡', '🎯 长期最优']
      },
      {
        contribution: 11500,
        predictedT2: 9.8,
        subsidy: 833,
        taxSave: 3450,
        npv: 58200,
        label: '平衡方案',
        reasons: ['⚖️ 风险平衡', '💼 适中缴费', '📈 稳健收益', '🛡️ 灵活调整']
      },
      {
        contribution: 11000,
        predictedT2: 9.5,
        subsidy: 797,
        taxSave: 3300,
        npv: 56500,
        label: '保守方案',
        reasons: ['🛡️ 低风险', '💵 现金流优先', '🔒 安全稳定', '📉 最小缴费']
      }
    ]
  } finally {
    isLoading.value = false
  }
}

const goBack = () => {
  router.push('/path-a/input')
}

// 选择方案
const selectScenario = (scenario: any, index: number) => {
  const scenarioName = index === 0 ? '方案1（NPV最优）' : index === 1 ? '方案2（平衡）' : '方案3（保守）'
  
  showToast(
    'success',
    '方案已选择',
    `您选择了【${scenarioName}】，年缴费额 ¥${scenario.contribution.toLocaleString()}，预期NPV ¥${scenario.npv.toLocaleString()}`
  )
  
  console.log('用户选择方案:', scenarioName, scenario)
}

// 导出方案为图片
const exportScenarioAsImage = async (scenario: any, index: number) => {
  try {
    showToast('info', '正在生成图片...', '请稍候', 1500)
    
    const element = scenarioRefs.value[index]
    if (!element) {
      throw new Error('无法找到方案元素')
    }

    // 使用 html2canvas 将DOM元素转换为canvas
    const canvas = await html2canvas(element, {
      backgroundColor: '#1A3A52',
      scale: 2, // 提高清晰度
      logging: false,
      useCORS: true
    })

    // 将 canvas 转换为图片并下载
    canvas.toBlob((blob) => {
      if (blob) {
        const url = URL.createObjectURL(blob)
        const link = document.createElement('a')
        const scenarioName = index === 0 ? '方案1_NPV最优' : index === 1 ? '方案2_平衡' : '方案3_保守'
        const timestamp = new Date().toISOString().slice(0, 10)
        link.download = `AIPPOF_PathA_${scenarioName}_${timestamp}.png`
        link.href = url
        link.click()
        URL.revokeObjectURL(url)
        
        showToast('success', '导出成功', `方案图片已保存为: ${link.download}`)
      }
    }, 'image/png')
  } catch (err: any) {
    console.error('导出图片失败:', err)
    showToast('error', '导出失败', err.message || '图片生成过程中出现错误')
  }
}

const handleAccept = () => {
  // TODO: 记录用户选择到数据库（用于A/B测试分析）
  console.log('用户采纳AI建议', {
    group: nudgeGroup.value,
    decision: 'accept'
  })
  showToast('success', '感谢您的信任！', '系统将为您生成详细实施方案', 4000)
}

const handleReject = () => {
  // TODO: 记录用户选择到数据库
  console.log('用户拒绝AI建议', {
    group: nudgeGroup.value,
    decision: 'reject'
  })
  showToast('info', '我们尊重您的选择', '您可以随时回来查看报告', 4000)
}

onMounted(() => {
  console.log('📊 Report页面加载，Nudge Group:', nudgeGroup.value)
  console.log('📝 表单数据:', formData.value)
  loadPredictionData()
})
</script>

<style scoped>
.report-page {
  background: linear-gradient(135deg, #2C2A4A 0%, #1A3A52 100%);
  min-height: 100vh;
}

table {
  border-collapse: separate;
  border-spacing: 0;
}

tr:hover {
  background: rgba(124, 58, 237, 0.05);
}
</style>
