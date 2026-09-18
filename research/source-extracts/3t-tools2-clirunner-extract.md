# Source Extract: `CliRunner.java`

| Attribute | Value |
| --- | --- |
| **Source Repository** | `https://github.com/3tio/3t.tools` |
| **File Path** | `product-suite/data-man-mongodb-ent/src/main/java/t3/dataman/mongodb/app/cli/CliRunner.java` |
| **Pinned Revision** | `b7970662ba0` |
| **Extracted At SHA** | `b7970662ba02e32ff04f7969854438a9b8c2e800` |

## Extracted Symbols & Citations

### Symbol: `CliRunner` (javadoc)
**Origin Line (Audited Baseline):** `24`

```java
/**
 * Runs the application as a command line client and returns the process exit code.
 * <p>
 * Nothing here creates a Display, a Shell or any part of the application window: this
 * path must be usable from a script and from continuous integration, where a modal
 * dialog would hang forever.
 * <p>
 * The result of an operation is the only thing written to standard output, so that
 * {@code studio3t --exec … | jq} works. Everything else goes to standard error.
 */
```

### Symbol: `run(CliOptions)` (method)
**Origin Line (Audited Baseline):** `43`

```java
    public static int run(CliOptions options) {
        configureLogging(options);

        if (options.error().isPresent()) {
            return reportUsageProblem(options);
        }
        if (options.isHelpRequested()) {
            System.out.println(CliOptions.usage());
            return CliExitCode.SUCCESS.code();
        }

        CliCommand command = options.command().orElse(null);
        if (command == null) {
            System.err.println(CliOptions.usage());
            return CliExitCode.USAGE_ERROR.code();
        }

        try (OperationClient client = createClient(options)) {
            return execute(command, options, client);
        }
        catch (OperationException e) {
            System.err.println(e.getMessage());
            Logger.debug(e, "Command line operation failed");
            return e.exitCode().code();
        }
        catch (RuntimeException e) {
            System.err.println("Unexpected failure: " + e);
            Logger.error(e, "Unexpected failure in command line mode");
            return CliExitCode.OPERATION_ERROR.code();
        }
    }
```
