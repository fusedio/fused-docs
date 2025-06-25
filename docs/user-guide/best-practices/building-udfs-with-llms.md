# Building UDFs with LLMs

> Speed up your UDF development using LLMs

This guide will help you leverage Large Language Models (LLMs) to accelerate your Fused UDF development process.

## Prerequisites

Before you begin, ensure you have:
- Access to an LLM (like ChatGPT, Claude, etc.)
- Basic understanding of Fused UDFs
- An AI code editor (preferably Cursor IDE)

## Setting Up Documentation

To help the LLM understand Fused UDFs, you'll need to provide it with the necessary documentation. You have two options:

### Option 1: Manual Documentation Setup

1. Visit [https://docs.fused.io/llms.txt](https://docs.fused.io/llms.txt) and copy the full documentation text

:::note
`llms.txt` is a standard in development for parsing sites into LLM-friendly formats. Learn more at [llmstxt.org](https://llmstxt.org/).
:::

2. Download the [common utilities](https://github.com/fusedio/udfs/blob/main/public/common/utils.py)
3. Add both documents as context in your LLM conversation

### Option 2: Using Cursor IDE

For a more streamlined experience:

1. Open Cursor IDE
2. Navigate to Settings
3. Click "Add new doc"
4. Enter the documentation URL: [https://docs.fused.io/](https://docs.fused.io/)
5. The IDE will automatically fetch and index the documentation

![Adding documentation in Cursor IDE](/img/user-guide/building-with-llm/building_with_llm.png)

## Advanced Setup: Local Development

For a more integrated development experience, you can set up the [fused-mcp server](https://github.com/fusedio/fused-mcp). This setup enables Claude to:
- Read UDFs 
- Execute UDFs using prompts
- Provide more context 

## Next Steps

Once you've set up your development environment, you can:
1. Start creating new UDFs with LLM assistance
2. Modify existing UDFs
3. Debug and optimize your code



