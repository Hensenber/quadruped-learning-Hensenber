1.git常用命令
git init            #将文件夹git初始化，交给git管理
git status          #查看git状态
git add <file>      #将文件加入暂存去
git add .           #将整个文件夹加入暂存区
git commit -m ""    #提交本次的更新，""里是本次提交的内容
git log             #查看日志
常用:
git log --oneline --graph --decorate --all
让日志内容排版好看一点
git diff            #查看工作区相对暂存区的变化
git diff --staged   #查看暂存区相对最近一次提交的变化



2.  .gitignore的应用
有时.venv虚拟环境、__pycache__/缓存等文件是我们不想也不需要提交给git管理的，这时我们可以使用.gitignore来让git忽略它们。
在项目根目录创建.gitignore,在里面写诸如:
# 忽略一个文件
password.txt

# 忽略一个文件夹
.venv/

# 忽略 Python 缓存
__pycache__/

# 忽略所有 .log 文件
*.log

# 忽略所有 .tmp 文件
*.tmp


就可以忽略掉相应的文件


3.分支
分支是指向某次提交的可移动引用，可以理解为一种指针：
A ─── B ─── C
            ↑
           main

它的作用是让我们在开发时可以尝试一些具有风险的技术路径，比如我们在开发到C时，机器人已经能实现稳定的站立，下一步要开发它的步态控制单元，我们就可以这样写：

git switch -c feature/gait

这样即使我们在后续进行了新的开发，main也会停留在-c处：

A ─── B ─── C
            │
            └── D ─── E
                      ↑
                feature/gait

            ↑
           main

只有在完成技术验证，确保稳定后才会将分支合并回主线。

4.合并
合并分为快速合并(fast-forward)、三方合并(three-way merge)、合并冲突(merge conflict)

快速合并是指main本身不发生变化，branch在main的版本之后，此时git只需要让main追上branch就行了：

A ─ B ─ C ─ D ─ E
        ↑       ↑
       main   feature/gait

三方合并是指main和branch都发生了变化，但是git发现自己可以处理得了这种变化，于是它综合main和branch两种版本

                   D ─── E
                  /       \
A ─── B ─── C              H
                  \       /
                   F ─── G
                           ↑
                          main

合并冲突是最麻烦的，两个分支修改同一个文件中无法自动兼容的区域时，Git 会停止合并并标记冲突。比如同一个变量在两个分支中值不同

这时候我们要用git status查看冲突文件，手动修改或确定冲突的部分最终的值，然后git add controller.py来进行提交人工决定的最终版本

果发现合并方向错了且合并尚未完成，可以：
git merge --abort
来回溯到合并开始前



合并完成后，feature/gait这样的指针可以删除，使用：
git branch -d feature/gait 即可做到


5.小结
# 我有哪些分支？
git branch

# 创建一个新分支，并进入它
git switch -c feature/gait

# 回到 main
git switch main

# 把 feature/gait 合并进当前的 main
git merge feature/gait

# 已经合并完成，不需要这个分支了
git branch -d feature/gait




6.与github的协作

加入已有项目时，通常直接克隆远程仓库：
git clone git@github.com:USER/REPOSITORY.git
也可以使用 HTTPS 地址。 git clone 会创建本地仓库、下载远程历史，并通常将该远
程仓库命名为 origin 。进入仓库后可以查看远程信息：
git remote -v
这并非简单地下载文件，而是将日志、commit、branch等一并下载


使用：
git remote add origin git@github.com:USER/REPOSITORY.git
可以将本地项目添加到github上

fetch、push与pull：
                GitHub
             远程仓库 origin
                  │
          ┌───────┴────────┐
          │                ▲
       fetch              push
          │                │
          ▼                │
      获取远程信息           │
          │                │
          ▼                │
       本地 Git 仓库 ────────┘


pull ≈ “获取远程更新 + 尝试整合进当前分支”

