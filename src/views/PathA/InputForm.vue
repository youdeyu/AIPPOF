<template>
  <div class="input-form-page min-h-screen p-8">
    <div class="container max-w-4xl mx-auto">
      <!-- 返回按钮 -->
      <button @click="goBack" class="mb-6 text-white/70 hover:text-white flex items-center transition-colors">
        <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
        </svg>
        返回首页
      </button>

      <!-- 页面标题 -->
      <div class="text-center mb-8 fade-in">
        <h1 class="text-4xl font-bold mb-3 text-white">新参与者 - AI方案预测</h1>
        <p class="text-white/70">请填写您的基本信息，AI将为您预测工资增长率并计算最优缴费方案</p>
        
        <!-- 快速说明 -->
        <div class="mt-6 max-w-2xl mx-auto bg-accent-purple/10 border border-accent-purple/30 rounded-lg p-4 text-left">
          <div class="flex items-start">
            <svg class="w-5 h-5 text-accent-purple mr-2 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
            <div class="text-sm text-white/80">
              <strong class="text-accent-purple">PathA为新参与者设计</strong>，基于您的行业、职级和年龄，我们的AI模型将：
              <ul class="mt-2 space-y-1 ml-4">
                <li>• 预测您未来的工资增长率（g）</li>
                <li>• 计算个性化缴费上限（Formula 5-5）</li>
                <li>• 计算T2税收优惠率（蓝浩歌论文）</li>
                <li>• 计算T3领取期税率（双逻辑函数）</li>
                <li>• 计算精准补贴额度（渐进式补贴机制）</li>
                <li>• 推荐3个NPV最优方案供您选择</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- 表单卡片 -->
      <div class="glass-card p-8 fade-in">
        <form @submit.prevent="handleSubmit">
          <!-- 基本信息区域 -->
          <div class="mb-8">
            <h2 class="text-xl font-semibold mb-4 text-white flex items-center">
              <span class="w-8 h-8 rounded-full bg-accent-purple/20 flex items-center justify-center mr-3 text-sm">1</span>
              基本信息
            </h2>
            <div class="grid md:grid-cols-2 gap-6">
              <div>
                <label class="block text-white/80 mb-2 text-sm">年龄 *</label>
                <input
                  v-model.number="formData.age"
                  type="number"
                  min="18"
                  max="59"
                  required
                  class="input-field"
                  placeholder="请输入您的年龄（18-59岁）"
                />
              </div>
              <div>
                <label class="block text-white/80 mb-2 text-sm">性别 *</label>
                <select v-model="formData.gender" required class="input-field">
                  <option value="" disabled>请选择性别</option>
                  <option value="male">男</option>
                  <option value="female">女</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 收入信息区域 -->
          <div class="mb-8">
            <h2 class="text-xl font-semibold mb-4 text-white flex items-center">
              <span class="w-8 h-8 rounded-full bg-accent-purple/20 flex items-center justify-center mr-3 text-sm">2</span>
              收入信息
            </h2>
            <div>
              <label class="block text-white/80 mb-2 text-sm">年薪（税前）*</label>
              <div class="relative">
                <input
                  v-model.number="formData.annualSalary"
                  type="number"
                  min="0"
                  step="1000"
                  required
                  class="input-field pr-12"
                  placeholder="请输入您的年薪（元）"
                />
                <span class="absolute right-4 top-1/2 -translate-y-1/2 text-white/50">元</span>
              </div>
              <p class="text-xs text-white/50 mt-1">* 请输入税前年薪，包括基本工资、奖金、补贴等</p>
            </div>
          </div>

          <!-- 职业信息区域 -->
          <div class="mb-8">
            <h2 class="text-xl font-semibold mb-4 text-white flex items-center">
              <span class="w-8 h-8 rounded-full bg-accent-purple/20 flex items-center justify-center mr-3 text-sm">3</span>
              职业信息
            </h2>
            <div class="grid md:grid-cols-2 gap-6">
              <div>
                <label class="block text-white/80 mb-2 text-sm">所属行业 *</label>
                <select v-model="formData.industry" required class="input-field">
                  <option value="" disabled>请选择所属行业</option>
                  <option value="it">IT/互联网</option>
                  <option value="finance">金融</option>
                  <option value="manufacturing">制造业</option>
                  <option value="education">教育</option>
                  <option value="healthcare">医疗</option>
                  <option value="government">政府/事业单位</option>
                  <option value="retail">零售/服务业</option>
                  <option value="construction">建筑/房地产</option>
                  <option value="other">其他</option>
                </select>
              </div>
              <div>
                <label class="block text-white/80 mb-2 text-sm">职级 *</label>
                <select v-model="formData.jobLevel" required class="input-field">
                  <option value="" disabled>请选择职级</option>
                  <option value="entry">初级（0-2年）</option>
                  <option value="intermediate">中级（3-5年）</option>
                  <option value="senior">高级（6-10年）</option>
                  <option value="management">管理层（10年以上）</option>
                </select>
              </div>
            </div>
          </div>

          <!-- 提交按钮 -->
          <div class="flex justify-center mt-8">
            <button type="submit" class="btn-primary text-lg px-12" :disabled="isSubmitting">
              <span v-if="!isSubmitting">开始AI预测分析</span>
              <span v-else>分析中...</span>
            </button>
          </div>
        </form>
      </div>

      <!-- 底部提示 -->
      <div class="text-center mt-6 text-white/50 text-sm fade-in">
        <p>您的数据将被加密传输，仅用于AI模型计算，不会用于其他用途</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

interface FormData {
  age: number | null
  gender: string
  annualSalary: number | null
  industry: string
  jobLevel: string
}

const formData = ref<FormData>({
  age: null,
  gender: '',
  annualSalary: null,
  industry: '',
  jobLevel: ''
})

const isSubmitting = ref(false)

const goBack = () => {
  router.push('/')
}

const handleSubmit = async () => {
  isSubmitting.value = true
  
  try {
    // 跳转到报告页面（携带数据）
    router.push({
      name: 'PathAReport',
      query: {
        age: formData.value.age?.toString(),
        salary: formData.value.annualSalary?.toString(),
        gender: formData.value.gender,
        industry: formData.value.industry,
        level: formData.value.jobLevel
      }
    })
  } catch (error) {
    console.error('提交失败:', error)
    alert('提交失败，请稍后重试')
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.input-form-page {
  background: linear-gradient(135deg, #2C2A4A 0%, #1A3A52 100%);
  min-height: 100vh;
}

select.input-field {
  cursor: pointer;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
