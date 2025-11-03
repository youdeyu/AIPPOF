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
        <h1 class="text-4xl font-bold mb-3 text-white">已参与者 - 方案诊断</h1>
        <p class="text-white/70">请提供您的历史缴费数据，AI将诊断您的缴费效率</p>
      </div>

      <!-- 表单卡片 -->
      <div class="glass-card p-8 fade-in">
        <!-- 数据输入方式选择 -->
        <div class="mb-8">
          <h2 class="text-xl font-semibold mb-4 text-white">请选择数据输入方式</h2>
          <div class="grid md:grid-cols-3 gap-4">
            <button
              @click="inputMethod = 'api'"
              :class="['p-4 rounded-lg border-2 transition-all', 
                       inputMethod === 'api' ? 'border-accent-purple bg-accent-purple/10' : 'border-white/20']"
            >
              <div class="text-center">
                <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <div class="font-semibold">自动对接</div>
                <div class="text-xs text-white/60 mt-1">授权连接养老金平台API</div>
              </div>
            </button>
            
            <button
              @click="inputMethod = 'upload'"
              :class="['p-4 rounded-lg border-2 transition-all', 
                       inputMethod === 'upload' ? 'border-accent-purple bg-accent-purple/10' : 'border-white/20']"
            >
              <div class="text-center">
                <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                </svg>
                <div class="font-semibold">上传截图</div>
                <div class="text-xs text-white/60 mt-1">工资/税务/人社APP截图（OCR识别）</div>
              </div>
            </button>
            
            <button
              @click="inputMethod = 'manual'"
              :class="['p-4 rounded-lg border-2 transition-all', 
                       inputMethod === 'manual' ? 'border-accent-purple bg-accent-purple/10' : 'border-white/20']"
            >
              <div class="text-center">
                <svg class="w-8 h-8 mx-auto mb-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
                <div class="font-semibold">手动录入</div>
                <div class="text-xs text-white/60 mt-1">填写近3年收入和缴费</div>
              </div>
            </button>
          </div>
        </div>

        <!-- 条件渲染不同输入表单 -->
        <!-- 方式1: API对接 -->
        <div v-if="inputMethod === 'api'" class="mb-8">
          <div class="bg-blue-500/10 border border-blue-500/30 rounded-lg p-6">
            <h3 class="font-semibold text-white mb-4">授权连接养老金平台</h3>
            <p class="text-white/70 text-sm mb-4">
              点击下方按钮，将跳转到养老金管理平台进行身份验证。授权后系统将自动获取您的历史缴费记录。
            </p>
            <button class="btn-primary">
              <svg class="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              授权连接
            </button>
          </div>
        </div>

        <!-- 方式2: 上传截图 -->
        <div v-if="inputMethod === 'upload'" class="mb-8">
          <h3 class="font-semibold text-white mb-4">上传APP截图（支持OCR自动识别）</h3>
          <div class="border-2 border-dashed border-white/30 rounded-lg p-8 text-center">
            <svg class="w-16 h-16 mx-auto mb-4 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
            </svg>
            <p class="text-white/70 mb-4">拖拽文件至此或点击上传</p>
            <input
              type="file"
              multiple
              accept="image/*"
              @change="handleFileUpload"
              class="hidden"
              ref="fileInput"
            />
            <button @click="triggerFileUpload" class="btn-secondary">
              选择文件
            </button>
            <p class="text-xs text-white/50 mt-4">支持格式: JPG, PNG (最多5张)</p>
          </div>
          <div v-if="uploadedFiles.length > 0" class="mt-4">
            <div class="text-sm text-white/70 mb-2">已上传 {{ uploadedFiles.length }} 个文件:</div>
            <div class="space-y-2">
              <div v-for="(file, index) in uploadedFiles" :key="index" 
                   class="flex items-center justify-between bg-white/5 rounded p-2">
                <span class="text-sm">{{ file.name }}</span>
                <button @click="removeFile(index)" class="text-red-400 hover:text-red-300">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 方式3: 手动录入 -->
        <div v-if="inputMethod === 'manual'">
          <!-- 基本信息 -->
          <h3 class="font-semibold text-white mb-4">基本信息</h3>
          <div class="glass-card p-6 mb-6">
            <div class="grid md:grid-cols-3 gap-4">
              <div>
                <label class="block text-white/80 mb-2 text-sm">当前年龄</label>
                <div class="relative">
                  <input
                    v-model.number="basicInfo.age"
                    type="number"
                    min="18"
                    max="60"
                    class="input-field pr-12"
                    placeholder="请输入年龄"
                  />
                  <span class="absolute right-4 top-1/2 -translate-y-1/2 text-white/50">岁</span>
                </div>
              </div>
              <div>
                <label class="block text-white/80 mb-2 text-sm">所属行业</label>
                <select v-model="basicInfo.industry" class="input-field">
                  <option value="">请选择</option>
                  <option value="it">互联网/IT</option>
                  <option value="finance">金融/保险</option>
                  <option value="manufacturing">制造业</option>
                  <option value="education">教育/培训</option>
                  <option value="healthcare">医疗/健康</option>
                  <option value="retail">零售/贸易</option>
                  <option value="construction">建筑/房地产</option>
                  <option value="service">服务业</option>
                  <option value="government">政府/事业单位</option>
                  <option value="other">其他</option>
                </select>
              </div>
              <div>
                <label class="block text-white/80 mb-2 text-sm">职级/职位</label>
                <select v-model="basicInfo.jobLevel" class="input-field">
                  <option value="">请选择</option>
                  <option value="entry">初级（1-3年）</option>
                  <option value="intermediate">中级（3-5年）</option>
                  <option value="senior">高级（5-10年）</option>
                  <option value="expert">专家级（10年以上）</option>
                  <option value="manager">管理岗</option>
                </select>
              </div>
            </div>
          </div>
          
          <h3 class="font-semibold text-white mb-4">近3年收入与缴费记录</h3>
          <div class="space-y-6">
            <div v-for="year in years" :key="year" class="glass-card p-6">
              <h4 class="text-lg font-semibold text-white mb-4">{{ year }}年</h4>
              <div class="grid md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-white/80 mb-2 text-sm">年薪（税前）</label>
                  <div class="relative">
                    <input
                      v-model.number="manualData[year].salary"
                      type="number"
                      min="0"
                      class="input-field pr-12"
                      placeholder="请输入年薪"
                    />
                    <span class="absolute right-4 top-1/2 -translate-y-1/2 text-white/50">元</span>
                  </div>
                </div>
                <div>
                  <label class="block text-white/80 mb-2 text-sm">个人养老金缴费额</label>
                  <div class="relative">
                    <input
                      v-model.number="manualData[year].contribution"
                      type="number"
                      min="0"
                      class="input-field pr-12"
                      placeholder="请输入缴费额"
                    />
                    <span class="absolute right-4 top-1/2 -translate-y-1/2 text-white/50">元</span>
                  </div>
                  <p class="text-white/60 text-xs mt-1">
                    💡 提示：缴费上限根据您的年薪和T2动态计算，系统会自动验证
                  </p>
                  <p v-if="manualData[year].contribution && manualData[year].contribution! < 0" 
                     class="text-red-400 text-xs mt-1">
                    ⚠️ 缴费额不能为负数
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 提交按钮 -->
        <div v-if="inputMethod" class="flex justify-center mt-8 gap-4">
          <!-- 测试数据快速填充按钮 -->
          <button 
            v-if="inputMethod === 'manual'"
            @click="fillTestData" 
            class="px-6 py-3 rounded-lg bg-blue-500/20 border border-blue-400/50 text-blue-300 hover:bg-blue-500/30 transition-colors"
          >
            🧪 填充测试数据
          </button>
          
          <button @click="handleSubmit" class="btn-primary text-lg px-12" :disabled="!canSubmit">
            <span v-if="!isSubmitting">开始诊断分析</span>
            <span v-else>分析中...</span>
          </button>
        </div>
      </div>

      <!-- 底部提示 -->
      <div class="text-center mt-6 text-white/50 text-sm fade-in">
        <p>您的数据将被加密存储，仅用于诊断计算，不会泄露给第三方</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

