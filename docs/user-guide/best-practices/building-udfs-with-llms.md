# Building UDFs with LLMs

> Speed up your UDF development using LLMs such as Claude!

This guide will help you use LLMs to help you build custom User Defined Functions (UDFs) for Fused. We'll be focusing on Claude for this tutorial, but you can do this with any frontier LLM.

## Preparing the documentation

Before starting, gather the necessary documentation to help the LLM understand Fused UDFs:

1. Visit [https://docs.fused.io/llms.txt](https://docs.fused.io/llms.txt) and copy the full documentation text
2. Download the [common utilities](https://github.com/fusedio/udfs/blob/main/public/common/utils.py) and add it as a context which contains helpful functions for UDF development
3. Add the [UDF Best Practices](https://docs.fused.io/user-guide/best-practices/udf-best-practices/) guide for important patterns and recommendations
4. Paste these documents into your conversation with the LLM

### Adding documentation in Cursor IDE

Alternatively, you can add the documentation directly in Cursor IDE:

1. Click on "Add new doc" in Cursor Settings
2. Paste the documentation link: [https://docs.fused.io/](https://docs.fused.io/)
3. The IDE will automatically fetch and index the documentation

![Adding documentation in Cursor IDE](/img/user-guide/building-with-llm/building_with_llm.png)

## Alternatively: Install the fused-mcp server

For a more integrated experience, you can set up the [fused-mcp server](https://github.com/fusedio/fused-mcp) which allows LLMs like Claude to make HTTP requests and connect directly to APIs and executable code. This repository provides:

* A simple step-by-step notebook workflow to set up MCP Servers with Claude's Desktop App
* Python-based implementation built on top of Fused UDFs
* Direct integration with your desktop Claude app
* Ability to pass Python code directly to Claude

The fused-mcp server can be used in several ways:
* Integrated directly with the Claude Desktop App
* Installed with other MCP clients
* Used with the [Fused AI Builder](https://docs.fused.io/blog/announcing-fused-ai-builder/) for a more streamlined development experience

This approach can provide a more seamless development experience by giving the LLM direct access to documentation and code execution capabilities.

## Describing your UDF

Once you've provided the documentation, clearly describe to the LLM what kind of UDF you want to build. Be specific about:

* What data sources you'll be working with
* What transformations or analysis you need to perform
* What output format you require
* Any specific performance requirements

Before starting, you can explore existing UDFs for inspiration:
* Browse the [public UDFs repository](https://github.com/fusedio/udfs/tree/main/public) to see real-world examples
* Use the [list_public_udfs](https://github.com/fusedio/fused-mcp/tree/main/udfs/list_public_udfs) tool within fused-mcp to explore and analyze existing UDFs

For example:

```
Build a UDF that:
- Reads satellite imagery from a specific region
- Performs NDVI analysis on the imagery
- Returns the results as a GeoJSON with vegetation indices
- Optimizes for large-scale processing
```



