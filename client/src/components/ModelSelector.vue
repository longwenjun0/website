<template>
  <div class="model-selector">
    <label for="model">Select Model:</label>
    <select v-model="selected" @change="handleChange">
      <option v-for="option in options" :key="option" :value="option">
        {{ option }}
      </option>
    </select>

    <!-- 只有选择 others 时弹窗 -->
    <div v-if="showModal" class="modal-overlay">
      <div class="modal">
        <p>Please input model:</p>
        <input v-model="customModel" placeholder="Enter model name..." />
        <div class="modal-actions">
          <button @click="confirmCustom">OK</button>
          <button @click="cancelCustom">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  model: { type: String, default: 'gpt-4o' }
});
const emit = defineEmits(['update:model']);

// const options = ['gpt-4o', 'o4-mini', 'others'];
const options = ref(['gpt-4o', 'o4-mini', 'others']);
const selected = ref(props.model);

const showModal = ref(false);
const customModel = ref('');

const handleChange = () => {
  if (selected.value === 'others') {
    showModal.value = true;
  } else {
    emit('update:model', selected.value);
  }
};

// 确认自定义模型
const confirmCustom = () => {
  const value = customModel.value.trim();
  if (value) {
    if (!options.value.includes(value)) {
      options.value.push(value); // ✅ options 是 ref，才有 .value
    }
    selected.value = value;
    emit('update:model', value); 
  } else {
    selected.value = props.model;
  }
  showModal.value = false;
  customModel.value = '';
};
const cancelCustom = () => {
  selected.value = props.model;
  showModal.value = false;
  customModel.value = '';
};
</script>

<style scoped>
.model-selector {
  margin: 10px 0;
  display: flex;
  align-items: center;
  gap: 10px;
  font-family: DM Sans, sans-serif;
}

select {
  padding: 5px 8px;
  font-size: 14px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  min-width: 300px;
}

.modal-actions {
  margin-top: 15px;
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
