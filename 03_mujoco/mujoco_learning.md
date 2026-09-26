1.xml文件
xml本质是文本文件，它可以理解为一种“世界说明书”，主要负责向mujoco描述这个世界的物理规则。
xml文件的基本语法只需要记住两个：一、标签。基本格式是：
    <body>
    ...
    </body>
    前面的叫开始标签，后面的叫结束标签
二、标签，如<body name="box" pos="0 0 1">

真正让xml文件运转起来的是simulate.py文件

一般而言为了让三维图形更加具有立体感，需要在某位置放置一个light，这样上面的光影会更加有层次

rgba中，r g b分别代表红绿蓝，即三原色，而a代表透明度，这组数值决定了某个实体的颜色。



2.MJCF
MJCF是MuJoCo规定的一套“用 XML 写机器人/物理模型的规则”。MJCF 是基于 XML 语法制定的 MuJoCo 模型描述语言，而 .xml 是保存它的文件格式。
┌───────────────────────────────┐
│         MuJoCo 模型           │
│                               │
│ compiler → 模型怎么解析/编译   │
│ option   → 物理世界怎么运行    │
│ asset    → 要用哪些资源        │
│ worldbody→ 世界里有什么东西    │
│ actuator → 怎么驱动关节        │
│ sensor   → 要测量什么东西      │
└───────────────────────────────┘
                   MJCF
                    │
                 <mujoco>
                    │
     ┌──────────────┼──────────────┐
     │              │              │
 compiler         option          asset
 怎么解析          怎么仿真         用什么资源
                                    │
                              mesh/材质/纹理

                    │
          ┌─────────┼─────────┐
          │         │         │
      worldbody  actuator   sensor
          │         │         │
      世界里有啥   怎么驱动   测量什么
          │         │         │
       机器人      电机等     传感信息
       地面等

3.MJCF机器人结构：body、joint与geom
body 表示刚体以及局部坐标系；joint 定义当前 body 相对于父 body 如何运动；geom 描述几何形状，可用于碰撞和显示。

例如：
       机器人机身
          │
          ● ← 髋关节
          │
        大腿
          │
          ● ← 膝关节
          │
        小腿

会被Mujoco理解成：
body：机身
│
└── body：大腿
    │
    ├── joint：髋关节
    │
    └── body：小腿
        │
        └── joint：膝关节

joint分为
hinge → 绕轴旋转
slide → 沿轴直线移动
free  → 六自由度自由运动

geom表示几何形状，一个body可能会有多个geom

4.机器人的运动：freejoint
刚体的freejoint有六个自由度

为了描述机器人的运动，就必须引入位置、姿态、速度这些参数
qpos：
[x, y, z, qw, qx, qy, qz]
 └位置┘    └─四元数姿态─┘
3 + 4 = 7个参数
 qvel：
[vx, vy, vz, wx, wy, wz]
 └线速度┘   └角速度┘
3 + 3 = 6个参数


5.运动与碰撞的动力学仿真
动力学仿真需要知道每个刚体的质量、质心和惯量等参数。即让机器人动起来“像是真的”
我们需要知道质量、质心和惯量会直接影响机器人运动。如果模型在仿真中表现出明显异常，例如轻微接触就快速弹飞、某条腿运动得异常剧烈，除了检查控制器，还应该检查质量、惯量、碰撞几何和关节参数。

另外，机器人的外观模型visual model和碰撞模型collision model可以不同
             同一个机器人部件
                    │
          ┌─────────┴─────────┐
          ↓                   ↓
       外观模型             碰撞模型
       visual              collision
          │                   │
     复杂 mesh            简单几何体
          │                   │
      “看起来像”           “算碰撞用”


6.小结：
                 四足机器人
                     │
                     ▼
              【第 7 节：结构】
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
     body          joint          geom
   有哪些刚体     怎么连接运动      什么形状
       │
       └─────────────┬─────────────┘
                     ▼
              搭出机器人的身体
                     │
                     ▼
             【第 8 节：自由运动】
                     │
                 freejoint
                     │
           让整个基座可以自由运动
                     │
              ┌──────┴──────┐
              ▼             ▼
            qpos           qvel
          当前在哪/姿态     当前怎么动
                     │
                     ▼
             【第 9 节：物理性质】
                     │
       ┌─────────────┼─────────────┐
       ▼             ▼             ▼
      质量           惯量          碰撞
    mass          inertia       collision
       │             │             │
       └─────────────┴─────────────┘
                     ▼
          决定机器人实际怎样运动

7.URDF与MJCF的联系与区别

实际机器人项目经常给你的是 URDF，而进入 MuJoCo 后常常需要面对 MJCF。两者都在描述机器人，但组织方式和仿真能力不同。转换完成后还必须检查模型，不能以“能打开”作为“模型正确”的标准。后续需要阅读和修改 MJCF、加入执行器、组织场景，并逐渐接触 MuJoCo 特有的模型参数；显式完成转换过程也有助于理解 URDF 和 MJCF 的对应关系。

URDF 常用 link + joint 描述父子关系，而 MJCF 主要通过嵌套 body 构成运动学树。MJCF 还提供 MuJoCo 仿真相关的执行器、传感器、默认参数等功能。

URDF 在 ROS 和机器人项目里很常见，主要通过 link 和 joint 描述机器人结构；MJCF 是 MuJoCo 原生模型语言，主要通过嵌套 body 建立运动学树，而且还能描述 actuator、sensor 等 MuJoCo 仿真内容。MuJoCo 可以读取 URDF，但实际项目中经常整理成 MJCF 方便进一步配置仿真。




8.场景复用
models/
   ↓
放“机器人”

scenes/
   ↓
放“机器人所在的世界”

scripts/
   ↓
