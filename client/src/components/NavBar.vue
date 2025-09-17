<!-- src/components/NavBar.vue -->
<template>
  <div class="container">
    <!-- Logo and title -->
    <img src="/images/Logo.png" alt="Logo" class="logo-image" />
    <router-link to="/" class="name-style">Demo</router-link>

    <!-- link -->
    <div class="subtitle-container">
      <div class="spacer-left"></div>

      <!-- 汉堡按钮（小屏显示） -->
      <div class="menu-icon" @click="menuOpen = !menuOpen">☰</div>

      <!-- 导航链接 -->
      <nav :class="['nav-links', { 'show': menuOpen }]">
        <router-link to="/Live_Demo" class="subtitle-style">Live Demo</router-link>
        <router-link to="/Download" class="subtitle-style">Download</router-link>
        <router-link to="/Publication" class="subtitle-style">Publication</router-link>
        <router-link to="/Contact_Us" class="subtitle-style">Contact Us</router-link>
      </nav>

      <div class="spacer-right"></div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
const menuOpen = ref(false);
</script>

<style scoped>
.container {
  width: 100%;
  max-width: 2400px;
  margin: 0 auto;
  padding: 20px;
  box-sizing: border-box;
}

.subtitle-container {
  display: flex;
  align-items: center;
  gap: 50px;
  margin-top: -70px;
  position: relative;
}

.subtitle-style {
  text-decoration: none;
  font-size: 20px;
  font-family: DM Sans, sans-serif;
  color: #333;
}

.spacer-left {
  flex: 2 1 50px;
}
.spacer-right {
  flex: 1 1 10px;
}

.logo-image {
  width: 100px;
  height: auto;
  top: 20px;
  left: 100px;
}

.name-style {
  text-decoration: none;
  position: relative;
  top: -30px;
  font-size: 48px;
  font-weight: bold;
  color: #333;
  font-family: DM Sans, sans-serif;
}

/* 默认导航栏样式（大屏） */
.nav-links {
  display: flex;
  gap: 50px;
}

/* 汉堡按钮默认隐藏（大屏） */
.menu-icon {
  display: none;
  font-size: 28px;
  cursor: pointer;
  user-select: none;
}

/* 小屏幕响应式样式 */
@media (max-width: 768px) {
  .nav-links {
    display: none;
    flex-direction: column;
    position: absolute;
    top: 50px;
    right: 20px;
    background: white;
    padding: 15px;
    border: 1px solid #ccc;
    gap: 20px;
    z-index: 999;
  }

  .nav-links.show {
    display: flex;
  }

  .menu-icon {
    display: block;
  }
}
</style>
