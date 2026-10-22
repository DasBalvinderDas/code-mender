# CodeMender Security Analysis
**Repo:** demo/vulnerable-app @ `0cb0d41`  |  **Generated:** 2026-10-22 08:53 UTC
**Engine:** Built-in rule engine (CodeMender-style)

**Risk score:** 100/100 | **Findings:** 33 | **Auto-fixable:** 11 | **Files/Lines scanned:** 5/119

| Critical | High | Medium | Low |
|---|---|---|---|
| 9 | 16 | 8 | 0 |

## OWASP Top 10 coverage
- A01:2021 Broken Access Control: 3
- A02:2021 Cryptographic Failures: 4
- A03:2021 Injection: 10
- A05:2021 Security Misconfiguration: 4
- A06:2021 Vulnerable and Outdated Components: 2
- A07:2021 Identification and Authentication Failures: 6
- A08:2021 Software and Data Integrity Failures: 3
- A10:2021 Server-Side Request Forgery: 1

## Top findings
### [CRITICAL] SQL injection via string-built query — `Vuln.java:10` (CWE-89)
```
s.executeQuery("SELECT * FROM users WHERE name = '" + user + "'");
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] Insecure deserialisation — `Vuln.java:14` (CWE-502)
```
Object read(InputStream in) throws Exception { return new ObjectInputStream(in).readObject(); }
```
- **Why it matters:** Deserialising untrusted bytes can instantiate arbitrary objects and lead to remote code execution.
- **Fix:** Use JSON or yaml.safe_load; for Java apply ObjectInputFilter allow-lists.
- **Verification plan:** Deserialise a benign gadget that writes a marker file in a sandbox and confirm it executes.

### [CRITICAL] SQL injection via string-built query — `app.py:13` (CWE-89)
```
cur.execute("SELECT * FROM users WHERE name = '" + name + "'")
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] OS command injection — `app.py:20` (CWE-78)
```
os.system("ping -c 1 " + host)
```
- **Why it matters:** A shell command is built from dynamic input, enabling arbitrary command execution.
- **Fix:** Pass arguments as a list with shell=False (or execFile), validate against an allow-list.
- **Verification plan:** In a sandbox, supply a value containing a shell metacharacter plus a harmless marker command and check whether the marker executes.

### [CRITICAL] OS command injection — `app.py:26` (CWE-78)
```
subprocess.call("ls " + request.args["d"], shell=True)
```
- **Why it matters:** A shell command is built from dynamic input, enabling arbitrary command execution.
- **Fix:** Pass arguments as a list with shell=False (or execFile), validate against an allow-list.
- **Verification plan:** In a sandbox, supply a value containing a shell metacharacter plus a harmless marker command and check whether the marker executes.

```diff
--- a/app.py
+++ b/app.py
@@ -24,5 +24,5 @@
 @app.route("/run")
 def run():
-    subprocess.call("ls " + request.args["d"], shell=True)
+    subprocess.call("ls " + request.args["d"], shell=False)
     return "done"
```

### [CRITICAL] Insecure deserialisation — `app.py:42` (CWE-502)
```
obj = pickle.loads(request.data)
```
- **Why it matters:** Deserialising untrusted bytes can instantiate arbitrary objects and lead to remote code execution.
- **Fix:** Use JSON or yaml.safe_load; for Java apply ObjectInputFilter allow-lists.
- **Verification plan:** Deserialise a benign gadget that writes a marker file in a sandbox and confirm it executes.

### [CRITICAL] Insecure deserialisation — `app.py:43` (CWE-502)
```
cfg = yaml.load(request.data)
```
- **Why it matters:** Deserialising untrusted bytes can instantiate arbitrary objects and lead to remote code execution.
- **Fix:** Use JSON or yaml.safe_load; for Java apply ObjectInputFilter allow-lists.
- **Verification plan:** Deserialise a benign gadget that writes a marker file in a sandbox and confirm it executes.

