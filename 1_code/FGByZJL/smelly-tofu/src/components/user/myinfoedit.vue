<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item><a href="/">个人信息</a></el-breadcrumb-item>
      <el-breadcrumb-item>个人信息修改</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片试图 -->
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <template>
          <el-button style="float: right;" type="primary" @click="pushEditDialog()">保存</el-button>
        </template>
      </div>
      <span>修改个人信息</span>
        <el-form ref="EditFormRef" :model="EditForm">
                <el-form-item label="昵称" prop="username">
                    <el-input v-model="EditForm.Name" type="Name" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="手机号" prop="phone">
                    <el-input v-model="EditForm.Phone" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="用户类型" prop="Type">
                    <template>
                    <el-select v-model="EditForm.UserType" disabled  placeholder="请选择用户类型">
                      <el-option
                      v-for="item in options"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                      </el-option>
                    </el-select>
                    </template>
                </el-form-item>
                <el-form-item label="用户等级" prop="Type">
                    <template>
                    <el-select v-model="EditForm.MenberStatus" disabled  placeholder="请选择用户等级">
                      <el-option
                      v-for="item in options2"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                      </el-option>
                    </el-select>
                    </template>
                </el-form-item>
                <el-form-item label="地址" prop="phone">
                    <el-input v-model="EditForm.Address" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="购物车(JSON形式)" prop="phone">
                    <el-input v-model="EditForm.Cart" prefix-icon="el-icon-user" :disabled="true"></el-input>
                </el-form-item>
        </el-form>
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
    this.showEditDialog()
  },
  methods: {
    ResetAddForm () {
      this.$refs.AddFormRef.resetFields()
    },
    async showEditDialog () {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('targetSecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('TargetUserUID', '1')
      const res = await this.$http.post('Admin/SingleUserView/', params)
      if (res.data.StatusCode !== 200) {
        return this.$message.error('获取失败！')
      }
      this.$message.success('获取成功！')
      this.EditForm = res.data
    },
    async pushEditDialog () {
      const params2 = new URLSearchParams()
      params2.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params2.append('TargetUserUID', this.EditForm.UID)
      params2.append('Name', this.EditForm.Name)
      params2.append('Phone', this.EditForm.Phone)
      params2.append('Address', this.EditForm.Address)
      const res2 = await this.$http.post('Admin/ModifyUser/', params2)
      this.EditdialogVisible = false
      if (res2.data.StatusCode !== 200) {
        return this.$message.error('保存失败！')
      }
      this.$message.success('保存成功！')
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
