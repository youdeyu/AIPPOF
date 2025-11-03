<template>
  <div class="efficiency-score-display">
    <!-- 效率评分仪表盘 -->
    <div class="relative">
      <!-- 圆形进度条 -->
      <svg class="transform -rotate-90" :width="size" :height="size" viewBox="0 0 200 200">
        <!-- 背景圆环 -->
        <circle
          cx="100"
          cy="100"
          :r="radius"
          fill="none"
          stroke="rgba(255, 255, 255, 0.1)"
          :stroke-width="strokeWidth"
        />
        
        <!-- 进度圆环 -->
        <circle
          cx="100"
          cy="100"
          :r="radius"
          fill="none"
          :stroke="scoreColor"
          :stroke-width="strokeWidth"
          :stroke-dasharray="circumference"
          :stroke-dashoffset="dashOffset"
          stroke-linecap="round"
          class="transition-all duration-1000 ease-out"
        />
      </svg>

      <!-- 中心文字 -->
      <div class="absolute inset-0 flex flex-col items-center justify-center">
        <div class="text-5xl font-bold mb-2" :style="{ color: scoreColor }">
          {{ displayScore }}
        </div>
        <div class="text-white/60 text-sm">{{ scoreLabel }}</div>
        <div class="mt-2 text-white/80 text-xs">效率评分</div>
      </div>
    </div>

    <!-- 评分说明 -->
    <div class="mt-6 space-y-3">
      <!-- 优秀 -->
      <div class="flex items-center justify-between p-3 rounded-lg" 
           :class="score >= 90 ? 'bg-green-500/20 border border-green-500/50' : 'bg-white/5'">
        <div class="flex items-center">
          <div class="w-3 h-3 rounded-full bg-green-400 mr-3"></div>
          <span class="text-white/80 text-sm">90-100分: 优秀</span>
        </div>
        <span v-if="score >= 90" class="text-green-400 text-sm">✓ 当前等级</span>
      </div>

      <!-- 良好 -->
      <div class="flex items-center justify-between p-3 rounded-lg" 
           :class="score >= 70 && score < 90 ? 'bg-blue-500/20 border border-blue-500/50' : 'bg-white/5'">
        <div class="flex items-center">
          <div class="w-3 h-3 rounded-full bg-blue-400 mr-3"></div>
          <span class="text-white/80 text-sm">70-89分: 良好</span>
        </div>
        <span v-if="score >= 70 && score < 90" class="text-blue-400 text-sm">✓ 当前等级</span>
      </div>

      <!-- 一般 -->
      <div class="flex items-center justify-between p-3 rounded-lg" 
           :class="score >= 50 && score < 70 ? 'bg-yellow-500/20 border border-yellow-500/50' : 'bg-white/5'">
        <div class="flex items-center">
          <div class="w-3 h-3 rounded-full bg-yellow-400 mr-3"></div>
          <span class="text-white/80 text-sm">50-69分: 一般</span>
        </div>
        <span v-if="score >= 50 && score < 70" class="text-yellow-400 text-sm">✓ 当前等级</span>
      </div>

      <!-- 待改进 -->
      <div class="flex items-center justify-between p-3 rounded-lg" 
           :class="score < 50 ? 'bg-red-500/20 border border-red-500/50' : 'bg-white/5'">
        <div class="flex items-center">
          <div class="w-3 h-3 rounded-full bg-red-400 mr-3"></div>
          <span class="text-white/80 text-sm">0-49分: 待改进</span>
        </div>
        <span v-if="score < 50" class="text-red-400 text-sm">✓ 当前等级</span>
      </div>
    </div>

    <!-- 评分构成详情 -->
    <div v-if="showDetails && breakdown" class="mt-6 bg-white/5 rounded-lg p-4">
      <h4 class="text-white font-semibold mb-3 text-sm">评分构成详情</h4>
      <div class="space-y-2">
        <div v-for="(item, key) in breakdown" :key="key" class="flex items-center justify-between text-sm">
          <span class="text-white/70">{{ getBreakdownLabel(key) }}</span>
          <div class="flex items-center">
            <div class="w-24 h-2 bg-white/10 rounded-full mr-2 overflow-hidden">
              <div 
                class="h-full bg-accent-purple rounded-full transition-all duration-500"
                :style="{ width: `${(item / score * 100)}%` }"
              ></div>
            </div>
            <span class="text-white font-semibold w-12 text-right">{{ item.toFixed(1) }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'

interface Props {
  score: number          // 0-100
  size?: number          // SVG大小
  strokeWidth?: number   // 线条宽度
  showDetails?: boolean  // 是否显示详情
  breakdown?: Record<string, number>  // 评分构成
  animated?: boolean     // 是否启用动画
}

const props = withDefaults(defineProps<Props>(), {
  score: 0,
  size: 200,
  strokeWidth: 12,
  showDetails: false,
  breakdown: undefined,
  animated: true
})

const displayScore = ref(0)
const radius = computed(() => (props.size / 2) - (props.strokeWidth / 2) - 10)
const circumference = computed(() => 2 * Math.PI * radius.value)

const dashOffset = computed(() => {
  const progress = displayScore.value / 100
  return circumference.value * (1 - progress)
})

const scoreColor = computed(() => {
  if (displayScore.value >= 90) return '#4ade80'  // green-400
  if (displayScore.value >= 70) return '#60a5fa'  // blue-400
  if (displayScore.value >= 50) return '#fbbf24'  // yellow-400
  return '#f87171'  // red-400
})

const scoreLabel = computed(() => {
  if (displayScore.value >= 90) return '优秀'
  if (displayScore.value >= 70) return '良好'
  if (displayScore.value >= 50) return '一般'
  return '待改进'
})

const getBreakdownLabel = (key: string): string => {
  const labels: Record<string, string> = {
    subsidyUtilization: '补贴利用率',
    t2Efficiency: 'T2效率',
    capUtilization: '上限利用率',
    consistency: '一致性',
    optimization: '优化空间'
  }
  return labels[key] || key
}

// 动画效果
const animateScore = () => {
  if (!props.animated) {
    displayScore.value = props.score
    return
  }

  const duration = 1500  // 1.5秒
  const steps = 60
  const increment = props.score / steps
  let current = 0
  
  const interval = setInterval(() => {
    current += increment
    if (current >= props.score) {
      displayScore.value = props.score
      clearInterval(interval)
    } else {
      displayScore.value = Math.floor(current)
    }
  }, duration / steps)
}

watch(() => props.score, () => {
  animateScore()
})

onMounted(() => {
  animateScore()
})
</script>

<style scoped>
.transition-all {
  transition: all 0.3s ease;
}
</style>
