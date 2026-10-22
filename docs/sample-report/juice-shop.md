# CodeMender Security Analysis
**Repo:** https://github.com/juice-shop/juice-shop @ `shallow`  |  **Generated:** 2026-10-22 08:58 UTC
**Engine:** Built-in rule engine (CodeMender-style)

**Risk score:** 100/100 | **Findings:** 93 | **Auto-fixable:** 5 | **Files/Lines scanned:** 613/136940

| Critical | High | Medium | Low |
|---|---|---|---|
| 13 | 44 | 32 | 4 |

## OWASP Top 10 coverage
- A01:2021 Broken Access Control: 8
- A02:2021 Cryptographic Failures: 2
- A03:2021 Injection: 28
- A05:2021 Security Misconfiguration: 30
- A07:2021 Identification and Authentication Failures: 20
- A09:2021 Security Logging and Monitoring Failures: 4
- A10:2021 Server-Side Request Forgery: 1

## Top findings
### [CRITICAL] SQL injection via string-built query — `data/static/codefixes/dbSchemaChallenge_1.ts:5` (CWE-89)
```
models.sequelize.query("SELECT * FROM Products WHERE ((name LIKE '%"+criteria+"%' OR description LIKE '%"+criteria+"%') AND deletedAt IS NULL) ORDER BY name")
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] SQL injection via string-built query — `data/static/codefixes/dbSchemaChallenge_3.ts:11` (CWE-89)
```
models.sequelize.query(`SELECT * FROM Products WHERE ((name LIKE '%${criteria}%' OR description LIKE '%${criteria}%') AND deletedAt IS NULL) ORDER BY name`)
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] SQL injection via string-built query — `data/static/codefixes/loginAdminChallenge_1.ts:18` (CWE-89)
```
models.sequelize.query(`SELECT * FROM Users WHERE email = '${req.body.email || ''}' AND password = '${security.hash(req.body.password || '')}' AND deletedAt IS NULL`, { model: models.User, plain: true
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] SQL injection via string-built query — `data/static/codefixes/loginAdminChallenge_2.ts:15` (CWE-89)
```
models.sequelize.query(`SELECT * FROM Users WHERE email = $1 AND password = '${security.hash(req.body.password || '')}' AND deletedAt IS NULL`,
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] SQL injection via string-built query — `data/static/codefixes/loginBenderChallenge_1.ts:18` (CWE-89)
```
models.sequelize.query(`SELECT * FROM Users WHERE email = '${req.body.email || ''}' AND password = '${security.hash(req.body.password || '')}' AND deletedAt IS NULL`, { model: models.User, plain: true
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] SQL injection via string-built query — `data/static/codefixes/loginBenderChallenge_3.ts:15` (CWE-89)
```
models.sequelize.query(`SELECT * FROM Users WHERE email = :mail AND password = '${security.hash(req.body.password || '')}' AND deletedAt IS NULL`,
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] SQL injection via string-built query — `data/static/codefixes/loginBenderChallenge_4.ts:15` (CWE-89)
```
models.sequelize.query(`SELECT * FROM Users WHERE email = '${req.body.email || ''}' AND password = '${security.hash(req.body.password || '')}' AND deletedAt IS NULL`, { model: models.User, plain: fals
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] SQL injection via string-built query — `data/static/codefixes/loginJimChallenge_2.ts:15` (CWE-89)
```
models.sequelize.query(`SELECT * FROM Users WHERE email = '${req.body.email || ''}' AND password = '${security.hash(req.body.password || '')}' AND deletedAt IS NULL`, { model: models.User, plain: fals
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] SQL injection via string-built query — `data/static/codefixes/loginJimChallenge_4.ts:18` (CWE-89)
```
models.sequelize.query(`SELECT * FROM Users WHERE email = '${req.body.email || ''}' AND password = '${security.hash(req.body.password || '')}' AND deletedAt IS NULL`, { model: models.User, plain: true
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] SQL injection via string-built query — `data/static/codefixes/unionSqlInjectionChallenge_1.ts:6` (CWE-89)
```
models.sequelize.query(`SELECT * FROM Products WHERE ((name LIKE '%${criteria}%' OR description LIKE '%${criteria}%') AND deletedAt IS NULL) ORDER BY name`)
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] SQL injection via string-built query — `data/static/codefixes/unionSqlInjectionChallenge_3.ts:10` (CWE-89)
```
models.sequelize.query(`SELECT * FROM Products WHERE ((name LIKE '%${criteria}%' OR description LIKE '%${criteria}%') AND deletedAt IS NULL) ORDER BY name`)
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] SQL injection via string-built query — `routes/login.ts:34` (CWE-89)
```
models.sequelize.query(`SELECT * FROM Users WHERE email = '${req.body.email || ''}' AND password = '${security.hash(req.body.password || '')}' AND deletedAt IS NULL`, { model: UserModel, plain: true }
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [CRITICAL] SQL injection via string-built query — `routes/search.ts:23` (CWE-89)
```
models.sequelize.query(`SELECT * FROM Products WHERE ((name LIKE '%${criteria}%' OR description LIKE '%${criteria}%') AND deletedAt IS NULL) ORDER BY name`) // vuln-code-snippet vuln-line unionSqlInje
```
- **Why it matters:** User-influenced data is concatenated/interpolated into a SQL statement, allowing query manipulation.
- **Fix:** Use parameterised queries / prepared statements; never build SQL with string formatting.
- **Verification plan:** Send a quote-breaking value to the affected parameter in an isolated test DB and confirm the query structure changes or errors.

### [HIGH] NoSQL / query operator injection — `data/static/codefixes/chatbotGreedyInjectionChallenge_1.ts:65` (CWE-943)
```
return await db.reviewsCollection.find({ $where: 'this.product == ' + productId }) as Review[]
```
- **Why it matters:** Request objects are passed directly to a database query, allowing operator injection ($ne, $gt, $where).
- **Fix:** Validate and cast types explicitly; reject objects where scalars are expected.
- **Verification plan:** Send {"$ne": null} as a credential field in a test DB and confirm authentication bypass.

### [HIGH] NoSQL / query operator injection — `data/static/codefixes/chatbotGreedyInjectionChallenge_2_correct.ts:66` (CWE-943)
```
return await db.reviewsCollection.find({ $where: 'this.product == ' + productId }) as Review[]
```
- **Why it matters:** Request objects are passed directly to a database query, allowing operator injection ($ne, $gt, $where).
- **Fix:** Validate and cast types explicitly; reject objects where scalars are expected.
- **Verification plan:** Send {"$ne": null} as a credential field in a test DB and confirm authentication bypass.

### [HIGH] NoSQL / query operator injection — `data/static/codefixes/chatbotGreedyInjectionChallenge_3.ts:66` (CWE-943)
```
return await db.reviewsCollection.find({ $where: 'this.product == ' + productId }) as Review[]
```
- **Why it matters:** Request objects are passed directly to a database query, allowing operator injection ($ne, $gt, $where).
- **Fix:** Validate and cast types explicitly; reject objects where scalars are expected.
- **Verification plan:** Send {"$ne": null} as a credential field in a test DB and confirm authentication bypass.

### [HIGH] NoSQL / query operator injection — `data/static/codefixes/chatbotGreedyInjectionChallenge_4.ts:66` (CWE-943)
```
return await db.reviewsCollection.find({ $where: 'this.product == ' + productId }) as Review[]
```
- **Why it matters:** Request objects are passed directly to a database query, allowing operator injection ($ne, $gt, $where).
- **Fix:** Validate and cast types explicitly; reject objects where scalars are expected.
- **Verification plan:** Send {"$ne": null} as a credential field in a test DB and confirm authentication bypass.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:3` (CWE-798)
```
password: 'admin123'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:31` (CWE-798)
```
password: 'ncc-1701'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:63` (CWE-798)
```
password: 'OhG0dPlease1nsertLiquor!'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:88` (CWE-798)
```
password: 'bW9jLmxpYW1nQGhjaW5pbW1pay5ucmVvamI='
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:107` (CWE-798)
```
password: 'mDLx?94T~1CfVfZMzw@sJ9f?s3L6lbMqE70FfI8^54jbNikY5fymx7c!YbJb'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:115` (CWE-798)
```
password: 'J6aVjTgOpRs@?5l!Zkq2AYnCE@RF$P'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:123` (CWE-798)
```
password: 'focusOnScienceMorty!focusOnScience'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:141` (CWE-798)
```
password: '0Y8rMnww$*9VFYE§59-!Fg1L6t&6lB'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:150` (CWE-798)
```
password: 'EinBelegtesBrotMitSchinkenSCHINKEN!'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:159` (CWE-798)
```
password: 'K1f.....................'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:239` (CWE-798)
```
password: 'y&x5Z#f6W532Z4445#Ae2HkwZVyDb7&oCUaDzFU'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:245` (CWE-798)
```
password: 'y&x5Z#f6W532ZUf$q3DsdgfgfgxxUsvoCUaDzFU'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:261` (CWE-798)
```
password: 'private'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:272` (CWE-798)
```
password: 'IamUsedForTesting'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `data/static/users.yml:277` (CWE-798)
```
password: 'DVKH3gn7G$2Rk!f5Tz@9Lm&Qp4Wx#Yj8Bc0Ns6Ue1Io7Ah2Sd4Fg6Hj8Kl0Zx3Cv5Bn7Mq9Wr1Et3Yu5Ip'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/app/data-export/data-export.component.ts:72` (CWE-79)
```
window.open('', '_blank', 'width=500')?.document.write(this.userData)
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

### [HIGH] Hard-coded credential / API key — `frontend/src/app/faucet/faucet.component.ts:34` (CWE-798)
```
const BeeTokenAddress = '0x36435796Ca9be2bf150CE0dECc2D8Fab5C4d6E13'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `frontend/src/app/login/login.component.ts:69` (CWE-798)
```
public testingPassword = 'IamUsedForTesting'
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/three.js:11354` (CWE-79)
```
e.innerHTML = "Loading ...";
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/three.js
+++ b/frontend/src/assets/private/three.js
@@ -11352,5 +11352,5 @@
 		e.style.zIndex = 1000;
 
-		e.innerHTML = "Loading ...";
+		e.textContent = "Loading ...";
 
 		return e;
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/three.js:11375` (CWE-79)
```
this.statusDomElement.innerHTML = message;
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/three.js
+++ b/frontend/src/assets/private/three.js
@@ -11373,5 +11373,5 @@
 		}
 
-		this.statusDomElement.innerHTML = message;
+		this.statusDomElement.textContent = message;
 
 	},
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/hacking-instructor/helpers/helpers.ts:138` (CWE-79)
```
if (element && element.innerHTML === value) {
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/hacking-instructor/helpers/helpers.ts
+++ b/frontend/src/hacking-instructor/helpers/helpers.ts
@@ -136,5 +136,5 @@
       )
 
-      if (element && element.innerHTML === value) {
+      if (element && element.textContent === value) {
         break
       }
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/hacking-instructor/index.ts:126` (CWE-79)
```
textBox.innerHTML = snarkdown(hint.text)
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/hacking-instructor/index.ts
+++ b/frontend/src/hacking-instructor/index.ts
@@ -124,5 +124,5 @@
 
   const textBox = createElement('span', { flexGrow: '2' })
-  textBox.innerHTML = snarkdown(hint.text)
+  textBox.textContent = snarkdown(hint.text)
 
   const cancelButtonStyles = {
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/hacking-instructor/index.ts:142` (CWE-79)
```
cancelButton.innerHTML = '<div>&times;</div>'
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/hacking-instructor/index.ts
+++ b/frontend/src/hacking-instructor/index.ts
@@ -140,5 +140,5 @@
 
   const cancelButton = createElement('button', cancelButtonStyles, { id: 'cancelButton', title: 'Cancel the tutorial' })
-  cancelButton.innerHTML = '<div>&times;</div>'
+  cancelButton.textContent = '<div>&times;</div>'
 
   elem.appendChild(picture)
```

### [HIGH] Hard-coded credential / API key — `infrastructure/terraform/networking.tf:171` (CWE-798)
```
private_key      = "-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQDNwqLEe9wgTXCbC7+RPdDbBbeqjdbs4kOPOIGzqLpXvJXlxxW8\niMz0EaM4BKUqYsIa+ndv3NAn2RxCd5ubVdJJcX43zO6Ko0TFEZx/65gY3BE0O6sy\nCEmUP4qbSd6exou
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Hard-coded credential / API key — `lib/insecurity.ts:21` (CWE-798)
```
const privateKey = '-----BEGIN RSA PRIVATE KEY-----\r\nMIICXAIBAAKBgQDNwqLEe9wgTXCbC7+RPdDbBbeqjdbs4kOPOIGzqLpXvJXlxxW8iMz0EaM4BKUqYsIa+ndv3NAn2RxCd5ubVdJJcX43zO6Ko0TFEZx/65gY3BE0O6syCEmUP4qbSd6exou/F
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [HIGH] Code injection via eval/exec — `routes/captcha.ts:22` (CWE-95)
```
const answer = eval(expression).toString() // eslint-disable-line no-eval
```
- **Why it matters:** Dynamic evaluation of strings can execute attacker-controlled code.
- **Fix:** Remove eval/exec; use ast.literal_eval or JSON parsing for data.
- **Verification plan:** Feed an expression with an observable side-effect marker in a sandbox and confirm evaluation.

### [HIGH] NoSQL / query operator injection — `routes/chat.ts:149` (CWE-943)
```
return await db.reviewsCollection.find({ $where: 'this.product == ' + productId }) as Review[]
```
- **Why it matters:** Request objects are passed directly to a database query, allowing operator injection ($ne, $gt, $where).
- **Fix:** Validate and cast types explicitly; reject objects where scalars are expected.
- **Verification plan:** Send {"$ne": null} as a credential field in a test DB and confirm authentication bypass.

### [HIGH] Path traversal in file access — `routes/languages.ts:31` (CWE-22)
```
const content = await readFile('frontend/dist/frontend/assets/i18n/' + fileName, 'utf-8')
```
- **Why it matters:** A file path is derived from request input without canonicalisation or base-directory checks.
- **Fix:** Resolve the path, verify it stays under an allowed base directory, and use an ID-to-file mapping.
- **Verification plan:** Request a path containing parent-directory segments against a test file tree and confirm a file outside the base is returned.

### [HIGH] Path traversal in file access — `routes/languages.ts:40` (CWE-22)
```
const backendContent = await readFile('i18n/' + fileName, 'utf-8')
```
- **Why it matters:** A file path is derived from request input without canonicalisation or base-directory checks.
- **Fix:** Resolve the path, verify it stays under an allowed base directory, and use an ID-to-file mapping.
- **Verification plan:** Request a path containing parent-directory segments against a test file tree and confirm a file outside the base is returned.

### [HIGH] Server-side request forgery (SSRF) — `routes/profileImageUrlUpload.ts:24` (CWE-918)
```
const response = await fetch(url)
```
- **Why it matters:** The server fetches a URL controlled by the caller and can be pointed at internal services or metadata endpoints.
- **Fix:** Validate scheme/host against an allow-list and block link-local/private ranges.
- **Verification plan:** Point the parameter at a local canary listener and confirm the server connects to it.

### [HIGH] NoSQL / query operator injection — `routes/showProductReviews.ts:36` (CWE-943)
```
db.reviewsCollection.find({ $where: 'this.product == ' + id }).then((reviews: Review[]) => {
```
- **Why it matters:** Request objects are passed directly to a database query, allowing operator injection ($ne, $gt, $where).
- **Fix:** Validate and cast types explicitly; reject objects where scalars are expected.
- **Verification plan:** Send {"$ne": null} as a credential field in a test DB and confirm authentication bypass.

### [HIGH] NoSQL / query operator injection — `routes/trackOrder.ts:18` (CWE-943)
```
db.ordersCollection.find({ $where: `this.orderId === '${id}'` }).then((order: any) => {
```
- **Why it matters:** Request objects are passed directly to a database query, allowing operator injection ($ne, $gt, $where).
- **Fix:** Validate and cast types explicitly; reject objects where scalars are expected.
- **Verification plan:** Send {"$ne": null} as a credential field in a test DB and confirm authentication bypass.

### [HIGH] Code injection via eval/exec — `routes/userProfile.ts:65` (CWE-95)
```
username = eval(code) // eslint-disable-line no-eval
```
- **Why it matters:** Dynamic evaluation of strings can execute attacker-controlled code.
- **Fix:** Remove eval/exec; use ast.literal_eval or JSON parsing for data.
- **Verification plan:** Feed an expression with an observable side-effect marker in a sandbox and confirm evaluation.

### [HIGH] Path traversal in file access — `routes/videoHandler.ts:82` (CWE-22)
```
const data = fs.readFileSync('frontend/dist/frontend/assets/public/videos/' + subtitles, 'utf8')
```
- **Why it matters:** A file path is derived from request input without canonicalisation or base-directory checks.
- **Fix:** Resolve the path, verify it stays under an allowed base directory, and use an ID-to-file mapping.
- **Verification plan:** Request a path containing parent-directory segments against a test file tree and confirm a file outside the base is returned.

### [HIGH] Path traversal in file access — `routes/vulnCodeFixes.ts:30` (CWE-22)
```
const content = fs.readFileSync(`${FixesDir}/${file}`).toString()
```
- **Why it matters:** A file path is derived from request input without canonicalisation or base-directory checks.
- **Fix:** Resolve the path, verify it stays under an allowed base directory, and use an ID-to-file mapping.
- **Verification plan:** Request a path containing parent-directory segments against a test file tree and confirm a file outside the base is returned.

### [HIGH] Path traversal in file access — `routes/vulnCodeFixes.ts:83` (CWE-22)
```
const codingChallengeInfos = yaml.load(fs.readFileSync('./data/static/codefixes/' + key + '.info.yml', 'utf8'))
```
- **Why it matters:** A file path is derived from request input without canonicalisation or base-directory checks.
- **Fix:** Resolve the path, verify it stays under an allowed base directory, and use an ID-to-file mapping.
- **Verification plan:** Request a path containing parent-directory segments against a test file tree and confirm a file outside the base is returned.

### [HIGH] Path traversal in file access — `routes/vulnCodeSnippet.ts:90` (CWE-22)
```
const codingChallengeInfos = yaml.load(await fs.readFile('./data/static/codefixes/' + key + '.info.yml', { encoding: 'utf8' }))
```
- **Why it matters:** A file path is derived from request input without canonicalisation or base-directory checks.
- **Fix:** Resolve the path, verify it stays under an allowed base directory, and use an ID-to-file mapping.
- **Verification plan:** Request a path containing parent-directory segments against a test file tree and confirm a file outside the base is returned.

### [HIGH] Path traversal in file access — `rsn/rsnUtil.ts:66` (CWE-22)
```
const fileData = fs.readFileSync(fixesPath + '/' + val).toString()
```
- **Why it matters:** A file path is derived from request input without canonicalisation or base-directory checks.
- **Fix:** Resolve the path, verify it stays under an allowed base directory, and use an ID-to-file mapping.
- **Verification plan:** Request a path containing parent-directory segments against a test file tree and confirm a file outside the base is returned.

### [HIGH] Path traversal in file access — `rsn/rsnUtil.ts:155` (CWE-22)
```
const fileData = fs.readFileSync(fixesPath + '/' + file).toString()
```
- **Why it matters:** A file path is derived from request input without canonicalisation or base-directory checks.
- **Fix:** Resolve the path, verify it stays under an allowed base directory, and use an ID-to-file mapping.
- **Verification plan:** Request a path containing parent-directory segments against a test file tree and confirm a file outside the base is returned.

### [HIGH] Hard-coded credential / API key — `terraform/networking.tf:171` (CWE-798)
```
private_key      = "-----BEGIN RSA PRIVATE KEY-----\nMIICXAIBAAKBgQDNwqLEe9wgTXCbC7+RPdDbBbeqjdbs4kOPOIGzqLpXvJXlxxW8\niMz0EaM4BKUqYsIa+ndv3NAn2RxCd5ubVdJJcX43zO6Ko0TFEZx/65gY3BE0O6sy\nCEmUP4qbSd6exou
```
- **Why it matters:** A secret is embedded in source and will leak via version control, logs and build artifacts.
- **Fix:** Rotate the secret immediately; load from Secret Manager / environment at runtime.
- **Verification plan:** Confirm the value is live using a read-only identity check in a controlled setting, then rotate.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_1.tf:45` (CWE-250)
```
cidr_block = "0.0.0.0/0"
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_1.tf:71` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_1.tf:78` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_1.tf:85` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_1.tf:111` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_1.tf:238` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_2.tf:45` (CWE-250)
```
cidr_block = "0.0.0.0/0"
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_2.tf:71` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_2.tf:78` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_2.tf:85` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_2.tf:111` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_2.tf:238` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_3_correct.tf:45` (CWE-250)
```
cidr_block = "0.0.0.0/0"
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_3_correct.tf:71` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_3_correct.tf:78` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_3_correct.tf:85` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_3_correct.tf:111` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `data/static/codefixes/iacLeakedKeyChallenge_3_correct.tf:238` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `infrastructure/terraform/networking.tf:46` (CWE-250)
```
cidr_block = "0.0.0.0/0"
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `infrastructure/terraform/networking.tf:72` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `infrastructure/terraform/networking.tf:79` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `infrastructure/terraform/networking.tf:86` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `infrastructure/terraform/networking.tf:112` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `infrastructure/terraform/networking.tf:239` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Weak hash algorithm (MD5/SHA-1) — `lib/insecurity.ts:41` (CWE-328)
```
export const hash = (data: string) => crypto.createHash('md5').update(data).digest('hex')
```
- **Why it matters:** MD5/SHA-1 are collision-prone and unsuitable for security purposes such as password storage.
- **Fix:** Use SHA-256+ for integrity and Argon2/bcrypt/scrypt for passwords.
- **Verification plan:** Demonstrate collision/pre-image cost vs. modern hash using a test corpus; confirm use on a security path.

### [MEDIUM] Weak hash algorithm (MD5/SHA-1) — `scripts/package.mjs:121` (CWE-328)
```
const hash = crypto.createHash('md5').update(content).digest('hex')
```
- **Why it matters:** MD5/SHA-1 are collision-prone and unsuitable for security purposes such as password storage.
- **Fix:** Use SHA-256+ for integrity and Argon2/bcrypt/scrypt for passwords.
- **Verification plan:** Demonstrate collision/pre-image cost vs. modern hash using a test corpus; confirm use on a security path.

### [MEDIUM] Container / infra runs privileged or as root — `terraform/networking.tf:46` (CWE-250)
```
cidr_block = "0.0.0.0/0"
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `terraform/networking.tf:72` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `terraform/networking.tf:79` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `terraform/networking.tf:86` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `terraform/networking.tf:112` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [MEDIUM] Container / infra runs privileged or as root — `terraform/networking.tf:239` (CWE-250)
```
cidr_blocks = ["0.0.0.0/0"]
```
- **Why it matters:** Over-privileged workload or world-open network rule increases blast radius.
- **Fix:** Drop privileges, set runAsNonRoot and restrict CIDR ranges.
- **Verification plan:** Inspect the rendered manifest/plan with a policy engine to confirm the privileged setting.

### [LOW] Sensitive data written to logs — `data/datacreator.ts:278` (CWE-532)
```
logger.error(`Could not create card: ${utils.getErrorMessage(err)}`)
```
- **Why it matters:** Credentials or personal data in logs persist in log stores with broader access.
- **Fix:** Redact sensitive fields before logging.
- **Verification plan:** Exercise the flow and grep emitted logs for the test credential.

### [LOW] Sensitive data written to logs — `frontend/src/app/faucet/faucet.component.ts:239` (CWE-532)
```
console.log('BEE tokens extracted successfully')
```
- **Why it matters:** Credentials or personal data in logs persist in log stores with broader access.
- **Fix:** Redact sensitive fields before logging.
- **Verification plan:** Exercise the flow and grep emitted logs for the test credential.

### [LOW] Sensitive data written to logs — `frontend/src/hacking-instructor/helpers/helpers.ts:191` (CWE-532)
```
console.log('Role from token could not be accessed.')
```
- **Why it matters:** Credentials or personal data in logs persist in log stores with broader access.
- **Fix:** Redact sensitive fields before logging.
- **Verification plan:** Exercise the flow and grep emitted logs for the test credential.

### [LOW] Sensitive data written to logs — `routes/chat.ts:255` (CWE-532)
```
logger.warn('Failed to record chat token usage metrics: ' + summarizeLlmError(metricError))
```
- **Why it matters:** Credentials or personal data in logs persist in log stores with broader access.
- **Fix:** Redact sensitive fields before logging.
- **Verification plan:** Exercise the flow and grep emitted logs for the test credential.


---
_Findings come from the engine named above. Verification plans describe how a finding would be confirmed; no exploit was run. Patches are suggestions that must be reviewed and tested before merge. Test folders and test files (test, tests, spec, e2e, cypress, fixtures, *.spec.*, *.test.*, minified files) and vendored/build folders are not scanned._