# [xiaomi yu7 notify](https://github.com/arthurfsy2/xiaomi_yu7_bark_notify)
![img](/img/para_succeed.jpg)
一个可以自动获取小米YU7交付进度，通过Bark通知给用户的脚本。

PS：本脚本采用Cookie的方式进行获取数据，可能存在Cookie过期的情况，需要手动更新


## Github Action

如果你想通过 Github Action 来实现定时获取数据，可进行以下步骤

1. fork 本项目到你自己的仓库，然后修改 fork 仓库内的 `.github/workflows/run_notify_sync.yml`文件，以下内容改为你自己的 github 信息。

```
env:
  GITHUB_NAME: arthurfsy2 （修改成你的github名称）
  GITHUB_EMAIL: fsyflh@gmail.com （修改为你的github账号邮箱）
```

    默认执行时间是每5分钟会自动执行脚本。

    如需修改时间，可修改以下代码的`cron`

```
on:
  workflow_dispatch:
  schedule:
    - cron: '*/5 * * * *'
```

2. 为 GitHub Actions 添加代码提交权限 访问 repo Settings > Actions > General 页面，找到 Workflow permissions 的设置项，将选项配置为 Read and write permissions。
   
   > 如果不设置允许的话，会导致 workflows 无法更新配置文件

3. 在 repo Settings > Security > Secrets > secrets and variables > Actions > New repository secret > 增加:
   COOKIE、DEVICE_TOKEN、ORDERID、USERID 这4个变量

   ![img](/img/添加变量.png)

4. 以上变量的值获取方法：
使用[Reqable](https://reqable.com/zh-CN)等抓包工具，抓取小米汽车微信小程序
查看：https://api.retail.xiaomiev.com/mtop/car-order/order/detail

- ORDERID、USERID的获取：
![img](/img/1.png)

- COOKIE的获取

> 注意：COOKIE变量在粘贴到github action时，首尾要添加`"`符号

![img](/img/2.png)

- DEVICE_TOKEN的获取
IOS下载`Bark`-->服务器-->复制device_token
![img](/img/3.png)

> 在device_token正确的情况下，运行action后，如果ORDERID、USERID、COOKIE任意一个参数存在问题，会发送错误提醒

![img](/img/para_error.jpg)

## 青龙面板
如果你是和我一样，是一个略懂青龙面板的“脚本小子”，也可以通过以下来设置定时任务来执行脚本
1. 安装Python依赖：requests、toml
![img](/img/ql-1.png)

2. 复制文件
- 需复制文件：yu7_notify.py、configBAK.toml（需手动改名为config.toml）
- 修改config.toml当中的orderId、userId、Cookie、device_token（取值来源可参考上文）
![img](/img/ql-2.1.png)
![img](/img/ql-2.2.png)

> 如果是docker部署的青龙面板，可以将上述2个文件复制粘贴到宿主机对应的目录

3. 调试脚本（可选）
![img](/img/ql-3.1.png)
![img](/img/ql-3.2.png)

> 如果依赖安装正常、账号参数正确，则会输出对应的日志提示

4. 设置定时任务

- 名称：`yu7_notify`（可修改）
- 命令/脚本：`python  /ql/data/scripts/yu7_notify/yu7_notify.py`
- 定时规则：`*/5 * * * *` (默认每5分钟执行一次)

![img](/img/ql-4.1.png)
![img](/img/ql-4.2.png)