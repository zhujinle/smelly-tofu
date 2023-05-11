<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item><a href="/">用户功能</a></el-breadcrumb-item>
      <el-breadcrumb-item>点菜</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片试图 -->
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <template>
          <el-select v-model="ChooseShop" placeholder="请在此选择店铺">
            <el-option
              @click.native="getFoodlist()"
              v-for="item in UserList"
              :key="item.ShopName"
              :label="item.ShopName"
              :value="item.ShopUID" >
            </el-option>
          </el-select>
          <el-button style="float: right;" type="primary" @click="SaveCart()">保存菜单</el-button>
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
                <el-checkbox v-model="item.Checked" label="加入购物车" border></el-checkbox>
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
      UserList: [],
      FoodList: [],
      inputUID: '',
      dialogTableVisible: false,
      adddialogVisible: false,
      EditdialogVisible: false,
      SingleUserInfo: [],
      ChooseShop: '',
      CartNember: []
    }
  },
  created () {
    this.getSellerlist()
  },
  methods: {
    ResetAddForm () {
      this.$refs.AddFormRef.resetFields()
    },
    async getSellerlist () {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      const res = await this.$http.post('Customer/SellerList/', params)
      if (res.data.StatusCode !== 200) return this.$message.error('信息错误！')
      this.UserList = res.data.Shops
      console.log(this.UserList)
    },
    async getFoodlist () {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      console.log(this.ChooseShop)
      params.append('UID', this.ChooseShop)
      const res = await this.$http.post('Customer/FoodList/', params)
      if (res.data.StatusCode !== 200) return this.$message.error('信息错误！')
      this.FoodList = res.data.Foods
      console.log(this.FoodList)
    },
    async SaveCart () {
      var str = '{"CartNember": ['
      var bool = false
      for (var { Checked: c, FoodID: ID } of this.FoodList) {
        if (c === true) {
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
    }
  }
}
</script>

<style lang="less" scoped>
.time {
    font-size: 13px;
    color: #999;
  }
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
