## TODO

### Completed
- [x] Create new folder structure
- [x] Create index.mdx files for each section
- [x] Create persona quickstart templates
- [x] Update sidebars.ts with new structure
- [x] Initial content migration (index pages)

### MVP - Phase 2: Content Migration (Simple)
- [x] Move Core Concepts → split between Guide and Reference
- [x] Move Tutorials → Guide sections
- [x] Move Python SDK → `reference/python-sdk/` (full API reference)
- [x] Move Workbench → `reference/workbench/` (UDF Builder, App Builder)
- [x] Consolidate examples into `guide/use-cases/`

### MVP - Phase 3: Sidebar & Links
- [x] Update all internal links in moved files
- [x] Test navigation and check for broken links
- [ ] Make sure blogs link our properly to new pages 

### MVP - Phase 4: Redirects
Recommended approach: **Docusaurus `@docusaurus/plugin-client-redirects`**
- [ ] Install plugin: `npm install @docusaurus/plugin-client-redirects`
- [ ] Create redirect mapping for all moved pages
- [ ] Test redirects work locally before deploy
- [ ] Make sure command in README to generate Python SDK docs still works with new implementation

### MVP Fixing - Deduplicate Guide vs Reference

---

### H3 SEO (after dedup)
- [x] Already have: `h3-resolution-guide.mdx`, `when-to-use-h3.mdx`
- [ ] Add meta descriptions to remaining H3 pages
- [ ] Review page titles for SEO keywords

### Later
- [ ] Set up redirects with `@docusaurus/plugin-client-redirects`
- [ ] Full content migration from legacy sections
- [ ] Make sure no links still pointing to legacy pages before removing 
- [ ] Remove legacy sections once migration complete


### Notes to review -- Don't edit unless asked to specifically 

- [ ] Personnas need manual review -> Not so much focus on local work for now. focus in Workbench. So no focus on `pip install fused` to start. That's advanced concept 
- [ ] H3 section contents are correct? 
- [ ] Order each section properly (i.e. Use Cases not updated in the most useful order right now. Might also need to remove some)
- [ ] Review individual pages before merging
  - [ ] Local Files
  - [ ] Cloud Storage 
  - [ ] Databases 
  - [ ] API & STAC

### Topics I need to keep track of / find a place for

Blocking to make first MVP
- On Prem page
- Realtime / Batch / Submit stay the same for now
- On Prem page needs a place to live 

Improvements in next setup
- QA Tips? 
- Best Practices for working as a team (i.e. Github, Shared Canvas, etc.)
- PM Tiles export? 
- Explaining Canvas concepts 

### Review: Manual Page Checklist

#### Quickstart (Persona Entry Points)
- [x] quickstart/index.mdx
- [ ] quickstart/data-scientist.mdx
- [ ] quickstart/data-engineer.mdx
- [ ] quickstart/data-analyst.mdx

#### Guide  
**Getting Started**
- [ ] guide/getting-started/index.mdx
- [ ] guide/getting-started/your-first-udf.mdx
- [ ] guide/getting-started/two-min-with-fused.mdx

**Loading Data**
- [ ] guide/loading-data/index.mdx
- [ ] guide/loading-data/local-files.mdx
- [ ] guide/loading-data/cloud-storage.mdx
- [ ] guide/loading-data/databases.mdx
- [ ] guide/loading-data/apis.mdx
- [ ] guide/loading-data/gee.mdx
- [ ] guide/loading-data/file-formats.mdx

**Writing Data**
- [ ] guide/writing-data/index.mdx
- [ ] guide/writing-data/to-cloud-storage.mdx
- [ ] guide/writing-data/to-databases.mdx
- [ ] guide/writing-data/ingesting-large-datasets.mdx
- [ ] guide/writing-data/turn-your-data-into-an-api.mdx

**Geospatial Ingestion**
- [x] guide/geospatial-ingestion/index.mdx
- [x] guide/geospatial-ingestion/why-ingestion.mdx
- [x] guide/geospatial-ingestion/ingest-your-data.mdx
- [x] guide/geospatial-ingestion/geospatial-file-formats.mdx

**Running UDFs**
- [ ] guide/running-udfs/index.mdx
- [ ] guide/running-udfs/writing-udfs.mdx
- [ ] guide/running-udfs/realtime.mdx
- [ ] guide/running-udfs/batch-jobs.mdx
- [ ] guide/running-udfs/parallel-processing.mdx
- [ ] guide/running-udfs/http-endpoints.mdx

**H3 Hexagons**
- [ ] guide/h3-hexagons/index.mdx
- [ ] guide/h3-hexagons/when-to-use-h3.mdx
- [ ] guide/h3-hexagons/h3-resolution-guide.mdx
- [ ] guide/h3-hexagons/file-to-h3.mdx
- [ ] guide/h3-hexagons/dynamic-tile-to-h3.mdx
- [ ] guide/h3-hexagons/ingesting-dataset-to-h3.mdx
- [ ] guide/h3-hexagons/aggregating-h3-data.mdx
- [ ] guide/h3-hexagons/joining-h3-datasets.mdx
- [ ] guide/h3-hexagons/h3-zonal-stats.mdx

