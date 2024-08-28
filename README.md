# Fused Docs

The Fused documentatiob website: [docs.fused.io](https://docs.fused.io/)

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

# Development

## 1. Spin-up locally

```
npm install
npx docusaurus start
```

## 2. Deploy

Create a PR on this repo.
- Once PRs merge to `main`, GitHub actions will run to re-deploy the docs site to `https://docs.fused.io/`.
- Similarly, merges to `staging` branch deploy to `https://docs-staging.fused.io/`.