```diff
--- a/app.py
+++ b/app.py
@@ -41,5 +41,5 @@
 def load():
     obj = pickle.loads(request.data)
-    cfg = yaml.load(request.data)
+    cfg = yaml.safe_load(request.data)
     return str((obj, cfg))
```

### [CRITICAL] Unbounded string copy (buffer overflow) — `parser.c:6` (CWE-120)
```
strcpy(buf, input);
```
- **Why it matters:** Unbounded libc copies write past the destination buffer when input exceeds its size.
- **Fix:** Use bounded variants (snprintf, strlcpy) with explicit sizes or -fbounds-safety annotations.
- **Verification plan:** Fuzz the entry point with oversized input under AddressSanitizer and confirm a stack/heap overflow report.

```diff
--- a/parser.c
+++ b/parser.c
@@ -4,5 +4,5 @@
 void handle(char *input) {
     char buf[64];
-    strcpy(buf, input);
+    strlcpy(buf, input);
     printf(input);
     sprintf(buf, "%s", input);
```

### [CRITICAL] Unbounded string copy (buffer overflow) — `parser.c:8` (CWE-120)
```
sprintf(buf, "%s", input);
```
- **Why it matters:** Unbounded libc copies write past the destination buffer when input exceeds its size.
- **Fix:** Use bounded variants (snprintf, strlcpy) with explicit sizes or -fbounds-safety annotations.
- **Verification plan:** Fuzz the entry point with oversized input under AddressSanitizer and confirm a stack/heap overflow report.

### [HIGH] Hard-coded credential / API key — `Vuln.java:7` (CWE-798)
```
String password = "hunter2hunter2";
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Weak cipher / ECB mode — `Vuln.java:13` (CWE-327)
```
Cipher cipher() throws Exception { return Cipher.getInstance("AES/ECB/PKCS5Padding"); }
```
- **Why it matters:** Deprecated or structurally weak encryption leaks plaintext patterns.
- **Fix:** Use AES-GCM or ChaCha20-Poly1305 with unique nonces from a KMS-managed key.
- **Verification plan:** Encrypt repeated plaintext blocks in a test and confirm identical ciphertext blocks appear.

### [HIGH] Hard-coded credential / API key — `app.py:5` (CWE-798)
```
DB_PASSWORD = "SuperSecret123!"
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

```diff
--- a/app.py
+++ b/app.py
@@ -3,5 +3,5 @@
 
 app = Flask(__name__)
-DB_PASSWORD = "SuperSecret123!"
+DB_PASSWORD = os.environ["SECRET_FROM_ENV"]
 AWS_KEY = "AKIAABCDEFGHIJKLMNOP"
```

### [HIGH] Hard-coded credential / API key — `app.py:6` (CWE-798)
```
AWS_KEY = "AKIAABCDEFGHIJKLMNOP"
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

```diff
--- a/app.py
+++ b/app.py
@@ -4,5 +4,5 @@
 app = Flask(__name__)
 DB_PASSWORD = "SuperSecret123!"
-AWS_KEY = "AKIAABCDEFGHIJKLMNOP"
+AWS_KEY = os.environ["SECRET_FROM_ENV"]
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `app.py:32` (CWE-79)
```
return render_template_string("<h1>Hello " + request.args["n"] + "</h1>")
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

### [HIGH] Path traversal in file access — `app.py:37` (CWE-22)
```
return send_file(os.path.join("/srv/files", request.args["f"]))
```
- **Why it matters:** A file path is derived from request input without canonicalisation or base-directory checks.
- **Fix:** Resolve the path, verify it stays under an allowed base directory, and use an ID-to-file mapping.
- **Verification plan:** Request a path containing parent-directory segments against a test file tree and confirm a file outside the base is returned.

### [HIGH] TLS certificate verification disabled — `app.py:49` (CWE-295)
```
return requests.get(request.args["url"], verify=False).text
```
- **Why it matters:** Disabling certificate validation permits man-in-the-middle interception.
- **Fix:** Remove the override and trust a proper CA bundle.
- **Verification plan:** Route the call through a proxy presenting a self-signed cert and confirm the connection succeeds.

```diff
--- a/app.py
+++ b/app.py
@@ -47,5 +47,5 @@
 @app.route("/fetch")
 def fetch():
