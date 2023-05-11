<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item><a href="/">订单管理</a></el-breadcrumb-item>
      <el-breadcrumb-item>可用配送员查看</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片试图 -->
    <el-card class="box-card">
      <!-- 搜索 -->
      <el-row :gutter="20">
        <el-col :span="7">
            <el-input placeholder="请输入UID" v-model="inputUID" clearable @clear="getuserlist">
                <el-button slot="append" icon="el-icon-search" @click="getuserlist"></el-button>
            </el-input>
        </el-col>
        <el-col :span="4">
            <el-button type="primary" @click="adddialogVisible = true">添加用户</el-button>
        </el-col>
      </el-row>

      <!-- 用户列表 -->
      <template>
        <el-table :data="UserList" stripe style="width: 100%">
            <el-table-column prop="UID" label="UID" width="60"></el-table-column>
            <el-table-column prop="Name" label="姓名" width="150"></el-table-column>
            <el-table-column prop="Member" label="等级" width="180"></el-table-column>
            <el-table-column prop="Phone" label="电话" width="380"></el-table-column>
            <el-table-column prop="LastLogin" label="最后一次登录" width="280"></el-table-column>
            <el-table-column prop="is_sctive" label="状态">
                <template slot-scope="scope">
                    <el-switch
                        v-model="scope.row.is_active"
                        active-color="#13ce66"
                        inactive-color="#ff4949">
                    </el-switch>
                </template>
            </el-table-column>
        </el-table>
        </template>
    </el-card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      UserList: [],
      inputUID: '',
      dialogTableVisible: false,
      adddialogVisible: false,
      EditdialogVisible: false,
      SingleUserInfo: [],
      options: [{
        value: '1',
        label: '普通用户'
      }, {
        value: '2',
        label: '入驻商家'
      }, {
        value: '3',
        label: '配送员'
      }, {
        value: '4',
        label: '系统管理员'
      }]
    }
  },
  created () {
    this.getuserlist()
  },
  methods: {
    ResetAddForm () {
      this.$refs.AddFormRef.resetFields()
    },
    async getuserlist () {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      if (this.inputUID !== '') params.append('UID', this.inputUID)
      const res = await this.$http.post('Seller/DeliveryStaffList/', params)
      console.log(res)
      if (res.data.StatusCode !== 200) return this.$message.error('信息错误！')
      this.UserList = res.data.UserList
    }
  }
}
</script>

<style lang="less" scoped>
.text {
  font-size: 14px;
}

.item {
  padding: 18px 0;
}

.box-card {
}
</style>
