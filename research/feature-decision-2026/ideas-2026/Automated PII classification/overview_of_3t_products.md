 # PII Classification & Discovery — Detailed Sub-Feature Implementation Matrix

> **Scope:** All 3T Software Labs products · Status as of 2026-08-12  
> **Legend:** ✅ Shipped | 🟡 In Progress | 🔵 Backlog/Planned | ⚪ Spike Done | ❌ Not Present | 🚫 Won't Do / N/A

---

## 1. DATA SAMPLING & INPUT

| Sub-Feature | pii-scanner (Rust lib) | 3T MCP | PII Detector (Web) | 3T Lens | 3TL Bridge | Studio 3T Desktop |
|---|---|---|---|---|---|---|
| **1.1 Random $sample (N docs)** | ✅ Caller provides | ✅ Via stt-cli | ✅ Go orchestrator | ✅ Via Detector API | 🔵 scanner source | ✅ Schema discovery |
| **1.2 Full collection scan** | ✅ Caller provides | ❌ | ✅ "Full Scan" mode | ✅ Via Detector API | 🔵 Inventory pipeline | ❌ |
| **1.3 Configurable sample size** | ✅ ScanRequest.sampleSize | ✅ Tool param | ✅ UI config | ✅ UI config | 🔵 | ✅ (50–all, for masking) |
| **1.4 Schema-only mode (no values)** | ✅ scanMode: schema | ✅ Catalogue pass | ❌ | ❌ | ✅ At schema registration | ✅ (schema discovery only) |
| **1.5 Multi-collection batch** | 🚫 Single input array | ✅ Task per collection | ✅ Sequential scans | ✅ Sequential scans | 🔵 Multi-source pipeline | ❌ |
| **1.6 Source-agnostic input** | ✅ Any JSON array | ✅ MongoDB only | ✅ MongoDB only | ✅ MongoDB only | 🔵 Any pipeline source | ❌ MongoDB only |
| **1.7 Nested document traversal** | ✅ Recursive path | ✅ | ✅ | ✅ | 🔵 | ✅ (masking supports nesting) |
| **1.8 Array element scanning** | ✅ Index-aware paths | ✅ | ✅ | ✅ | 🔵 | ✅ (masking: array-aware) |
| **1.9 Polymorphic field handling** | ✅ Per-variant denominators | ✅ | ✅ | ✅ | ❌ | ❌ |
| **1.10 Pre-scan field exclusion (skipFields)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |

---

## 2. FIELD-NAME CLASSIFICATION (Heuristic)

| Sub-Feature | pii-scanner (Rust lib) | 3T MCP | PII Detector (Web) | 3T Lens | 3TL Bridge | Studio 3T Desktop |
|---|---|---|---|---|---|---|
| **2.1 Name-based category matching** | ✅ 17 categories | ✅ | ✅ | ✅ | 🔵 (13 curated rows) | ❌ |
| **2.2 English locale patterns** | ✅ ~80 patterns | ✅ | ✅ | ✅ | 🔵 | ❌ |
| **2.3 Multi-locale support (6 EU)** | ✅ DE/FR/ES/IT/PT/NL | ✅ | ✅ | ✅ | ❌ | ❌ |
| **2.4 Category: direct_pii** | ✅ | ✅ | ✅ | ✅ | 🔵 | ❌ |
| **2.5 Category: contact_pii** | ✅ | ✅ | ✅ | ✅ | 🔵 | ❌ |
| **2.6 Category: name_pii** | ✅ | ✅ | ✅ | ✅ | 🔵 | ❌ |
| **2.7 Category: financial** | ✅ | ✅ | ✅ | ✅ | 🔵 | ❌ |
| **2.8 Category: health** | ✅ | ✅ | ✅ | ✅ | 🔵 | ❌ |
| **2.9 Category: sensitive_demographic** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **2.10 Category: secret/credentials** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **2.11 Category: device_id** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **2.12 Category: biometric** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **2.13 Category: location / location_admin** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **2.14 Category: political_union_genetic** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **2.15 Category: criminal_record** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **2.16 Category: employment_hr** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **2.17 Category: vehicle** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **2.18 Path-context multiplier** | ✅ ×1.05 person / ×0.4 non-person | ✅ | ✅ | ✅ | ❌ | ❌ |

---

## 3. VALUE-PATTERN DETECTION (Regex)

