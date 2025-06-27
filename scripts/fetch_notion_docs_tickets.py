#!/usr/bin/env python3
"""
Script to fetch Notion tickets that start with "[Docs]" from a Notion database.
This helps sync documentation tasks from Notion to the docs repository.
"""

import os
import json
from typing import List, Dict, Any
from notion_client import Client
from datetime import datetime

# Try to load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, will use system environment variables
    pass

class NotionDocsTicketFetcher:
    def __init__(self, notion_token: str = None, database_id: str = None):
        """
        Initialize the Notion client.
        
        Args:
            notion_token: Notion integration token (if not provided, reads from env)
            database_id: Notion database ID (if not provided, reads from env)
        """
        self.notion_token = notion_token or os.getenv('NOTION_TOKEN')
        self.database_id = database_id or os.getenv('NOTION_DATABASE_ID')
        
        if not self.notion_token:
            raise ValueError("Notion token not provided. Set NOTION_TOKEN environment variable or pass as parameter.")
        
        if not self.database_id:
            raise ValueError("Database ID not provided. Set NOTION_DATABASE_ID environment variable or pass as parameter.")
        
        self.client = Client(auth=self.notion_token)
    
    def fetch_docs_tickets(self) -> List[Dict[str, Any]]:
        """
        Fetch all tickets from the Notion database that start with "[Docs]".
        
        Returns:
            List of dictionaries containing ticket information
        """
        try:
            # Query the database with filter for titles starting with "[Docs]"
            response = self.client.databases.query(
                database_id=self.database_id,
                filter={
                    "property": "Name",  # Assuming "Name" is the title property
                    "title": {
                        "starts_with": "[Docs]"
                    }
                },
                sorts=[
                    {
                        "property": "Created time",
                        "direction": "descending"
                    }
                ]
            )
            
            tickets = []
            for page in response["results"]:
                ticket_info = self._extract_ticket_info(page)
                tickets.append(ticket_info)
            
            return tickets
            
        except Exception as e:
            print(f"Error fetching tickets: {str(e)}")
            return []
    
    def _extract_ticket_info(self, page: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract relevant information from a Notion page.
        
        Args:
            page: Notion page object
            
        Returns:
            Dictionary with ticket information
        """
        properties = page.get("properties", {})
        
        # Extract title
        title = ""
        if "Name" in properties and properties["Name"]["type"] == "title":
            title_parts = properties["Name"]["title"]
            title = "".join([part["plain_text"] for part in title_parts])
        
        # Extract status (common property name)
        status = ""
        if "Status" in properties:
            status_prop = properties["Status"]
            if status_prop["type"] == "select" and status_prop["select"]:
                status = status_prop["select"]["name"]
            elif status_prop["type"] == "status" and status_prop["status"]:
                status = status_prop["status"]["name"]
        
        # Extract assignee
        assignee = ""
        if "Assignee" in properties or "Assigned" in properties:
            assignee_prop = properties.get("Assignee") or properties.get("Assigned")
            if assignee_prop and assignee_prop["type"] == "people" and assignee_prop["people"]:
                assignee = assignee_prop["people"][0]["name"]
        
        # Extract priority
        priority = ""
        if "Priority" in properties:
            priority_prop = properties["Priority"]
            if priority_prop["type"] == "select" and priority_prop["select"]:
                priority = priority_prop["select"]["name"]
        
        # Extract due date
        due_date = ""
        if "Due Date" in properties or "Due" in properties:
            due_prop = properties.get("Due Date") or properties.get("Due")
            if due_prop and due_prop["type"] == "date" and due_prop["date"]:
                due_date = due_prop["date"]["start"]
        
        # Extract created time
        created_time = page.get("created_time", "")
        
        # Extract page URL
        page_url = page.get("url", "")
        
        return {
            "title": title,
            "status": status,
            "assignee": assignee,
            "priority": priority,
            "due_date": due_date,
            "created_time": created_time,
            "page_url": page_url,
            "page_id": page.get("id", "")
        }
    
    def save_tickets_to_json(self, tickets: List[Dict[str, Any]], filename: str = None) -> str:
        """
        Save tickets to a JSON file.
        
        Args:
            tickets: List of ticket dictionaries
            filename: Output filename (optional)
            
        Returns:
            Filename of the saved file
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"notion_docs_tickets_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(tickets, f, indent=2, ensure_ascii=False)
        
        return filename
    
    def print_tickets_summary(self, tickets: List[Dict[str, Any]]):
        """
        Print a summary of the fetched tickets.
        
        Args:
            tickets: List of ticket dictionaries
        """
        if not tickets:
            print("No [Docs] tickets found.")
            return
        
        print(f"\n📋 Found {len(tickets)} [Docs] tickets:")
        print("=" * 80)
        
        for i, ticket in enumerate(tickets, 1):
            print(f"\n{i}. {ticket['title']}")
            print(f"   Status: {ticket['status']}")
            if ticket['assignee']:
                print(f"   Assignee: {ticket['assignee']}")
            if ticket['priority']:
                print(f"   Priority: {ticket['priority']}")
            if ticket['due_date']:
                print(f"   Due Date: {ticket['due_date']}")
            print(f"   URL: {ticket['page_url']}")
        
        # Summary by status
        status_counts = {}
        for ticket in tickets:
            status = ticket['status'] or 'No Status'
            status_counts[status] = status_counts.get(status, 0) + 1
        
        print(f"\n📊 Summary by Status:")
        for status, count in status_counts.items():
            print(f"   {status}: {count}")


def main():
    """
    Main function to run the script.
    """
    print("🔍 Fetching [Docs] tickets from Notion...")
    
    try:
        # Initialize the fetcher
        fetcher = NotionDocsTicketFetcher()
        
        # Fetch tickets
        tickets = fetcher.fetch_docs_tickets()
        
        if tickets:
            # Print summary
            fetcher.print_tickets_summary(tickets)
            
            # Save to JSON file
            filename = fetcher.save_tickets_to_json(tickets)
            print(f"\n💾 Tickets saved to: {filename}")
            
            # Optional: Create a markdown summary
            create_markdown_summary(tickets)
            
        else:
            print("No tickets found or error occurred.")
            
    except Exception as e:
        print(f"Error: {str(e)}")
        print("\nMake sure you have:")
        print("1. Set NOTION_TOKEN environment variable")
        print("2. Set NOTION_DATABASE_ID environment variable")
        print("3. Installed notion-client: pip install notion-client")


def create_markdown_summary(tickets: List[Dict[str, Any]]):
    """
    Create a markdown summary of the tickets.
    
    Args:
        tickets: List of ticket dictionaries
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    filename = f"docs_tickets_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# [Docs] Tickets Summary\n\n")
        f.write(f"Generated on: {timestamp}\n")
        f.write(f"Total tickets: {len(tickets)}\n\n")
        
        # Group by status
        status_groups = {}
        for ticket in tickets:
            status = ticket['status'] or 'No Status'
            if status not in status_groups:
                status_groups[status] = []
            status_groups[status].append(ticket)
        
        for status, group_tickets in status_groups.items():
            f.write(f"## {status} ({len(group_tickets)})\n\n")
            
            for ticket in group_tickets:
                f.write(f"### {ticket['title']}\n\n")
                if ticket['assignee']:
                    f.write(f"**Assignee:** {ticket['assignee']}\n\n")
                if ticket['priority']:
                    f.write(f"**Priority:** {ticket['priority']}\n\n")
                if ticket['due_date']:
                    f.write(f"**Due Date:** {ticket['due_date']}\n\n")
                f.write(f"**Notion URL:** [{ticket['title']}]({ticket['page_url']})\n\n")
                f.write("---\n\n")
    
    print(f"📄 Markdown summary saved to: {filename}")


if __name__ == "__main__":
    main() 