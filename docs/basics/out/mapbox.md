# Mapbox (React)

Embed responsive maps into your Notion pages to significantly enhance the utility and interactivity of your documentation, project plans, internal apps, or any other type of content you manage within Notion.

![alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/a_notion.png)

To render a map into a Notion page you'll embed an HTML map that you can host on AWS S3.

## Step 1. Generate a signed URL for a UDF

First, on Workbench, create and save a UDF that successfully renders in `Tile` mode. Under the "Settings" tab, click "Share" to [generate a signed URL](/basics/core-concepts/#generate-endpoints-with-workbench) that enables running the specific URL via HTTP requests. Copy the generated `HTTP` URL which you will use in the next step.

![Alt text](https://fused-magic.s3.us-west-2.amazonaws.com/docs_assets/snippets_share.png)


## Step 2. Create a Leaflet HTML map

On your local system, create a `.html` file following the template below.