| Sub-Feature | pii-scanner (Rust lib) | 3T MCP | PII Detector (Web) | 3T Lens | 3TL Bridge | Studio 3T Desktop |
|---|---|---|---|---|---|---|
| **3.1 Email pattern** | ✅ | ✅ | ✅ | ✅ | ⚪ Spike (Rhai) | ❌ |
| **3.2 IPv4 / IPv6** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.3 Credit card (Luhn validation)** | ✅ | ✅ | ✅ | ✅ | ⚪ Spike | ❌ |
| **3.4 Phone — international (E.164 strict)** | ✅ | ✅ | ✅ | ✅ | ⚪ Spike (phone_shape) | ❌ |
| **3.5 SSN (anchored pattern)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.6 Date of birth** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.7 IBAN** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.8 JWT token** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.9 UUID** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.10 bcrypt hash** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.11 SHA hex (exact-length)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.12 Base64 (strict mode)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.13 IMEI (Luhn)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.14 UK NIN** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.15 BIC/SWIFT** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.16 ETH wallet** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.17 BTC wallet** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.18 Geo coordinates (range-checked)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.19 FR NIR (French social security)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.20 IT Codice Fiscale** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.21 ES DNI/NIE** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **3.22 Custom regex (user-defined)** | ❌ | ❌ | ❌ | ❌ | ✅ Rhai-based | ❌ |

---

## 4. NLP / NER DETECTION (AI-Powered)

| Sub-Feature | pii-scanner (Rust lib) | 3T MCP | PII Detector (Web) | 3T Lens | 3TL Bridge | Studio 3T Desktop |
|---|---|---|---|---|---|---|
| **4.1 GLiNER ONNX model** | ✅ gline-rs crate | ✅ | ✅ | ✅ (via Detector) | ❌ | ❌ |
| **4.2 Zero-shot NER (no training)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.3 Prose/free-text field scanning** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.4 Per-character-offset attribution** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.5 Batch inference (50-record)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.6 Cooperative cancellation** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.7 NER label: person** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.8 NER label: email address** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.9 NER label: phone number** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.10 NER label: social security number** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.11 NER label: credit card number** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.12 NER label: date of birth** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.13 NER label: home address** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.14 NER label: passport number** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.15 NER label: driver license** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.16 NER label: bank account number** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.17 NER label: IP address** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.18 NER label: medical record number** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **4.19 Configurable NER on/off** | ✅ scanMode: hybrid/nlp | ✅ | ✅ | ✅ | 🚫 | ❌ |

---

## 5. SCORING & CONFIDENCE

| Sub-Feature | pii-scanner (Rust lib) | 3T MCP | PII Detector (Web) | 3T Lens | 3TL Bridge | Studio 3T Desktop |
|---|---|---|---|---|---|---|
| **5.1 Composite score (0.6×name + 0.4×value)** | ✅ | ✅ | ✅ | ✅ | ❌ Counts only | ❌ |
| **5.2 Co-occurrence bonus (+0.10)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **5.3 Multi-name bonus (+0.05)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **5.4 Person-context multiplier (×1.05)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **5.5 Non-person penalty (×0.4)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **5.6 Score cap at 1.0** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **5.7 4-bucket classification** | ✅ Critical/PII/Pot.Sensitive/Likely Safe | ✅ | ✅ | ✅ | ❌ | ❌ |
| **5.8 Occurrence counts + denominators** | ✅ | ✅ | ✅ | ✅ | ✅ (design) | ❌ |
| **5.9 Per-field signal (name_signal + value_signal)** | ✅ | ✅ | ✅ | ✅ | 🔵 | ❌ |

---

## 6. REGULATION & POLICY MAPPING

| Sub-Feature | pii-scanner (Rust lib) | 3T MCP | PII Detector (Web) | 3T Lens | 3TL Bridge | Studio 3T Desktop |
|---|---|---|---|---|---|---|
| **6.1 GDPR (Art. 4/9/10)** | ✅ | ✅ | ✅ | ✅ | 🔵 policyIds | ❌ |
| **6.2 PCI-DSS** | ✅ | ✅ | ✅ | ✅ | 🔵 | ❌ |
| **6.3 HIPAA** | ✅ | ✅ | ✅ | ✅ | 🔵 | ❌ |
| **6.4 CCPA** | ✅ | ✅ | ✅ | ✅ | 🔵 | ❌ |
| **6.5 LGPD (Brazil)** | ✅ | ✅ | ✅ | ✅ | 🔵 | ❌ |
| **6.6 Credentials (non-regulation)** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **6.7 Custom policy definitions** | ❌ | ❌ | ❌ | ❌ | 🔵 Customer script | ❌ |
| **6.8 Versioned taxonomy** | ✅ taxonomyVersion field | ✅ | ✅ | ✅ | ❌ | ❌ |
| **6.9 Versioned policy** | ✅ policyVersion field | ✅ | ✅ | ✅ | ❌ | ❌ |

---

## 7. MASKING EXECUTION

