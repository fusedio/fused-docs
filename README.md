# Fused Docs

The Fused documentation website: [docs.fused.io](https://docs.fused.io/)

This website is built using [Docusaurus](https://docusaurus.io/), a modern static website generator.

# Development

## 1. Spin-up locally

```
npm install
npm run start
```

## 2. Deploy

Create a PR on this repo.

- Once PRs merge to `main`, GitHub actions will run to re-deploy the docs site to `https://docs.fused.io/`.
- PRs automatically create a preview build at `https://docs-staging.fused.io/`.