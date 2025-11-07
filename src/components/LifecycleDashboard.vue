<template>
  <div class="dashboard-container">
    <div class="dashboard-header">
      <h2>全生命周期可视化分析</h2>
      <p class="subtitle">50年养老金账户动态仿真（缴费期30年 + 领取期20年）</p>
    </div>

    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>正在生成可视化数据...</p>
    </div>

    <!-- 主要图表区域 -->
    <div v-else class="charts-grid">
      <!-- 图表1: 账户余额增长曲线 -->
      <div class="chart-card">
        <h3>📊 账户余额增长曲线</h3>
        <div ref="balanceChart" class="chart-container"></div>
      </div>

      <!-- 图表2: 缴费期收益分解 -->
      <div class="chart-card">
        <h3>💰 缴费期收益构成</h3>
        <div ref="benefitChart" class="chart-container"></div>
      </div>

      <!-- 图表3: 领取期现金流 -->
      <div class="chart-card">
        <h3>📈 领取期现金流分析</h3>
        <div ref="withdrawalChart" class="chart-container"></div>
      </div>

      <!-- 图表4: 不同缴费额对比 -->
      <div class="chart-card full-width">
        <h3>🎯 缴费策略对比（NPV优化）</h3>
        <div ref="comparisonChart" class="chart-container"></div>
      </div>

      <!-- 数据汇总卡片 -->
      <div class="summary-card">
        <h3>📋 全周期汇总</h3>
        <div class="summary-grid">
          <div class="summary-item">
            <span class="label">缴费期总投入</span>
            <span class="value">¥{{ formatNumber(summary.contributionPhase.totalContribution) }}</span>
          </div>
          <div class="summary-item">
            <span class="label">累计税收节省</span>
            <span class="value positive">+¥{{ formatNumber(summary.contributionPhase.totalTaxSavings) }}</span>
          </div>
          <div class="summary-item">
            <span class="label">累计补贴收入</span>
            <span class="value positive">+¥{{ formatNumber(summary.contributionPhase.totalSubsidies) }}</span>
          </div>
          <div class="summary-item">
            <span class="label">退休账户余额</span>
            <span class="value highlight">¥{{ formatNumber(summary.contributionPhase.finalAccountBalance) }}</span>
          </div>
          <div class="summary-item">
            <span class="label">领取期总税负</span>
            <span class="value negative">-¥{{ formatNumber(summary.withdrawalPhase.totalTax) }}</span>
          </div>
          <div class="summary-item">
            <span class="label">净现值NPV</span>
            <span class="value" :class="summary.overall.npv > 0 ? 'positive' : 'negative'">
              ¥{{ formatNumber(summary.overall.npv) }}
            </span>
          </div>
          <div class="summary-item">
            <span class="label">投资回报率ROI</span>
            <span class="value" :class="summary.overall.roi > 0 ? 'positive' : 'negative'">
              {{ summary.overall.roi }}%
            </span>
          </div>
          <div class="summary-item">
            <span class="label">年均收益</span>
            <span class="value">¥{{ formatNumber(summary.overall.averageAnnualBenefit) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 导出按钮 -->
    <div class="export-actions">
      <button @click="exportPDF" class="export-btn">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4M7 10l5 5 5-5M12 15V3"/>
        </svg>
        导出PDF报告
      </button>
      <button @click="exportExcel" class="export-btn">
        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
          <path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/>
          <polyline points="14 2 14 8 20 8"/>
        </svg>
        导出Excel数据
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import * as echarts from 'echarts'
import axios from 'axios'
import { API_BASE_URL } from '@/config'

interface Props {
  params: {
    age: number
    annualSalary: number
    contributionAmount: number
    t2: number
    t3: number
    wageGrowthRate: number
  }
}

const props = defineProps<Props>()

const loading = ref(true)
const balanceChart = ref<HTMLElement>()
const benefitChart = ref<HTMLElement>()
const withdrawalChart = ref<HTMLElement>()
const comparisonChart = ref<HTMLElement>()

const lifecycleData = ref<any>(null)
const comparisonData = ref<any>(null)
const summary = ref({
  contributionPhase: {
    totalContribution: 0,
    totalTaxSavings: 0,
    totalSubsidies: 0,
    finalAccountBalance: 0
  },
  withdrawalPhase: {
    totalTax: 0,
    totalNetIncome: 0
  },
  overall: {
    npv: 0,
    roi: 0,
    averageAnnualBenefit: 0
  }
})

onMounted(async () => {
  await loadData()
  renderCharts()
})

watch(() => props.params, async () => {
  await loadData()
  renderCharts()
}, { deep: true })

async function loadData() {
  loading.value = true
  try {
    // 加载生命周期数据
    const response1 = await axios.post(`${API_BASE_URL}/api/lifecycle-data`, props.params)
    lifecycleData.value = response1.data
    summary.value = response1.data.summary

    // 加载对比场景数据
    const response2 = await axios.post(`${API_BASE_URL}/api/comparison-scenarios`, props.params)
    comparisonData.value = response2.data
  } catch (error) {
    console.error('加载数据失败:', error)
  } finally {
    loading.value = false
  }
}

function renderCharts() {
  if (!lifecycleData.value) return

  renderBalanceChart()
  renderBenefitChart()
  renderWithdrawalChart()
  renderComparisonChart()
}

function renderBalanceChart() {
  if (!balanceChart.value) return

  const chart = echarts.init(balanceChart.value)
  const data = lifecycleData.value

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      borderColor: '#7C3AED',
      textStyle: { color: '#fff' }
    },
    legend: {
      data: ['缴费期账户余额', '领取期账户余额'],
      textStyle: { color: '#fff' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: [...data.contributionPhase.years, ...data.withdrawalPhase.years],
      axisLabel: { color: '#999' }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#999',
        formatter: '¥{value}'
      }
    },
    series: [
      {
        name: '缴费期账户余额',
        type: 'line',
        data: data.contributionPhase.accountBalance,
        smooth: true,
        lineStyle: { color: '#7C3AED', width: 3 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(124, 58, 237, 0.3)' },
            { offset: 1, color: 'rgba(124, 58, 237, 0.05)' }
          ])
        }
      },
      {
        name: '领取期账户余额',
        type: 'line',
        data: [...Array(data.contributionPhase.years.length).fill(null), ...data.withdrawalPhase.accountBalance],
        smooth: true,
        lineStyle: { color: '#60a5fa', width: 3 },
        areaStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: 'rgba(96, 165, 250, 0.3)' },
            { offset: 1, color: 'rgba(96, 165, 250, 0.05)' }
          ])
        }
      }
    ]
  }

  chart.setOption(option)
}

