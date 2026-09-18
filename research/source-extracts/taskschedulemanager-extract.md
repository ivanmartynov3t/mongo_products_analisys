# Source Extract: `TaskScheduleManager.java`

| Attribute | Value |
| --- | --- |
| **Source Repository** | `https://github.com/3tio/3t.tools` |
| **File Path** | `product-suite/data-man-mongodb-ent/src/main/java/t3/tasks/TaskScheduleManager.java` |
| **Pinned Revision** | `7ad943c5452` |
| **Extracted At SHA** | `09795bb500bd9eb7aaea21fd2573f2d528fa0cee` |

## Extracted Symbols & Citations

### Symbol: `executeTasks` (method_snippet)
**Origin Line (Audited Baseline):** `86`

```java
Display display = AppWindow.getShell().getDisplay();
```

### Symbol: `scheduleLoop` (method_snippet)
**Origin Line (Audited Baseline):** `74`

```java
Instant thisMinute = now.truncatedTo(ChronoUnit.MINUTES);
```