type InputMethod = 'api' | 'upload' | 'manual' | null

const inputMethod = ref<InputMethod>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const uploadedFiles = ref<File[]>([])
const isSubmitting = ref(false)

// 基本信息（用于AI预测）
const basicInfo = ref({
  age: null as number | null,
  industry: '',
  jobLevel: ''
})

const years = [2022, 2023, 2024]
const manualData = ref<Record<number, { salary: number | null; contribution: number | null }>>({
  2022: { salary: null, contribution: null },
  2023: { salary: null, contribution: null },
  2024: { salary: null, contribution: null }
})

// 测试数据填充函数
const fillTestData = () => {
  basicInfo.value.age = 27
  basicInfo.value.industry = 'finance'
  basicInfo.value.jobLevel = 'intermediate'
  manualData.value[2022] = { salary: 200000, contribution: 12000 }
  manualData.value[2023] = { salary: 210000, contribution: 13000 }
  manualData.value[2024] = { salary: 220000, contribution: 15000 }
  console.log('✅ 测试数据已填充')
}

const canSubmit = computed(() => {
  if (inputMethod.value === 'upload') {
    return uploadedFiles.value.length > 0
  } else if (inputMethod.value === 'manual') {
    // 检查基本信息是否完整
    const hasBasicInfo = basicInfo.value.age !== null && 
                         basicInfo.value.industry !== '' && 
                         basicInfo.value.jobLevel !== ''
    // 检查历史数据是否完整
    const hasHistoryData = years.every(year => 
      manualData.value[year].salary !== null && 
      manualData.value[year].contribution !== null
    )
    return hasBasicInfo && hasHistoryData
  } else if (inputMethod.value === 'api') {
    // API方式需要完成授权（这里简化处理）
    return true
  }
  return false
})

