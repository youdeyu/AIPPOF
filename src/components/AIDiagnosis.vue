<template>
  <div class="ai-diagnosis">
    <!-- AI诊断建议 -->
    <div class="glass-card p-8 mb-8 fade-in">
      <h2 class="text-2xl font-bold mb-6 text-white flex items-center">
        <svg class="w-7 h-7 mr-3 text-accent-purple" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
        </svg>
        🤖 AI个性化诊断建议
      </h2>

      <!-- 加载状态 -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-accent-purple mb-4"></div>
        <p class="text-white/70">AI正在分析您的历史数据...</p>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="bg-red-500/10 border border-red-500/30 rounded-lg p-6">
        <p class="text-red-400">{{ error }}</p>
      </div>

      <!-- AI建议内容 -->
      <div v-else-if="aiSuggestions" class="space-y-6">
        <!-- 预期收益 -->
        <div class="bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-500/30 rounded-lg p-6">
          <div class="flex items-center mb-3">
            <svg class="w-6 h-6 text-green-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
            <h3 class="text-lg font-semibold text-green-400">预期优化收益</h3>
          </div>
          <p class="text-white/90 text-lg">
            {{ aiSuggestions.expectedBenefit }}
          </p>
        </div>

        <!-- 优先级建议列表 -->
        <div class="space-y-4">
          <div 
            v-for="(suggestion, index) in aiSuggestions.suggestions" 
            :key="index"
            class="bg-white/5 rounded-lg p-5 border border-white/10 hover:border-accent-purple/50 transition-colors"
          >
            <div class="flex items-start">
              <!-- 优先级图标 -->
              <div :class="[
                'w-10 h-10 rounded-full flex items-center justify-center mr-4 flex-shrink-0',
                suggestion.priority === 'high' ? 'bg-red-500/20' : 
                suggestion.priority === 'medium' ? 'bg-yellow-500/20' : 'bg-blue-500/20'
              ]">
                <span :class="[
                  'text-lg font-bold',
                  suggestion.priority === 'high' ? 'text-red-400' : 
                  suggestion.priority === 'medium' ? 'text-yellow-400' : 'text-blue-400'
                ]">
                  {{ index + 1 }}
                </span>
              </div>

              <!-- 建议内容 -->
              <div class="flex-1">
                <div class="flex items-center mb-2">
                  <h4 class="font-semibold text-white">{{ suggestion.title }}</h4>
                  <span :class="[
                    'ml-2 px-2 py-0.5 rounded text-xs font-medium',
                    suggestion.priority === 'high' ? 'bg-red-500/20 text-red-400' : 
                    suggestion.priority === 'medium' ? 'bg-yellow-500/20 text-yellow-400' : 
                    'bg-blue-500/20 text-blue-400'
                  ]">
                    {{ suggestion.priority === 'high' ? '高优先级' : 
                       suggestion.priority === 'medium' ? '中优先级' : '低优先级' }}
                  </span>
                </div>
                <p class="text-white/80 text-sm leading-relaxed">
                  {{ suggestion.description }}
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- 行动计划 -->
        <div v-if="aiSuggestions.actionPlan && aiSuggestions.actionPlan.length > 0" 
             class="bg-blue-500/10 border border-blue-500/30 rounded-lg p-6">
          <div class="flex items-center mb-4">
            <svg class="w-6 h-6 text-blue-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4" />
            </svg>
            <h3 class="text-lg font-semibold text-blue-400">📋 立即行动计划</h3>
          </div>
          <ol class="space-y-2">
            <li v-for="(step, index) in aiSuggestions.actionPlan" :key="index" 
                class="flex items-start text-white/80">
              <span class="text-blue-400 font-bold mr-3">{{ index + 1 }}.</span>
              <span>{{ step }}</span>
            </li>
          </ol>
        </div>

        <!-- 风险提示 -->
        <div v-if="aiSuggestions.riskWarnings && aiSuggestions.riskWarnings.length > 0" 
             class="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-6">
          <div class="flex items-center mb-4">
            <svg class="w-6 h-6 text-yellow-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                    d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <h3 class="text-lg font-semibold text-yellow-400">⚠️ 风险提示</h3>
          </div>
          <ul class="space-y-2">
            <li v-for="(warning, index) in aiSuggestions.riskWarnings" :key="index" 
                class="flex items-start text-white/80">
              <span class="text-yellow-400 mr-2">•</span>
              <span>{{ warning }}</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { API_ENDPOINTS } from '../config'

interface Suggestion {
  title: string
  description: string
  priority: 'high' | 'medium' | 'low'
}

interface AISuggestions {
  suggestions: Suggestion[]
  actionPlan: string[]
  riskWarnings: string[]
  expectedBenefit: string
}

interface Props {
  diagnosisResult: any  // 来自history_diagnosis的诊断结果
  currentAge: number
  autoLoad?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  autoLoad: true
})

const isLoading = ref(false)
const error = ref('')
const aiSuggestions = ref<AISuggestions | null>(null)

// 加载AI建议
const loadAISuggestions = async () => {
  if (!props.diagnosisResult) {
    error.value = '缺少诊断结果数据'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    const response = await fetch(API_ENDPOINTS.aiSuggestions, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        diagnosisResult: props.diagnosisResult,
        currentAge: props.currentAge
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    const data = await response.json()
    aiSuggestions.value = data
  } catch (err: any) {
    error.value = `加载AI建议失败: ${err.message}`
    console.error('AI建议加载错误:', err)
  } finally {
    isLoading.value = false
  }
}

// 监听诊断结果变化
watch(() => props.diagnosisResult, (newVal) => {
  if (newVal && props.autoLoad) {
    loadAISuggestions()
  }
}, { immediate: true })

onMounted(() => {
  if (props.diagnosisResult && props.autoLoad) {
    loadAISuggestions()
  }
})

// 暴露方法供父组件调用
defineExpose({
  loadAISuggestions
})
</script>

<style scoped>
.fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
