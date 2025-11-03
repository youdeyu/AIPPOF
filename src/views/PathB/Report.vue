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

      <!-- 加载状态 -->
      <div v-if="isLoading" class="flex flex-col items-center justify-center min-h-[60vh]">
        <div class="animate-spin rounded-full h-16 w-16 border-t-4 border-b-4 border-accent-purple mb-4"></div>
        <p class="text-white/70 text-lg">正在分析您的历史缴费数据...</p>
      </div>

      <!-- 报告内容 -->
      <div v-else>
        <!-- 页面标题 -->
        <div class="text-center mb-8 fade-in">
          <h1 class="text-4xl font-bold mb-3 text-white">缴费效率诊断报告</h1>
          <p class="text-white/70">基于您的历史缴费数据，AI为您生成以下诊断结果</p>
        </div>

        <!-- 核心指标卡片 -->
        <div class="grid md:grid-cols-3 gap-6 mb-8">
          <!-- 累积T2值 -->
          <div class="glass-card p-6 slide-in-left">
            <div class="text-white/60 text-sm mb-2">您的累积加权平均 T2</div>
            <div class="text-4xl font-bold text-accent-purple mb-2">{{ reportData.cumulativeT2.toFixed(2) }}%</div>
            <div class="text-white/50 text-xs">基于历史数据计算(蓝浩歌公式)</div>
          </div>

          <!-- 缴费效率评分 - 使用可视化组件 -->
          <div class="glass-card p-6 fade-in" style="animation-delay: 0.1s">
            <EfficiencyScoreDisplay 
              :score="reportData.efficiencyScore" 
              :size="160"
            :stroke-width="10"
            :showDetails="false"
          />
        </div>

        <!-- 累计补贴 -->
        <div class="glass-card p-6 slide-in-right" style="animation-delay: 0.2s">
          <div class="text-white/60 text-sm mb-2">累计获得补贴</div>
          <div class="text-4xl font-bold text-green-400 mb-2">¥{{ reportData.totalSubsidy.toLocaleString() }}</div>
          <div class="text-white/50 text-xs">近3年总计</div>
        </div>
      </div>

      <!-- 历史缴费趋势图 -->
      <div class="glass-card p-8 mb-8 fade-in">
        <h2 class="text-2xl font-bold mb-6 text-white">您的历史缴费趋势分析</h2>
        <div class="h-80 rounded-lg">
          <VChart :option="chartOption" class="h-full w-full" autoresize />
        </div>
        <!-- 移除平均数据,仅保留图表展示个人真实轨迹 -->
      </div>

      <!-- 诊断结果与建议 -->
      <div class="glass-card p-8 mb-8 fade-in">
        <h2 class="text-2xl font-bold mb-6 text-white flex items-center">
          <svg class="w-6 h-6 mr-3 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
          </svg>
          AI诊断结果
        </h2>

        <div class="space-y-6">
          <!-- 诊断项1 -->
          <div class="bg-white/5 rounded-lg p-6">
            <div class="flex items-start">
              <div :class="['w-10 h-10 rounded-full flex items-center justify-center mr-4 flex-shrink-0',
                            reportData.diagnosis.overContribution ? 'bg-red-500/20' : 'bg-green-500/20']">
                <svg v-if="reportData.diagnosis.overContribution" class="w-6 h-6 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                </svg>
                <svg v-else class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="flex-1">
                <h3 class="font-semibold text-white mb-2">缴费额度诊断</h3>
                <p v-if="reportData.diagnosis.overContribution" class="text-white/80 mb-3">
                  <span class="text-red-400 font-semibold">检测到过度缴费：</span>
                  您的缴费额超过最优区间，导致补贴边际递减，建议调整至 <span class="font-semibold">¥{{ reportData.recommendedAmount.toLocaleString() }}/年</span>
                </p>
                <p v-else class="text-white/80 mb-3">
                  <span class="text-green-400 font-semibold">缴费策略合理：</span>
                  {{ reportData.diagnosis.message || '您的缴费额处于最优区间，能够充分享受补贴且避免过度税负' }}
                </p>
              </div>
            </div>
          </div>

          <!-- 诊断项2 -->
          <div class="bg-white/5 rounded-lg p-6">
            <div class="flex items-start">
              <div class="w-10 h-10 rounded-full bg-blue-500/20 flex items-center justify-center mr-4 flex-shrink-0">
                <svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                </svg>
              </div>
              <div class="flex-1">
                <h3 class="font-semibold text-white mb-2">T3税负预警</h3>
                <p class="text-white/80 mb-3">
                  基于当前缴费轨迹，预测您的领取期税率 t3 = <span class="font-semibold text-accent-purple">{{ reportData.predictedT3.toFixed(1) }}%</span>。
                  {{ reportData.predictedT3 > 5 ? '需优化缴费策略以降低领取期税负' : reportData.predictedT3 > 3 ? '处于合理区间' : '优秀，领取期税负较低' }}
                </p>
                <p class="text-white/60 text-xs">
                  💡 T3由您的T2和年薪动态计算，不同于传统固定3%税率
                </p>
              </div>
            </div>
          </div>

          <!-- 诊断项3 -->
          <div class="bg-white/5 rounded-lg p-6">
            <div class="flex items-start">
              <div class="w-10 h-10 rounded-full bg-purple-500/20 flex items-center justify-center mr-4 flex-shrink-0">
                <svg class="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <div class="flex-1">
                <h3 class="font-semibold text-white mb-2">潜在优化空间</h3>
                <p class="text-white/80 mb-3">
                  <template v-if="reportData.potentialGain > 0">
                    若采纳AI优化建议调整未来缴费策略，预计可额外获得补贴 
                    <span class="font-semibold text-green-400">¥{{ reportData.potentialGain.toLocaleString() }}</span>，
                    且全周期NPV提升 <span class="font-semibold">{{ Math.abs(reportData.npvImprovement).toFixed(2) }}%</span>
                  </template>
                  <template v-else>
                    当前缴费策略已接近最优，建议保持当前策略并关注政策变化
                  </template>
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- AI个性化诊断建议 (新增) -->
      <AIDiagnosis 
        :diagnosisResult="reportData"
        :currentAge="userAge"
        :autoLoad="true"
      />

      <!-- 五档缴费方案对比 (新增) -->
      <FiveTierSuggestions
        :currentAge="userAge"
        :annualSalary="userSalary"
        :autoLoad="true"
        @selectTier="handleTierSelection"
      />

      <!-- 优化建议 -->
      <div class="glass-card p-8 mb-8 fade-in">
        <h2 class="text-2xl font-bold mb-6 text-white">未来缴费策略优化建议</h2>
        <div class="bg-gradient-to-r from-accent-purple/20 to-blue-500/20 border border-accent-purple/30 rounded-lg p-6">
          <div class="flex items-start mb-4">
            <svg class="w-8 h-8 text-accent-purple mr-4 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
            </svg>
            <div>
              <h3 class="text-xl font-semibold text-white mb-3">AIPPOF智能建议</h3>
              <ul class="space-y-2 text-white/80">
                <li class="flex items-start">
                  <span class="text-accent-purple mr-2">•</span>
                  <span><strong>调整年度缴费至 ¥{{ reportData.recommendedAmount.toLocaleString() }}</strong>（当前：¥{{ reportData.currentAmount.toLocaleString() }}）</span>
                </li>
                <li class="flex items-start">
                  <span class="text-accent-purple mr-2">•</span>
                  <span>避免在补贴递减区间（收入40k-100k）过度缴费</span>
                </li>
                <li class="flex items-start">
                  <span class="text-accent-purple mr-2">•</span>
                  <span>优先在高边际税率年份（如获得奖金年份）增加缴费</span>
                </li>
                <li class="flex items-start">
                  <span class="text-accent-purple mr-2">•</span>
                  <span>关注政策调整，及时重新评估缴费策略</span>
                </li>
              </ul>
            </div>
          </div>
          <div class="flex justify-center mt-6">
            <button class="btn-primary">
              接受建议并设置提醒
            </button>
          </div>
        </div>
      </div>

      <!-- 底部说明 -->
      <div class="text-center text-white/50 text-sm fade-in">
        <p>* 以上诊断基于历史数据，建议结合个人实际情况调整</p>
        <p class="mt-2">系统每季度自动更新诊断报告，确保策略最优</p>
      </div>
    </div><!-- 关闭 v-else -->
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import axios from 'axios'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart, BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
} from 'echarts/components'
import EfficiencyScoreDisplay from '@/components/EfficiencyScoreDisplay.vue'
import AIDiagnosis from '@/components/AIDiagnosis.vue'
import FiveTierSuggestions from '@/components/FiveTierSuggestions.vue'

