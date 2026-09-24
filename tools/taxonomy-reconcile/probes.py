#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# ///
"""
Definition probes used as evidence for the taxonomy reconciliation (issue #15).

OUR_EXTRAS     one probe per dictionary ID that the silo did not have (76; PROP-* excluded)
DEAD_SILO_IDS  one looser probe per silo ID whose own pattern matched 0 documents (65)

These are hand-written approximations of each definition, not the silo classifier.
Use them to gather evidence for a decision; acceptance of a silo change must use the
silo's own catalog output (see reconcile.py).

Usage:
    uv run tools/taxonomy-reconcile/probes.py [--silo ../prod_info_silo] [ID ...]
Prints, per probe: matching documents, distinct snippets, products; writes 8 random
sample snippets per probe to probe-samples.txt in the current directory.
"""

import argparse
import os
import random
import re
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

OUR_EXTRAS = {
    'AI-001': r'\b(azure\s+openai|anthropic|openai)\b.{0,80}\b(provider|backend)',
    'AI-002': r'\bAI\b.{0,40}\b(temperature|enable\s+AI|disable\s+AI)',
    'AI-003': r'\b(natural\s+language)\b.{0,60}\b(query|pipeline|script|aggregation)',
    'AI-004': r'\b(apply|insert|copy)\b.{0,30}\b(generated|AI)\b.{0,30}\b(query|result|code|editor)',
    'AI-005': r'\b(AI|chat)\s+(session\s+)?history\b',
    'AI-006': r'\bAI\b.{0,40}\b(keyboard\s+shortcut|hotkey)',
    'AI-007': r'\b(local\s+)?MCP\s+server\b',
    'AI-008': r'\bMCP\s+tools?\b',
    'AI-009': r'\b(claude\s+desktop|cursor|windsurf|vs\s*code|copilot)\b.{0,60}\bMCP\b|\bMCP\s+client',
    'AI-010': r'\bstt-cli\b',
    'AI-011': r'\bstt-cli\b',
    'AI-012': r'\b3T\s+Explore\b.{0,80}\b(AI|agent)\b',
    'AI-context-turns': r'\b(follow-up|multi-turn|conversation\s+(history|context))\b',
    'AI-local-mcp': r'\b(local\s+)?MCP\s+server\b',
    'AI-mcp-client': r'\bMCP\s+client',
    'AI-mcp-tools': r'\bMCP\s+tools?\b',
    'AI-model-chooser': r'\b(choose|select|switch)\b.{0,20}\b(AI\s+)?model\b',
    'AI-named-configs': r'\bAI\s+(configurations?|profiles?)\b',
    'AI-plan-gate': r'\bAI\b.{0,60}\b(requires?|available\s+in|only\s+in)\b.{0,30}\b(pro|ultimate|enterprise|edition|plan|subscription|license)',
    'AI-plan-req': r'\bAI\b.{0,60}\b(requires?|available\s+in|only\s+in)\b.{0,30}\b(pro|ultimate|enterprise|edition|plan|subscription|license)',
    'AI-sample-data-toggle': r'\b(send|include|share)\b.{0,30}\bsample\s+(data|documents)\b',
    'AI-schema-context': r'\b(schema|field\s+names?)\b.{0,40}\b(sent|context|prompt)\b.{0,20}\b(AI|LLM|model)',
    'AI-stt-cli': r'\bstt-cli\b',
    'GOV-002': r'\b(policy|compliance)\s+templates?\b',
    'GOV-003': r'\b(alert|notification)\s+channels?\b|\b(slack|webhook)\b.{0,30}\balert',
    'GOV-004': r'\bPII\s+(scan|scanning|classification|detection)',
    'GOV-005': r'\b(field|document)\s+(history|versions?|diffs?)\b|\bversioned\s+diff',
    'GOV-006': r'\b(performance|index)\s+(suggestions?|recommendations?|advisor)',
    'GOV-007': r'\b(3T\s+)?Lens\b.{0,60}\bMCP\b|\bgoverned\s+(tool|MCP)',
    'GOV-010': r'\btransform(ation)?\s+studio\b',
    'GOV-011': r'\b(real-time|dynamic)\s+(PII\s+)?masking\b',
    'GOV-012': r'\bBridge\b.{0,60}\b(OIDC|credentials?)\b',
    'GOV-013': r'\b(helm\s+chart|kubernetes)\b',
    'GOV-ai-controls': r'\b(disable|approve|approval)\b.{0,30}\bAI\b|\bAI\b.{0,30}\b(data\s+sharing|disclosure|consent)',
    'GOV-cli-policy': r'\b(command-line|CLI)\s+(flags?|options?|arguments?)\b.{0,60}\b(security|policy|protect|read-?only)',
    'GOV-cred-storage-os': r'\b(keytar|keychain|credential\s+manager|secret\s+service|OS\s+credential)',
    'GOV-isolated-edition': r'\bisolated\s+edition\b|\breadonly\s+edition\b',
    'GOV-platform-bridge': r'\b3TL?\s+Bridge\b',
    'GOV-platform-explore': r'\b3T\s+Explore\b.{0,80}\b(workspace|access\s+manager)',
    'GOV-platform-k8s': r'\b(helm\s+chart|kubernetes)\b',
    'GOV-platform-oidc': r'\bOIDC\s+providers?\b|\b(multiple|multi)\b.{0,20}\bOIDC',
    'GOV-protect-mode': r'\bprotect(ion)?\s+mode\b|\bsafe\s+mode\b',
    'GOV-rbac-actions': r'\bprivilege\s+actions?\b|\b(dbAdmin|userAdmin|readWrite)\b',
    'GOV-startup-policy': r'\b(global|admin)\s+(configuration|config)\s+file\b|\bstartup\s+(policy|configuration)',
    'GOV-telemetry-config': r'\btelemetry\b.{0,40}\b(opt[\s-]?out|disable|setting)',
    'SCHED-actions': r'\b(run\s+now|pause|resume|clone)\b.{0,40}\b(task|schedule)',
    'SCHED-batch': r'\bbatch\s+size\b',
    'SCHED-compare-results': r'\bcompare\s+results?\b|\bdiff\s+(view|results?)\b',
    'SCHED-compare-schedule': r'\b(schedule|save\s+as\s+task)\b.{0,40}\bcompar',
    'SCHED-compare-setup': r'\b(data|collection)\s+compar(e|ison)\b',
    'SCHED-compare-sync': r'\bsync(hroni[sz]e)?\b.{0,30}\b(differences|target|source)\b',
    'SCHED-concurrent': r'\bconcurrent\s+(tasks?|jobs?|executions?)\b',
    'SCHED-email': r'\b(smtp|email\s+(server|provider|settings))\b',
    'SCHED-history': r'\b(execution|task|job)\s+(history|log)\b',
    'SCHED-history-retention': r'\b(retain|retention|keep)\b.{0,30}\b(history|records|executions)\b',
    'SCHED-plan-limits': r'\b(scheduler|scheduled\s+tasks?|automation)\b.{0,60}\b(requires?|available\s+in|only\s+in|limit)\b.{0,30}\b(pro|ultimate|enterprise|edition|plan)',
    'SCHED-preset-types': r'\b(hourly|daily|weekly|monthly)\b',
    'SCHED-recur-daily': r'\bdaily\b',
    'SCHED-recur-interval': r'\bevery\s+\d*\s*(minutes?|hours?)\b',
    'SCHED-recur-monthly': r'\bmonthly\b',
    'SCHED-recur-once': r'\b(one-time|run\s+once|once)\b.{0,20}\b(schedule|task)',
    'SCHED-recur-weekly': r'\bweekly\b',
    'SCHED-retry': r'\bretr(y|ies)\b.{0,30}\b(count|attempts?|policy|failed)',
    'SCHED-script-tasks': r'\b(script|javascript)\s+tasks?\b|\bschedul\w+\s+scripts?\b',
    'SCHED-task-actions': r'\b(run\s+now|pause|resume|clone)\b.{0,40}\b(task|schedule)',
    'SCHED-task-save': r'\bsave\s+(as\s+)?(a\s+)?task\b',
    'SHELL-auto-reconnect': r'\b(auto(matic(ally)?)?[\s-]?reconnect)',
    'SHELL-background-exec': r'\b(background\s+execution|runs?\s+in\s+the\s+background)\b',
    'SHELL-open-from': r'\bopen\s+(in|with)\s+(IntelliShell|shell|mongo\s*shell)\b',
    'SHELL-persistent-vars': r'\bvariables?\b.{0,30}\bpersist',
    'SHELL-sessions': r'\b(multiple|several)\s+(shell\s+)?(sessions|tabs)\b',
    'SQL-export-monitor': r'\b(SQL\s+export|export\s+to\s+SQL)\b',
    'SQL-migration-1to-many': r'\bone[\s-]to[\s-]many\b',
    'SQL-migration-1to1': r'\bone[\s-]to[\s-]one\b',
    'SQL-migration-schema': r'\b(SQL\s+(to|→)\s+MongoDB|SQL\s+migration)\b',
    'TRANSFER-plan-limits': r'\b(import|export|transfer)\b.{0,60}\b(requires?|only\s+in|limit)\b.{0,30}\b(pro|ultimate|enterprise|edition|plan)',
}

