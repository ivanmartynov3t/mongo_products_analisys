# Feature Matrix — VisuaLeaf / Shell

## Navigation

- [← Product Report](../../product-report.md)
- [Feature Report](feature-report.md)
- [← Data Transfer Matrix](../data-transfer/feature-matrix.md)
- [→ AI Matrix](../ai/feature-matrix.md)
- [→ Governance Matrix](../governance/feature-matrix.md)

## Source index

- S1: https://visualeaf.com/docs/mongodb-shell

## Capability matrix

| Sub-feature ID | Capability | Status | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources |
| --- | --- | --- | --- | --- | --- | --- |
| SHELL-engine | Monaco editor engine | confirmed | Same editor engine as VS Code; full JavaScript/MongoDB syntax highlighting. | — | confirmed | S1 |
| SHELL-minimap | Monaco minimap | confirmed | Code minimap panel for navigation in large scripts. | — | confirmed | S1 |
| SHELL-autocomplete | Autocomplete | confirmed | db. triggers collection list + db-level methods. db.collection. triggers find(), aggregate(), insertOne(), etc. Field names suggested within query contexts derived from collection schema. | — | confirmed | S1 |
| SHELL-validation | Syntax validation and error highlighting | confirmed | Real-time syntax error highlighting as user types; on execution failure, the error line is highlighted in red. | — | confirmed | S1 |
| SHELL-run-all | Run All (F5) | confirmed | Executes all scripts top-to-bottom; auto-splits into sequential commands. Currently executing line highlighted; progress shown as "Running script X of Y"; editor read-only during execution; execution halts on error and problematic line highlighted in red. | — | confirmed | S1 |
| SHELL-run-select | Run Selected (Ctrl+F5) | confirmed | Executes only the highlighted/selected text. | — | confirmed | S1 |
| SHELL-run-cursor | Run to Line (Ctrl+Shift+F5) | confirmed | Executes from start of script to the cursor line. | — | confirmed | S1 |
| SHELL-result-tabs | Result tabs | confirmed | Shell Output tab: dedicated for print()/printjson() output, execution logs, and error messages. Per-query result tabs: each query returning data opens a separate tab (Result 1, Result 2, …). | — | confirmed | S1 |
| SHELL-result-views | Result tab view modes | confirmed | Tree View, Table View, BSON View with pagination in each result tab. | — | confirmed | S1 |
| SHELL-save-load | Script save, load, and export | confirmed | Save current script; Save As under new name; Load previously saved script; Export as .json; Export as .js (portable to mongosh and MongoDB Compass); Import script from external file. | — | confirmed | S1 |
| SHELL-history | Query history | confirmed | Auto-saved history with search, filter, and preview capability. | — | confirmed | S1 |
| SHELL-sessions-vars | Persistent variable scope | confirmed | Variables persist across executions within the same session tab. | — | confirmed | S1 |
| SHELL-sessions-multi | Multiple shell sessions | confirmed | Multiple independent sessions via multiple Shell activity tabs. | — | confirmed | S1 |
| SHELL-reconnect | Auto-reconnect | confirmed | Automatically reconnects on network interruption. | — | confirmed | S1 |
| SHELL-background | Background execution | confirmed | Script execution continues when user switches to other activity tabs. | — | confirmed | S1 |
