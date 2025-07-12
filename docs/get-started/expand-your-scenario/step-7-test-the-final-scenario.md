---
sidebar_position: 8
title: 步骤 7. 测试最终场景
---

**2 分钟**

现在您已经将聚合器添加到您的场景中，是时候测试完整的场景，以确保一切按预期运行。

1

转到您的潜在客户电子表格，并添加三行或更多新行：

- 至少两行，其中国家/地区设置为 USA
- 一行设置为其他国家/地区

![](/img/get-started/image_136_79f026aa.png)

2

在场景构建器工具栏中，点击**运行一次**按钮。

![](/img/get-started/image_028_3dc8ce58.png)

默认情况下，“监视新行”模块只会检测自上次运行场景以来添加的新行。要重新处理所有行：

- 右键点击 Google Sheets 模块
- 选择**选择起始位置**
- 选择“All”并点击**保存**

3

检查每个模块上方的操作气泡，以查看结果。气泡中显示的数字表示执行了多少操作。

![](/img/get-started/image_088_ee68f0e7.png)

4

点击气泡查看详细信息。

Google Sheets 模块应显示您添加的所有新潜在客户，具体取决于您设置的限制：

![](/img/get-started/image_021_7a881be5.png?format=webp)

Slack 模块应接收并处理所有潜在客户：

![](/img/get-started/image_123_ac049450.png?format=webp)

过滤器应仅允许 USA 潜在客户通过：

![](/img/get-started/image_112_da1a7ec2.png)

文本聚合器应将 USA 潜在客户合并成一个单一的捆绑包：

![](/img/get-started/image_144_b60b20d4.png)

Apple iOS 模块应仅处理这个单一的聚合捆绑包：

![](/img/get-started/image_081_45abb03a.png)

5

检查您的 Slack 频道，以确认所有通知已成功到达。

![](/img/get-started/image_067_d00acffb.png)

6

检查您的移动设备，以确认您只收到一个包含所有美国潜在客户的通知。

![](/img/get-started/image_163_a9575c74.png)

现在，您已经创建了一个场景，该场景可以：

- 监视 Google Sheets 中的新潜在客户
- 将所有潜在客户发送到 Slack 频道
- 仅将基于美国的潜在客户发送到销售经理的移动设备
- 将多个美国潜在客户合并成一个单一的移动通知

![](/img/get-started/image_069_80f54ad4.png)

**下一步是什么？**

现在您已经学会了如何使用路由器创建多条路径、使用过滤器进行条件性数据处理，以及使用聚合器组合相关信息，您可以继续扩展您的场景，例如：

- 为其他国家/地区或标准添加更多过滤器
- 整合其他应用，如电子邮件或 CRM 系统
- 探索其他类型的聚合器，以处理不同数据格式
- 学习错误处理程序，以使您的场景更具鲁棒性

要提升您的 Make 知识，请探索我们免费的在线课程，网址为 [Make Academy](https://academy.make.com/ "Make Academy")。
