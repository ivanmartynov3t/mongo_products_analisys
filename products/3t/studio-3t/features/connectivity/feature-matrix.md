# Feature Matrix — Studio 3T / Connectivity

## Navigation

- [Product report](../../product-report.md)
- [Feature report](feature-report.md)
- [Feature dictionary](../../../../../feature-dictionary.md)
- [Low-level comparison](../../../../../reports/comparisons/low-level-feature-comparison.md)

## Source index

- S1: https://studio3t.com/knowledge-base/articles/connect-to-mongodb/
- S2: https://studio3t.com/knowledge-base/articles/mongodb-password-encryption/

## Capability matrix

| Capability ID | Capability | Current support | Detailed behavior | Constraints / prerequisites | Roadmap status | Sources | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| CONN-topology | Topology types | Supported | Standalone (single host + port), Replica Set (multiple members + replica set name + read preference), Sharded Cluster (multiple mongos hosts + read preference), DNS Seedlist (mongodb+srv://) — all configurable in Connection Manager. | DNS Seedlist requires SRV-capable DNS; Replica Set requires valid replica set name. | confirmed | S1 | All editions. |
| CONN-read-pref | Read preference on Replica Set | Supported | Six options: Primary, Primary Preferred, Secondary, Secondary Preferred, Nearest. Read preference tags with ordering also configurable. | Only meaningful on Replica Set and Sharded topologies. | confirmed | S1 | All editions. |
| CONN-uri-paste | Connection setup — URI paste | Supported | Paste standard mongodb:// or mongodb+srv:// URI; auto-populates all Connection Manager tabs (auth, TLS, SSH, advanced). | URI must be syntactically valid; some driver options may not round-trip via UI. | confirmed | S1 | All editions. |
| CONN-import-clients | Connection setup — import from other clients | Supported | Auto-detects and imports connections from Robo 3T / Robomongo and NoSQLBooster, including SSH tunnel credentials. Import via .uri files also supported. | Source client must be installed and have saved connections. | confirmed | S1 | All editions. |
| CONN-auth-std | Authentication — standard mechanisms | Supported | None, SCRAM-SHA-256, SCRAM-SHA-1 (Legacy), X.509. Available in all editions. | X.509 requires PEM client certificate + CA certificate. | confirmed | S1 | All editions. |
| CONN-auth-enterprise | Authentication — enterprise mechanisms | Supported (Ultimate only) | Kerberos (GSSAPI), LDAP (Plain), AWS IAM, MongoDB OIDC. OIDC includes "Consider target endpoint trusted" and "Use ID token instead of Access token" toggles. | Requires Ultimate edition. Kerberos/LDAP require corresponding server-side configuration. AWS IAM requires valid IAM credentials. | confirmed | S1 | Ultimate edition only. |
| CONN-tls | TLS/SSL configuration | Supported | Enable SSL checkbox; CA cert options: own Root CA file, OS-trusted certs, or accept any (insecure); client PEM cert + passphrase; X.509 user override; "Allow invalid hostnames" toggle (disables hostname validation); Server Name Indication (SNI) with custom server name field. | "Accept any" and "Allow invalid hostnames" are insecure and should be avoided in production. | confirmed | S1 | All editions. |
| CONN-ssh | SSH tunnel | Supported | Toggle "Use SSH tunnel to connect"; auth modes: Password or Private Key (+ passphrase); SSH Profiles: reusable named profiles in Connection Manager or Preferences > Advanced > SSH Profiles. Multiple connections assignable to one profile; updating profile password propagates to all assigned connections. | SSH server must be accessible; private key must be compatible format. | confirmed | S1 | All editions. |
| CONN-proxy | Proxy support | Supported | Four proxy modes per connection: Direct / No proxy (default), Application default proxy (from Preferences > Advanced > Network), Custom HTTP proxy, Custom SOCKS proxy. Applies to MongoDB connections, SQL source connections for import, and app HTTPS requests. | Custom proxy modes require valid proxy server address + port. | confirmed | S1 | All editions. |
| CONN-pool-params | Advanced connection parameters | Supported | Max connection idle time (ms) — Azure workaround documented at 60,000 ms; max connection pool size; server selection timeout (default 30,000 ms); socket timeout (default 0 = no timeout); connect timeout (default 10,000 ms); application name; Enable Retry Writes (default on); Enable Load Balanced (loadBalanced driver option); Write concern (W, Wtimeout, Journal). | Load Balanced mode requires a load balancer in front of MongoDB. | confirmed | S1 | All editions. |
| CONN-org-folders | Connection organization — folders and color-coding | Supported | Connections grouped into folders (displayed in Connection Manager and My Resources sidebar). Per-connection color-coding applied to server/database/collection tabs and result tabs — prevents production/test environment confusion. | Color is cosmetic only; does not enforce access restrictions. | confirmed | S1 | All editions. |
| CONN-team-sharing | Shared folders (team sharing) | Supported (Pro/Base+) | Invite team members by email to a shared folder; permission levels: Manage, Edit, View; shared connections are accessible to all invited members. | Requires Pro/Base or Ultimate edition. | confirmed | S1 | Pro/Base+ only. |
| CONN-readonly-lock | Read-only connection lock | Supported | Per-connection read-only lock prevents all write operations within that connection's Result tabs. | Lock is enforced at the UI layer; does not modify MongoDB server permissions. | confirmed | S1 | All editions. |
| CONN-cred-storage | Credential storage and encryption | Supported | Default: passwords encrypted at rest with built-in key. Cryptographic key store option: master password required at app startup; all connection files moved to encrypted store; previous unencrypted files deleted. | Cryptographic key store option increases security but adds a required startup step. | confirmed | S2 | All editions. |
