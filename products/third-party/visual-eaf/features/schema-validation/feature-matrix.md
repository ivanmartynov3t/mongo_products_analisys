# VisuaLeaf — Schema Validation Feature Matrix

| ID | Capability | Status | Detail | Source |
|---|---|---|---|---|
| SCH-001 | Two-tab manager: Saved Schemas | **confirmed** | Local library with folder hierarchy, search, sort, drag-and-drop reordering | https://visualeaf.com/docs/json-schema |
| SCH-002 | Two-tab manager: MongoDB Schemas | **confirmed** | View and edit validators configured on live MongoDB collections | https://visualeaf.com/docs/json-schema |
| SCH-003 | Deploy schema validator to collection | **confirmed** | Push local schema to collection as $jsonSchema validator directly from UI | https://visualeaf.com/docs/json-schema |
| SCH-004 | Tree-based editor: hierarchical view | **confirmed** | Expand/collapse nested fields; full path display (e.g., user.address.city) | https://visualeaf.com/docs/json-schema |
| SCH-005 | Tree editor: drag to reorder fields | **confirmed** | Drag-and-drop reordering of fields within schema tree | https://visualeaf.com/docs/json-schema |
| SCH-006 | Required field checkbox per field | **confirmed** | Per-field required toggle directly in tree editor | https://visualeaf.com/docs/json-schema |
| SCH-007 | View Mode ↔ Edit Mode toggle | **confirmed** | Switch between read-only view and full edit mode | https://visualeaf.com/docs/json-schema |
| SCH-008 | Field operation: Add Field | **confirmed** | Add a new top-level or nested field to the schema | https://visualeaf.com/docs/json-schema |
| SCH-009 | Field operation: Add Child | **confirmed** | Add nested child field under an object field | https://visualeaf.com/docs/json-schema |
| SCH-010 | Field operation: Delete | **confirmed** | Remove a field from the schema | https://visualeaf.com/docs/json-schema |
| SCH-011 | Field operation: Duplicate | **confirmed** | Clone an existing field definition including all constraints | https://visualeaf.com/docs/json-schema |
| SCH-012 | BSON type: string | **confirmed** | Constraints: minLength, maxLength, pattern (regex), enum, description | https://visualeaf.com/docs/json-schema |
| SCH-013 | BSON type: number | **confirmed** | Constraints: minimum, maximum, multipleOf, exclusiveMinimum, exclusiveMaximum | https://visualeaf.com/docs/json-schema |
| SCH-014 | BSON type: int | **confirmed** | 32-bit integer (int32) | https://visualeaf.com/docs/json-schema |
| SCH-015 | BSON type: long | **confirmed** | 64-bit integer (int64) | https://visualeaf.com/docs/json-schema |
| SCH-016 | BSON type: double | **confirmed** | 64-bit IEEE 754 floating point | https://visualeaf.com/docs/json-schema |
| SCH-017 | BSON type: decimal (Decimal128) | **confirmed** | High-precision decimal; maps to BSON Decimal128 | https://visualeaf.com/docs/json-schema |
| SCH-018 | BSON type: bool | **confirmed** | Boolean true/false | https://visualeaf.com/docs/json-schema |
| SCH-019 | BSON type: object | **confirmed** | Nested object with properties schema and additionalProperties support | https://visualeaf.com/docs/json-schema |
| SCH-020 | BSON type: array | **confirmed** | Array with minItems, maxItems, uniqueItems, items schema | https://visualeaf.com/docs/json-schema |
| SCH-021 | BSON type: date | **confirmed** | BSON Date type | https://visualeaf.com/docs/json-schema |
| SCH-022 | BSON type: objectId | **confirmed** | BSON ObjectId type | https://visualeaf.com/docs/json-schema |
| SCH-023 | BSON type: binData | **confirmed** | BSON Binary data type | https://visualeaf.com/docs/json-schema |
| SCH-024 | BSON type: null | **confirmed** | Null type | https://visualeaf.com/docs/json-schema |
| SCH-025 | BSON type: regex | **confirmed** | BSON regular expression type | https://visualeaf.com/docs/json-schema |
| SCH-026 | BSON type: timestamp | **confirmed** | BSON Timestamp (internal MongoDB type) | https://visualeaf.com/docs/json-schema |
| SCH-027 | Polymorphic fields (multiple types) | **confirmed** | Multiple BSON types selectable per field (e.g., string \| null) | https://visualeaf.com/docs/json-schema |
| SCH-028 | String constraint: minLength | **confirmed** | Minimum string length (integer) | https://visualeaf.com/docs/json-schema |
| SCH-029 | String constraint: maxLength | **confirmed** | Maximum string length (integer) | https://visualeaf.com/docs/json-schema |
| SCH-030 | String constraint: pattern (regex) | **confirmed** | Regular expression pattern validation | https://visualeaf.com/docs/json-schema |
| SCH-031 | String constraint: enum | **confirmed** | Allowed string values list | https://visualeaf.com/docs/json-schema |
| SCH-032 | String constraint: description | **confirmed** | Field documentation string | https://visualeaf.com/docs/json-schema |
| SCH-033 | Number constraint: minimum / maximum | **confirmed** | Inclusive min/max boundaries | https://visualeaf.com/docs/json-schema |
| SCH-034 | Number constraint: multipleOf | **confirmed** | Value must be a multiple of this number | https://visualeaf.com/docs/json-schema |
| SCH-035 | Number constraint: exclusiveMinimum / exclusiveMaximum | **confirmed** | Strict (exclusive) min/max boundaries | https://visualeaf.com/docs/json-schema |
| SCH-036 | Array constraint: minItems | **confirmed** | Minimum number of array elements | https://visualeaf.com/docs/json-schema |
| SCH-037 | Array constraint: maxItems | **confirmed** | Maximum number of array elements | https://visualeaf.com/docs/json-schema |
| SCH-038 | Array constraint: uniqueItems | **confirmed** | Enforce unique elements within array | https://visualeaf.com/docs/json-schema |
| SCH-039 | Array constraint: items schema | **confirmed** | Schema definition applied to each array element | https://visualeaf.com/docs/json-schema |
| SCH-040 | Object constraint: required fields | **confirmed** | Required field list for nested object | https://visualeaf.com/docs/json-schema |
| SCH-041 | Object constraint: properties | **confirmed** | Per-property schema definitions | https://visualeaf.com/docs/json-schema |
| SCH-042 | Object constraint: additionalProperties | **confirmed** | Allow or deny extra fields beyond defined properties | https://visualeaf.com/docs/json-schema |
| SCH-043 | Schema Verification against collection | **confirmed** | Runs $jsonSchema filter; opens new Collection Activity tab with all non-matching documents | https://visualeaf.com/docs/json-schema |
| SCH-044 | Import Schema from Database | **confirmed** | Analyzes 100-document sample; auto-detects BSON types, nested objects/arrays | https://visualeaf.com/docs/json-schema |
| SCH-045 | Export schema as .json | **confirmed** | Exports $jsonSchema-compatible JSON; follows JSON Schema Draft 4 with BSON extensions | https://visualeaf.com/docs/json-schema |
| SCH-046 | Plan requirement | **confirmed** | Schema Validation requires Basic or Professional plan | https://visualeaf.com/features/schema-validation/ |

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Aggregation Matrix](../aggregation/feature-matrix.md)
- [→ Indexing & Performance Matrix](../indexing-performance/feature-matrix.md)
- [→ Data Import/Export Matrix](../data-import-export/feature-matrix.md)
- [→ Visual Schema Matrix](../visual-schema/feature-matrix.md)
- [→ Shell Matrix](../shell/feature-matrix.md)
- [→ AI Assistant Matrix](../ai-assistant/feature-matrix.md)
- [→ Security & Governance Matrix](../security-governance/feature-matrix.md)