function renderBenefitChart() {
  if (!benefitChart.value) return

  const chart = echarts.init(benefitChart.value)
  const data = lifecycleData.value.contributionPhase

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      borderColor: '#7C3AED',
      textStyle: { color: '#fff' }
    },
    legend: {
      data: ['税收节省', '补贴收入', '累计收益'],
      textStyle: { color: '#fff' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.years,
      axisLabel: { color: '#999' }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#999',
        formatter: '¥{value}'
      }
    },
    series: [
      {
        name: '税收节省',
        type: 'bar',
        stack: 'benefit',
        data: data.taxSavings,
        itemStyle: { color: '#22c55e' }
      },
      {
        name: '补贴收入',
        type: 'bar',
        stack: 'benefit',
        data: data.subsidies,
        itemStyle: { color: '#3b82f6' }
      },
      {
        name: '累计收益',
        type: 'line',
        data: data.cumulativeBenefit,
        smooth: true,
        lineStyle: { color: '#f59e0b', width: 3 }
      }
    ]
  }

  chart.setOption(option)
}

function renderWithdrawalChart() {
  if (!withdrawalChart.value) return

  const chart = echarts.init(withdrawalChart.value)
  const data = lifecycleData.value.withdrawalPhase

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      borderColor: '#7C3AED',
      textStyle: { color: '#fff' }
    },
    legend: {
      data: ['领取总额', '领取税', '实际到手'],
      textStyle: { color: '#fff' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: data.ages,
      axisLabel: {
        color: '#999',
        formatter: '{value}岁'
      }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#999',
        formatter: '¥{value}'
      }
    },
    series: [
      {
        name: '领取总额',
        type: 'bar',
        data: data.withdrawalAmounts,
        itemStyle: { color: '#a78bfa' }
      },
      {
        name: '领取税',
        type: 'bar',
        data: data.taxes,
        itemStyle: { color: '#ef4444' }
      },
      {
        name: '实际到手',
        type: 'line',
        data: data.netIncome,
        smooth: true,
        lineStyle: { color: '#22c55e', width: 3 }
      }
    ]
  }

  chart.setOption(option)
}

