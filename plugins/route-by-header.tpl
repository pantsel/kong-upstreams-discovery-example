---
_format_version: '3.0'
add-plugins:
- selectors:
  - "$..services[0]"
  overwrite: false
  plugins:
    - name: route-by-header
      config:
        __ROUTE_BY_HEADER_CONFIG__
      enabled: true
    - name: request-transformer-advanced
      ordering:
        before:
          access:
            - route-by-header
      config:
        add:
          headers:
            - location:$(uri_captures.location or query_params.location)
      enabled: true