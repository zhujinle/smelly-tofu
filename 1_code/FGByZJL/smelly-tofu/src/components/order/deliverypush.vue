<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item><a href="/">订单管理</a></el-breadcrumb-item>
      <el-breadcrumb-item>订单配送信息推送</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片试图 -->
    <el-card class="box-card">
      <!-- 搜索 -->
      <template>
        <el-select v-model="inputUID" placeholder="请选择配送员">
          <el-option
            v-for="item in UserList"
            :key="item.Name"
            :label="item.Name"
            :value="item.UID">
          </el-option>
        </el-select>
        <el-select v-model="inputOrderID" placeholder="请选择订单ID">
          <el-option
            v-for="item in OrderList"
            :key="item.OrderNumber"
            :label="item.OrderNumber"
            :value="item.OrderNumber">
          </el-option>
        </el-select>
        <el-button type="success" @click="pushDelivery()">推送！</el-button>
      </template>

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
        <!-- 订单列表 -->
      <template>
        <el-table :data="OrderList" stripe style="width: 100%">
            <el-table-column prop="UID" label="订单创建者UID" width="60"></el-table-column>
            <el-table-column prop="OrderNumber" label="订单号" width="80"></el-table-column>
            <el-table-column prop="Phone" label="联系方式" width="120"></el-table-column>
            <el-table-column prop="Address" label="地址" width="380"></el-table-column>
            <el-table-column prop="Notes" label="备注" width="280"></el-table-column>
            <el-table-column prop="MoneySum" label="总金额" width="80"></el-table-column>
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
      OrderList: [],
      inputUID: '',
      inputOrderID: '',
      SelectDeliverystaff: '',
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
    this.getOrderlist()
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
    },
    async getOrderlist () {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      if (this.inputUID !== '') params.append('UID', this.inputUID)
      const res = await this.$http.post('Admin/OrderListView/', params)
      if (res.data.StatusCode !== 200) return this.$message.error('信息错误！')
      this.OrderList = res.data.OrderList
      console.log(this.OrderList)
    },
    async pushDelivery () {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('OrderNumber', this.inputOrderID)
      params.append('DeliveryStaffUID', this.inputUID)
      const res = await this.$http.post('Seller/DeliveryPush/', params)
      if (res.data.StatusCode !== 200) return this.$message.error('推送失败！')
      this.$message.success('推送成功！')
      console.log(this.OrderList)
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
.el-select {
  margin-left: 10px;
}
.el-button {
  margin-left: 10px;
}
.box-card {
}
</style>