function renderComparisonChart() {
  if (!comparisonChart.value || !comparisonData.value) return

  const chart = echarts.init(comparisonChart.value)
  const scenarios = comparisonData.value.scenarios

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      borderColor: '#7C3AED',
      textStyle: { color: '#fff' }
    },
    legend: {
      data: scenarios.map((s: any) => s.name),
      textStyle: { color: '#fff' }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['总缴费', '税收节省', '补贴收入', '退休余额', '领取税负', 'NPV'],
      axisLabel: { color: '#999', rotate: 20 }
    },
    yAxis: {
      type: 'value',
      axisLabel: {
        color: '#999',
        formatter: '¥{value}'
      }
    },
    series: scenarios.map((scenario: any, index: number) => ({
      name: scenario.name,
      type: 'bar',
      data: [
        scenario.data.summary.contributionPhase.totalContribution,
        scenario.data.summary.contributionPhase.totalTaxSavings,
        scenario.data.summary.contributionPhase.totalSubsidies,
        scenario.data.summary.contributionPhase.finalAccountBalance,
        -scenario.data.summary.withdrawalPhase.totalTax,
        scenario.data.summary.overall.npv
      ],
      itemStyle: {
        color: ['#7C3AED', '#3b82f6', '#22c55e'][index]
      }
    }))
  }

  chart.setOption(option)
}

function formatNumber(num: number): string {
  return num.toLocaleString('zh-CN', { maximumFractionDigits: 0 })
}

function exportPDF() {
  alert('PDF导出功能开发中...')
  // TODO: 实现PDF导出
}

function exportExcel() {
  alert('Excel导出功能开发中...')
  // TODO: 实现Excel导出
}
</script>

<style scoped>
.dashboard-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  text-align: center;
  margin-bottom: 40px;
}

.dashboard-header h2 {
  font-size: 2em;
  color: #fff;
  margin-bottom: 10px;
}

.subtitle {
  color: rgba(255, 255, 255, 0.7);
  font-size: 1.1em;
}

.loading-state {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(124, 58, 237, 0.3);
  border-top-color: #7C3AED;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
}

.chart-card {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 16px;
  padding: 24px;
  backdrop-filter: blur(10px);
}

.chart-card.full-width {
  grid-column: 1 / -1;
}

.chart-card h3 {
  color: #a78bfa;
  margin-bottom: 16px;
  font-size: 1.2em;
}

.chart-container {
  height: 350px;
}

.summary-card {
  grid-column: 1 / -1;
  background: rgba(124, 58, 237, 0.1);
  border: 1px solid rgba(124, 58, 237, 0.3);
  border-radius: 16px;
  padding: 24px;
}

.summary-card h3 {
  color: #c4b5fd;
  margin-bottom: 20px;
  font-size: 1.3em;
}

.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.summary-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.summary-item .label {
  color: rgba(255, 255, 255, 0.6);
  font-size: 0.9em;
}

.summary-item .value {
  color: #fff;
  font-size: 1.5em;
  font-weight: 600;
}

.summary-item .value.positive {
  color: #22c55e;
}

.summary-item .value.negative {
  color: #ef4444;
}

.summary-item .value.highlight {
  color: #a78bfa;
}

.export-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-top: 32px;
}

.export-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: #7C3AED;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1em;
  cursor: pointer;
  transition: all 0.3s ease;
}

.export-btn:hover {
  background: #6d28d9;
  box-shadow: 0 4px 15px rgba(124, 58, 237, 0.6);
}

.export-btn .icon {
  width: 20px;
  height: 20px;
}

@media (max-width: 768px) {
  .charts-grid {
    grid-template-columns: 1fr;
  }
  
  .summary-grid {
    grid-template-columns: 1fr;
  }
}
</style>
