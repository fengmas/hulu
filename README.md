
---

# 🚀 葫芦侠三楼签到自动化脚本 📝

> **💯 自动完成多个板块的签到**
>
> **🗂️ 支持多个账号管理**
>
> **🕗 自动化，省时省力**
>
> **❇️ 通过邮件推送签到结果**

###### **最后更新日期：2025年3月30日 12点00分**

### 配置步骤 🛠️

1. **克隆本项目**：
   - 点击右上角`Fork`按钮，将本项目Fork到你的仓库。
   - 或者直接克隆到本地：
     ```bash
     git clone https://github.com/ilhmtfmlt2/huluxia_thirdfloor_signin.git
     cd huluxia_thirdfloor_signin
     ```

2. **配置账号信息**：
   - 将账号信息通过环境变量进行配置，每个账号的格式为`账号:密码`，多个账号之间用逗号 `,` 隔开。例如：
     ```bash
     export HULUXIA_ACCOUNTS="账号1:密码1,账号2:密码2,账号3:密码3"
     ```
   - 在 Windows 系统下，使用以下命令进行配置：
     ```bash
     set HULUXIA_ACCOUNTS=账号1:密码1,账号2:密码2,账号3:密码3
     ```

3. **配置邮箱推送**：
   - 在 `config.json` 文件中，配置邮箱推送设置。确保你能收到签到结果的邮件通知。示例配置如下：
     ```json
     {
       "email": {
         "smtp_server": "smtp.qq.com",
         "port": 465,
         "sender_email": "********@qq.com",
         "password": "**************",
         "receiver_email": "********@qq.com"
       }
     }
     ```
   - 请记得将 `********@qq.com` 和 `**************` 替换为你的邮箱地址和密码。

4. **运行脚本**：
   - 配置完成后，运行脚本开始自动签到：
     ```bash
     python3 huluxia_signin.py
     ```
   - 脚本将会为你自动进行签到，并在完成后将结果通过邮件发送到你指定的邮箱！📬

### 消息推送方式 📢

1. **邮箱推送**：
   - 邮箱推送功能将在 `config.json` 文件中配置。你需要提供邮箱的 SMTP 服务器信息以及发送和接收邮件的账户。
   - 配置完成后，每次签到都会通过邮件推送签到状态，确保你能够及时查看签到结果。

2. **不推送**：
   - 如果你不希望接收签到结果的邮件，可以选择关闭邮件推送功能，方法是将配置中的相关邮件设置注释掉或删除。

### 常见问题解答 💬

#### Q1: 如何设置多个账号？
你可以通过环境变量配置多个账号，格式为：
```bash
export HULUXIA_ACCOUNTS="账号1:密码1,账号2:密码2,账号3:密码3"
```

#### Q2: 邮箱推送配置不成功怎么办？
请确保你在 `config.json` 文件中正确配置了邮箱服务器、端口、发送者和接收者邮箱。如果你使用的是 QQ 邮箱，记得开启 "SMTP 服务" 并获取授权码作为密码。

#### Q3: 如何保证脚本每天都能运行？
你可以将该脚本设置为定时任务，确保它在每天的固定时间自动签到。具体设置方法取决于你的操作系统，可以使用 cron 或任务计划来实现。

### 使用声明 ⚠️

本项目仅供学习和交流使用，请勿用于任何商业用途。使用者需自行承担因使用本项目而产生的任何风险和责任。

[![Star History Chart](https://api.star-history.com/svg?repos=ilhmtfmlt2/huluxia_thirdfloor_signin&type=Date)](https://star-history.com/#ilhmtfmlt2/huluxia_thirdfloor_signin&Date)

---

感谢你的使用！如果有任何问题或建议，欢迎在 [GitHub Issues](https://github.com/ilhmtfmlt2/huluxia_thirdfloor_signin/issues) 中提问，我们会尽快处理！💬

---
