# Source Extract: `DCSTask.java`

| Attribute | Value |
| --- | --- |
| **Source Repository** | `https://github.com/3tio/3t.tools` |
| **File Path** | `product-suite/data-man-mongodb-ent/src/main/java/t3/tasks/DCSTask.java` |
| **Pinned Revision** | `7ad943c5452` |
| **Extracted At SHA** | `09795bb500bd9eb7aaea21fd2573f2d528fa0cee` |

## Extracted Symbols & Citations

### Symbol: `DCSTask` (javadoc)
**Origin Line (Audited Baseline):** `41`

```java
/**
 * Representation of a DCS task. Created by saving a comparison as a Task in the Data Compare and Sync tab.
 */
```

### Symbol: `execute(boolean)` (method)
**Origin Line (Audited Baseline):** `162`

```java
    public void execute(boolean silent) {
        execute(AppWindow.getInstance().getTabFolderComposite(), silent);
    }
```

### Symbol: `execute(boolean)` (javadoc)
**Origin Line (Audited Baseline):** `156`

```java
    /**
     * Here we don't implement the execute method from the interface. This is the only task that
     * creates new tabs when run so we need tabFolderComposite to determine into which
     * DTabFolder tabs are created.
     */
```