DEAD_SILO_IDS = {
    'AGG-chart-builder': r'\b(chart|visuali[sz]\w*)\b.{0,40}\b(aggregation|pipeline)\s+(output|results?)\b|\b(aggregation|pipeline)\s+(output|results?)\b.{0,40}\bcharts?\b',
    'AGG-clipboard': r'\b(copy|paste)\b.{0,25}\b(pipeline|aggregation)\b.{0,25}\b(clipboard|json)\b',
    'AGG-js-import-export': r'\b(export|import|save|load)\b.{0,30}\b(pipeline|aggregation)\b.{0,30}\.js\b',
    'AGG-keyboard': r'\b(aggregation|pipeline)\s+editor\b.{0,80}\b(shortcuts?|hotkeys?)\b|\b(shortcuts?|hotkeys?)\b.{0,40}\b(aggregation|pipeline)\b',
    'AGG-pagination': r'\b(aggregation|pipeline|stage)\b.{0,40}\b(pagination|paginat\w+|next\s+page|page\s+size)\b',
    'AGG-vqb-sync': r'\b(visual\s+query\s+builder|VQB)\b.{0,60}\b(aggregation|pipeline|\$match)',
    'AI-agentic-mode': r'\b(agentic|AI\s+agent|agent\s+mode|tool[\s-]calling)\b',
    'AI-chart-render': r'\b(AI|chat|assistant)\b.{0,40}\b(renders?|generates?|creates?|draws?)\b.{0,20}\b(charts?|graphs?)\b',
    'AI-error-fix': r'\b(fix|explain|correct)\w*\s+(the\s+)?(errors?|query|failing)\b.{0,30}\b(with\s+)?AI\b|\bAI\b.{0,30}\b(fix|explain)\w*\s+(the\s+)?errors?\b',
    'AI-guardrail-layer': r'\b(guard[\s-]?rails?)\b',
    'AI-inline-completion': r'\b(inline|AI)\s+(code\s+)?(completion|suggestions?|autocomplete)\b|\bcopilot\b',
    'AI-multi-conversation': r'\b(multiple|new|switch|rename)\s+(chat|conversation)s?\b|\bconversation\s+(list|history|titles?)\b',
    'AI-nl-pipeline': r'\b(natural\s+language|plain\s+english|describe)\b.{0,60}\b(aggregation|pipeline)\b',
    'AI-prompt-templates': r'\bprompt\s+(templates?|library|presets?)\b|\b(saved|custom)\s+prompts?\b',
    'AI-tab-context': r'\b(open\s+tabs?|active\s+tabs?)\b.{0,40}\b(AI|agent|context)\b',
    'AI-voice-query': r'\b(voice\s+(input|query|queries|commands?)|speech[\s-]to[\s-]text)\b',
    'CONN-git-repo-sharing': r'\b(git)\b.{0,40}\bconnections?\b.{0,40}\b(shar\w+|sync\w*|push|pull)\b',
    'IDX-explain-sources': r'\b(visual\s+)?explain\b.{0,40}\b(from|in)\s+(the\s+)?(shell|aggregation\s+editor|query\s+tab|profiler)\b',
    'IDX-log-parser': r'\b(log\s+(parser|analy[sz]\w+|viewer)|parse\s+(mongod\s+)?logs?|mongod\s+logs?)\b',
    'IDX-profiler-drilldown': r'\bprofiler\b.{0,60}\b(details?|drill|open\s+in|add\s+index)\b',
    'IDX-profiler-export': r'\bprofiler\b.{0,60}\bexport\w*\b|\bexport\w*\b.{0,40}\bprofil\w+\s+data\b',
    'PROP-ai-gateway-sso': r'\bAI\s+gateway\b|\b(SSO|single\s+sign-on)\b.{0,40}\b(AI|LLM)\b',
    'PROP-bi-dashboard': r'\b(dashboards?|BI)\b.{0,30}\b(builder|charts?|widgets?)\b',
    'PROP-git-integration': r'\b(git\s+integration|version\s+control\s+integration|commit\s+and\s+push)\b',
    'PROP-qe-key-vault-ui': r'\b(key\s+vault|queryable\s+encryption|CSFLE|client-side\s+field\s+level\s+encryption)\b',
    'PROP-schema-erd-cluster': r'\b(ERD|entity[\s-]relationship\s+diagram)\b',
    'PROP-vector-search-tooling': r'\b(vector\s+search|\$vectorSearch|vector\s+index)\b',
    'QUERY-undo-redo': r'\bundo\b.{0,15}\bredo\b|\bundo\s+(changes?|edits?)\b',
    'QUERY-vqb-plan': r'\b(visual\s+query\s+builder|VQB)\b.{0,60}\b(edition|license|pro|ultimate|enterprise|plan)\b',
    'QUERY-vqb-proj-sort': r'\b(visual\s+query\s+builder|VQB)\b.{0,80}\b(projection|sort)\b',
    'SCHED-progress': r'\b(progress\s+(bar|monitor\w*|indicator)|real[\s-]time\s+progress|track\s+progress)\b',
    'SCHEMA-date-dist': r'\bdate\b.{0,30}\b(distribution|histogram)\b',
    'SCHEMA-deploy-validator': r'\b(apply|push|deploy)\w*\b.{0,40}\b(\$jsonSchema|validator|validation\s+rules?)\b',
    'SCHEMA-designer-color': r'\b(schema|diagram|canvas|designer)\b.{0,40}\bcolou?r\s*(cod\w+|presets?)?\b',
    'SCHEMA-designer-layouts': r'\b(saved?|named|custom)\s+layouts?\b',
    'SCHEMA-explore-docs': r'\b(explore|find|show)\s+documents?\b.{0,40}\b(field|containing|missing)\b',
    'SCHEMA-rename-discover': r'\brename\b.{0,30}\bfields?\b.{0,40}\b(schema|outlier|analysis)\b',
    'SCHEMA-validation-limits': r'\b(validation|\$jsonSchema)\b.{0,40}\b(limits?|limitations?|not\s+supported|unsupported)\b',
    'SCHEMA-validation-ui': r'\b(validation\s+rules?|\$jsonSchema|schema\s+validation)\b.{0,50}\b(add|edit|generat\w+|preview|apply)\b',
    'SCHEMA-view-from-sql': r'\b(create|generate)\b.{0,20}\bviews?\b.{0,40}\bSQL\b',
    'SHELL-destructive-guard': r'\b(destructive|dangerous)\s+(commands?|operations?|queries)\b',
    'SHELL-oidc-auth': r'\b(shell|mongosh|intellishell)\b.{0,60}\bOIDC\b|\bOIDC\b.{0,60}\b(shell|mongosh)\b',
    'SHELL-result-tab-limit': r'\b(result|results)\s+tabs?\b.{0,40}\b(limit|maximum|max)\b',
    'SHELL-result-views': r'\b(tree|table|json)\s+view\b.{0,40}\b(tree|table|json)\s+view\b',
    'SHELL-run-cursor': r'\b(run|execute)\b.{0,20}\b(to|up\s+to|at)\s+(the\s+)?cursor\b',
    'SHELL-storedjs-rename': r'\bstored\s+(javascript|js|functions?)\b',
    'SQL-code-gen': r'\b(query\s+code|code\s+generation|generate\s+code|SQL\s+to\s+(MongoDB|MQL|mongo\s+shell))\b',
    'SQL-export-field-map': r'\b(export)\b.{0,40}\bSQL\b.{0,60}\b(column|field)\s+mapping\b|\b(field|column)\s+mapping\b.{0,40}\bSQL\b',
    'SQL-export-relations': r'\b(export)\b.{0,40}\bSQL\b.{0,60}\b(relationships?|foreign\s+keys?|child\s+tables?)\b',
    'SQL-federated-query': r'\b(federated\s+quer\w+|cross[\s-]database\s+(quer\w+|joins?))\b',
    'SQL-join-mapping': r'\bJOINs?\b.{0,60}\$lookup|\$lookup.{0,60}\bJOINs?\b',
    'TRANSFER-export-bson': r'\b(export|dump)\w*\b.{0,30}\b(BSON|mongodump)\b',
    'TRANSFER-transform-filter': r'\bimport\w*\b.{0,40}\b(filter|query)\b.{0,30}\b(documents?|conditions?)\b',
    'TRANSFER-transform-js': r'\b(javascript|js)\s+(functions?|transform\w*)\b.{0,40}\b(import|export|document)\b',
    'TRANSFER-transform-pipeline': r'\b(export)\w*\b.{0,40}\b(aggregation\s+pipeline|pipeline\s+results?)\b',
    'AI-conversation': r'\b(follow[\s-]up\s+(questions?|prompts?)|multi[\s-]turn|previous\s+(messages|prompts)|conversation\s+context)\b',
    'AI-privacy': r'\b(schema[\s-]only|privacy\s+mode|send\s+(sample|actual)\s+data)\b',
    'AI-sample-context': r'\b(send|include|share)\b.{0,30}\bsample\s+(data|documents)\b',
    'PROP-cli-automation': r'\b(headless|CI/CD|command[\s-]line\s+(interface|tool))\b.{0,60}\b(tasks?|automat\w+|pipelines?|scripts?)\b',
    'PROP-idx-perf-advisor': r'\b(performance|index)\s+(suggestions?|recommendations?|advisor)\b',
    'SCHED-types-time': r'\b(hourly|daily|weekly|monthly|one[\s-]time)\b[^.\n]{0,25}\b(schedul\w+|tasks?|jobs?|runs?|executions?|backups?|exports?)\b|\b(schedul\w+|tasks?|jobs?)\b[^.\n]{0,40}\b(hourly|daily|weekly|monthly)\b',
    'SHELL-background': r'\b(scripts?|shell|queries|IntelliShell)\b[^.\n]{0,60}\b(keep|continue)s?\s+(running|executing)\b',
    'SHELL-integrations': r'\bopen\b.{0,20}\b(in|into)\s+(IntelliShell|the\s+shell|mongo\s*shell)\b',
    'SHELL-reconnect': r'\b(auto(matic(ally)?)?[\s-]?reconnect\w*)\b',
    'SHELL-sessions-vars': r'\bvariables?\b.{0,40}\b(persist|retain|kept|available)\b.{0,40}\b(session|executions?)\b',
}

