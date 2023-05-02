# API列表
所有命名使用驼峰准则


---

所有的页面需要检查Session Token是否存在及是否过期

### 平台API

- [ ] `POST`CheckSessionToken 检查Session Token的有效性

  输入(String)`DeviceID`/(String)`Session Token`

  输出(String)``StatusCode`

- [ ] `GET`GetSessionToken 获取一个新的Session Token

  输入(String)`DeviceID`

  输出(String)`StatusCode`/(String)`Session Token`

- [ ] `POST`Login 登录，获取Secret Key

  输入(String)`DeviceID`/(HASH)`UserName`/(HASH)`Password`/(String)`CAPTCHA Code`(这个懒得写，默认1先)

  输出(Int)`StatusCode`/(String)`Secret Key`/(Int)`UID`

### 客户层  -  Customer

- [ ] `POST`PersonalInformationView 查看个人信息

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`

  输出(String)`StatusCode`/(String)`UserName`/(UrlString)`AvatarUrl`/(Int)`MenberStatus`/(Double)`MoneySum`/(String)`Address`/(String)`Phone`

- [ ] `POST`ModifyPersonalInformation 修改个人信息

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`/(String)`UserName`/(UrlString)`AvatarUrl`/(String)`Address`/(String)`Phone`

  输出(String)`StatusCode`/(String)`UserName`/(String)`Address`

- [ ] `POST`ViewShoppingCart 查看购物车

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`

  输出(String)StatusCode/(json)CartMenber{[Foodid1,Number1,Money1,Discount1],[Foodid2,Number2,Money2,Discount2]......[FoodidN,NumberN,MoneyN,DiscountN]}

- [ ] `POST`ModifyShoppingCart 修改购物车

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`/(json)CartMenber{[Foodid1,Number1,Money1,Discount1],[Foodid2,Number2,Money2,Discount2]......[FoodidN,NumberN,MoneyN,DiscountN]}

  输出(String)StatusCode

- [ ] `POST`MakeOrder 下单

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`/(String)Address/(String)Phone/(String)Notes/(Int)Payment(1:Alipay,2:Wechat,3:balance)/(Int)OrderCheck

  输出(String)StatusCode/(String)OrderNumber

- [ ] `POST`OrderList 查看订单列表

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`

  输出(String)`StatusCode`/(json)`OrderList` `{OrderNumber1,OrderNumber2.......OrderNumberN}`

- [ ] `POST`CheckOrder 订单信息查看

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`/(String)OrderNumber

  输出(String)`StatusCode`(Int)`OrderNumber`/(String)`Address`/(String)`Phone`/(String)`Notes`/(Int)`Payment` `(1:Alipay,2:Wechat,3:balance)`/(Int)`PayStatus`/(String)`ShopAddress`/(String)`ShopPhone`/(String)`DeliveryStaffName`/(String)`DeliveryStaffPhone`/(Int)`DeliveryStatus` `(0:商家未接单,1:商家已结单未分配配送,2:商家已结单已分配配送未取餐,3:配送正在店内取餐,4:配送中,5:已送达)`/(Json)`OrderList` `{OrderNumber1,OrderNumber2.......OrderNumberN}`/(Double)`MoneySum`

  

  