| Sub-Feature | pii-scanner (Rust lib) | 3T MCP | PII Detector (Web) | 3T Lens | 3TL Bridge | Studio 3T Desktop |
|---|---|---|---|---|---|---|
| **7.1 Null out** | 🚫 Detection only | ❌ | ❌ | 🟡 Proxy response | ✅ Rhai | ✅ |
| **7.2 Remove field entirely** | 🚫 | ❌ | ❌ | 🟡 | ✅ | ✅ |
| **7.3 Fixed string substitution** | 🚫 | ❌ | ❌ | 🟡 | ✅ | ✅ |
| **7.4 Fixed number substitution** | 🚫 | ❌ | ❌ | ❌ | ✅ | ✅ |
| **7.5 Percentage add/subtract (numeric)** | 🚫 | ❌ | ❌ | ❌ | ✅ | ✅ |
| **7.6 Random string generation** | 🚫 | ❌ | ❌ | ❌ | ✅ | ✅ (KONG-6051) |
| **7.7 Partial masking (e.g. last 4 digits)** | 🚫 | ❌ | ❌ | 🟡 | ✅ Truncation | ✅ |
| **7.8 Credit card truncation** | 🚫 | ❌ | ❌ | ❌ | ✅ (confirmed) | ✅ |
| **7.9 Customer name tokenization** | 🚫 | ❌ | ❌ | ❌ | ✅ (confirmed) | ❌ |
| **7.10 Synthetic value substitution** | 🚫 | ❌ | ❌ | ❌ | ✅ (confirmed) | ❌ |
| **7.11 Hashing (SHA/MD5)** | 🚫 | ❌ | ❌ | ❌ | ✅ | ❌ |
| **7.12 Generate new ObjectId** | 🚫 | ❌ | ❌ | ❌ | ❌ | ✅ |
| **7.13 Conditional masking (by field type)** | 🚫 | ❌ | ❌ | ❌ | ✅ | ✅ (KONG-4987) |
| **7.14 Masking in exports** | 🚫 | ❌ | ❌ | ❌ | ❌ | ✅ (KONG-4985) |
| **7.15 Masking in imports** | 🚫 | ❌ | ❌ | ❌ | ❌ | ✅ (KONG-5218) |
| **7.16 Mask in-place** | 🚫 | ❌ | ❌ | ❌ | ❌ | ✅ |
| **7.17 Mask to new collection** | 🚫 | ❌ | ❌ | ❌ | ✅ (sink) | ✅ |
| **7.18 Rule-based masking (conditional logic)** | 🚫 | ❌ | ❌ | 🔵 PolicySet | ✅ Rhai scripts | 🚫 (KONG-4988 Won't Do) |

---

## 8. SCAN → MASK PIPELINE (Discovery-to-Action)

| Sub-Feature | pii-scanner (Rust lib) | 3T MCP | PII Detector (Web) | 3T Lens | 3TL Bridge | Studio 3T Desktop |
|---|---|---|---|---|---|---|
| **8.1 Auto-generate masking config from scan** | 🚫 | ❌ | ✅ /bridge endpoint | 🟡 PII → Proxy rules | ✅ Auto-gen Rhai | ❌ (Manual config) |
| **8.2 "Send to Bridge" handoff** | 🚫 | ❌ | ✅ UI button | ❌ | ✅ (receives) | ❌ |
| **8.3 Pre-populate masking rules per field** | 🚫 | ❌ | ✅ Per-signal rules | 🟡 | ✅ | ❌ |
| **8.4 User review/override before masking** | 🚫 | ❌ | ✅ (UI edit) | 🟡 | ❌ (pipeline auto) | ✅ (manual only) |
| **8.5 Scan → schema discovery feed** | ✅ Schema mode | ✅ | ✅ | ✅ | 🔵 | ❌ |
| **8.6 One-click mask after discovery** | 🚫 | ❌ | ✅ | 🟡 | 🔵 | ❌ |

---

## 9. REAL-TIME / RUNTIME ENFORCEMENT

| Sub-Feature | pii-scanner (Rust lib) | 3T MCP | PII Detector (Web) | 3T Lens | 3TL Bridge | Studio 3T Desktop |
|---|---|---|---|---|---|---|
| **9.1 Wire-protocol interception** | ❌ | ❌ | ❌ | ✅ OP_MSG + OP_QUERY | ❌ | ❌ |
| **9.2 Request-phase deny/drop** | ❌ | ❌ | ❌ | ✅ (E2E proved) | ❌ | ❌ |
| **9.3 Response-phase masking** | ❌ | ❌ | ❌ | 🟡 P1 roadmap | ❌ | ❌ |
| **9.4 Pipeline-layer masking (in-transit)** | ❌ | ❌ | ❌ | ❌ | ✅ | ❌ |
| **9.5 LLM-context masking (before AI)** | ❌ | ✅ Data minimization | ❌ | ❌ | ✅ (before LLM) | ✅ (KONG-11124 credentials) |
| **9.6 Query classification taxonomy** | ❌ | ❌ | ❌ | ✅ Command types | ❌ | ❌ |
| **9.7 Bulk write payload inspection** | ❌ | ❌ | ❌ | 🔵 P1 blocker | ❌ | ❌ |
| **9.8 Audit logging of access** | ❌ | ❌ | ❌ | ✅ Pluggable sink | ❌ | ❌ |

---

## 10. OUTPUT & REPORTING

| Sub-Feature | pii-scanner (Rust lib) | 3T MCP | PII Detector (Web) | 3T Lens | 3TL Bridge | Studio 3T Desktop |
|---|---|---|---|---|---|---|
| **10.1 Structured JSON report** | ✅ ScanReport | ✅ | ✅ | ✅ | 🔵 Findings sink | ❌ |
| **10.2 Per-field signal list** | ✅ FieldSignal[] | ✅ | ✅ | ✅ | 🔵 | ❌ |
| **10.3 Scan history persistence** | ❌ (stateless lib) | ✅ list_pii_scans | ✅ MongoDB pii_scans | ✅ History tab | 🔵 | ❌ |
| **10.4 Real-time progress reporting** | ❌ | ✅ task-manager | ✅ GET /scan/:id/progress | ✅ | ❌ | ❌ |
| **10.5 Export findings (file/API)** | ✅ (return value) | ✅ (tool output) | ✅ (REST API) | ✅ | 🔵 (catalogue) | ❌ |
| **10.6 OpenLineage emission** | ❌ | ❌ | ❌ | ❌ | 🔵 Column-level | ❌ |
| **10.7 Data catalogue integration** | ❌ | ❌ | ❌ | ❌ | 🔵 OpenMetadata | ❌ |
| **10.8 Recall benchmarking suite** | ✅ Canonical baselines | ❌ | ✅ recall-snapshot.sh | ❌ | ❌ | ❌ |
| **10.9 engineVersion in report** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |
| **10.10 taxonomyVersion in report** | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ |

---

## 11. USER INTERFACE / INTERACTION MODEL

| Sub-Feature | pii-scanner (Rust lib) | 3T MCP | PII Detector (Web) | 3T Lens | 3TL Bridge | Studio 3T Desktop |
|---|---|---|---|---|---|---|
| **11.1 Dedicated PII scan UI** | 🚫 Library | ❌ (AI chat) | ✅ React (New Scan/Results/History) | ✅ Tools → PII sidebar | ❌ (config-as-code) | ❌ |
| **11.2 AI/Chat-driven scanning** | 🚫 | ✅ scan_pii tool | ❌ | ❌ | ❌ | ❌ |
| **11.3 CLI invocation** | 🚫 | ✅ stt-cli | ❌ | ❌ | 🔵 CLI commands | ❌ |
| **11.4 REST API** | 🚫 | ✅ Internal routes | ✅ Full REST API | ✅ Via Detector | ❌ | ❌ |
| **11.5 Connection picker integration** | 🚫 | ✅ (user connections) | ✅ (Access Manager) | ✅ (Access Manager) | 🔵 Pipeline source | ✅ (connection tree) |
| **11.6 Results visualization** | 🚫 | ❌ (text output) | ✅ Table + badges | ✅ Table + badges | ❌ | ❌ |
| **11.7 RBAC-controlled access** | 🚫 | ❌ (local) | ✅ | ✅ | ❌ | ❌ |
| **11.8 Background/async execution** | 🚫 | ✅ task-manager | ✅ | ✅ | 🔵 | ❌ |
| **11.9 Scheduled/recurring scans** | 🚫 | ✅ Cron via task-manager | ❌ | ❌ | 🔵 | ❌ |

---

## 12. DEPLOYMENT & DATA RESIDENCY

| Sub-Feature | pii-scanner (Rust lib) | 3T MCP | PII Detector (Web) | 3T Lens | 3TL Bridge | Studio 3T Desktop |
|---|---|---|---|---|---|---|
| **12.1 Runs client-side (air-gap OK)** | ✅ Embedded | ✅ Local process | ❌ Server-side | ❌ Server-side | ❌ Server-side | ✅ Local (for masking) |
| **12.2 No data leaves machine** | ✅ | ✅ | ❌ | ❌ | ❌ | ✅ (masking only) |
| **12.3 Server-managed deployment** | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **12.4 Docker/container deployment** | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ |
| **12.5 Shared library (Nexus registry)** | ✅ manatee/3t-cargo | ✅ (consumer) | ✅ (consumer) | ✅ (via Detector) | ❌ (own impl) | ❌ |

---

## 13. INTEGRATION & HANDOFF

| Sub-Feature | pii-scanner (Rust lib) | 3T MCP | PII Detector (Web) | 3T Lens | 3TL
