<template>
  <Teleport to="body">
    <Transition name="toast">
      <div 
        v-if="visible" 
        class="toast-container"
        :class="typeClass"
      >
        <div class="toast-content">
          <!-- 图标 -->
          <div class="toast-icon">
            <svg v-if="type === 'success'" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
            </svg>
            <svg v-else-if="type === 'error'" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
            <svg v-else-if="type === 'warning'" class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
            </svg>
            <svg v-else class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
          
          <!-- 消息内容 -->
          <div class="toast-message">
            <p class="toast-title" v-if="title">{{ title }}</p>
            <p class="toast-text">{{ message }}</p>
          </div>
          
          <!-- 关闭按钮 -->
          <button @click="close" class="toast-close">
            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'

interface Props {
  type?: 'success' | 'error' | 'warning' | 'info'
  title?: string
  message: string
  duration?: number
  show?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  type: 'info',
  duration: 3000,
  show: false
})

const emit = defineEmits<{
  (e: 'close'): void
}>()

const visible = ref(false)
let timer: ReturnType<typeof setTimeout> | null = null

const typeClass = computed(() => {
  const classes: Record<string, string> = {
    success: 'toast-success',
    error: 'toast-error',
    warning: 'toast-warning',
    info: 'toast-info'
  }
  return classes[props.type]
})

const close = () => {
  visible.value = false
  if (timer) {
    clearTimeout(timer)
    timer = null
  }
  emit('close')
}

watch(() => props.show, (newVal) => {
  if (newVal) {
    visible.value = true
    
    if (props.duration > 0) {
      timer = setTimeout(() => {
        close()
      }, props.duration)
    }
  } else {
    visible.value = false
  }
})

onMounted(() => {
  if (props.show) {
    visible.value = true
    
    if (props.duration > 0) {
      timer = setTimeout(() => {
        close()
      }, props.duration)
    }
  }
})
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 80px;
  right: 20px;
  z-index: 9999;
  max-width: 400px;
  min-width: 300px;
  backdrop-filter: blur(10px);
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
  overflow: hidden;
}

.toast-content {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  gap: 12px;
}

.toast-icon {
  flex-shrink: 0;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.toast-success {
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.2) 0%, rgba(5, 150, 105, 0.1) 100%);
  border: 1px solid rgba(16, 185, 129, 0.3);
}

.toast-success .toast-icon {
  background: rgba(16, 185, 129, 0.2);
  color: #10b981;
}

.toast-error {
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.2) 0%, rgba(220, 38, 38, 0.1) 100%);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.toast-error .toast-icon {
  background: rgba(239, 68, 68, 0.2);
  color: #ef4444;
}

.toast-warning {
  background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(217, 119, 6, 0.1) 100%);
  border: 1px solid rgba(245, 158, 11, 0.3);
}

.toast-warning .toast-icon {
  background: rgba(245, 158, 11, 0.2);
  color: #f59e0b;
}

.toast-info {
  background: linear-gradient(135deg, rgba(139, 92, 246, 0.2) 0%, rgba(124, 58, 237, 0.1) 100%);
  border: 1px solid rgba(139, 92, 246, 0.3);
}

.toast-info .toast-icon {
  background: rgba(139, 92, 246, 0.2);
  color: #8b5cf6;
}

.toast-message {
  flex: 1;
  color: white;
}

.toast-title {
  font-weight: 600;
  font-size: 15px;
  margin-bottom: 4px;
}

.toast-text {
  font-size: 14px;
  opacity: 0.9;
  line-height: 1.5;
}

.toast-close {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  opacity: 0.6;
  transition: all 0.2s;
  background: transparent;
  border: none;
  cursor: pointer;
}

.toast-close:hover {
  opacity: 1;
  background: rgba(255, 255, 255, 0.1);
}

/* 动画 */
.toast-enter-active {
  animation: slideInRight 0.3s ease-out;
}

.toast-leave-active {
  animation: slideOutRight 0.3s ease-in;
}

@keyframes slideInRight {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideOutRight {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(400px);
    opacity: 0;
  }
}
</style>