### 商家层 - Seller
- [ ] `GET`InformationView 商家信息查看

  输入(Int)`UID`(Shop's)

  输出(String)`StatusCode`(String)`ShopName`/(UrlString)`AvatarUrl`/(Int)`MenberStatus`/(String)`Address`/(String)`Phone`/(UrlString)`BusinessLicenseUrl`/

- [ ] `POST`ModifyInformation 商家信息修改

  输入(Int)`UID`(Shop's)/(String)`Session Token`/(String)`Secret Key`/(String)`ShopName`/(UrlString)`AvatarUrl`/(Int)`MenberStatus`/(String)`Address`/(String)`Phone`/(UrlString)`BusinessLicenseUrl`/

  输出(String)`StatusCode`

- [ ] `GET`MenuView 菜单信息查看

  输入(Int)`UID`(Shop's)

  输出(String)`StatusCode`(String)/(Json)`MenuList` `{[Foodid1,Money1,Discount1],[Foodid2,Money2,Discount2]......[FoodidN,MoneyN,DiscountN]}`

- [ ] `POST`ModifyMenu 菜单信息修改

  输入(Int)`UID`(Shop's)/(String)`Session Token`/(String)`Secret Key`/(Json)`MenuList` `{[Foodid1,Money1,Discount1],[Foodid2,Money2,Discount2]......[FoodidN,MoneyN,DiscountN]}`

  输出(String)`StatusCode`(String)

- [ ] `POST`DashboardView 商家交易数据信息查看

  输入(Int)`UID`(Shop's)/(String)`Session Token`/(String)`Secret Key`

  输出(String)`StatusCode`(String)/(Double)`SumMoney`/(Double)`DailyMoney`/(Double)`WeeklyMoeny`/(Double)`MonthlyMoney`/(Int)`DailyCustomerSum`

- [ ] `POST`OrderList 查看订单列表

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`

  输出(String)`StatusCode`/(json)`OrderList` `{OrderNumber1,OrderNumber2.......OrderNumberN}`

- [ ] `POST`DeliveryStaffList 查看可用配送员

  输入(Int)`UID`(Shop's)/(String)`Session Token`/(String)`Secret Key`

  输出(String)`StatusCode`/(json)`DeliveryStaffList` `{[UID1,Name1],[UID2,Name2].......[UIDN,NameN]}`

- [ ] `POST`DeliveryPush 通知配送

  输入(Int)`UID`(Shop's)/(String)`Session Token`/(String)`Secret Key`/(String)`OrderNumber`/(Int)`DeliveryStaffUID`

  输出(String)`StatusCode`

- [ ] `POST`CheckOrder 订单信息查询

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`/(String)OrderNumber

  输出(String)`StatusCode`(Int)`OrderNumber`/(String)`Address`/(String)`Phone`/(String)`Notes`/(Int)`Payment` `(1:Alipay,2:Wechat,3:balance)`/(Int)`PayStatus`/(String)`ShopAddress`/(String)`ShopPhone`/(String)`DeliveryStaffName`/(String)`DeliveryStaffPhone`/(Int)`DeliveryStatus` `(0:商家未接单,1:商家已结单未分配配送,2:商家已结单已分配配送未取餐,3:配送正在店内取餐,4:配送中,5:已送达)`/(Json)`OrderList` `{OrderNumber1,OrderNumber2.......OrderNumberN}`/(Double)`MoneySum`

### 配送层 - DeliveryStaff
- [ ] `GET`InformationView 配送员信息查看

  输入(Int)`UID`

  输出(String)`StatusCode`(String)`UserName`/(UrlString)`AvatarUrl`/(Int)`MenberStatus`/(Double)`MoneySum`/(String)`Address`/(String)`Phone`/(UrlString)HealthCertUrl

- [ ] `POST`ModifyInformation 配送员信息修改

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`/(String)`UserName`/(UrlString)`AvatarUrl`/(String)`Address`/(String)`Phone`

  输出(String)`StatusCode`/(String)`UserName`/(String)`Address`

- [ ] `POST`OrderListView 订单列表查看

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`

  输出(String)`StatusCode`/(json)`OrderList` `{OrderNumber1,OrderNumber2.......OrderNumberN}`

- [ ] `POST`CheckOrder 订单信息查看

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`/(String)OrderNumber

  输出(String)`StatusCode`(Int)`OrderNumber`/(String)`Address`/(String)`Phone`/(String)`Notes`/(Int)`Payment` `(1:Alipay,2:Wechat,3:balance)`/(Int)`PayStatus`/(String)`ShopAddress`/(String)`ShopPhone`/(String)`DeliveryStaffName`/(String)`DeliveryStaffPhone`/(Int)`DeliveryStatus` `(0:商家未接单,1:商家已结单未分配配送,2:商家已结单已分配配送未取餐,3:配送正在店内取餐,4:配送中,5:已送达)`/(Json)`OrderList` `{OrderNumber1,OrderNumber2.......OrderNumberN}`/(Double)`MoneySum

- [ ] `POST`ModifyOrder 订单信息修改

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`/(String)OrderNumber/(Int)`DeliveryStatus` `(0:商家未接单,1:商家已结单未分配配送,2:商家已结单已分配配送未取餐,3:配送正在店内取餐,4:配送中,5:已送达)`/

  输出(String)`StatusCode`

- [ ] DashboardView 个人收入信息查看

  输入(Int)`UID`(Shop's)/(String)`Session Token`/(String)`Secret Key`

  输出(String)`StatusCode`(String)/(Double)`SumMoney`/(Double)`DailyMoney`/(Double)`WeeklyMoeny`/(Double)`MonthlyMoney`/(Int)`DailyOrderNumber`

### 后台管理层
- [ ] UserView 用户信息查看

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`

  输出(String)`StatusCode`/(json)`UserList` `{[UserNumber1,UserType1],[UserNumber2,UserType2].......[UserNumberN,UserTypeN]}`

- [ ] SingleUserView 单个用户信息查看

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`/(Int)TargetUserUID

  输出(String)`StatusCode`/(String)`UserName`/(UrlString)`AvatarUrl`/(Int)`MenberStatus`/(Double)`MoneySum`/(String)`Address`/(String)`Phone`/(Int)UserType

- [ ] ModifyUser 用户信息修改

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`/(String)`UserName`/(UrlString)`AvatarUrl`/(String)`Address`/(String)`Phone`/(Int)UserType

  输出(String)`StatusCode`

- [ ] MenuView 菜单信息查看

  输入(Int)`TargetShopUID`

  输出(String)`StatusCode`(String)/(Json)`MenuList` `{[Foodid1,Money1,Discount1],[Foodid2,Money2,Discount2]......[FoodidN,MoneyN,DiscountN]}`

- [ ] ModifyMenu 菜单信息修改

  输入(Int)`TargetShopUID`/(String)`Session Token`/(String)`Secret Key`/(Json)`MenuList` `{[Foodid1,Money1,Discount1],[Foodid2,Money2,Discount2]......[FoodidN,MoneyN,DiscountN]}`

  输出(String)`StatusCode`(String)

- [ ] OrderListView 订单列表查询

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`

  输出(String)`StatusCode`/(json)`OrderList` `{OrderNumber1,OrderNumber2.......OrderNumberN}

- [ ] CheckOrder 订单信息查看

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`/(String)OrderNumber

  输出(String)`StatusCode`/(Int)`OrderNumber`/(String)`Address`/(String)`Phone`/(String)`Notes`/(Int)`Payment` `(1:Alipay,2:Wechat,3:balance)`/(Int)`PayStatus`/(String)`ShopAddress`/(String)`ShopPhone`/(String)`DeliveryStaffName`/(String)`DeliveryStaffPhone`/(Int)`DeliveryStatus` `(0:商家未接单,1:商家已结单未分配配送,2:商家已结单已分配配送未取餐,3:配送正在店内取餐,4:配送中,5:已送达)`/(Json)`OrderList` `{OrderNumber1,OrderNumber2.......OrderNumberN}`/(Double)`MoneySum

- [ ] ModifyOrder 订单信息修改

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`/(Int)`OrderNumber`/(String)`Address`/(String)`Phone`/(String)`Notes`/(Int)`Payment` `(1:Alipay,2:Wechat,3:balance)`/(Int)`PayStatus`/(String)`ShopAddress`/(String)`ShopPhone`/(String)`DeliveryStaffName`/(String)`DeliveryStaffPhone`/(Int)`DeliveryStatus` `(0:商家未接单,1:商家已结单未分配配送,2:商家已结单已分配配送未取餐,3:配送正在店内取餐,4:配送中,5:已送达)`/(Json)`OrderList` `{OrderNumber1,OrderNumber2.......OrderNumberN}`/(Double)`MoneySum

  输出(String)`StatusCode`

- [ ] DeliveryPush 配送员分配

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`/(String)`OrderNumber`/(Int)`DeliveryStaffUID`

  输出(String)`StatusCode`

- [ ] DashboardView 整体信息查看

  输入(Int)`UID`/(String)`Session Token`/(String)`Secret Key`

  输出(String)`StatusCode`(String)/(Double)`SumMoney`/(Double)`DailyMoney`/(Double)`WeeklyMoeny`/(Double)`MonthlyMoney`/(Int)`DailyCustomerSum`





---

## Status Code 定义

定义类Http Request状态码定义

- 200 OK
- 302 Move Temporarily
- 400 Bad Request
- 401 Unauthorized
- 403 Forbidden
- 404 Not Found
- 405 Method Not Allowed
- 408 Request Timeout
- 411 Length Required
- 418 I'm a teapot
- 451 Unavailable For Legal Reasons
- 500 Internal Server Error
- 502 Bad Gateway
- 503 Service Unavailable