# Feature Report — Studio 3T / Querying

## Navigation

- [Product report](../../product-report.md)
- [Feature matrix](feature-matrix.md)
- [High-level comparison](../../../../../reports/comparisons/high-level-product-comparison.md)

## Scope

This report covers Studio 3T's querying capabilities: the Collection Tab query bar, result views (Table, Tree, JSON), in-place editing, the Visual Query Builder (VQB), Date Tags, IntelliShell, and Query Manager.

## Behavioral walkthrough

Studio 3T provides a layered querying experience designed to serve users ranging from beginners (VQB drag-and-drop) to power users (IntelliShell scripting). The Collection Tab query bar is the default entry point: it accepts raw MongoDB query JSON with BSON extensions, autocomplete, and five query-shaping fields (Query, Projection, Sort, Skip, Limit). A shorthand system allows typing a bare ObjectId hex or UUID string and having it auto-expanded into a properly typed query — a practical convenience for _id lookups.

Result display offers three views: Table View (spreadsheet-style with column reorder, hide, and expand-embedded-field navigation), Tree View (hierarchical JSON tree with in-place editing), and JSON View (raw document display with a full Document JSON Editor). The Table View is especially mature: it supports stepping into arrays and embedded objects through a breadcrumb navigation trail, BSON type coloring, and direct copy-as-CSV or copy-for-Excel exports. In-place editing is available in all three views, and the multi-document update dialog provides an updateMany-equivalent workflow without writing shell code.

The Visual Query Builder deserves specific attention. It operates as a drag-and-drop interface where fields and values from Table View or Tree View cells can be dragged directly into query condition rows. The VQB and the Query Bar stay bidirectionally in sync in real time — any change in one immediately updates the other. The VQB also generates query code (JavaScript, Java, Python, etc.) visible live in the Query Code tab, making it a learning tool for MongoDB query syntax as well as a productivity tool. Array querying is supported through a dedicated "Has array element(s) matching" mode.

Date Tags are a cross-cutting feature unique to Studio 3T. Rather than manually writing ISODate range expressions, users write semantic tags like `#lastcalmonth` or `#last7days` that expand to {$gt, $lt} date ranges at runtime. Tags are supported in every query entry point: Collection Tab, IntelliShell, VQB, Aggregation Editor $match stages, and Export query filters.

IntelliShell is a mongosh-based shell embedded in the IDE. It adds two modes: Shell mode (raw script execution) and Query Assist mode (which intercepts standalone find/aggregate calls and opens them as editable result tabs with Query Code and Visual Explain). This bridges the gap between shell scripting and structured result management. Destructive operation warnings and per-session suppressibility add a safety layer.

## Capability findings

| Capability ID | Finding | Impact |
| --- | --- | --- |
| QRY-001 | Five-field query bar with shorthand expansions and BSON type autocomplete significantly reduces friction for common _id and type-qualified queries. | Faster query construction for daily use patterns. |
| QRY-004 | Table View's embedded-field breadcrumb navigation and array step-in are among the most functional document navigation patterns in any MongoDB GUI. | Critical for working with deeply nested document schemas. |
| QRY-008 | VQB's real-time bidirectional sync with the query bar is a genuine differentiator — no need to choose between visual and code-based query authoring. | Lowers barrier to MongoDB query adoption; maintains parity for power users. |
| QRY-010 | Date Tags across all query entry points reduce boilerplate date math and enable semantic time-range queries without ISODate literal syntax. | High value for time-series and event log use cases. |
| QRY-011 | IntelliShell's Query Assist mode merges shell scripting with structured result tabs — distinct from Compass's shell, which only shows raw output. | Enables iterative find/aggregate development with editable results. |
| QRY-013 | Query Manager organizes queries by type (collection, IntelliShell, SQL, aggregation) in a unified folder structure, including auto-saved history as a separate store. | Reduces lost-query friction in multi-session workflows. |

## Constraints and risks

- Date Tags are Studio 3T–specific syntax and will not execute if a query is copied to a native mongosh session outside the tool.
- VQB sync is bidirectional but operates at the Collection Tab level; complex shell scripts in IntelliShell are not represented in the VQB.
- Shared folder query save requires Pro/Base+ edition — Free users are limited to local file storage.
- IntelliShell Query Assist mode is scoped to standalone find() and aggregation() calls; complex multi-step scripts use Shell mode only.

## Conclusion

Querying is one of Studio 3T's strongest feature areas. The combination of VQB bidirectional sync, Date Tags, IntelliShell's Query Assist mode, and mature Table View navigation makes Studio 3T competitive for a wide range of MongoDB querying workflows from simple document lookup to complex aggregation pipeline development. The key differentiator versus MongoDB Compass is the IntelliShell Query Assist bridge between scripting and structured result management.
