<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item><a href="/">用户功能</a></el-breadcrumb-item>
      <el-breadcrumb-item>购物车管理</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 支付弹窗 -->
    <el-dialog
      title="请支付"
      :visible.sync="PaydialogVisible"
      width="30%">
      <span>请扫码支付</span>
      <img :src="payimage" class="image" onerror="this.src='https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png'">
      <span slot="footer" class="dialog-footer">
        <el-button @click="PaydialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="paysuccess()">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 下单信息 -->
    <el-dialog title="下单信息填写" :visible.sync="EditdialogVisible" width="50%">
        <span>请填写收件信息</span>
        <el-form ref="EditFormRef" :model="EditForm">
                <el-form-item label="店铺UID">
                    <el-input v-model="EditForm.shopUID" prefix-icon="el-icon-user" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="手机号" prop="phone">
                    <el-input v-model="EditForm.Phone" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="取餐地址" prop="Address">
                    <el-input v-model="EditForm.Address" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="订单备注">
                    <el-input v-model="EditForm.Notes" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="支付方式选择" prop="Type">
                    <template>
                    <el-select v-model="EditForm.MenberStatus" placeholder="请选择支付方式">
                      <el-option
                      v-for="item in options"
                      :key="item.value"
                      :label="item.label"
                      :value="item.value">
                      </el-option>
                    </el-select>
                    </template>
                </el-form-item>
                <el-form-item label="确认下单">
                    <el-checkbox v-model="EditForm.OrderCheck" label="确认下单" border></el-checkbox>                </el-form-item>
                <el-form-item label="购物车(JSON形式)" >
                    <el-input v-model="EditForm.Cart" prefix-icon="el-icon-user" :disabled="true"></el-input>
                </el-form-item>
                <el-form-item label="总金额" >
                    <el-input v-model="EditForm.moneysum" prefix-icon="el-icon-user" :disabled="true"></el-input>
                </el-form-item>
        </el-form>
        <!-- 页脚 -->
        <span slot="footer" class="dialog-footer">
            <el-button @click="EditdialogVisible = false">取 消</el-button>
            <el-button type="primary" @click="pushEditDialog">确 定</el-button>
        </span>
    </el-dialog>
    <!-- 卡片试图 -->
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <template>
          <el-button style="float: right;" type="primary" @click="SaveCart()">保存菜单</el-button>
          <el-button style="float: right; margin-right: 10px;" type="success" @click="makeOrder()">下单</el-button>
        </template>
      </div>
      <el-row>
        <el-col :index="item.FoodID + ''" :span="8" v-for="item in FoodList" :key="item.FoodID" >
          <el-card :body-style="{ padding: '0px'}" class="box_card">
            <img :src="item.FoodPhoto" class="image" onerror="this.src='https://shadow.elemecdn.com/app/element/hamburger.9cf7b091-55e9-11e9-a976-7f4d0b07eef6.png'">
            <div style="padding: 14px;">
              <span>价格：{{item.Money}} ￥</span>
              <div class="bottom clearfix">
                <span>折扣系数: {{ item.Discount }}</span>
                <el-checkbox v-model="item.Checked" label="移除" border></el-checkbox>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      FoodList: [],
      inputUID: '',
      dialogTableVisible: false,
      adddialogVisible: false,
      EditdialogVisible: false,
      PaydialogVisible: false,
      ordernumber: 0,
      Cart: [],
      payimage: 'http://127.0.0.1:8000/media/static/qrcode/1.jpg',
      EditForm: {
        shopUID: '',
        Phone: '',
        Address: '',
        Notes: '',
        MenberStatus: '',
        Cart: '',
        moneysum: 0.0
      },
      options: [{
        value: '1',
        label: '支付宝支付'
      }, {
        value: '2',
        label: '微信支付'
      }, {
        value: '3',
        label: '余额支付'
      }],
      AddFormrules: {
        Address: [
          { required: true, message: '请输入地址', trigger: 'blur' }
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
      const res = await this.$http.post('Customer/ViewShoppingCart/', params)
      if (res.data.StatusCode !== 200) return this.$message.error('信息错误！')
      this.Cart = JSON.parse(res.data.CartMenber).CartNember
      console.log(this.Cart)
      this.FoodList = []
      for (var { Foodid: food } of this.Cart) {
        const params = new URLSearchParams()
        params.append('FoodID', food)
        params.append('UID', '2')
        const res = await this.$http.post('Seller/MenuView/', params)
        console.log(res)
        if (res.data.StatusCode !== 200) return this.$message.error('菜单信息错误！')
        this.FoodList.push(res.data.Menu)
        this.EditForm.moneysum += parseFloat(res.data.Menu.Money)
        this.EditForm.shopUID = res.data.Menu.ShopID
        console.log(res.data.Menu.ShopID)
        console.log('======')
      }
    },
    async SaveCart () {
      var str = '{"CartNember": ['
      var bool = false
      for (var { Checked: c, FoodID: ID } of this.FoodList) {
        if (c === false) {
          if (bool === true) {
            str = str + ', '
          }
          str = str + '{"Foodid": ' + ID + '} '
          bool = true
        }
      }
      str = str + ']}'
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('CartMenber', str)
      const res = await this.$http.post('Customer/ModifyShoppingCart/', params)
      if (res.data.StatusCode !== 200) return this.$message.error('保存失败！')
      this.$message.success('保存成功！')
      this.getuserlist()
    },
    async makeOrder () {
      this.EditdialogVisible = true
      var str = '{"CartNember": ['
      var bool = false
      for (var { Checked: c, FoodID: ID } of this.FoodList) {
        if (c === false) {
          if (bool === true) {
            str = str + ', '
          }
          str = str + '{"Foodid": ' + ID + '} '
          bool = true
        }
      }
      str = str + ']}'
      this.EditForm.Cart = str
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('CartMenber', str)
      const res = await this.$http.post('Customer/ModifyShoppingCart/', params)
      if (res.data.StatusCode !== 200) return this.$message.error('保存失败！')
      this.$message.success('保存成功！')
    },
    async pushEditDialog () {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('Address', this.EditForm.Address)
      params.append('Phone', this.EditForm.Phone)
      params.append('Notes', this.EditForm.Notes)
      params.append('Payment', this.EditForm.MenberStatus)
      params.append('OrderCheck', this.EditForm.OrderCheck)
      params.append('ShopUID', this.EditForm.shopUID)
      const res = await this.$http.post('Customer/MakeOrder/', params)
      if (res.data.StatusCode !== 200) return this.$message.error('提交失败！')
      this.$message.success('提交成功！')
      this.EditdialogVisible = false
      this.ordernumber = res.data.OrderNumber
      this.payimage = res.data.PayUrl
      console.log(this.payimage)
      this.PaydialogVisible = true
    },
    async paysuccess () {
      this.PaydialogVisible = false
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params.append('OrderNumber', this.ordernumber)
      const res = await this.$http.post('Customer/ConfirmOrder/', params)
      if (res.data.StatusCode !== 200) return this.$message.error('支付状态保存失败！')
      this.$message.success('支付成功！')
    }
  }
}
</script>

<style lang="less" scoped>
.bottom {
    margin-top: 13px;
    line-height: 12px;
  }
  .el-checkbox {
    padding: 0;
    float: right;
  }
  .image {
    width: 100%;
    display: block;
  }
  .clearfix:before,
  .clearfix:after {
      display: table;
      content: "";
  }
  .clearfix:after {
      clear: both
  }

  .text {
  font-size: 14px;
}
.box_card{
  margin-left: 10px;
}
</style>
