<template>
  <div class="five-tier-suggestions">
    <div class="glass-card p-8 mb-8 fade-in">
      <h2 class="text-2xl font-bold mb-6 text-white flex items-center">
        <svg class="w-7 h-7 mr-3 text-accent-purple" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
        </svg>
        📊 五档缴费方案NPV对比
      </h2>

      <p class="text-white/70 mb-6">
        基于您的当前年龄{{ currentAge }}岁和年薪¥{{ annualSalary.toLocaleString() }}，
        我们为您提供5个不同风险偏好的缴费方案，助您做出最优选择
      </p>

      <!-- 加载状态 -->
      <div v-if="isLoading" class="text-center py-12">
        <div class="inline-block animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-accent-purple mb-4"></div>
        <p class="text-white/70">正在计算各档方案...</p>
      </div>

      <!-- 错误状态 -->
      <div v-else-if="error" class="bg-red-500/10 border border-red-500/30 rounded-lg p-6">
        <p class="text-red-400">{{ error }}</p>
      </div>

      <!-- 5档方案展示 -->
      <div v-else-if="tiers && tiers.length > 0" class="space-y-6">
        <!-- 方案卡片 -->
        <div 
          v-for="(tier, index) in tiers" 
          :key="index"
          class="border rounded-lg p-6 transition-all hover:shadow-xl"
          :class="[
            index === 2 ? 'border-accent-purple bg-accent-purple/10 scale-105' : 'border-white/20 hover:border-accent-purple/50'
          ]"
        >
          <!-- 方案标题 -->
          <div class="flex items-center justify-between mb-4">
            <div class="flex items-center">
              <span class="text-3xl mr-3">{{ tier.icon }}</span>
              <div>
                <h3 class="text-xl font-bold text-white flex items-center">
                  {{ tier.name }}
                  <span v-if="index === 2" class="ml-2 px-2 py-0.5 bg-accent-purple text-white text-xs rounded-full">
                    ✨ AI推荐
                  </span>
                </h3>
                <p class="text-white/60 text-sm">{{ tier.suitableFor }}</p>
              </div>
            </div>
            <div class="text-right">
              <div class="text-sm text-white/60">上限利用率</div>
              <div :class="[
                'text-2xl font-bold',
                tier.capUtilization >= 70 ? 'text-red-400' : 
                tier.capUtilization >= 50 ? 'text-yellow-400' : 'text-green-400'
              ]">
                {{ tier.capUtilization }}%
              </div>
            </div>
          </div>

          <!-- 核心指标 -->
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
            <div class="bg-black/20 rounded-lg p-3 text-center">
              <div class="text-white/60 text-xs mb-1">年度缴费</div>
              <div class="text-white font-bold text-lg">¥{{ tier.contribution.toLocaleString() }}</div>
            </div>
            <div class="bg-black/20 rounded-lg p-3 text-center">
              <div class="text-white/60 text-xs mb-1">年度收益</div>
              <div class="text-green-400 font-bold text-lg">¥{{ tier.annualBenefit.toLocaleString() }}</div>
            </div>
            <div class="bg-black/20 rounded-lg p-3 text-center">
              <div class="text-white/60 text-xs mb-1">全周期NPV</div>
              <div class="text-accent-purple font-bold text-lg">¥{{ tier.npv.toLocaleString() }}</div>
            </div>
            <div class="bg-black/20 rounded-lg p-3 text-center">
              <div class="text-white/60 text-xs mb-1">风险等级</div>
              <div :class="[
                'font-bold text-lg',
                tier.riskLevel === '低' ? 'text-green-400' : 
                tier.riskLevel === '中' ? 'text-yellow-400' : 'text-red-400'
              ]">
                {{ tier.riskLevel }}
              </div>
            </div>
          </div>

          <!-- 方案特点 -->
          <div class="mb-4">
            <div class="text-white/80 text-sm font-semibold mb-2">💡 方案特点：</div>
            <ul class="space-y-1">
              <li v-for="(char, cidx) in tier.characteristics" :key="cidx" 
                  class="text-white/70 text-sm flex items-start">
                <span class="text-accent-purple mr-2">•</span>
                <span>{{ char }}</span>
              </li>
            </ul>
          </div>

          <!-- 选择按钮 -->
          <button 
            @click="selectTier(tier, index)"
            :class="[
              'w-full py-2 rounded-lg font-semibold transition-all',
              index === 2 
                ? 'bg-accent-purple text-white hover:bg-accent-purple/80' 
                : 'bg-white/10 text-white hover:bg-white/20'
            ]"
          >
            {{ index === 2 ? '✨ 选择推荐方案' : '选择此方案' }}
          </button>
        </div>

        <!-- 方案对比说明 -->
        <div class="bg-blue-500/10 border border-blue-500/30 rounded-lg p-5">
          <div class="flex items-start">
            <svg class="w-5 h-5 text-blue-400 mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div class="text-sm text-white/80">
              <strong class="text-blue-400">方案选择建议</strong>：
              <ul class="mt-2 space-y-1 ml-4">
                <li>• <strong>保守型</strong>：适合风险厌恶者，现金流压力小，但NPV较低</li>
                <li>• <strong>稳健型</strong>：平衡风险与收益，适合大多数人</li>
                <li>• <strong>平衡型</strong>：⭐ AI推荐，NPV最优，综合性价比最高</li>
                <li>• <strong>进取型</strong>：高缴费高收益，适合高收入且对未来乐观者</li>
                <li>• <strong>激进型</strong>：接近上限，收益最大但流动性压力大</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { API_ENDPOINTS } from '../config'

