# 空间站凌日凌月预报信息机器人
从 [https://transit-finder.com](https://transit-finder.com) 爬取中国空间站、国际空间站凌日凌月信息，利用Github Actions定期自动运行并向指定邮箱发送邮件。

## 配置此程序
首先**配置主程序**。按照您的要求，依次修改以下内容。

地理位置设置：`main.py`文件第10、11、12行。（默认为北京大学静园草坪）

预报时间范围：`main.py`文件第13行。（默认为7天）


然后，**配置自动运行**。

点击Settings，在Secrets中新建4个变量，分别为

`HOST`：邮件发件服务器地址。例如`smtp.163.com`

`USERNAME`：发件邮箱用户名。

`PASSWORD`：发件邮箱密码（一般需要申请SMTP服务的专用授权码，即用于登录第三方邮件客户端的专用密码，可在邮箱设置中找到）。

`RECEIVERS`：收件人列表。如有多个收件人，用逗号分隔并用双引号包裹。例如`example@pku.edu.cn`（一个收件人）或者`"example1@163.com, example2@126.com"`（多个收件人）。

设置自动运行时间：修改`.github/workflows/main.yml`文件第5行的cron表达式。默认为北京时间每周日中午12:20。

