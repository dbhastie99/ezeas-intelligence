# Cockpit Contract Extract

Source files:

- `metadata/analytics_builder/cockpit_functional_contract.v0_1.json`
- `metadata/analytics_builder/cockpit_data_contract.v0_1.json`
- `metadata/analytics_builder/cockpit_export_contract.v0_1.json`
- `metadata/analytics_builder/cockpit_module_connector_contract.v0_1.json`
- `metadata/analytics_builder/cockpit_runtime_entrypoint_contract.v0_1.json`
- `metadata/analytics_builder/access_control_doctrine.v0_1.json`
- `metadata/analytics_builder/refresh_model_doctrine.v0_1.json`
- `metadata/analytics_builder/standalone_cockpit_architecture_discovery.v0_1.json`

## Covered Contract Areas

- Cockpit functional contract.
- Cockpit data contract.
- Cockpit export and evidence pack contract.
- Module connector contract.
- Runtime entrypoint contract.
- Access-control doctrine.
- Refresh model doctrine.
- Standalone/hybrid cockpit architecture discovery.

The runtime entrypoint contract prefers `analytics.ezeas.com` as a future entrypoint, while the final auth mechanism remains pending cross-platform auth alignment.

## Minerva Use

Minerva may use this extract for future productisation planning and cockpit-related answer baselines. It must not imply that a runtime cockpit, API, UI, route, or production deployment exists in `ezeas-intelligence`.

## Safety Notes

- Refresh/update is not certification.
- Export is not publishing unless a governed publishing workflow says so.
- Access-control doctrine does not create runtime enforcement in this slice.
- Cockpit contracts are productisation source material, not production runtime behavior.