放“运行和控制程序”

在这种目录结构下，机器人可以复用在多个不同的场景中。MJCF支持通过 include 组合多个XML文件

MJCF 支持通过 include 组合多个 XML 文件

如：
<include file="../models/robot.xml"/>
就表示把另一个 XML 文件里的相关内容包含到当前模型中。

9.模型-场景-控制 三级结构
在阅读一个新的mujoco项目时，应当从三个方面去分析它的结构
                 MuJoCo 项目
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
     机器人本体     环境场景       控制程序
        │            │            │
    robot.xml    scene.xml    simulate.py
        │            │            │
       body          地面        加载模型
       joint         灯光        读取状态
       geom          相机        写入控制
       actuator      环境物体     mj_step()
       ...           ...

10. data.ctrl 控制数组
不同于data.qpos数组表示广义位置，data.qvol表示广义速度，这里的data.ctrl数组表示电机的控制输入。

它们的结构类似：
                    Python 控制程序
                         │
            ┌────────────┴────────────┐
            │                         │
        读取机器人                 控制机器人
            │                         │
       ┌────┴────┐                    │
       ↓         ↓                    ↓
     qpos       qvel                 ctrl
       │         │                    │
    在哪？     怎么动？             给多大控制？
       │         │                    │
       └────┬────┘                    │
            │                         │
            ▼                         ▼
         当前状态                  执行器输入

data.ctrl这个数组的维度由model.nu决定，也就是整个模型的独立model actuator数量。

而数组里每个元素的值，表示一台独立的执行器actuator的控制输入，而输入单位则有actuator的类型决定，比如一个hinge + motor + gear=1的模型，由于是铰链连接的关节传动，所以输入单位自然是力矩的单位N·m

11.机器人控制的基本思想
              MuJoCo 机器人
                   │
                   │
                   ▼
           qpos / qvel
          “我现在怎么样？”
                   │
                   ▼
             Python 控制器
                   │
              根据状态计算
                   │
                   ▼
                 ctrl
          “接下来施加什么控制？”
                   │
                   ▼
               actuator
                   │
                   ▼
                 joint
                   │
                   ▼
              机器人运动
                   │
                   ▼
               mj_step()
                   │
                   ▼
         新的 qpos / qvel
                   │
                   └──────────↺

12.关于零力矩
给所有电机的力矩都设置成 0，机器人也并一定保持不动。这只代表控制程序没有通过执行器提供主动驱动力矩。机器人仍然受到重力、接触力、关节阻尼以及模型中其他物理因素的影响。例如一只四足机器人站着时，腿部电机往往需要产生力矩来支撑身体。

13.关于一个完整的基础力矩控制程序的组成
实例：
import time             
import mujoco
import mujoco.viewer            #引入时间等库

model = mujoco.MjModel.from_xml_path("scene.xml")           #通过xml文件引入物理世界的说明
data = mujoco.MjData(model)                                 #生成data表征世界实时状态 

with mujoco.viewer.launch_passive(model, data) as viewer:   #用launch_passive打开Viwer可视化界面，但python主程
                                                            #序仍然由用户来控制
    while viewer.is_running():                              #当viewer还在运行时就继续推进该循环

        step_start = time.time()                            #获取当前时间存入开始时间

        # 读取当前状态
        qpos = data.qpos.copy()                             #获取广义坐标qpos的备份
        qvel = data.qvel.copy()                             #获取广义速度qvel的备份

        # 计算控制量
        torque = 0.0

        # 写入执行器控制输入
        if model.nu > 0:
            data.ctrl[:] = torque

        # 推进仿真
        mujoco.mj_step(model, data)                         #mujoco会根据模型的世界物理规则和当前状态data来计算下
                                                            #一个时间步长的世界状态
        # 更新 Viewer
        viewer.sync()               

        # 让显示速度大致接近真实时间
        time_left = model.opt.timestep - (time.time() - step_start)

        if time_left > 0:
            time.sleep(time_left)

基本的闭环控制程序流程循环可以表示为
        ┌──────────────────────┐
        │                      │
        ▼                      │
   读取 qpos/qvel              │
        │                      │
        ▼                      │
   计算控制量                  │
        │                      │
        ▼                      │
   写入 data.ctrl              │
        │                      │
        ▼                      │
      mj_step()                │
        │                      │
        ▼                      │
  得到新的 qpos/qvel ──────────┘





  14.如何阅读 unitree_mujoco 一类开源项目
不应从第一行开始，一直看到结尾，正确的观看方法应当是：
    README
            ↓
    运行命令
            ↓
    程序入口
            ↓
    模型在哪里加载
            ↓
    MjModel / MjData 在哪里创建
            ↓
    主循环在哪里
            ↓
    状态在哪里读取
            ↓
    data.ctrl 在哪里写入
            ↓
    mj_step 在哪里执行
            ↓
    其他模块分别负责什么

同时要注意，遇到陌生的类时，先搞清楚这个类在整个运行流程里负责什么，然后再读它内部细节。

    谁创建了 RobotController？
        ↓
    谁调用它？
        ↓
    给它输入了什么？
        ↓
    它返回什么？
        ↓
    返回结果去了哪里？





15.常见纠错方法
如果模型出现问题了，不要一股脑的乱改一通参数，而要按照这个顺序慢慢排查错误：
程序出问题
   │
   ▼
① 模型成功加载了吗？
   │
   ▼
② 模型结构正确吗？
   │
   ▼
③ 初始状态正确吗？
   │
   ▼
④ actuator 正确吗？
   │
   ▼
⑤ ctrl 真的写进去了吗？
   │
   ▼
⑥ mj_step() 正常执行吗？
   │
   ▼
⑦ 最后再分析机器人运动

