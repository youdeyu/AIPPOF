<template>
  <div class="formula-explanation">
    <!-- 公式说明标题 -->
    <div class="flex items-center justify-between mb-6">
      <h3 class="text-xl font-bold text-white flex items-center">
        <svg class="w-6 h-6 mr-2 text-accent-purple" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                d="M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z" />
        </svg>
        {{ title }}
      </h3>
      <button 
        @click="isExpanded = !isExpanded" 
        class="text-white/60 hover:text-white transition-colors text-sm flex items-center"
      >
        <span class="mr-1">{{ isExpanded ? '收起' : '展开详情' }}</span>
        <svg 
          class="w-4 h-4 transition-transform" 
          :class="{ 'rotate-180': isExpanded }"
          fill="none" 
          stroke="currentColor" 
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
        </svg>
      </button>
    </div>

    <!-- 展开的详细内容 -->
    <transition name="slide-down">
      <div v-if="isExpanded" class="space-y-6">
        
        <!-- T2税收优惠说明 -->
        <div v-if="showT2" class="bg-blue-500/10 border border-blue-500/30 rounded-lg p-5">
          <div class="flex items-center mb-3">
            <div class="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center mr-3">
              <span class="text-blue-400 font-bold">T2</span>
            </div>
            <h4 class="text-lg font-semibold text-blue-400">税收优惠率 (缴费期)</h4>
          </div>
          
          <div class="mb-4">
            <div class="text-white/80 text-sm mb-2">
              <strong>公式</strong>（蓝浩歌论文）：
            </div>
            <div class="bg-black/30 rounded p-3 font-mono text-sm text-blue-300">
              T2 = (缴费前个税 - 缴费后个税) / 缴费额 × 100%
            </div>
          </div>
          
          <div class="mb-4">
            <div class="text-white/80 text-sm mb-2">
              <strong>您的计算</strong>：
            </div>
            <div class="bg-black/30 rounded p-3 text-sm text-white/90">
              <div class="mb-2">年薪：¥{{ annualSalary.toLocaleString() }}</div>
              <div class="mb-2">缴费额：¥{{ contribution.toLocaleString() }}</div>
              <div class="mb-2">实际税收节约：¥{{ (contribution * t2 / 100).toFixed(0) }}</div>
              <div class="text-blue-400 font-bold text-lg mt-3">
                T2 = {{ t2.toFixed(1) }}%
              </div>
            </div>
          </div>
          
          <div class="text-white/70 text-xs bg-black/20 rounded p-3">
            💡 <strong>重要说明</strong>：T2 ≠ 边际税率！由于中国累进税制，实际税收节约需要精确计算跨税阶的影响。
          </div>
        </div>

        <!-- T3领取期税率说明 -->
        <div v-if="showT3" class="bg-green-500/10 border border-green-500/30 rounded-lg p-5">
          <div class="flex items-center mb-3">
            <div class="w-8 h-8 rounded-full bg-green-500/20 flex items-center justify-center mr-3">
              <span class="text-green-400 font-bold">T3</span>
            </div>
            <h4 class="text-lg font-semibold text-green-400">领取期税率</h4>
          </div>
          
          <div class="mb-4">
            <div class="text-white/80 text-sm mb-2">
              <strong>公式</strong>（双逻辑函数模型）：
            </div>
            <div class="bg-black/30 rounded p-3 font-mono text-sm text-green-300">
              T3 = L1(T2) + L2(T2) + 收入调整 + 年龄折扣
            </div>
          </div>
          
          <div class="mb-4">
            <div class="text-white/80 text-sm mb-2">
              <strong>您的T3预测</strong>：
            </div>
            <div class="bg-black/30 rounded p-3 text-sm text-white/90">
              <div class="mb-2">缴费期T2：{{ t2.toFixed(1) }}%</div>
              <div class="mb-2">年龄：{{ age }}岁</div>
              <div class="mb-2">年薪：¥{{ annualSalary.toLocaleString() }}</div>
              <div class="text-green-400 font-bold text-lg mt-3">
                T3 = {{ t3.toFixed(1) }}%
              </div>
            </div>
          </div>
          
          <div class="text-white/70 text-xs bg-black/20 rounded p-3">
            💡 <strong>T3范围</strong>：0-14%，随T2增长而增加，但受双逻辑函数约束，高T2时增长放缓。
          </div>
        </div>

        <!-- 精准补贴说明 -->
        <div v-if="showSubsidy" class="bg-yellow-500/10 border border-yellow-500/30 rounded-lg p-5">
          <div class="flex items-center mb-3">
            <div class="w-8 h-8 rounded-full bg-yellow-500/20 flex items-center justify-center mr-3">
              <span class="text-yellow-400 font-bold">S</span>
            </div>
            <h4 class="text-lg font-semibold text-yellow-400">精准财政补贴</h4>
          </div>
          
          <div class="mb-4">
            <div class="text-white/80 text-sm mb-2">
              <strong>公式</strong>（AIPPOF文档）：
            </div>
            <div class="bg-black/30 rounded p-3 font-mono text-xs text-yellow-300">
              S = (基础补贴150 + 首档配比 + 超额配比) × taper因子
            </div>
          </div>
          
          <div class="mb-4">
            <div class="text-white/80 text-sm mb-2">
              <strong>您的补贴计算</strong>：
            </div>
            <div class="bg-black/30 rounded p-3 text-sm text-white/90">
              <div class="mb-2">年薪：¥{{ annualSalary.toLocaleString() }}</div>
              <div class="mb-2">缴费额：¥{{ contribution.toLocaleString() }}</div>
              <div v-if="subsidyBreakdown" class="space-y-1 text-xs mt-3 border-t border-white/10 pt-3">
                <div>基础补贴：¥{{ subsidyBreakdown.baseGrant?.toFixed(0) || 0 }}</div>
                <div>首档配比(2%工资内)：¥{{ subsidyBreakdown.tier1Match?.toFixed(0) || 0 }}</div>
                <div>超额配比：¥{{ subsidyBreakdown.tier2Match?.toFixed(0) || 0 }}</div>
                <div>递减因子：{{ (subsidyBreakdown.taperFactor || 1).toFixed(2) }}</div>
              </div>
              <div class="text-yellow-400 font-bold text-lg mt-3">
                补贴 = ¥{{ subsidy.toFixed(0) }}
              </div>
            </div>
          </div>
          
          <div class="text-white/70 text-xs bg-black/20 rounded p-3">
            💡 <strong>补贴规则</strong>：
            <ul class="mt-2 space-y-1 ml-4">
              <li>• 收入≤4万：全额补贴(taper=1.0)</li>
              <li>• 4-10万：线性递减</li>
              <li>• 收入>10万：补贴归零</li>
              <li>• 低收入加成：首档配比45%(普通30%)</li>
            </ul>
          </div>
        </div>

        <!-- 缴费上限说明 -->
        <div v-if="showCap" class="bg-purple-500/10 border border-purple-500/30 rounded-lg p-5">
          <div class="flex items-center mb-3">
            <div class="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center mr-3">
              <span class="text-purple-400 font-bold">C</span>
            </div>
            <h4 class="text-lg font-semibold text-purple-400">个性化缴费上限</h4>
          </div>
          
          <div class="mb-4">
            <div class="text-white/80 text-sm mb-2">
              <strong>公式</strong>（Formula 5-5混合动态上限）：
            </div>
            <div class="bg-black/30 rounded p-3 font-mono text-xs text-purple-300">
              C_final = min(C_dynamic, C_fixed × τ(w))
              <br>其中 C_dynamic = 工资 × 8%
            </div>
          </div>
          
          <div class="mb-4">
            <div class="text-white/80 text-sm mb-2">
              <strong>您的上限计算</strong>：
            </div>
            <div class="bg-black/30 rounded p-3 text-sm text-white/90">
              <div class="mb-2">年薪：¥{{ annualSalary.toLocaleString() }}</div>
              <div class="mb-2">动态上限(8%)：¥{{ (annualSalary * 0.08).toFixed(0) }}</div>
              <div v-if="capBreakdown">
                <div class="mb-2">固定上限：¥{{ capBreakdown.fixedCap?.toFixed(0) || 0 }}</div>
                <div class="mb-2">高收入递减因子：{{ (capBreakdown.taperFactor || 1).toFixed(2) }}</div>
              </div>
              <div class="text-purple-400 font-bold text-lg mt-3">
                最终上限 = ¥{{ cap.toFixed(0) }}
              </div>
            </div>
          </div>
          
          <div class="text-white/70 text-xs bg-black/20 rounded p-3">
            💡 <strong>上限机制</strong>：混合动态上限确保高收入者不会过度缴费，同时保证低收入者有足够缴费空间。
          </div>
        </div>

        <!-- NPV计算说明 -->
        <div v-if="showNPV" class="bg-indigo-500/10 border border-indigo-500/30 rounded-lg p-5">
          <div class="flex items-center mb-3">
            <div class="w-8 h-8 rounded-full bg-indigo-500/20 flex items-center justify-center mr-3">
              <span class="text-indigo-400 font-bold">NPV</span>
            </div>
            <h4 class="text-lg font-semibold text-indigo-400">全生命周期净现值</h4>
          </div>
          
          <div class="mb-4">
            <div class="text-white/80 text-sm mb-2">
              <strong>公式</strong>（财政中性约束）：
            </div>
            <div class="bg-black/30 rounded p-3 font-mono text-xs text-indigo-300">
              NPV = Σ(节税+补贴) / (1+r)^t - Σ(领取期税负) / (1+r)^t
            </div>
          </div>
          
          <div class="mb-4">
            <div class="text-white/80 text-sm mb-2">
              <strong>您的NPV预测</strong>：
            </div>
            <div class="bg-black/30 rounded p-3 text-sm text-white/90">
              <div class="mb-2">工资增长率：{{ wageGrowth.toFixed(1) }}%</div>
              <div class="mb-2">缴费期年数：{{ 60 - age }}年</div>
              <div class="mb-2">领取期年数：~20年</div>
              <div class="mb-2">折现率：1.75%</div>
              <div class="text-indigo-400 font-bold text-lg mt-3">
                NPV = ¥{{ npv.toLocaleString() }}
              </div>
            </div>
          </div>
          
          <div class="text-white/70 text-xs bg-black/20 rounded p-3">
            💡 <strong>NPV最优</strong>：我们的AI模型会自动搜索使NPV最大化的缴费方案，确保您获得最优长期收益。
          </div>
        </div>

      </div>
    </transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'

// Props定义
interface Props {
  title?: string
  showT2?: boolean
  showT3?: boolean
  showSubsidy?: boolean
  showCap?: boolean
  showNPV?: boolean
  t2?: number
  t3?: number
  subsidy?: number
  subsidyBreakdown?: any
  cap?: number
  capBreakdown?: any
  npv?: number
  annualSalary?: number
  contribution?: number
  age?: number
  wageGrowth?: number
}

const props = withDefaults(defineProps<Props>(), {
  title: '📐 核心公式详解',
  showT2: true,
  showT3: true,
  showSubsidy: true,
  showCap: true,
  showNPV: false,
  t2: 0,
  t3: 0,
  subsidy: 0,
  subsidyBreakdown: null,
  cap: 0,
  capBreakdown: null,
  npv: 0,
  annualSalary: 0,
  contribution: 0,
  age: 30,
  wageGrowth: 4.5
})

const isExpanded = ref(false)
</script>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease-out;
  max-height: 2000px;
  overflow: hidden;
}

.slide-down-enter-from,
.slide-down-leave-to {
  max-height: 0;
  opacity: 0;
}

.rotate-180 {
  transform: rotate(180deg);
}
</style>
