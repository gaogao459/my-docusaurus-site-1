---
sidebar_position: 7
title: 步骤 6. 添加聚合器
---

**中文翻译：**

2 分钟

想象一下，如果您的营销团队在一天内添加了多个美国潜在客户，您的销售经理可能会被大量独立的移动通知淹没。通过在您的场景中添加一个聚合器，您可以将所有这些潜在客户组合成一个单一的通知——这让信息更易管理，同时仍确保及时警报。

要添加聚合器：

1  
右键单击过滤器和 Apple iOS 模块之间的点，然后选择 **添加模块**。这将打开一个窗口，显示您可以添加到场景中的应用程序和模块列表。

![](/img/get-started/image_071_252d0e9b.png?format=webp)

2  
在搜索栏中搜索“Tools”，然后从可用模块中选择“Text Aggregator”。

![](/img/get-started/image_065_9eb82ec8.png?format=webp)

或者，您可以在搜索栏中直接输入“Text Aggregator”来更快地找到它。

![](/img/get-started/image_076_1b8b0f42.png)

3  
在 **Tools** 设置中，从 **Source Module** 字段下的下拉列表中选择“Google Sheets - Watch New Rows (1)”。

![](/img/get-started/image_132_fa1be540.png)

4  
切换窗口底部的 **显示高级设置** 开关，以打开更多选项。

![](/img/get-started/image_085_bb4cf1f1.png?format=webp)

5  
在 **行分隔符** 字段中，从下拉列表中选择“新行”。

![](/img/get-started/image_009_4ae8175b.png?format=webp)

6  
在 **文本** 字段中，从 Google Sheets 模块中拖放或点击 (First Name) 和 (Last Name) 的值。

![](/img/get-started/image_002_53f02c03.png?format=webp)

7  
点击 **保存** 以保存聚合器设置。

8  
接下来，您需要更新 Apple iOS “发送推送通知”模块，以使用聚合后的文本。点击 Apple iOS 模块以打开其设置。

![](/img/get-started/image_116_8f6468df.png?format=webp)

9  
在 **正文** 字段中，删除任何现有的映射值，然后拖放或点击 (text) 值。

![](/img/get-started/image_089_01176719.png)

10  
点击 **保存** 以保存更改，并确保通过点击场景构建器工具栏中的 **保存** 图标来保存整个场景。

现在，您的场景中已添加了一个聚合器，它可以将新到达的美国潜在客户组合成一个单一的通知。在下一步，您将测试整个场景。

![](/img/get-started/image_039_7f30e928.png)

**理解聚合器**

聚合器可以将多个数据包组合成一个单一的数据包。没有聚合器时，每个潜在客户都会触发单独的通知。使用聚合器后：

- 多个潜在客户被组合成一个通知
- 销售经理收到一个全面的警报，而不是多个
- 场景使用的操作更少

Make 提供不同类型的聚合器：

- **文本聚合器**：使用分隔符组合文本（本场景中使用的类型）
- **数字聚合器**：执行计算（如求和、平均值、计数）
- **数组聚合器**：将数据分组成结构化的数组

在本场景中，文本聚合器有助于防止通知过多问题，通过发送一个有组织的美国潜在客户列表来实现。
