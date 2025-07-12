---
title: "Manage AI agents"
---

# Manage AI agents

# Title: Manage AI agents -

When you create multiple AI agents, managing them through scenario modules could become quite a challenge. To make managing AI agents easier, we added a new tab to the Make platform navigation called **AI Agents**.

The**AI Agents** tab shows you the list of AI agents that available in your team.

AI agents are shared across all team members, like connections. If you want to have a private agent, use a team where you are the only member.

In the **AI Agents** tab, you can:

*   C reate and duplicate agents

*   C onfigure agents

*   D elete agents

Create agents
-------------------------------------------------------------

To create a new AI agent, click the button **Create agent** in the top right corner. A **Create agent** pop-up appears:

1

In the **Connection**, select your AI service provider connection or click **Add**. **Create a connection** pop-up appears.

1.   In the **Connection type** drop-down, select your AI service provider.

2.   Fill in the rest of the form according to the documentation for creating a connection to the AI service provider. Check the list of .

3.   Click **Save** to finish creating the connection.

2

In the **Agent name** field, specify name for the agent.

3

In the **Model** field, select the AI service model that the agent should use for reasoning.

4

In the **System prompt** field, define the agent's purpose and constraints. We recommend providing a short system prompt for the agent and leverage the **Additional system instructions** to customize the agent for a specific scenario.

We recommend starting with a short system prompt and checking your resource (token) usage in your AI service provider.

If your agent is using a lot of tools or is processing long descriptions your AI service usage might increase.

5

Click **Save** to confirm agent settings.

Next, to add the agent's tools and context, click **Configure**on the right-hand side of your agent in the**Make AI Agents** tab:

1

In **Context**, click **Add**to upload files that the agent can use.

**Context**lets you add external information that improves the agent's knowledge base, helping it to properly achieve its goal. Examples include internal knowledge bases or reference tables. The files in **Context**are stored in a database and enable long-term AI memory.

Current limitations for uploading in **Context**:

*   TXT, PDF, DOCX, CSV, and JSON files

*   20 MB maximum per file

*   50 files maximum per team

*   100 files maximum per organization

*   20 files maximum per AI agent

2

In **System tools**, click **Add** to select the scenarios the agent can use.

3

Click **Save**.

You have created an AI agent. You can now use it in a **Run an agent** module, or you can continue configuring it.

Duplicate agents
----------------------------------------------------------------

If you need to create a new agent based on an existing agent, you might create a duplicate of an agent to set up the new agent faster. To create a copy of an agent, click the three dots next to the **Configure** button and select **Duplicate**.

Configure agents
----------------------------------------------------------------

When using AI agents, you might need to adapt them to your processes or update them to improve their efficiency. To configure an agent, go to the **AI Agents**tab and click **Configure**. Alternatively, you can click the **Configuration** link in the **Run an agent** module settings:

Options for configuring or reconfiguring your agent:

*   U pdate agent's system prompt in **System prompt**

*   Add background information or data for the agent to use in **Context**

*   Add scenarios the agent can use as its tools in**System tools**

The scenarios you select in the agent's settings are always available to the agent, in addition to scenarios you add in the **Run an agent** module.

Keep in mind that updating agent settings influences all **Run an agent** modules where you use the agent. If you would need to revert changes, you need to put them back manually.

To make further changes to the agent's model, click the **Agent settings** button. The pop-up form allows you to:

*   C hange the name of the agent

*   C hange the language model the agent is using if the AI service has different models

*   I f the AI service supports configuring the model, you can change the model configuration. The configuration options are available based on the agent's language model. Example configuration options:

    *   **Maximum tokens**: The maximum amount of tokens that the agent can generate and send back to the **Run an agent** module.

    *   **Maximum steps**: The maximum number of iterations the agent can run before providing the final reply to your request.

    *   **Maximum history**: The maximum number of messages that the agent adds to its context from the communication thread. This setting influences the agent's context only if you specify the **Thread ID** in the **Run an agent** module settings.

You can't change an agent's AI service provider or agent's connection. If you need to use a different AI service provider or if you need to change agent's connection, you have to create a new agent instead.

Delete agents
-------------------------------------------------------------

To delete an agent, go to the agent settings, click the button with the three dots and select **Delete**.

Deleting an AI agent is irreversible. If you remove an AI agent, all modules that use the agent stop working.