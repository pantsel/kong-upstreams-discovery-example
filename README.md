# Backend discovery with upstreams example

This demo showcases how Kong can proxy requests to various backends located in different geographical regions 
by utilizing `upstreams` in combination with the `Request Transformer Advanced` and `Route by Header` plugins.

The configurations for `upstreams` and `plugins` are dynamically applied and managed based on records provided by an `Upstream Registry` service.

## Demo components

1. Kong
2. Upstream Registry service (http://localhost:3000)
3. 3 Echo servers representing EU, US, CH backends

## Important files

1. OAS: `openapi.yaml`
2. Kong Plugins template: `plugins/plugins.json`
3. Workflow: `.github/workflows/promote-api.yaml`

## Workflow

```mermaid
graph TB;
    A[OAS]
    B[Extract mock server url]
    C[Fetch available upstreams]
    D[Generate upstreams definition]
    E[Prepare plugins]
    F["Deck Ops
        --------------
        - openapi2kong
        - merge upstreams
        - add plugins
        - patch
    "]
    G[Validate]
    H[Sync]

    A --> B --> C --> D --> E --> F --> G --> H
```