PROBES = {**OUR_EXTRAS, **DEAD_SILO_IDS}
FRONTMATTER = re.compile(r"^---\n.*?\n---\n", re.S)


def _excluded(path: Path, data: Path) -> bool:
    """Same exclusions as the silo classifier (taxonomy.is_generated_dashboard_or_strings)."""
    if path.name == "repo_source_strings.md":
        return True
    rel = path.relative_to(data).parts
    return (len(rel) == 1 and rel[0] == "README.md") or (len(rel) == 3 and rel[2] in ("README.md", "DIFF.md"))


def _scan(args):
    paths, probes = args
    compiled = {k: re.compile(v, re.I) for k, v in probes.items()}
    out = {k: [] for k in probes}
    for p in paths:
        text = FRONTMATTER.sub("", Path(p).read_text(encoding="utf-8", errors="ignore"), count=1)
        for k, c in compiled.items():
            m = c.search(text)
            if m:
                out[k].append((Path(p).parts[-3] if len(Path(p).parts) > 2 else "?",
                               text[max(0, m.start() - 70): m.end() + 60].replace("\n", " ")))
    return out


def main() -> None:
    root = Path(__file__).resolve().parent.parent.parent
    ap = argparse.ArgumentParser(description="Run definition probes over the silo corpus")
    ap.add_argument("--silo", type=Path, default=root.parent / "prod_info_silo")
    ap.add_argument("ids", nargs="*", help="probe IDs (default: all)")
    a = ap.parse_args()
    probes = {k: PROBES[k] for k in a.ids} if a.ids else PROBES
    data = a.silo / "data"
    paths = [str(Path(r) / f) for r, _, fs in os.walk(data) for f in fs if f.endswith(".md")
             and not _excluded(Path(r) / f, data)]
    n = max(1, (os.cpu_count() or 2) - 1)
    hits = {k: [] for k in probes}
    with ProcessPoolExecutor(n) as ex:
        for part in ex.map(_scan, [(paths[i::n], probes) for i in range(n)]):
            for k, v in part.items():
                hits[k] += v
    random.seed(3)
    with open("probe-samples.txt", "w", encoding="utf-8") as fh:
        for k, v in hits.items():
            distinct = {re.sub(r"\W+", " ", s).lower() for _, s in v}
            products = {p for p, _ in v}
            print(f"{k}\tdocs={len(v)}\tdistinct={len(distinct)}\tproducts={len(products)}")
            fh.write(f"==== {k} docs={len(v)}\n")
            for p, s in random.sample(v, min(8, len(v))):
                fh.write(f"  {p} | {s[:170]}\n")


if __name__ == "__main__":
    main()
