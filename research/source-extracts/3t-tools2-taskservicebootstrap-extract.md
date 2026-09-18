# Source Extract: `TaskServiceBootstrap.java`

| Attribute | Value |
| --- | --- |
| **Source Repository** | `https://github.com/3tio/3t.tools` |
| **File Path** | `product-suite/data-man-mongodb-ent/src/main/java/t3/taskservice/server/TaskServiceBootstrap.java` |
| **Pinned Revision** | `b7970662ba0` |
| **Extracted At SHA** | `b7970662ba02e32ff04f7969854438a9b8c2e800` |

## Extracted Symbols & Citations

### Symbol: `TaskServiceBootstrap` (javadoc)
**Origin Line (Audited Baseline):** `24`

```java
/**
 * Starts and stops the task service: its own Jetty server, on its own port, speaking plain
 * HTTP and JSON.
 * <p>
 * It shares three things with the MCP server and nothing else. It reuses the same host
 * allow list file and the same filter class, so one security-relevant list on disk governs
 * both listeners rather than two that can drift apart. It reuses the tool implementations,
 * reached by a direct in-process call. And it runs in the same process. The MCP server's
 * connector, context, session handling and protocol are untouched.
 * <p>
 * The tool service here is constructed rather than shared, which is the point: cancelling
 * a queued job interrupts every active thread on its tool service instance, so sharing the
 * AI Helper's would let a queued job's cancellation kill the user's in-flight work.
 */
```
