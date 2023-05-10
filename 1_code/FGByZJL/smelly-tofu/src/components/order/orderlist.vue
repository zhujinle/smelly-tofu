<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item><a href="/">订单管理</a></el-breadcrumb-item>
      <el-breadcrumb-item>订单列表</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 添加订单对话框 -->
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
        <span>订单信息修改</span>
        <el-form ref="EditFormRef" :model="EditForm">
                <el-form-item label="收件地址" prop="Address">
                    <el-input v-model="EditForm.Address" type="Name" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="联系方式" prop="phone">
                    <el-input v-model="EditForm.Phone" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="备注">
                    <el-input v-model="EditForm.Notes" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="用户支付方式选择" prop="Type">
                    <template>
                    <el-select v-model="EditForm.Payment" placeholder="请选择支付方式">
                      <el-option
                      v-for="item in options"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                      </el-option>
                    </el-select>
                    </template>
                </el-form-item>
                <el-form-item label="订单状态" prop="Type">
                    <template>
                    <el-select v-model="EditForm.DeliveryStatus" placeholder="请选择用户等级">
                      <el-option
                      v-for="item in options2"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                      </el-option>
                    </el-select>
                    </template>
                </el-form-item>
        </el-form>
        <!-- 页脚 -->
        <span slot="footer" class="dialog-footer">
            <el-button @click="EditdialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="pushEditDialog">确 定</el-button>
        </span>
    </el-dialog>
    <!-- 用户信息视图 -->
    <el-dialog title="订单信息" :visible.sync="dialogTableVisible">
        <el-descriptions class="margin-top" title="订单详细信息表" :column="3" border>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-user"></i>
                UID
            </template>
            {{this.SingleOrderInfo.UserUID}}
            </el-descriptions-item>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-user"></i>
                订单ID
            </template>
            {{this.SingleOrderInfo.OrderNumber}}
            </el-descriptions-item>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-mobile-phone"></i>
                联系方式
            </template>
            {{SingleOrderInfo.Phone}}
            </el-descriptions-item>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-mobile-phone"></i>
                地址
            </template>
            {{SingleOrderInfo.Address}}
            </el-descriptions-item>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-location-outline"></i>
                备注
            </template>
            {{SingleOrderInfo.Notes}}
            </el-descriptions-item>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-tickets"></i>
                付款方式
            </template>
            <el-tag size="small">{{SingleOrderInfo.Payment}}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-office-building"></i>
                付款标记
            </template>
            <el-tag size="small">{{SingleOrderInfo.PayStatus}}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-office-building"></i>
                商店地址
            </template>
            {{SingleOrderInfo.ShopAddress}}
            </el-descriptions-item>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-office-building"></i>
                商店联系方式
            </template>
            {{SingleOrderInfo.ShopPhone}}
            </el-descriptions-item>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-office-building"></i>
                配送员姓名
            </template>
            {{SingleOrderInfo.DeliveryStaffName}}
            </el-descriptions-item>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-office-building"></i>
                配送员联系方式
            </template>
            {{SingleOrderInfo.DeliveryStaffPhone}}
            </el-descriptions-item>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-office-building"></i>
                配送状态
            </template>
            {{SingleOrderInfo.DeliveryStatus}}
            </el-descriptions-item>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-office-building"></i>
               购物车内容
            </template>
            {{SingleOrderInfo.CartMenber}}
            </el-descriptions-item>
            <el-descriptions-item>
            <template slot="label">
                <i class="el-icon-office-building"></i>
                总金额
            </template>
            {{SingleOrderInfo.MoneySum}}
            </el-descriptions-item>
        </el-descriptions>
    </el-dialog>
    <!-- 卡片试图 -->
    <el-card class="box-card">
      <!-- 搜索 -->
      <el-row :gutter="20">
        <el-col :span="7">
            <el-input placeholder="请输入OrderID" v-model="inputUID" clearable @clear="getOrderlist">
                <el-button slot="append" icon="el-icon-search" @click="getOrderlist"></el-button>
            </el-input>
        </el-col>
        <el-col :span="4">
            <el-button type="primary" @click="adddialogVisible = true">下订单</el-button>
        </el-col>
      </el-row>

      <!-- 订单列表 -->
      <template>
        <el-table :data="UserList" stripe style="width: 100%">
            <el-table-column prop="UID" label="订单创建者UID" width="60"></el-table-column>
            <el-table-column prop="OrderNumber" label="订单号" width="80"></el-table-column>
            <el-table-column prop="Phone" label="联系方式" width="120"></el-table-column>
            <el-table-column prop="Address" label="地址" width="380"></el-table-column>
            <el-table-column prop="Notes" label="备注" width="280"></el-table-column>
            <el-table-column prop="MoneySum" label="总金额" width="80"></el-table-column>
            <el-table-column label="操作" fixed="right" width="200">
                <template slot-scope="scope">
                    <!-- 查看 -->
                    <el-tooltip effect="dark" content="查看信息" placement="top" :enterable="false">
                        <el-button type="primary" icon="el-icon-view" size="mini" @click="GetOrderInfo(scope.row)" ></el-button>
                    </el-tooltip>
                    <!-- 修改 -->
                    <el-tooltip effect="dark" content="修改信息" placement="top" :enterable="false">
                        <el-button type="warning" icon="el-icon-edit" size="mini" @click="showEditDialog(scope.row)"></el-button>
                    </el-tooltip>
                    <!-- 删除 -->
                    <el-tooltip effect="dark" content="删除订单" placement="top" :enterable="false">
                        <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteuser(scope.row)"></el-button>
                    </el-tooltip>
                </template>
            </el-table-column>
            <el-table-column label="购物车">
              <template slot-scope="scope">
              {{ scope.row.Cart }}
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
      Orderlist: [],
      inputUID: '',
      dialogTableVisible: false,
      adddialogVisible: false,
      EditdialogVisible: false,
      SingleOrderInfo: [],
      AddForm: {
        Name: '',
        password: '',
        phone: '',
        Type: '',
        secretkey: '1'
      },
      EditForm: {
        Phone: '',
        Address: '',
        Notes: '',
        Payment: '',
        DeliveryStaffName: '',
        DeliveryStaffPhone: '',
        DeliveryStatus: ''
      },
      AddFormrules: {
        Address: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ],
        ShopAddress: [
          { required: true, message: '请输入手机号', trigger: 'blur' }
        ],
        phone: [
          { required: true, message: '请输入手机号', trigger: 'blur' }
        ],
        Type: [
          { required: true, message: '请选择用户类型', trigger: 'blur' }
        ]
      },
      options: [{
        value: '1',
        label: 'AliPay'
      }, {
        value: '2',
        label: 'Wechat'
      }, {
        value: '3',
        label: 'Balance'
      }],
      options2: [{
        value: '0',
        label: 'NoJieDan'
      }, {
        value: '1',
        label: 'NoDeliveryStaff'
      }, {
        value: '2',
        label: 'NoQuCan'
      }, {
        value: '3',
        label: 'QuCaning'
      }, {
        value: '4',
        label: 'OnRoad'
      }, {
        value: '5',
        label: 'Done'
      }]
    }
  },
  created () {
    this.getOrderlist()
  },
  methods: {
    ResetAddForm () {
      this.$refs.AddFormRef.resetFields()
    },
    async getOrderlist () {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      if (this.inputUID !== '') params.append('UID', this.inputUID)
      const res = await this.$http.post('Admin/OrderListView/', params)
      if (res.data.StatusCode !== 200) return this.$message.error('信息错误！')
      this.UserList = res.data.OrderList
      console.log(this.UserList)
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
        if (res.data.StatusCode !== 200) return this.$message.error('注册失败！可能用户名已存在')
        this.$message.success('注册成功！')
        this.getOrderlist()
      })
    },
    // 获取用户信息
    async GetOrderInfo (Orderinfo) {
      this.dialogTableVisible = true
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('OrderNumber', Orderinfo.OrderNumber)
      const res = await this.$http.post('Admin/CheckOrder/', params)
      if (res.data.StatusCode !== 200) {
        return this.$message.error('获取失败！')
      }
      this.$message.success('获取成功！')
      this.SingleOrderInfo = res.data
      console.log(this.SingleOrderInfo)
    },
    async showEditDialog (Orderinfo) {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('OrderNumber', Orderinfo.OrderNumber)
      const res = await this.$http.post('Admin/CheckOrder/', params)
      if (res.data.StatusCode !== 200) {
        return this.$message.error('获取失败！')
      }
      this.$message.success('获取成功！')
      this.EditForm = res.data
      console.log(this.EditForm)
      this.EditdialogVisible = true
    },
    async pushEditDialog () {
      const params2 = new URLSearchParams()
      params2.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params2.append('OrderNumber', this.EditForm.OrderNumber)
      params2.append('Address', this.EditForm.Address)
      params2.append('Phone', this.EditForm.Phone)
      params2.append('Notes', this.EditForm.Notes)
      params2.append('Payment', this.EditForm.Payment)
      params2.append('DeliveryState', this.EditForm.DeliveryStatus)
      const res2 = await this.$http.post('Admin/ModifyOrder/', params2)
      this.EditdialogVisible = false
      if (res2.data.StatusCode !== 200) {
        console.log(res2)
        return this.$message.error('保存失败！')
      }
      this.$message.success('保存成功！')
    },
    async deleteuser (Orderinfo) {
      const params2 = new URLSearchParams()
      params2.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params2.append('TargetUserUID', Orderinfo.OrderNumber)
      console.log(Orderinfo)
      const res2 = await this.$http.post('Admin/DeleteOrder/', params2)
      this.EditdialogVisible = false
      if (res2.data.StatusCode !== 200) {
        console.log(res2)
        return this.$message.error('删除失败！')
      }
      this.$message.success('删除成功！')
      this.getOrderlist()
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
