# Feature Matrix — VisuaLeaf / Schema

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Aggregation Matrix](../aggregation/feature-matrix.md)
- [→ Indexing & Performance Matrix](../indexing-performance/feature-matrix.md)
- [→ Data Transfer Matrix](../data-transfer/feature-matrix.md)
- [→ Shell Matrix](../shell/feature-matrix.md)
- [→ AI Matrix](../ai/feature-matrix.md)
- [→ Governance Matrix](../governance/feature-matrix.md)
- [→ Task Scheduler Matrix](../task-scheduler/feature-matrix.md)

## Source index

- S_SCH: https://visualeaf.com/docs/json-schema
- S_VIS: https://visualeaf.com/docs/schema-designer
- S_FEAT_SCH: https://visualeaf.com/features/schema-validation/
- S_FEAT_VIS: https://visualeaf.com/features/visual-schema/

## Capability matrix

### Schema Validation

| Sub-feature ID | Capability | Status | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| SCHEMA-validation-model | Validation model | confirmed | $jsonSchema-based validation deployed to MongoDB collections; JSON Schema Draft 4 with BSON extensions. | Basic or Professional plan required | confirmed | S_SCH, S_FEAT_SCH |
| SCHEMA-validation-ui | Validation UI workflows | confirmed | Full UI for add, edit, verify, and deploy schema validators to collections. | Basic or Professional plan | confirmed | S_SCH |
| SCHEMA-validation-strictness | Validation action and strictness | unknown/unverified | Warn/error action level and strict/moderate enforcement level not documented in VisuaLeaf docs. | — | unknown/unverified | S_SCH |
| SCHEMA-stats-notes | Schema library and live validators | confirmed | Two-tab manager: Saved Schemas tab = local schema library with folder hierarchy, search, sort, drag-and-drop reordering. MongoDB Schemas tab = view and edit validators configured on live MongoDB collections. | Basic or Professional plan | confirmed | S_SCH |
| SCHEMA-deploy-validator | Deploy validator to collection | confirmed | Push local schema to collection as $jsonSchema validator directly from UI. | — | confirmed | S_SCH |
| SCHEMA-json-editor | Tree-based schema editor | confirmed | Hierarchical expand/collapse; full path display (e.g., user.address.city); drag-to-reorder fields; per-field required toggle; View Mode ↔ Edit Mode toggle; Add Field (top-level or nested); Add Child (nested under object field); Delete field; Duplicate field (clones all constraints). | — | confirmed | S_SCH |
| SCHEMA-bson-types | Supported BSON types | confirmed | string, number (generic), int (int32), long (int64), double (IEEE 754), decimal (Decimal128), bool, object (nested with properties/additionalProperties), array (with items schema), date, objectId, binData, null, regex, timestamp. Polymorphic fields: multiple BSON types per field (e.g., string \| null). | — | confirmed | S_SCH |
| SCHEMA-field-constraints | Field constraints by type | confirmed | String: minLength, maxLength, pattern (regex), enum, description. Number/int/long/double/decimal: minimum, maximum, multipleOf, exclusiveMinimum, exclusiveMaximum. Array: minItems, maxItems, uniqueItems, items schema. Object: required fields list, properties (per-property schema), additionalProperties (allow/deny extra fields). | — | confirmed | S_SCH |
| SCHEMA-verify | Schema verification against collection | confirmed | Runs $jsonSchema filter on collection; opens new Collection Activity tab showing all non-matching documents. | — | confirmed | S_SCH |
| SCHEMA-import-from-db | Import schema from database | confirmed | Analyzes 100-document sample; auto-detects BSON types, nested objects, and arrays to generate schema. | — | confirmed | S_SCH |
| SCHEMA-file-export | Export schema as file | confirmed | Exports $jsonSchema-compatible JSON; follows JSON Schema Draft 4 with BSON extensions. | — | confirmed | S_SCH |

### Visual Schema Designer

| Sub-feature ID | Capability | Status | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| SCHEMA-designer-canvas | Designer canvas | confirmed | Infinite canvas; free drag positioning of collections; zoom in/out and pan; auto-arrange instant layout; multi-select multiple collections simultaneously. Requires Basic or Professional plan. | Basic or Professional plan | confirmed | S_VIS, S_FEAT_VIS |
| SCHEMA-designer-auto | Auto-generate diagram from database | confirmed | Analyzes all existing collections and generates full diagram automatically. | — | confirmed | S_VIS |
| SCHEMA-designer-links | Relationship detection and management | confirmed | Graph-theory-based algorithm detects collection relationships. Find Links: auto-detect and create relationship lines to/from a selected collection. Remove Links: all relationships on canvas. Remove Links: per-collection. Multi-selection: bulk find links, bulk remove links for all selected collections. | — | confirmed | S_VIS |
| SCHEMA-designer-color | Color coding | confirmed | 11 color presets; applied via right-click "Change Color" context menu. Multi-selection bulk color change: apply one color to all selected collections at once. | — | confirmed | S_VIS |
| SCHEMA-designer-layouts | Custom layouts | confirmed | Manual arrangement persisted as named custom layout; multi-selection bulk delete from canvas (not from database). | — | confirmed | S_VIS, S_FEAT_VIS |
| SCHEMA-designer-portability | Diagram import/export | confirmed | Export canvas diagram to file (format not specified in docs); import previously exported diagram file. | — | confirmed | S_VIS |