// 注册ECharts组件
use([
  CanvasRenderer,
  LineChart,
  BarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent
])

const router = useRouter()
const route = useRoute()

// 从route query获取用户基本信息
const userAge = ref(30)
const userSalary = ref(150000)

// 诊断报告数据(从后端API获取)
const reportData = ref({
  cumulativeT2: 0,
  efficiencyScore: 0,
  totalSubsidy: 0,
  diagnosis: {
    overContribution: false,
    underContribution: false,
    message: ''
  },
  predictedT3: 0,
  potentialGain: 0,
  npvImprovement: 0,
  recommendedAmount: 0,
  currentAmount: 0,
  historicalDetails: {
    t2ByYear: [] as Array<{year: number, t2: number, contribution: number, salary: number}>,
    subsidyByYear: [] as Array<{year: number, subsidy: number, contribution: number, salary: number}>
  }
})

const isLoading = ref(true)

// ECharts图表配置
const chartOption = computed(() => {
  const years = reportData.value.historicalDetails.t2ByYear.map(item => item.year.toString())
  const salaries = reportData.value.historicalDetails.t2ByYear.map(item => item.salary / 1000) // 转换为千元
  const contributions = reportData.value.historicalDetails.t2ByYear.map(item => item.contribution)
  const t2Values = reportData.value.historicalDetails.t2ByYear.map(item => item.t2)
  const subsidies = reportData.value.historicalDetails.subsidyByYear.map(item => item.subsidy)

  return {
    backgroundColor: 'transparent',
    title: {
      show: false
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(17, 24, 39, 0.95)',
      borderColor: 'rgba(99, 102, 241, 0.5)',
      borderWidth: 1,
      textStyle: {
        color: '#E5E7EB'
      },
      formatter: (params: any) => {
        const year = params[0].axisValue
        let result = `<div style="padding: 8px;"><b>${year}年</b><br/>`
        params.forEach((param: any) => {
          const marker = param.marker
          const name = param.seriesName
          let value = param.value
          if (name === '年薪') {
            value = `¥${value.toLocaleString()}千`
          } else if (name === '缴费额' || name === '补贴金额') {
            value = `¥${value.toLocaleString()}`
          } else if (name === 'T2值') {
            value = `${value}%`
          }
          result += `${marker} ${name}: ${value}<br/>`
        })
        result += '</div>'
        return result
      }
    },
    legend: {
      data: ['年薪', '缴费额', 'T2值', '补贴金额'],
      top: 10,
      textStyle: {
        color: '#E5E7EB'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '10%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: years,
      axisLine: {
        lineStyle: {
          color: 'rgba(255, 255, 255, 0.3)'
        }
      },
      axisLabel: {
        color: '#E5E7EB'
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '年薪(千元)/缴费额(元)',
        position: 'left',
        axisLine: {
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.3)'
          }
        },
        axisLabel: {
          color: '#E5E7EB',
          formatter: (value: number) => value.toLocaleString()
        },
        splitLine: {
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.1)'
          }
        }
      },
      {
        type: 'value',
        name: 'T2值(%)/补贴(元)',
        position: 'right',
        axisLine: {
          lineStyle: {
            color: 'rgba(255, 255, 255, 0.3)'
          }
        },
        axisLabel: {
          color: '#E5E7EB'
        },
        splitLine: {
          show: false
        }
      }
    ],
    series: [
      {
        name: '年薪',
        type: 'bar',
        data: salaries,
        yAxisIndex: 0,
        itemStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(99, 102, 241, 0.8)' },
              { offset: 1, color: 'rgba(99, 102, 241, 0.3)' }
            ]
          }
        },
        barWidth: '20%'
      },
      {
        name: '缴费额',
        type: 'bar',
        data: contributions,
        yAxisIndex: 0,
        itemStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(168, 85, 247, 0.8)' },
              { offset: 1, color: 'rgba(168, 85, 247, 0.3)' }
            ]
          }
        },
        barWidth: '20%'
      },
      {
        name: 'T2值',
        type: 'line',
        data: t2Values,
        yAxisIndex: 1,
        smooth: true,
        lineStyle: {
          color: '#10B981',
          width: 3
        },
        itemStyle: {
          color: '#10B981'
        },
        symbol: 'circle',
        symbolSize: 8
      },
      {
        name: '补贴金额',
        type: 'line',
        data: subsidies,
        yAxisIndex: 1,
        smooth: true,
        lineStyle: {
          color: '#F59E0B',
          width: 3
        },
        itemStyle: {
          color: '#F59E0B'
        },
        symbol: 'diamond',
        symbolSize: 8
      }
    ]
  }
})

