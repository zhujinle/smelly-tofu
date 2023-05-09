<template>
    <div class="login_container">
        <div class="login_box">
            <!-- Avatar -->
            <div class="avatar_box">
                <img src="../assets/logo.png" alt="" srcset="">
            </div>
            <div class="Name">
                  <span>Smelly-Tofu 外卖系统</span>
            </div>
            <!-- Form -->
            <el-form ref="loginFormRef" class="login_form" :model="LoginForm" :rules="LoginFormrules">
                <el-form-item prop="username">
                    <el-input v-model="LoginForm.username" type="username" prefix-icon="el-icon-user"></el-input>
                </el-form-item>
                <el-form-item prop="password">
                    <el-input v-model="LoginForm.password" type="password" prefix-icon="el-icon-lock"></el-input>
                </el-form-item>
                <el-form-item class="btns">
                    <el-button type="primary" @click="Login">登录</el-button>
                    <el-button type="info" @click="ResetLoginForm">重置</el-button>
                </el-form-item>
            </el-form>
        </div>
    </div>
</template>

<script>
export default {
  data () {
    return {
      LoginForm: {
        username: '',
        password: ''
      },

      LoginFormrules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    ResetLoginForm () {
      this.$refs.loginFormRef.resetFields()
    },
    Login () {
      this.$refs.loginFormRef.validate(async valid => {
        if (!valid) return
        const params = new URLSearchParams()
        params.append('username', this.LoginForm.username)
        params.append('password', this.LoginForm.password)
        const res = await this.$http.post('Login', params)
        console.log(res)
        if (res.data.StatusCode !== 200) return this.$message.error('登陆失败！账号或密码错误！')
        console.log(res)
        window.sessionStorage.setItem('SecretKey', res.data.SecreyKey)
        this.$message.success('登录成功！')
        this.$router.push('/home')
      })
    }
  }
}
</script>

<style lang="less" scoped>
.login_container{
    background-color: #2b4b6b;
    height: 100%;
}
.login_box{
    // width: 450px;
    // height: 300px;
    width: 40%;
    height: 40%;
    background-color: #fff;
    border-radius: 20px;
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%,-50%);
    .Name{
      display: flex;
      height: 20%;
      align-items: center;
      justify-content: center;
      padding: 10% 20%;
      font-size: 3.5vw;
    }
    .avatar_box{
        // weight: 130px;
        // height: 130px;
        weight: 20%;
        height: 20%;
        border: 1px solid #eee;
        border-radius: 50%;
        padding: 10px;
        box-shadow: 0 0 10px #ddd;
        position: absolute;
        left: 50%;
        transform: translate(-50%, -50%);
        background-color: #fff;
        img{
            width: 100%;
            height: 100%;
            border-radius: 50%;
            background-color: #eee;
        }
    }
}

.btns{
    display: flex;
    justify-content: flex-end;
}

.login_form{
    position: absolute;
    bottom: 0%;
    width: 100%;
    // height: 80%;
    padding: 0% 10%;
    box-sizing: border-box;
}
</style>
