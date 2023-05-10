<template>
  <el-container class="home-container">
  <!-- 头部 -->
  <el-header>
    <div>
        <img src="../assets/logo.png" alt="">
        <span>Smelly-Tofu 外卖系统</span>
    </div>
    <el-button type="info" @click="logout">退出</el-button>
  </el-header>
  <!-- 侧边 -->
  <el-container>
  <!-- 侧边栏 -->
    <el-menu :unique-opened="true" default-active="1-4-1" class="el-menu-vertical-demo" @open="handleOpen" @close="handleClose" :collapse="isCollapse" router>
      <div class="toggle-button" @click="toggleCallapse">
        <i class="el-icon-s-unfold"></i>
      </div>
      <!-- <el-switch
        v-model="isCollapse"
        style="padding-left: 30%;">
      </el-switch> -->
      <!-- 一级菜单 -->
      <el-submenu :index="item.id + ''" v-for="item in MenuList" :key="item.id">
        <template slot="title">
          <i :class="iconsObj[item.id]"></i>
          <span slot="title">{{item.authName}}</span>
        </template>
        <!-- 二级菜单 -->
        <el-menu-item-group>
          <el-menu-item :index="'/' + subItem.path" v-for="subItem in item.children" :key="subItem.id" >
          <i class="el-icon-menu"></i>
          <span>{{subItem.authName}}</span>
          </el-menu-item>
        </el-menu-item-group>
      </el-submenu>
    </el-menu>
    <!-- 主体 -->
      <el-main>
        <!-- 路由占位符 -->
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
export default {
  created () {
    this.getMenuList()
  },
  data () {
    return {
      isCollapse: true,
      // 左侧菜单数据
      MenuList: [],
      iconsObj: {
        100: 'el-icon-s-custom',
        200: 'el-icon-s-goods',
        300: 'el-icon-s-order',
        400: 'el-icon-s-shop',
        500: 'el-icon-s-operation'
      }
    }
  },
  methods: {
    logout () {
      window.sessionStorage.clear()
      this.$message.info('已退出登录，正在跳转登录页！')
      this.$router.push('/login')
    },
    handleOpen (key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose (key, keyPath) {
      console.log(key, keyPath)
    },
    async getMenuList () {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      const res = await this.$http.post('GetMenuList', params)
      if (res.data.StatusCode !== 200) return this.$message.error('信息错误！')
      this.MenuList = res.data.List
    },
    toggleCallapse () {
      this.isCollapse = !this.isCollapse
    }
  }
}
</script>

<style lang="less" scoped>
.el-header {
    background-color: #373d41;
    display: flex;
    justify-content: space-between;
    padding-left: 0;
    align-items: center;
    color: #fff;
    font-size: 20px;
    > div {
        display: flex;
        align-items: center;
        span {
            margin-left: 15px;
        }
    }
}
.el-menu-vertical-demo:not(.el-menu--collapse) {
    width: 200px;
    min-height: 400px;
  }
.el-aside {
    background-color: #333744;
}

.el-main {
    background-color: #eaedf1;
}

.home-container {
    height: 100%;
}

.toggle-button {
  color: #333744;
  text-align: center;
  cursor: pointer;
}
</style>