git fetch功能是获取github上的最新状态，比如队友进行了一些新的提交，想知道项目的最新状态，就可以使用该命令

git pull则是获取最新的状态并尝试整合



7.工作流
实际开发中可以采用下面的简单流程：同步 main → 从 main 创建任务分支 → 修改和提交 → 推送任务分支到 GitHub → 通过 Pull Request 审查并合并

比如一个同学负责电机控制研发
先用
git switch main
git pull
确保main的开发进度是最新的，然后使用git switch -c feature/motor-state来创建自己的电机开发分支，最终commit自己的开发进度，通过pull request审查后便可整合到团队最新的main开发进度中

pull request（PR）是一种团队审查流程，可以理解为：

main
│
│
└──────── feature/motor-state
              │
              │
              │ Pull Request
              │
              ▼
        “申请合并进 main”
              │
        ┌─────┴─────┐
        │           │
      检查代码     自动测试
        │           │
        └─────┬─────┘
              ↓
           通过
              ↓
            Merge
              ↓
             main


8.撤销与版本回溯
常见的开发流程是：
修改文件
   ↓
【工作区】
   │
   │ git add
   ↓
【暂存区】
   │
   │ git commit
   ↓
【本地仓库】
   │
   │ git push
   ↓
【GitHub 远程仓库】

撤销需要根据进行到哪一步来判断

一、add出现问题
如果git add .之后临时反悔，可以通过git restore --<file>来把文件取消加入暂存区

二、代码出现问题，需要回滚到之前commit的版本
先git diff <file>确认想要新的修改,然后用git restore <file>来用之前的版本覆盖当前的修改

三、commit出现问题
如果commit出现问题，我们想修改最新一次的commit，可以使用amend命令，即：
git add motor.hpp
git commit --amend
这样git会将最近一次的修改撤销，并更换一个新的commit

四、回滚commit
git reset有三种常用模式
git reset --soft <commit-id>
git reset --mixed <commit-id>
git reset --hard <commit-id>

reset --soft：撤销 commit，但保留在暂存区               #适合“这个 commit 组织得不好，我想重新整理后再 commit。”
reset --mixed：撤销 commit，并取消暂存，但代码还在       #这是默认设置
reset --hard：撤销commit，并删除工作区修改信息           #风险最高。虽然某些已经提交过的对象可能暂时还能通过 reflog 找回                                                    #来，但未提交的工作区修改可能无法恢复



9.总结
使用git的核心是理解四层状态

① 工作区
   Working Tree
       │
       │ git add
       ▼
② 暂存区
   Staging Area
       │
       │ git commit
       ▼
③ 本地仓库
   Local Repository
       │
       │ git push
       ▼
④ 远程仓库
   GitHub

常用命令对应表：
看当前情况	                git status
看具体改了什么	             git diff
把修改加入暂存区	         git add .
创建一次提交	             git commit -m "..."
查看历史	                git log --oneline --graph --decorate --all
创建并进入新分支	         git switch -c <branch>
切换分支	                git switch <branch>
合并分支	                git merge <branch>
查看 GitHub 地址	        git remote -v
获取远程信息	             git fetch
获取并整合更新	             git pull
上传提交	                git push

流程图：
                 你正在编辑文件
                       │
                       ▼
                ┌────────────┐
                │   工作区    │
                └─────┬──────┘
                      │
                   git add
                      │
                      ▼
                ┌────────────┐
                │   暂存区    │
                └─────┬──────┘
                      │
                  git commit
                      │
                      ▼
             ┌────────────────┐
             │    本地仓库     │
             │                │
             │ A ─ B ─ C      │
             │       ├─ D     │ ← branch
             │       └─ E     │
             └───────┬────────┘
                     │
                  git push
                     │
                     ▼
              ┌──────────────┐
              │    GitHub     │
              │   远程仓库    │
              └──────┬───────┘
                     │
               fetch / pull
                     │
                     ▼
                  本地仓库