const goBack = () => {
  router.push('/path-b/input')
}

const getEfficiencyColor = (score: number): string => {
  if (score >= 90) return 'text-green-400'
  if (score >= 70) return 'text-blue-400'
  if (score >= 50) return 'text-yellow-400'
  return 'text-red-400'
}

const getEfficiencyLabel = (score: number): string => {
  if (score >= 90) return '优秀'
  if (score >= 70) return '良好'
  if (score >= 50) return '一般'
  return '待改进'
}

// 处理5档方案选择
const handleTierSelection = (tier: any, index: number) => {
  console.log('用户选择方案:', tier.name, '缴费额:', tier.contribution)
  // TODO: 可以在这里记录用户选择,或跳转到下一步
  alert(`您选择了${tier.name}方案\n年度缴费: ¥${tier.contribution.toLocaleString()}\nNPV: ¥${tier.npv.toLocaleString()}`)
}

// 页面加载时调用后端API获取真实数据
onMounted(async () => {
  try {
    isLoading.value = true
    
    // 从route query中获取历史数据
    const historyDataStr = route.query.historyData as string
    if (!historyDataStr) {
      console.error('❌ 未找到历史数据')
      return
    }
    
    const historyData = JSON.parse(historyDataStr)
    const age = Number(route.query.age) || 30
    const currentSalary = Number(route.query.currentSalary) || 150000
    const wageGrowthRate = Number(route.query.wageGrowthRate) || 0.05
    
    // 保存用户信息以供组件使用
    userAge.value = age
    userSalary.value = currentSalary
    
    // 构造历史数据数组
    const yearsData = Object.entries(historyData).map(([year, data]: [string, any]) => ({
      year: Number(year),
      salary: data.salary,
      contribution: data.contribution
    })).sort((a, b) => a.year - b.year)
    
    // 如果没有从query获取到currentSalary,使用最新年份的年薪
    if (!route.query.currentSalary && yearsData.length > 0) {
      userSalary.value = yearsData[yearsData.length - 1].salary
    }
    
    console.log('📊 调用历史诊断API:', { yearsData, age, currentSalary, wageGrowthRate })
    console.log('👤 用户信息:', { userAge: userAge.value, userSalary: userSalary.value })
    
    // 调用历史诊断API (修复字段名匹配后端期望)
    const diagnosisResponse = await axios.post('http://localhost:8000/api/diagnose-history', {
      historyData: yearsData,  // 后端期望 historyData 不是 years_data
      age: age                 // 后端期望 age 不是 current_age
    })
    
    const diagnosisData = diagnosisResponse.data
    console.log('✅ 历史诊断API响应:', diagnosisData)
    
    // 更新报告数据 (后端返回的是camelCase格式,直接使用)
    reportData.value = {
      cumulativeT2: diagnosisData.cumulativeT2 || 0,
      efficiencyScore: diagnosisData.efficiencyScore || 0,
      totalSubsidy: diagnosisData.totalSubsidy || 0,
      diagnosis: {
        overContribution: diagnosisData.diagnosis?.overContribution || false,
        underContribution: diagnosisData.diagnosis?.underContribution || false,
        message: diagnosisData.diagnosis?.message || '缴费策略合理'
      },
      predictedT3: diagnosisData.predictedT3 || 0,
      potentialGain: diagnosisData.potentialGain || 0,
      npvImprovement: diagnosisData.npvImprovement || 0,
      recommendedAmount: diagnosisData.recommendedAmount || 12000,
      currentAmount: yearsData[yearsData.length - 1]?.contribution || 12000,
      historicalDetails: {
        t2ByYear: diagnosisData.historicalDetails?.t2ByYear || [],
        subsidyByYear: diagnosisData.historicalDetails?.subsidyByYear || [],
        averageSalary: diagnosisData.historicalDetails?.averageSalary || 0,
        averageContribution: diagnosisData.historicalDetails?.averageContribution || 0,
        totalContribution: diagnosisData.historicalDetails?.totalContribution || 0
      }
    }
    
    console.log('✅ PathB报告数据已更新:', reportData.value)
    
  } catch (error) {
    console.error('❌ 调用历史诊断API失败:', error)
    alert('加载诊断数据失败，请返回重试')
  } finally {
    isLoading.value = false
  }
})

</script>

<style scoped>
.report-page {
  background: linear-gradient(135deg, #2C2A4A 0%, #1A3A52 100%);
  min-height: 100vh;
}
</style>