-    return requests.get(request.args["url"], verify=False).text
+    return requests.get(request.args["url"], verify=True).text
```

### [HIGH] Server-side request forgery (SSRF) — `app.py:49` (CWE-918)
```
return requests.get(request.args["url"], verify=False).text
```
- **Why it matters:** The server fetches a URL controlled by the caller and can be pointed at internal services or metadata endpoints.
- **Fix:** Validate scheme/host against an allow-list and block link-local/private ranges.
- **Verification plan:** Point the parameter at a local canary listener and confirm the server connects to it.

### [HIGH] Format-string vulnerability — `parser.c:7` (CWE-134)
```
printf(input);
```
- **Why it matters:** A non-constant format string lets input read or write memory through %n / %s specifiers.
- **Fix:** Use a constant format: printf("%s", input).
- **Verification plan:** Pass %x sequences under ASan/UBSan and confirm leaked stack content.

### [HIGH] Hard-coded credential / API key — `server.js:5` (CWE-798)
```
const API_KEY = "demo-not-a-real-key-0123456789";
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] NoSQL / query operator injection — `server.js:8` (CWE-943)
```
db.collection("users").find(req.query).toArray((e, r) => res.json(r));
```
- **Why it matters:** Request objects are passed directly to a database query, allowing operator injection ($ne, $gt, $where).
- **Fix:** Validate and cast types explicitly; reject objects where scalars are expected.
- **Verification plan:** Send {"$ne": null} as a credential field in a test DB and confirm authentication bypass.

### [HIGH] Cross-site scripting (unsafe HTML sink) — `server.js:11` (CWE-79)
```
document.getElementById("out").innerHTML = req.query.name;
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/server.js
+++ b/server.js
@@ -9,5 +9,5 @@
 });
 app.get("/greet", (req, res) => {
-  document.getElementById("out").innerHTML = req.query.name;
+  document.getElementById("out").textContent = req.query.name;
   res.send("ok");
 });
```

### [HIGH] Code injection via eval/exec — `server.js:15` (CWE-95)
```
exec("zip -r out.zip " + req.query.dir, () => res.send("done"));
```
- **Why it matters:** Dynamic evaluation of strings can execute attacker-controlled code.
- **Fix:** Remove eval/exec; use ast.literal_eval or JSON parsing for data.
- **Verification plan:** Feed an expression with an observable side-effect marker in a sandbox and confirm evaluation.

### [HIGH] Code injection via eval/exec — `server.js:17` (CWE-95)
```
app.get("/calc", (req, res) => res.send(String(eval(req.query.expr))));
```
- **Why it matters:** Dynamic evaluation of strings can execute attacker-controlled code.
- **Fix:** Remove eval/exec; use ast.literal_eval or JSON parsing for data.
- **Verification plan:** Feed an expression with an observable side-effect marker in a sandbox and confirm evaluation.

### [HIGH] Path traversal in file access — `server.js:18` (CWE-22)
```
app.get("/file", (req, res) => res.send(require("fs").readFileSync("./uploads/" + req.query.name)));
```
- **Why it matters:** A file path is derived from request input without canonicalisation or base-directory checks.
- **Fix:** Resolve the path, verify it stays under an allowed base directory, and use an ID-to-file mapping.
- **Verification plan:** Request a path containing parent-directory segments against a test file tree and confirm a file outside the base is returned.

### [HIGH] JWT signature not verified / 'none' allowed — `server.js:20` (CWE-347)
```
const claims = jwt.decode(token, { algorithms: ["none"] });
```
- **Why it matters:** Tokens are accepted without cryptographic verification, letting anyone forge identities.
- **Fix:** Always verify signature, pin algorithms and enforce expiry.
- **Verification plan:** Submit an unsigned token with elevated claims and confirm acceptance in a test environment.