const goBack = () => {
  router.push('/')
}

const triggerFileUpload = () => {
  fileInput.value?.click()
}

const handleFileUpload = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files) {
    const newFiles = Array.from(target.files).slice(0, 5)
    uploadedFiles.value = newFiles
  }
}

const removeFile = (index: number) => {
  uploadedFiles.value.splice(index, 1)
}

const handleSubmit = async () => {
  if (!canSubmit.value) return
  
  isSubmitting.value = true
  
  try {
    let wageGrowthRate = 0.05 // 默认5%
    let currentSalary = 0
    
    if (inputMethod.value === 'manual') {
      // 计算最新年份的年薪（作为当前年薪）
      const latestYear = Math.max(...years)
      currentSalary = manualData.value[latestYear].salary || 0
      
      // 调用AI工资增长率预测API
      try {
        const response = await fetch('http://localhost:8000/api/predict-wage-growth', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            age: basicInfo.value.age,
            annualSalary: currentSalary,
            industry: basicInfo.value.industry,
            jobLevel: basicInfo.value.jobLevel
          })
        })
        
        if (response.ok) {
          const result = await response.json()
          // predictedGrowth是百分比数值（如5.2表示5.2%），需转换为小数（0.052）
          wageGrowthRate = (result.predictedGrowth || 5.0) / 100.0
          console.log('✅ AI预测工资增长率:', result.predictedGrowth + '%')
        } else {
          console.warn('⚠️ AI预测失败，使用默认增长率5%')
        }
      } catch (error) {
        console.warn('⚠️ AI预测API调用出错，使用默认增长率5%:', error)
      }
    }
    
    // 跳转到报告页面，传递数据
    router.push({
      name: 'PathBReport',
      query: {
        method: inputMethod.value || 'manual',
        age: String(basicInfo.value.age || 30),
        industry: basicInfo.value.industry || 'other',
        jobLevel: basicInfo.value.jobLevel || 'intermediate',
        wageGrowthRate: String(wageGrowthRate),
        currentSalary: String(currentSalary),
        // 传递历史数据
        historyData: JSON.stringify(manualData.value)
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

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
