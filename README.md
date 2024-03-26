# Website

The Fused docs website.

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.


## 1. Generate notebooks

Run after modifying a notebook. See `docs/basics/tutorials/tutorials.json` to configure notebook autogeneration.

```
python3 docs/basics/tutorials/_convert_ipynb_to_mdx.py 
```


## 2. Run scrape for typesense searh

Run locally every time there's a content update to reindex search.

```
docker run -it --env-file=.env -e "CONFIG=$(cat config.json | jq -r tostring)" typesense/docsearch-scraper:0.9.1
```

## 3. Deploy 

### a) To "staging" on GitHub pages

This deploys to [fusedio.github.io/fused-docs](https://fusedio.github.io/fused-docs/) which is a "staging" site.

NOTE: For GitHub pages set in `docusaurus.config.ts`:
```
baseUrl: '/fused-docs/'
url: "https://fusedio.github.io/"
```

```
npx docusaurus deploy   
```

### b) To "production"

NOTE: For prod set in `docusaurus.config.ts`:
```
baseUrl: '/'
url: "https://docs.fused.io"
```

The "production" site is [docs.fused.io](https://docs.fused.io/), and the deploy workflow runs with GitHub Actions on merges to main.