**Scaling Up**
- [ ] guide/scaling-up/index.mdx
- [ ] guide/scaling-up/cache.mdx
- [ ] guide/scaling-up/async.mdx
- [ ] guide/scaling-up/fused-advanced.mdx
- [ ] guide/scaling-up/engineering_etl.mdx

**Building Apps**
- [ ] guide/building-apps/index.mdx
- [ ] guide/building-apps/interactive-graphs-for-your-data.mdx
- [ ] guide/building-apps/standalone-maps.mdx
- [ ] guide/building-apps/visualization.mdx
- [ ] guide/building-apps/let-anyone-talk-to-your-data.mdx

**Use Cases**
- [ ] guide/use-cases/index.mdx
- [ ] guide/use-cases/stack-overflow-surveys.mdx
- [ ] guide/use-cases/currency-trading-prediction.mdx
- [ ] guide/use-cases/scraping.mdx
- [ ] guide/use-cases/pdf_scraping.mdx
- [ ] guide/use-cases/competitor_analysis.mdx
- [ ] guide/use-cases/vibe-coded-dashboard.mdx
- [ ] guide/use-cases/climate-dashboard.mdx
- [ ] guide/use-cases/dark-vessel-detection.mdx
- [ ] guide/use-cases/zonal-stats.mdx
- [ ] guide/use-cases/exploring_maxar_data.mdx
- **Crop Exploration with H3**
  - [ ] guide/use-cases/Crop Exploration with H3/index.mdx
  - [ ] guide/use-cases/Crop Exploration with H3/exploring_individual_dataset.mdx
  - [ ] guide/use-cases/Crop Exploration with H3/joining_datasets.mdx
  - [ ] guide/use-cases/Crop Exploration with H3/interactive_visualization.mdx
- [x] guide/use-cases/canvas-catalog.mdx

**Content Management**
- [ ] guide/content-management/index.mdx
- [ ] guide/content-management/file-system.mdx
- [ ] guide/content-management/git.mdx
- [ ] guide/content-management/download.mdx
- [ ] guide/content-management/environment-variables.mdx

**Best Practices**
- [ ] guide/best-practices/index.mdx
- [ ] guide/best-practices/udf-best-practices.mdx
- [ ] guide/best-practices/workbench-best-practices.mdx
- [ ] guide/best-practices/build_with_llms.mdx

---

#### Reference  

**Python SDK**
- [ ] reference/python-sdk/index.mdx
- [ ] reference/python-sdk/top-level-functions.mdx
- [ ] reference/python-sdk/authentication.mdx
- [ ] reference/python-sdk/dependencies.mdx
- [ ] reference/python-sdk/batch.mdx
- [ ] reference/python-sdk/changelog.mdx
- **API Reference**
  - [ ] reference/python-sdk/api-reference/api.mdx
  - [ ] reference/python-sdk/api-reference/core.mdx
  - [ ] reference/python-sdk/api-reference/h3.mdx
  - [ ] reference/python-sdk/api-reference/udf.mdx
  - [ ] reference/python-sdk/api-reference/job.mdx
  - [ ] reference/python-sdk/api-reference/jobpool.mdx
  - [ ] reference/python-sdk/api-reference/options.mdx

**H3 Reference**
- [ ] reference/h3/index.mdx
- [ ] reference/h3/conversions.mdx
- [ ] reference/h3/operations.mdx

**UDF Patterns**
- [x] reference/udf-patterns/index.mdx
- [x] reference/udf-patterns/bounds-and-tiles.mdx
- [x] reference/udf-patterns/parallel-processing.mdx
- [x] reference/udf-patterns/caching.mdx
- [x] reference/udf-patterns/http-endpoints.mdx
- [x] reference/udf-patterns/visualization.mdx
- [x] reference/udf-patterns/error-handling.mdx
- [x] reference/udf-patterns/integrations.mdx

**Data Loading**
- [ ] reference/data-loading/index.mdx
- [ ] reference/data-loading/files.mdx
- [ ] reference/data-loading/cloud.mdx
- [ ] reference/data-loading/databases.mdx
- [ ] reference/data-loading/specialized.mdx

**Data Writing**
- [ ] reference/data-writing/index.mdx

**Workbench Reference**
- [ ] reference/workbench/index.mdx
- [ ] reference/workbench/overview.mdx
- [ ] reference/workbench/account.mdx
- [ ] reference/workbench/preferences.mdx
- [ ] reference/workbench/file-explorer.mdx
- [ ] reference/workbench/udf-catalog.mdx
- [ ] reference/workbench/ai-assistant.mdx
- [ ] reference/workbench/free-tier.mdx

- **UDF Builder**
  - [ ] reference/workbench/udf-builder/udf-builder.mdx
  - [ ] reference/workbench/udf-builder/navigation.mdx
  - [ ] reference/workbench/udf-builder/code-editor.mdx
  - [ ] reference/workbench/udf-builder/map.mdx
  - [ ] reference/workbench/udf-builder/results.mdx
  - [ ] reference/workbench/udf-builder/canvas.mdx
  - [ ] reference/workbench/udf-builder/viz-styling.mdx

- **App Builder**
  - [ ] reference/workbench/app-builder/app-builder.mdx
  - [ ] reference/workbench/app-builder/app-overview.mdx
  - [ ] reference/workbench/app-builder/add-a-map.mdx

- [x] faq.mdx
