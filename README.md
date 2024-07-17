# Fused Docs

The Fused documentatiob website: [docs.fused.io](https://docs.fused.io/)

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

# Development

## 1. Spin-up locally

```
npx docusaurus start
```

## 2. Generate notebooks

Run after modifying a notebook. See `docs/basics/tutorials/tutorials.json` to configure notebook autogeneration.

```
python3 utils/convert_ipynb_to_mdx.py
```


## 3. Deploy 


### a. Production site

Create a PR on this repo. Once PRs merge to main, GitHub actions will run to re-deploy the docs site. 

### b. Staging site


Set the following on `docusaurus.config.ts`:
```
  baseUrl: '/fused-docs/', // needed for GitHub pages
  url: "https://fusedio.github.io/",
```

Run `USE_SSH=true npx docusaurus deploy`.
