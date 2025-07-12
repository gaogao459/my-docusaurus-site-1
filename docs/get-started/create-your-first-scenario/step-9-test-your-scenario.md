---
sidebar_position: 9
title: 步骤 9. 测试你的场景
---

1 分钟

为了确保两个模块能够协同工作，您需要测试您的场景。

1

右键点击 Google Sheets 模块，然后选择 **选择起始位置**。

![](/img/get-started/image_074_acd3d251.png?format=webp)

2

选择 "All" 并点击 **保存**。

![](/img/get-started/image_007_55a290ed.png?format=webp)

3

在场景构建器工具栏中，点击 **运行一次** 按钮。

![](/img/get-started/image_103_870f05e5.png)

4

检查每个模块上方的操作气泡，以查看结果。气泡中显示的数字表示已处理的操作为数。

![](/img/get-started/image_097_859789c2.png?format=webp)

5

点击 Google Sheets 模块上方的操作气泡，在输出部分查看所有已处理的行。由于在步骤 2 中选择了 "All"，它会处理您 Google 表格中的所有行（限于您先前设置的 20 行上限）。

点击 Slack 模块上方的操作气泡，以查看：

- 从 Google Sheets 接收到的输入信息。
- 关于它发送的 Slack 消息的输出信息。

![](/img/get-started/image_091_0abbb663.png)

6

转到您的 Slack 频道，检查通知是否正确出现。

![](/img/get-started/image_120_f18e783b.png)

7

将 Slack 消息中的数据与您的 Prospects 电子表格进行比较，确保所有信息都已正确传输。

![](/img/get-started/image_062_d4140765.png)

**理解数据包**

数据包是一种一起传递的数据集合。它可能包含单个信息（如电子邮件地址），或多个数据（如电子表格行）。当您点击操作气泡时，您会看到已处理的数据包：

- **输入数据包**：包含您输入到模块中的信息，以及从先前模块映射的数据。
- **输出数据包**：包含在应用程序中执行的操作结果，以及任何可映射到下一个模块生成的数据。
- 每个处理的数据包都会为动作模块（如您的 Slack 模块）计为一个操作。
- 触发模块（如您的 Google Sheets 模块）即使输出多个数据包，也仅使用一个操作。

例如，如果您的 Google 表格有 3 行，并且您选择了 "All"，则 Google Sheets 模块会生成 3 个输出数据包，但仅使用 1 个操作，因为它是一个触发模块。这些数据包会成为 Slack 模块的输入数据包，Slack 模块会处理它们并发送 3 条消息。因此，Slack 模块会使用 3 个操作，因为它处理了三个输入数据包。
