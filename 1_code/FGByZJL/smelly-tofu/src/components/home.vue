<template>
    <div>
        <el-button type="info" @click="logout">退出</el-button>
    </div>
</template>

<script>
export default {
  methods: {
    logout () {
      window.sessionStorage.clear()
      this.$message.info('已退出登录，正在跳转登录页！')
      this.$router.push('/login')
    }
  }
}
</script>

<style lang="less" scoped>
</style>
