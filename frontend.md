整个系统包括三个角色：

市政管理员

医院管理员

居民（公众用户）

🏛 一、系统整体导航架构
📌 首页（公共）
📌 医院列表（公共）
📌 医院详情（公共）

👨‍⚕️ 医院管理员后台
    ├── 医院信息管理
    ├── 科室资源管理
    ├── 医护人员管理
    ├── 突发事件上报/参与
    └── 评分上报

🏙 市政管理员后台
    ├── 医院管理（增删改）
    ├── 标准科室库管理
    ├── 全市医院资源总览
    ├── 全市医护人员统计
    ├── 突发事件管理
    └── 等级设置

🌏 二、公众端页面设计（无需登录）
① 首页（系统门户）
📌 页面作用

展示城市医疗公共服务入口

搜索医院

提供服务导航（医院查询、急诊、疫情、突发事件公告等）

📌 主要功能模块

搜索栏（按名称、区域、等级）

推荐医院列表

快捷入口（如预约挂号、最新事件公告）

② 医院列表页
📌 页面作用

用户按条件搜索医院。

📌 核心功能

左侧筛选：

地区

等级

医院类型

右侧列表：医院卡片（名称/地址/评分）

📌 数据来源

POST /api/public/search_hospital/

③ 医院详情页
📌 页面作用

展示医院详细信息。

📌 内容模块

医院基础信息

科室列表

医院评分（折线图或列表）

参与的突发事件记录

📌 API

/api/hospitals/{id}/

/api/hospitals/{id}/departments/

/api/hospitals/{id}/scores/

/api/hospitals/{id}/events/

🏥 三、医院管理员后台页面设计

医院管理员角色主要管理“自己医院的资源”。

布局采用后台 Admin Layout：

左侧菜单 / 顶部用户栏 / 右侧内容区

④ 医院信息管理
📌 页面作用

修改本院的基础资料（不能修改 hospital_id）。

包含模块：

医院基本信息编辑（名称、地址、电话等）

医院简介 Rich Text 富文本

医院等级（只读）

API
GET /api/hospitals/{id}/
PATCH /api/hospitals/{id}/

⑤ 科室资源管理（重点页面）

包含医院所有科室的设备、床位等资源。

📌 页面作用

医院管理员维护：

床位数

设备数量

可用情况

交互设计：

左侧科室树（方便快速切换）

右侧资源表格（可编辑）

API
GET /api/department_resources/?hospital=我的医院
POST /api/department_resources/
PATCH /api/department_resources/{id}/


系统会自动补全 hospital_id（后端已处理）。

⑥ 医护人员管理
页面分为两个子页：
A. 员工信息管理（全市员工库）

因为员工信息是全局的（staff 表）

API：

GET /api/staffs/
POST /api/staffs/

B. 医院员工执业关系（hospital_staff）

例如：

王医生（属于本院神经外科）

李护士（属于本院急诊科）

API：

GET /api/hospital_staffs/?hospital=本院
POST /api/hospital_staffs/


医院管理员新增员工时，系统自动绑定 hospital_id。

⑦ 突发事件响应中心
📌 页面作用

医院用于上报/参与突发事件。

两个页面：

A. 全部突发事件列表

显示所有事件（后端允许所有医院查看）

API：

GET /api/events/

B. 本院参与的事件（关键页）

医院管理员可执行：

参与事件（新增 hospital_event 记录）

更新处理进度

上传材料（附件未来可扩展）

API：

GET /api/hospital_events/?hospital=本院
POST /api/hospital_events/


后端会自动绑定 hospital_id，安全可靠。

⑧ 医院评分上报（自查）

用于医院向市政府提交自评结果（检查结果、得分）。

API：

GET /api/scores/?hospital=本院
POST /api/scores/

🏙 四、市政管理员后台页面设计

市政管理员可看全局数据，权限最大。

⑨ 医院管理（CRUD）
📌 功能

新建医院

修改医院信息

删除医院

API：

GET /api/hospitals/
POST /api/hospitals/
PATCH /api/hospitals/{id}/
DELETE /api/hospitals/{id}/

⑩ 标准科室库管理

用于维护“全市统一的科室列表”。

API：

GET /api/departments/
POST /api/departments/
DELETE /api/departments/{id}/

⑪ 全市医院资源总览（数据大屏）
📌 页面作用（核心决策页面）

市政管理员查看：

全市医院床位总数

ICU 总数

设备总数

各医院资源对比图（柱状 / 雷达图）

API：

GET /api/department_resources/
GET /api/hospitals/

⑫ 全市人员统计

医生人数

护士人数

各医院人员分布

API：

GET /api/staffs/
GET /api/hospital_staffs/

⑬ 突发事件管理

市政管理员可：

新建突发事件

查看所有事件处理情况

API：

GET /api/events/
POST /api/events/

⑭ 等级设置管理（医院等级库）
GET /api/hospital_levels/
POST /api/hospital_levels/
PATCH /api/hospital_levels/{id}/
DELETE /api/hospital_levels/{id}/