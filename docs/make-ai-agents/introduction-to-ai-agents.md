---
title: "Introduction to AI agents"
---

# Introduction to AI agents

An AI agent is an autonomous system that acts to achieve its goals while following certain rules and conditions. Think of it like a skilled assistant who performs tasks for you after understanding what you want to do.

Make AI agents consist of a few fundamental components that you can think of as a brain (LLM), instructions (system prompt), memory (context), and tools (scenarios):

* A Large Language Model (LLM) acts as the agent's brain, powering its reasoning for decision-making.
* The system prompt instructs the agent on how to behave. Like a job description, it defines its role, limitations, and processes.
* Context, or files stored in the agent's long-term memory, provides extra information that helps the agent tailor its responses to your needs. For example, an internal knowledge base or company policies.
* Tools provide the agent with the capabilities to do its job. The agent runs tools for you to complete your requested tasks. In Make, the agent's tools are scenarios. Scenarios used as tools for agents must be scheduled on demand or triggered by a Custom webhook.

The agent uses scenario names and descriptions to know which scenario to use to achieve a goal. It uses scenario input and output names and descriptions to understand the data it receives or sends back to you.

In the next section, you will explore these concepts in more detail.

**Note:** The Make AI agent's reasoning is transparent and easy to review. However, LLMs are still evolving, which could impact agent outcomes. Always check outputs to ensure their accuracy and reliability.