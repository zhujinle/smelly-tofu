<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item><a href="/">个人信息</a></el-breadcrumb-item>
      <el-breadcrumb-item>个人信息查看</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片试图 -->
    <el-card class="box-card">
      <!-- 用户信息视图 -->
      <el-descriptions class="margin-top" title="用户详细信息表" :column="3" border>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-user"></i>
            UID
        </template>
        {{this.SingleUserInfo.UID}}
        </el-descriptions-item>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-user"></i>
            用户名
        </template>
        {{this.SingleUserInfo.Name}}
        </el-descriptions-item>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-mobile-phone"></i>
            手机号
        </template>
        {{SingleUserInfo.Phone}}
        </el-descriptions-item>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-mobile-phone"></i>
            头像
        </template>
        <el-avatar :src="SingleUserInfo.AvatarUrl"></el-avatar>
        </el-descriptions-item>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-location-outline"></i>
            地址
        </template>
        {{SingleUserInfo.Address}}
        </el-descriptions-item>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-tickets"></i>
            类型
        </template>
        <el-tag size="small">{{SingleUserInfo.UserType}}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-office-building"></i>
            会员等级
        </template>
        <el-tag size="small">{{SingleUserInfo.MenberStatus}}</el-tag>
        </el-descriptions-item>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-office-building"></i>
            每日顾客
        </template>
        {{SingleUserInfo.CustomerDaily}}
        </el-descriptions-item>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-office-building"></i>
            总顾客
        </template>
        {{SingleUserInfo.CustomerSum}}
        </el-descriptions-item>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-office-building"></i>
            证照
        </template>
        <el-link type="info" :href="SingleUserInfo.License">链接</el-link>
        </el-descriptions-item>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-office-building"></i>
            每日收入
        </template>
        {{SingleUserInfo.MoneyDaily}}
        </el-descriptions-item>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-office-building"></i>
            每月收入
        </template>
        {{SingleUserInfo.MoneyMonthly}}
        </el-descriptions-item>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-office-building"></i>
            总收入
        </template>
        {{SingleUserInfo.MoneySum}}
        </el-descriptions-item>
        <el-descriptions-item>
        <template slot="label">
            <i class="el-icon-office-building"></i>
            购物车信息
        </template>
        {{SingleUserInfo.Cart}}
        </el-descriptions-item>
      </el-descriptions>
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
      AddForm: {
        Name: '',
        password: '',
        phone: '',
        Type: '',
        secretkey: '1'
      },
      EditForm: {
        Name: '',
        Phone: '',
        UserType: '',
        MenberStatus: '',
        Address: '',
        Cart: ''
      },
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
      }],
      options2: [{
        value: '1',
        label: 'Cu'
      }, {
        value: '2',
        label: 'Ag'
      }, {
        value: '3',
        label: 'Au'
      }, {
        value: '4',
        label: 'Diamond'
      }],
      AddFormrules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' }
        ],
        Type: [
          { required: true, message: '请选择用户类型', trigger: 'blur' }
        ]
      }
    }
  },
  created () {
    this.GetUserInfo()
  },
  methods: {
    ResetAddForm () {
      this.$refs.AddFormRef.resetFields()
    },
    async getuserlist () {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      if (this.inputUID !== '') params.append('UID', this.inputUID)
      const res = await this.$http.post('Admin/UserView/', params)
      if (res.data.StatusCode !== 200) return this.$message.error('信息错误！')
      this.UserList = res.data.UserList
    },

    // 获取用户信息
    async GetUserInfo () {
      this.dialogTableVisible = true
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('targetSecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('TargetUserUID', '1')
      const res = await this.$http.post('Admin/SingleUserView/', params)
      if (res.data.StatusCode !== 200) {
        console.log(res)
        return this.$message.error('获取失败！')
      }
      this.$message.success('获取成功！')
      this.SingleUserInfo = res.data
      console.log(this.SingleUserInfo)
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

.el-card {
  margin-bottom: 30px;
  margin-top: 30px;
}
</style>
