<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item><a href="/">用户管理</a></el-breadcrumb-item>
      <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 添加用户对话框 -->
    <el-dialog title="添加用户" :visible.sync="adddialogVisible" width="50%">
        <span>用户信息输入</span>
        <el-form ref="AddFormRef" :model="AddForm" :rules="AddFormrules">
                <el-form-item label="用户名" prop="username">
                    <el-input v-model="AddForm.username" type="username" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="密码" prop="password">
                    <el-input v-model="AddForm.password" type="password" prefix-icon="el-icon-lock"></el-input>
                </el-form-item>
                <el-form-item label="手机号" prop="phone">
                    <el-input v-model="AddForm.phone" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="用户类型选择" prop="Type">
                    <template>
                    <el-select v-model="AddForm.Type" placeholder="请选择用户类型">
                      <el-option
                      v-for="item in options"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                      </el-option>
                    </el-select>
                    </template>
                </el-form-item>
        </el-form>
        <!-- 底部 -->
        <span slot="footer" class="dialog-footer">
            <el-button @click="adddialogVisible = false">取 消</el-button>
            <el-button type="info" @click="ResetAddForm">重置</el-button>
            <el-button type="primary" @click="AddUser">确 定</el-button>
        </span>
    </el-dialog>
    <!-- 修改用户对话框 -->
    <el-dialog title="用户信息修改" :visible.sync="EditdialogVisible" width="50%">
        <span>这是一段信息</span>
        <el-form ref="EditFormRef" :model="EditForm">
                <el-form-item label="昵称" prop="username">
                    <el-input v-model="EditForm.Name" type="Name" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="手机号" prop="phone">
                    <el-input v-model="EditForm.Phone" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="用户类型选择" prop="Type">
                    <template>
                    <el-select v-model="EditForm.UserType" placeholder="请选择用户类型">
                      <el-option
                      v-for="item in options"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                      </el-option>
                    </el-select>
                    </template>
                </el-form-item>
                <el-form-item label="用户等级选择" prop="Type">
                    <template>
                    <el-select v-model="EditForm.MenberStatus" placeholder="请选择用户等级">
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
                    <el-input v-model="EditForm.Cart" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
        </el-form>
        <!-- 页脚 -->
        <span slot="footer" class="dialog-footer">
            <el-button @click="EditdialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="pushEditDialog">确 定</el-button>
        </span>
    </el-dialog>
    <!-- 用户信息视图 -->
    <el-dialog title="用户信息" :visible.sync="dialogTableVisible">
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
    </el-dialog>
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
            <el-table-column prop="UserName" label="姓名" width="150"></el-table-column>
            <el-table-column prop="UserType" label="类型" width="180"></el-table-column>
            <el-table-column prop="Address" label="地址" width="380"></el-table-column>
            <el-table-column prop="LastLogin" label="最后一次登录" width="280"></el-table-column>
            <el-table-column prop="is_sctive" label="状态" width="100">
                <template slot-scope="scope">
                    <el-switch
                        v-model="scope.row.is_sctive"
                        active-color="#13ce66"
                        inactive-color="#ff4949"
                        @change="UserStateChange(scope.row)">
                    </el-switch>
                </template>
            </el-table-column>
            <el-table-column label="操作" fixed="right" width="200">
                <template slot-scope="scope">
                    <!-- 查看 -->
                    <el-tooltip effect="dark" content="查看信息" placement="top" :enterable="false">
                        <el-button type="primary" icon="el-icon-view" size="mini" @click="GetUserInfo(scope.row)" ></el-button>
                    </el-tooltip>
                    <!-- 修改 -->
                    <el-tooltip effect="dark" content="修改信息" placement="top" :enterable="false">
                        <el-button type="warning" icon="el-icon-edit" size="mini" @click="showEditDialog(scope.row)"></el-button>
                    </el-tooltip>
                    <!-- 删除 -->
                    <el-tooltip effect="dark" content="删除用户" placement="top" :enterable="false">
                        <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteuser(scope.row)"></el-button>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column prop="Cart" label="购物车"></el-table-column>
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
      const res = await this.$http.post('Admin/UserView/', params)
      if (res.data.StatusCode !== 200) return this.$message.error('信息错误！')
      this.UserList = res.data.UserList
    },
    // 修改状态信息
    async UserStateChange (userinfo) {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('TargetUserUID', userinfo.UID)
      params.append('is_active', userinfo.is_sctive)
      const res = await this.$http.post('Admin/ModifyUser/', params)
      if (res.data.StatusCode !== 200) {
        userinfo.is_sctive = !userinfo.is_sctive
        return this.$message.error('保存失败！')
      }
      this.$message.success('保存成功！')
    },
    AddUser () {
      this.adddialogVisible = false
      this.$refs.AddFormRef.validate(async valid => {
        if (!valid) return
        const params = new URLSearchParams()
        params.append('Name', this.AddForm.username)
        params.append('Password', this.AddForm.password)
        params.append('Phone', this.AddForm.phone)
        params.append('Type', this.AddForm.Type)
        params.append('SecretKey', this.AddForm.SecreyKey)
        const res = await this.$http.post('Admin/UserCreate/', params)
        console.log(res)
        if (res.data.StatusCode !== 200) return this.$message.error('注册失败！可能用户名已存在')
        console.log(res)
        this.$message.success('注册成功！')
        this.getuserlist()
      })
    },
    // 获取用户信息
    async GetUserInfo (userinfo) {
      this.dialogTableVisible = true
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('TargetUserUID', userinfo.UID)
      const res = await this.$http.post('Admin/SingleUserView/', params)
      if (res.data.StatusCode !== 200) {
        return this.$message.error('获取失败！')
      }
      this.$message.success('获取成功！')
      this.SingleUserInfo = res.data
      console.log(this.SingleUserInfo)
    },
    async showEditDialog (userinfo) {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('TargetUserUID', userinfo.UID)
      const res = await this.$http.post('Admin/SingleUserView/', params)
      if (res.data.StatusCode !== 200) {
        return this.$message.error('获取失败！')
      }
      this.$message.success('获取成功！')
      this.EditForm = res.data
      if (this.EditForm.MenberStatus === 'Cu') this.EditForm.MenberStatus = 1
      if (this.EditForm.MenberStatus === 'Ag') this.EditForm.MenberStatus = 2
      if (this.EditForm.MenberStatus === 'Au') this.EditForm.MenberStatus = 3
      if (this.EditForm.MenberStatus === 'Diamond') this.EditForm.MenberStatus = 4
      if (this.EditForm.UserType === 'Admin') this.EditForm.UserType = 4
      if (this.EditForm.UserType === 'DeliveryStaff') this.EditForm.UserType = 3
      if (this.EditForm.UserType === 'Seller') this.EditForm.UserType = 2
      if (this.EditForm.UserType === 'Customer') this.EditForm.UserType = 1
      this.EditdialogVisible = true
    },
    async pushEditDialog () {
      const params2 = new URLSearchParams()
      params2.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params2.append('TargetUserUID', this.EditForm.UID)
      params2.append('Name', this.EditForm.Name)
      params2.append('Phone', this.EditForm.Phone)
      params2.append('Type', this.EditForm.UserType)
      params2.append('MemberType', this.EditForm.MenberStatus)
      params2.append('Address', this.EditForm.Address)
      params2.append('Cart', this.EditForm.Cart)
      const res2 = await this.$http.post('Admin/ModifyUser/', params2)
      this.EditdialogVisible = false
      if (res2.data.StatusCode !== 200) {
        return this.$message.error('保存失败！')
      }
      this.$message.success('保存成功！')
    },
    async deleteuser (userinfo) {
      const params2 = new URLSearchParams()
      params2.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params2.append('TargetUserUID', userinfo.UID)
      const res2 = await this.$http.post('Admin/DeleteUser/', params2)
      this.EditdialogVisible = false
      if (res2.data.StatusCode !== 200) {
        return this.$message.error('删除失败！')
      }
      this.$message.success('删除成功！')
      this.getuserlist()
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
