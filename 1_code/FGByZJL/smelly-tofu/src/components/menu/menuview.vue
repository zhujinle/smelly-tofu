<template>
  <div>
    <!-- 面包屑 -->
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item><a href="/">菜单管理</a></el-breadcrumb-item>
      <el-breadcrumb-item>食品列表</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 添加用户对话框 -->
    <el-dialog title="添加用户" :visible.sync="adddialogVisible" width="50%">
        <span>食品信息输入</span>
        <el-form ref="AddFormRef" :model="AddForm" :rules="AddFormrules">
                <el-form-item label="店铺UID" prop="UID">
                    <el-input v-model="AddForm.UID" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="金额" prop="Money">
                    <el-input v-model="AddForm.Money" prefix-icon="el-icon-lock"></el-input>
                </el-form-item>
                <el-form-item label="折扣" prop="Discount">
                    <el-input v-model="AddForm.Discount" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
        </el-form>
        <!-- 底部 -->
        <span slot="footer" class="dialog-footer">
            <el-button @click="adddialogVisible = false">取 消</el-button>
            <el-button type="info" @click="ResetAddForm">重置</el-button>
            <el-button type="primary" @click="AddFood">确 定</el-button>
        </span>
    </el-dialog>
    <!-- 修改用户对话框 -->
    <el-dialog title="用户信息修改" :visible.sync="EditdialogVisible" width="50%">
      <el-form ref="EditFormRef" :model="EditForm" :rules="AddFormrules">
                <el-form-item label="店铺UID" prop="ShopID_id">
                    <el-input v-model="EditForm.ShopID_id" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item label="金额" prop="Money">
                    <el-input v-model="EditForm.Money" prefix-icon="el-icon-lock"></el-input>
                </el-form-item>
                <el-form-item label="折扣" prop="Discount">
                    <el-input v-model="EditForm.Discount" prefix-icon="el-icon-user"></el-input>
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
      <!-- 搜索 -->
      <el-row :gutter="20">
        <el-col :span="7">
            <el-input placeholder="请输入店铺ID" v-model="inputFoodid" clearable @clear="getFoodlist">
                <el-button slot="append" icon="el-icon-search" @click="getFoodlist"></el-button>
            </el-input>
        </el-col>
        <el-col :span="4">
            <el-button type="primary" @click="adddialogVisible = true">添加食物</el-button>
        </el-col>
      </el-row>

      <!-- 食物列表 -->
      <template>
        <el-table :data="FoodList" stripe style="width: 100%">
            <el-table-column prop="FoodID" label="FoodID" width="60"></el-table-column>
            <el-table-column prop="ShopID_id" label="店铺ID" width="150"></el-table-column>
            <el-table-column prop="Money" label="价格" width="180"></el-table-column>
            <el-table-column prop="Discount" label="折扣" width="380"></el-table-column>
            <el-table-column prop="FoodPhoto" label="状态" width="100">
                <template slot-scope="scope">
                    <img :src="scope.row.FoodPhoto" class="image">
                </template>
            </el-table-column>
            <el-table-column label="操作" fixed="right" width="200">
                <template slot-scope="scope">
                    <!-- 修改 -->
                    <el-tooltip effect="dark" content="修改信息" placement="top" :enterable="false">
                        <el-button type="warning" icon="el-icon-edit" size="mini" @click="showEditDialog(scope.row)"></el-button>
                    </el-tooltip>
                    <!-- 删除 -->
                    <el-tooltip effect="dark" content="删除" placement="top" :enterable="false">
                        <el-button type="danger" icon="el-icon-delete" size="mini" @click="deleteFood(scope.row)"></el-button>
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
      FoodList: [],
      inputFoodid: '',
      dialogTableVisible: false,
      adddialogVisible: false,
      EditdialogVisible: false,
      SingleUserInfo: [],
      AddForm: {
        Discount: '',
        Money: '',
        ShopID_id: ''
      },
      EditForm: {
        Discount: '',
        Money: '',
        ShopID_id: ''
      },
      AddFormrules: {
        ShopID_id: [
          { required: true, message: '请输入', trigger: 'blur' }
        ],
        Money: [
          { required: true, message: '请输入', trigger: 'blur' }
        ],
        Discount: [
          { required: true, message: '请输入', trigger: 'blur' }
        ],
        Type: [
          { required: true, message: '请选择用户类型', trigger: 'blur' }
        ]
      }
    }
  },
  created () {
    this.getFoodlist()
  },
  methods: {
    ResetAddForm () {
      this.$refs.AddFormRef.resetFields()
    },
    async getFoodlist () {
      const params = new URLSearchParams()
      params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      if (this.inputFoodid !== '') params.append('TargetShopUID', this.inputFoodid)
      const res = await this.$http.post('Admin/MenuView/', params)
      if (res.data.StatusCode !== 200) return this.$message.error('信息错误！')
      this.FoodList = res.data.Menu
      console.log('========')
      console.log(res)
    },
    AddFood () {
      this.adddialogVisible = false
      this.$refs.AddFormRef.validate(async valid => {
        if (!valid) return
        const params = new URLSearchParams()
        params.append('UID', this.AddForm.UID)
        params.append('Money', this.AddForm.Money)
        params.append('Discount', this.AddForm.Discount)
        params.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
        const res = await this.$http.post('Admin/AddMenu/', params)
        console.log(res)
        if (res.data.StatusCode !== 200) return this.$message.error('添加失败！')
        console.log(res)
        this.$message.success('添加成功！')
        this.getFoodlist()
      })
    },
    async showEditDialog (foodinfo) {
      this.EditForm = foodinfo
      this.EditdialogVisible = true
    },
    async pushEditDialog () {
      const params2 = new URLSearchParams()
      params2.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params2.append('UID', this.EditForm.ShopID_id)
      params2.append('FoodID', this.EditForm.FoodID)
      params2.append('Money', this.EditForm.Money)
      params2.append('Discount', this.EditForm.Discount)
      const res2 = await this.$http.post('Admin/ModifyMenu/', params2)
      this.EditdialogVisible = false
      if (res2.data.StatusCode !== 200) {
        return this.$message.error('保存失败！')
      }
      this.$message.success('保存成功！')
    },
    async deleteFood (userinfo) {
      const params2 = new URLSearchParams()
      params2.append('SecretKey', window.sessionStorage.getItem('SecretKey'))
      params2.append('TargetFoodID', userinfo.FoodID)
      const res2 = await this.$http.post('Admin/DeleteFood/', params2)
      this.EditdialogVisible = false
      if (res2.data.StatusCode !== 200) {
        console.log(res2)
        return this.$message.error('删除失败！')
      }
      this.$message.success('删除成功！')
      this.getFoodlist()
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
