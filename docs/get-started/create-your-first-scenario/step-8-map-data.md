---
sidebar_position: 8
title: 步骤 8. 映射数据
---

1 分钟

映射是将数据在模块之间传输的方式。它涉及从一个模块获取信息（输出），并指定 Make 如何在下一个模块中使用这些信息（输入）。

在本场景中，您将从 Google Sheets 获取潜在客户信息（输出），并将其插入到 Slack 消息的特定位置（输入）。

要使用 Google Sheets 中的数据配置您的 Slack 消息：

1

对于 **输入频道 ID 或名称**，选择“从列表中选择”。

2

在 **频道类型** 中，选择“公共频道”。

3

在 **公共频道** 中，从下拉列表中选择“sales-team”。

![](/img/get-started/image_104_a0ef3243.png?format=webp)

4

单击 **文本** 字段，一个映射面板将出现，显示来自 Google Sheets 模块的数据。

![](/img/get-started/image_079_f479167e.png)

5

创建您的通知消息。您可以将以下模板复制并粘贴到 **文本** 字段中，或自行创作消息。

新潜在客户已添加！姓名： 电子邮件： 国家/地区： 电话： 详细信息：

![](/img/get-started/image_023_5c2007f6.png)

6

从 Google Sheets 模块中拖拽并放置值到 **文本** 字段中，或直接单击这些值以将其插入消息。

![](/img/get-started/image_193_842f3eb5.gif)

这就是数据映射的过程——将潜在客户信息从 Google Sheets 提取，并准确放置到 Slack 消息的指定位置。

7

单击 **保存** 以保存模块设置。

8

单击场景构建器工具栏上的 **保存** 图标，以保存整个场景。

![](/img/get-started/image_084_a51e76aa.png?format=webp)

现在，您的场景已包含两个连接的模块：

- Google Sheets “监视新行” 用于检测新潜在客户
- Slack “创建消息” 用于向团队发送通知

在下一步中，您将测试场景，以确保两个模块能顺利协作。
