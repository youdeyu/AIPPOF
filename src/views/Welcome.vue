<template>
  <div class="welcome-page min-h-screen flex items-center justify-center p-8">
    <div class="container max-w-6xl mx-auto">
      <!-- 标题区域 -->
      <div class="text-center mb-16 fade-in">
        <h1 class="text-5xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-purple-400 to-blue-400">
          AIPPOF
        </h1>
        <p class="text-2xl text-white/80 mb-2">AI-driven Personal Pension Optimization Framework</p>
        <p class="text-lg text-white/60">个人养老金智能优化决策支持系统</p>
        <div class="mt-8 text-white/70">
          <p class="text-sm">基于学术模型，为您提供个性化养老金缴费建议</p>
        </div>
      </div>

      <!-- 分流卡片区域 -->
      <div class="grid md:grid-cols-2 gap-8 mb-12">
        <!-- 路径A：新参与者 - 方案预测 -->
        <div class="glass-card p-8 hover:scale-105 transition-transform duration-300 cursor-pointer slide-in-left"
             @click="navigateToPathA">
          <div class="flex items-center justify-center mb-6">
            <div class="w-16 h-16 rounded-full bg-accent-purple/20 flex items-center justify-center">
              <svg class="w-8 h-8 text-accent-purple" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
              </svg>
            </div>
          </div>
          <h2 class="text-2xl font-bold mb-4 text-center">路径 A</h2>
          <h3 class="text-xl text-accent-purple mb-4 text-center">新参与者 - 方案预测</h3>
          <div class="space-y-3 text-white/80 mb-6">
            <div class="flex items-start">
              <span class="text-accent-purple mr-2">✓</span>
              <span>AI预测工资增长率 (g)</span>
            </div>
            <div class="flex items-start">
              <span class="text-accent-purple mr-2">✓</span>
              <span>计算个人化平均节税率 (T2)</span>
            </div>
            <div class="flex items-start">
              <span class="text-accent-purple mr-2">✓</span>
              <span>给出最优缴费额建议</span>
            </div>
            <div class="flex items-start">
              <span class="text-accent-purple mr-2">✓</span>
              <span>NPV对比：采纳 vs 维持现状</span>
            </div>
          </div>
          <div class="text-center">
            <button class="btn-primary w-full">
              开始预测
            </button>
          </div>
        </div>

        <!-- 路径B：已参与者 - 方案诊断 -->
        <div class="glass-card p-8 hover:scale-105 transition-transform duration-300 cursor-pointer slide-in-right"
             @click="navigateToPathB">
          <div class="flex items-center justify-center mb-6">
            <div class="w-16 h-16 rounded-full bg-blue-500/20 flex items-center justify-center">
              <svg class="w-8 h-8 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                      d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </div>
          </div>
          <h2 class="text-2xl font-bold mb-4 text-center">路径 B</h2>
          <h3 class="text-xl text-blue-400 mb-4 text-center">已参与者 - 方案诊断</h3>
          <div class="space-y-3 text-white/80 mb-6">
            <div class="flex items-start">
              <span class="text-blue-400 mr-2">✓</span>
              <span>解析历史缴费记录</span>
            </div>
            <div class="flex items-start">
              <span class="text-blue-400 mr-2">✓</span>
              <span>计算累积加权平均 T2</span>
            </div>
            <div class="flex items-start">
              <span class="text-blue-400 mr-2">✓</span>
              <span>诊断缴费效率问题</span>
            </div>
            <div class="flex items-start">
              <span class="text-blue-400 mr-2">✓</span>
              <span>优化未来缴费策略</span>
            </div>
          </div>
          <div class="text-center">
            <button class="btn-secondary w-full">
              开始诊断
            </button>
          </div>
        </div>
      </div>

      <!-- 底部说明 -->
      <div class="text-center text-white/50 text-sm fade-in">
        <p class="mb-2">* T2 = 平均节税率 | T3 = 领取期累进税率（0%-14%）</p>
        <p>基于财政中性约束的NPV优化模型，考虑补贴最大化与税负优化</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const navigateToPathA = () => {
  router.push('/path-a/input')
}

const navigateToPathB = () => {
  router.push('/path-b/input')
}
</script>

<style scoped>
.welcome-page {
  background: linear-gradient(135deg, #2C2A4A 0%, #1A3A52 100%);
}
</style>
