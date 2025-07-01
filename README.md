# [yunmai_weight_extract2json](https://github.com/arthurfsy2/yunmai_weight_extract2json/tree/main)

一个可以自动获取小米YU7交付进度，通过Bark通知给用户的脚本。

PS：本脚本采用Cookie的方式进行获取数据，可能存在Cookie过期的情况，需要手动更新


# Github Action

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

2. 为 GitHub Actions 添加代码提交权限 访问 repo Settings > Actions > General 页面，找到 Workflow permissions 的设置项，将选项配置为 Read and write permissions，支持 CI 将运动数据更新后提交到仓库中。
   **不设置允许的话，会导致 workflows 无法写入文件**
3. 在 repo Settings > Security > Secrets > secrets and variables > Actions > New repository secret > 增加:
   COOKIE、DEVICE_TOKEN、ORDERID、USERID 这4个变量

   ![img](/img/添加变量.png)

4. 以上变量的值获取方法：
使用Reqable等抓包工具，抓取小米汽车微信小程序
查看：https://api.retail.xiaomiev.com/mtop/car-order/order/detail

- ORDERID、USERID的获取：
![img](/img/1.png)

-COOKIE的获取

> 注意：COOKIE变量在粘贴到github action时，首尾要添加`"`符号

![img](/img/2.png)

-DEVICE_TOKEN的获取
IOS下载`Bark`-->服务器-->复制device_token
![img](/img/3.png)

> 在device_token正确的情况下，运行action后，如果ORDERID、USERID、COOKIE任意一个参数存在问题，会发送错误提醒

![img](/img/para_error.jpg)