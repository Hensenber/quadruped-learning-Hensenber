import time
import mujoco
import mujoco.viewer            #导入python自带的时间模块,导入mujoco和可视化模块。

model = mujoco.MjModel.from_xml_path("scene.xml")           #mujoco表示引用这个模块的函数,Mjmodel表示创建模型,from_xml_path表示从xml文件导入创建
data = mujoco.MjData(model)             #创建data

with mujoco.viewer.launch_passive(model, data) as viewer:           #打开一个 MuJoCo 可视化窗口，并把它叫作 viewer
    while viewer.is_running():              #只要 Viewer 还在运行，就不停执行下面的代码。
        step_start = time.time()

        mujoco.mj_step(model, data)         #根据当前的状态和时间步长，来计算下个时间步
        viewer.sync()           #把刚刚算出来的新状态同步到 Viewer,让画面更新。

        time_left = model.opt.timestep - (time.time() - step_start)
        if time_left > 0:
            time.sleep(time_left)           #让显示速度大致接近真实时间。