### [MEDIUM] Weak hash algorithm (MD5/SHA-1) — `Vuln.java:12` (CWE-328)
```
byte[] hash(byte[] d) throws Exception { return MessageDigest.getInstance("MD5").digest(d); }
```
- **Why it matters:** MD5/SHA-1 are collision-prone and unsuitable for security purposes such as password storage.
- **Fix:** Use SHA-256+ for integrity and Argon2/bcrypt/scrypt for passwords.
- **Verification plan:** Demonstrate collision/pre-image cost vs. modern hash using a test corpus; confirm use on a security path.

### [MEDIUM] Redirect to user-controlled URL — `app.py:54` (CWE-601)
```
return redirect(request.args.get("next"))
```
- **Why it matters:** Unvalidated redirect targets enable phishing via trusted domains.
- **Fix:** Allow only relative paths or an allow-list of hosts.
- **Verification plan:** Pass an external absolute URL and confirm a 3xx to that host.

### [MEDIUM] Insecure randomness for security token — `app.py:58` (CWE-338)
```
token = str(random.randint(100000, 999999))
```
- **Why it matters:** A predictable PRNG generates a value that must be unguessable.
- **Fix:** Use secrets.token_urlsafe / crypto.randomBytes / SecureRandom / crypto/rand.
- **Verification plan:** Seed-recover or enumerate generated values in a test harness to show predictability.

```diff
--- a/app.py
+++ b/app.py
@@ -56,5 +56,5 @@
 
 def make_reset_token():
-    token = str(random.randint(100000, 999999))
+    token = str(secrets.SystemRandom().choice(100000, 999999))
     return token
```

### [MEDIUM] Weak hash algorithm (MD5/SHA-1) — `app.py:63` (CWE-328)
```
return hashlib.md5(pw.encode()).hexdigest()
```
- **Why it matters:** MD5/SHA-1 are collision-prone and unsuitable for security purposes such as password storage.
- **Fix:** Use SHA-256+ for integrity and Argon2/bcrypt/scrypt for passwords.
- **Verification plan:** Demonstrate collision/pre-image cost vs. modern hash using a test corpus; confirm use on a security path.

```diff
--- a/app.py
+++ b/app.py
@@ -61,5 +61,5 @@
 
 def store_password(pw):
-    return hashlib.md5(pw.encode()).hexdigest()
+    return hashlib.sha256(pw.encode()).hexdigest()
```

### [MEDIUM] Debug mode / wildcard CORS enabled — `app.py:67` (CWE-489)
```
app.run(host="0.0.0.0", debug=True)
```
- **Why it matters:** Debug consoles or permissive CORS expose internals and authenticated endpoints to any origin.
- **Fix:** Disable debug in production; restrict CORS to known origins.
- **Verification plan:** Request an error page / cross-origin call and confirm debugger output or permissive headers are returned.

```diff
--- a/app.py
+++ b/app.py
@@ -65,3 +65,3 @@
 
 if __name__ == "__main__":
-    app.run(host="0.0.0.0", debug=True)
+    app.run(host="0.0.0.0", debug=False)
```

### [MEDIUM] Container / infra runs privileged or as root — `deployment.yaml:7` (CWE-250)
```
privileged: true
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

```diff
--- a/deployment.yaml
+++ b/deployment.yaml
@@ -5,4 +5,4 @@
     - name: app
       securityContext:
-        privileged: true
+        privileged: false
         runAsUser: 0
```

### [MEDIUM] Container / infra runs privileged or as root — `deployment.yaml:8` (CWE-250)
```
runAsUser: 0
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Debug mode / wildcard CORS enabled — `server.js:19` (CWE-489)
```
app.use(require("cors")({ origin: "*" }));
```
- **Why it matters:** Debug consoles or permissive CORS expose internals and authenticated endpoints to any origin.
- **Fix:** Disable debug in production; restrict CORS to known origins.
- **Verification plan:** Request an error page / cross-origin call and confirm debugger output or permissive headers are returned.


---
_Findings come from the engine named above. Verification plans describe how a finding would be confirmed; no exploit was run. Patches are suggestions that must be reviewed and tested before merge._