interface Tier {
  name: string
  icon: string
  contribution: number
  capUtilization: number
  npv: number
  annualBenefit: number
  characteristics: string[]
  suitableFor: string
  riskLevel: string
}

interface Props {
  currentAge: number
  annualSalary: number
  autoLoad?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  autoLoad: true
})

const emit = defineEmits<{
  (e: 'selectTier', tier: Tier, index: number): void
}>()

const isLoading = ref(false)
const error = ref('')
const tiers = ref<Tier[]>([])

// 加载5档方案
const load5TierSuggestions = async () => {
  if (!props.currentAge || !props.annualSalary) {
    error.value = '缺少必要参数'
    return
  }

  isLoading.value = true
  error.value = ''

  try {
    const response = await fetch(API_ENDPOINTS.fiveTierSuggestions, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        currentAge: props.currentAge,
        annualSalary: props.annualSalary
      })
    })

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`)
    }

    const data = await response.json()
    
    // 转换为前端需要的格式
    tiers.value = data.tiers.map((tier: any) => ({
      name: tier.name,
      icon: tier.icon,
      contribution: tier.contribution,
      capUtilization: tier.cap_utilization || tier.capUtilization,
      npv: typeof tier.npv === 'object' ? tier.npv.total_npv : tier.npv,  // 修复：提取total_npv
      annualBenefit: tier.annual_benefit || tier.annualBenefit,
      characteristics: tier.characteristics,
      suitableFor: tier.suitable_for || tier.suitableFor,
      riskLevel: tier.risk_level || tier.riskLevel
    }))
  } catch (err: any) {
    error.value = `加载5档方案失败: ${err.message}`
    console.error('5档方案加载错误:', err)
  } finally {
    isLoading.value = false
  }
}

// 选择方案
const selectTier = (tier: Tier, index: number) => {
  emit('selectTier', tier, index)
  console.log('用户选择方案:', tier.name, tier.contribution)
}

// 监听参数变化
watch([() => props.currentAge, () => props.annualSalary], () => {
  if (props.autoLoad) {
    load5TierSuggestions()
  }
})

onMounted(() => {
  if (props.autoLoad) {
    load5TierSuggestions()
  }
})

// 暴露方法供父组件调用
defineExpose({
  load5TierSuggestions
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


.scale-105 {
  transform: scale(1.02);
}
</style>
