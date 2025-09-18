<template>
  <div>
    <!-- 顶部导航栏 -->
    <NavBar />

    <!-- 页面标题 -->
    <!-- <h1 class="page-title">LLM Demo</h1> -->

    <!-- 聊天框主体 -->
    <div class="chat-wrapper">
      <!-- header: 模型选择器在右上角 -->
      <div class="chat-header">
        <div class="chat-title"></div> <!-- 可放标题或者空占位 -->
        <ModelSelector v-model:model="currentModel" />
      </div>

      <div class="chat-container">
        <div class="messages" ref="messageContainer">
          <div v-for="(msg, index) in messages" :key="index" class="message">
            <span :class="msg.role">{{ msg.text }}</span>
          </div>
        </div>

        <div class="input-bar">
          <input v-model="userInput" @keyup.enter="sendMessage" placeholder="Please input..." />
          <button @click="sendMessage">Send</button>
          <button @click="clearMessages">Clear</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';
import axios from 'axios';
import NavBar from '@/components/NavBar.vue';
import ModelSelector from '@/components/ModelSelector.vue';

const userInput = ref('');
const messages = ref([]);
const messageContainer = ref(null);
const currentModel = ref('gpt-4o'); // 默认模型

const sendMessage = async () => {
  if (userInput.value.trim() === '') return;

  const inputText = userInput.value;
  messages.value.push({ role: 'user', text: inputText });
  userInput.value = '';
  scrollToBottom();

  const placeholder = { role: 'assistant', text: 'Generating...' };
  messages.value.push(placeholder);
  messages.value = [...messages.value];
  scrollToBottom();

  try {
    const res = await axios.post('https://website-0lu7.onrender.com/api/chat', {
      model: currentModel.value,
      text: inputText,
    });

    Object.assign(placeholder, { text: res.data.reply.replace(/\n\s*\n/g, '\n') });
    messages.value = [...messages.value];
  } catch (err) {
    Object.assign(placeholder, { text: `Error: ${err.message}` });
    messages.value = [...messages.value];
  }

  scrollToBottom();
};

const clearMessages = () => {
  messages.value = [];
};

const scrollToBottom = () => {
  nextTick(() => {
    if (messageContainer.value) {
      messageContainer.value.scrollTop = messageContainer.value.scrollHeight;
    }
  });
};
</script>

<style scoped>
.page-title {
  text-align: center;
  font-size: 56px;
  margin-bottom: 20px;
  font-family: DM Sans, sans-serif;
}

.chat-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center; /* 居中聊天框 */
  margin-top: 10px;
  width: 100%;
}

.chat-header {
  width: 90%;
  max-width: 1400px;
  display: flex;
  justify-content: flex-end; /* 右端对齐 */
  margin-bottom: 10px;
}

.chat-container {
  width: 90%;
  max-width: 1400px;
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 10px;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
}

.messages {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  margin: 5px 0;
  max-height: 600px;
  min-height: 300px;
}

.message span {
  display: inline-block;
  padding: 8px;
  border-radius: 5px;
  white-space: pre-wrap;
}

.input-bar {
  display: flex;
  gap: 10px;
  margin-top: 10px;
}

.input-bar input {
  flex: 1;
  padding: 5px 10px;
  font-size: 16px;
}

.input-bar button {
  padding: 5px 10px;
  cursor: pointer;
}

.assistant {
  background-color: #f1f1f1;
  color: #000;
  display: inline-block;
  padding: 8px;
  border-radius: 5px;
  white-space: pre-wrap;
}
</style>
