# Notion Integration for [Docs] Tickets

This directory contains scripts to fetch Notion tickets that start with `[Docs]` from your Notion database, helping you sync documentation tasks with your docs repository.

## 📁 Files

- **`setup_notion_integration.py`** - Setup script that installs dependencies and provides configuration instructions
- **`fetch_notion_docs_tickets.py`** - Main script that fetches [Docs] tickets from Notion
- **`README_notion_integration.md`** - This documentation file

## 🚀 Quick Start

### 1. Run the Setup Script

```bash
python scripts/setup_notion_integration.py
```

This will:
- Install the required `notion-client` package
- Create a `.env` template file
- Show detailed setup instructions

### 2. Set Up Your Notion Integration

Follow the instructions shown by the setup script:

1. **Create a Notion Integration:**
   - Go to [https://www.notion.so/my-integrations](https://www.notion.so/my-integrations)
   - Click "New integration"
   - Give it a name (e.g., "Docs Ticket Fetcher")
   - Select your workspace and click "Submit"
   - Copy the "Internal Integration Token"

2. **Share Your Database:**
   - Go to your Notion database page
   - Click the "..." menu → "Add connections"
   - Select your integration and click "Confirm"

3. **Get Your Database ID:**
   - Copy your database URL: `https://www.notion.so/workspace/DATABASE_ID?v=VIEW_ID`
   - The DATABASE_ID is the 32-character string with dashes

### 3. Configure Credentials

Edit the `.env` file created by the setup script:

```bash
# Uncomment and fill in your actual values
NOTION_TOKEN=secret_your_actual_token_here
NOTION_DATABASE_ID=your_actual_database_id_here
```

### 4. Install dotenv (Optional but Recommended)

```bash
pip install python-dotenv
```

### 5. Fetch Your [Docs] Tickets

```bash
python scripts/fetch_notion_docs_tickets.py
```

## 📊 Output

The script will generate:

1. **Console Output:**
   - Summary of found tickets
   - Status breakdown
   - Ticket details (title, status, assignee, priority, due date)

2. **JSON File:**
   - `notion_docs_tickets_YYYYMMDD_HHMMSS.json`
   - Machine-readable data for further processing

3. **Markdown Summary:**
   - `docs_tickets_summary_YYYYMMDD_HHMMSS.md`
   - Human-readable summary grouped by status

## 🔧 Customization

### Database Properties

The script looks for these common property names in your Notion database:
- **Name/Title** - The ticket title (required)
- **Status** - Ticket status (e.g., "To Do", "In Progress", "Done")
- **Assignee/Assigned** - Person assigned to the ticket
- **Priority** - Ticket priority level
- **Due Date/Due** - When the ticket is due

### Filtering

Currently filters for tickets starting with `[Docs]`. To customize:

1. Edit the filter in `fetch_docs_tickets()` method:
```python
filter={
    "property": "Name",
    "title": {
        "starts_with": "[Your-Prefix]"  # Change this
    }
}
```

2. Or add additional filters:
```python
filter={
    "and": [
        {
            "property": "Name",
            "title": {
                "starts_with": "[Docs]"
            }
        },
        {
            "property": "Status",
            "select": {
                "does_not_equal": "Done"
            }
        }
    ]
}
```

## 🛠️ Troubleshooting

### Common Issues

1. **"Notion token not provided"**
   - Make sure you've set `NOTION_TOKEN` in your `.env` file or environment

2. **"Database ID not provided"**
   - Make sure you've set `NOTION_DATABASE_ID` in your `.env` file or environment

3. **"Error fetching tickets: The integration does not have access"**
   - You need to share your database with the integration (Step 2 above)

4. **"notion-client not installed"**
   - Run: `pip install notion-client`

5. **Empty results**
   - Check that you have tickets starting with `[Docs]`
   - Verify the property names match your database schema

### Testing Connection

Run the setup script again to test your connection:
```bash
python scripts/setup_notion_integration.py
```

### Manual Environment Variables

If you prefer not to use a `.env` file:

```bash
export NOTION_TOKEN="secret_your_token_here"
export NOTION_DATABASE_ID="your_database_id_here"
python scripts/fetch_notion_docs_tickets.py
```

## 🔄 Integration with Documentation Workflow

You can integrate this into your documentation workflow:

1. **Regular Sync:**
   ```bash
   # Add to cron job or GitHub Actions
   python scripts/fetch_notion_docs_tickets.py
   ```

2. **Process Results:**
   ```python
   import json
   
   # Load the generated JSON
   with open('notion_docs_tickets_*.json') as f:
       tickets = json.load(f)
   
   # Process tickets for your workflow
   for ticket in tickets:
       if ticket['status'] == 'In Progress':
           print(f"Working on: {ticket['title']}")
   ```

3. **Auto-create Issues:**
   - Use the ticket data to create GitHub issues
   - Link back to Notion for full context

## 📚 API Reference

The script uses the [Notion API](https://developers.notion.com/) with the [notion-client](https://github.com/ramnes/notion-sdk-py) Python library.

For advanced usage, refer to:
- [Notion API Documentation](https://developers.notion.com/reference)
- [Database Query Filter Reference](https://developers.notion.com/reference/post-database-query-filter) 