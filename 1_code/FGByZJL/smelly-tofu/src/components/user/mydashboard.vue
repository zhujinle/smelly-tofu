<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item><a href="/">个人信息</a></el-breadcrumb-item>
      <el-breadcrumb-item>个人数据看板</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 卡片试图 -->
    <el-card class="box-card">
      <template>
      <div>
        <el-row :gutter="20">
          <el-col :span="6">
            <div>
              <el-statistic group-separator="," :precision="2" ></el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic title="日收入">
                <template slot="formatter"> {{DailyMoney}} </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic title="月收入">
                <template slot="formatter"> {{MonthlyMoney}} </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic title="总收入">
                <template slot="formatter"> {{SumMoney}} </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic title="日顾客">
                <template slot="formatter"> {{DailyCustomerSum}} </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic title="月顾客">
                <template slot="formatter"> {{Sumcustomer}} </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic value="feedback" title="评价等级Feedback">
                <template slot="suffix">
                  {{ feedback }}
                  <span @click="like = !like" class="like">
                    <i class="el-icon-star-on" style="color:red" v-show="!!like"></i>
                    <i class="el-icon-star-off" v-show="!like"></i>
                  </span>
                </template>
              </el-statistic>
            </div>
          </el-col>
        </el-row>
      </div>
      </template>
    </el-card>
    <!-- 平台 -->
    <el-card class="box-card">
      <template>
      <div>
        <el-row :gutter="20">
          <el-col :span="6">
            <div>
              <el-statistic group-separator="," :precision="2" ></el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic title="平台总交易金额">
                <template slot="formatter"> {{ptSumMoney}} </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic title="平台平均交易金额">
                <template slot="formatter"> {{ptAvgMoney}} </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic title="平台最大订单交易金额">
                <template slot="formatter"> {{ptMaxMoney}} </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic title="平台最小订单交易金额">
                <template slot="formatter"> {{ptMinMoney}} </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic title="平台日流水">
                <template slot="formatter"> {{ptDailyMoney}} </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic title="平台月交易流水">
                <template slot="formatter"> {{ ptMonthlyMoney }} </template>
              </el-statistic>
            </div>
          </el-col>

          <el-col :span="6">
            <div>
              <el-statistic title="日顾客">
                <template slot="formatter"> {{ ptDailyCustomer }} </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic title="月顾客">
                <template slot="formatter"> {{ ptSumCustomer }} </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic title="总注册用户量">
                <template slot="formatter"> {{ ptUserCounnt }} </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic value="feedback" title="评价等级Feedback">
                <template slot="suffix">
                  {{ feedback }}
                  <span @click="like = !like" class="like">
                    <i class="el-icon-star-on" style="color:red" v-show="!!like"></i>
                    <i class="el-icon-star-off" v-show="!like"></i>
                  </span>
                </template>
              </el-statistic>
            </div>
          </el-col>
        </el-row>
      </div>
      </template>
    </el-card>
  </div>
</template>

<script>
export default {
  data () {
    return {
      DailyMoney: 0,
      MonthlyMoney: 0,
      SumMoney: 0,
      DailyCustomerSum: 0,
      Sumcustomer: 0,
      feedback: '',
      like: false,
      ptSumMoney: 0,
      ptAvgMoney: 0,
      ptMaxMoney: 0,
      ptMinMoney: 0,
      ptDailyMoney: 0,
      ptMonthlyMoney: 0,
      ptDailyCustomer: 0,
      ptSumCustomer: 0,
      ptUserCounnt: 0
    }
  },
  created () {
    this.showEditDialog()
    this.getfeedback()
  },
  methods: {
    async showEditDialog () {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      const res = await this.$http.post('Seller/DashboardView/', params)
      if (res.data.StatusCode !== 200) {
        return this.$message.error('获取失败！')
      }
      this.$message.success('获取成功！')
      this.SumMoney = res.data.SumMoney
      this.DailyMoney = res.data.DailyMoney
      this.MonthlyMoney = res.data.MonthlyMoney
      this.Sumcustomer = res.data.Sumcustomer
      this.DailyCustomerSum = res.data.DailyCustomerSum
    },
    async getfeedback () {
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
      this.feedback = res.data.MenberStatus
      console.log('Feedback')
      console.log(this.feedback)
      this.getpt()
    },
    async getpt () {
      this.dialogTableVisible = true
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      const res = await this.$http.post('Admin/DashboardView/', params)
      if (res.data.StatusCode !== 200) {
        console.log(res)
        console.log('shibai')
        return this.$message.error('获取失败！')
      }
      this.$message.success('获取成功！')
      this.ptSumMoney = res.data.SumMoney
      this.ptAvgMoney = res.data.AvgMoney
      this.ptMaxMoney = res.data.MaxMoney
      this.ptMinMoney = res.data.MinMoney
      this.ptDailyMoney = res.data.DailyMoney
      this.ptMonthlyMoney = res.data.MonthlyMoney
      this.ptDailyCustomer = res.data.DailyCustomer
      this.ptSumCustomer = res.data.SumCustomer
      this.ptUserCounnt = res.data.UserCounnt
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
  margin-bottom: 30px;
}

.like {
    cursor: pointer;
    font-size: 25px;
    display: inline-block;
    margin-top: 20px;
  }
</style>
