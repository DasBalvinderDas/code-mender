# CodeMender Security Analysis
**Repo:** https://github.com/juice-shop/juice-shop @ `shallow`  |  **Generated:** 2026-10-22 08:57 UTC
**Engine:** Built-in rule engine (CodeMender-style)

**Risk score:** 100/100 | **Findings:** 107 | **Auto-fixable:** 19 | **Files/Lines scanned:** 615/137028

| Critical | High | Medium | Low |
|---|---|---|---|
| 13 | 58 | 32 | 4 |

## OWASP Top 10 coverage
- A01:2021 Broken Access Control: 8
- A02:2021 Cryptographic Failures: 2
- A03:2021 Injection: 42
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

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/dat.gui.min.js:1` (CWE-79)
```
var dat=dat||{};dat.gui=dat.gui||{};dat.utils=dat.utils||{};dat.controllers=dat.controllers||{};dat.dom=dat.dom||{};dat.color=dat.color||{};dat.utils.css=function(){return{load:function(e,a){a=a||docu
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/dat.gui.min.js
+++ b/frontend/src/assets/private/dat.gui.min.js
@@ -1,3 +1,3 @@
-var dat=dat||{};dat.gui=dat.gui||{};dat.utils=dat.utils||{};dat.controllers=dat.controllers||{};dat.dom=dat.dom||{};dat.color=dat.color||{};dat.utils.css=function(){return{load:function(e,a){a=a||document;var b=a.createElement("link");b.type="text/css";b.rel="stylesheet";b.href=e;a.getElementsByTagName("head")[0].appendChild(b)},inject:function(e,a){a=a||document;var b=document.createElement("style");b.type="text/css";b.innerHTML=e;a.getElementsByTagName("head")[0].appendChild(b)}}}();
+var dat=dat||{};dat.gui=dat.gui||{};dat.utils=dat.utils||{};dat.controllers=dat.controllers||{};dat.dom=dat.dom||{};dat.color=dat.color||{};dat.utils.css=function(){return{load:function(e,a){a=a||document;var b=a.createElement("link");b.type="text/css";b.rel="stylesheet";b.href=e;a.getElementsByTagName("head")[0].appendChild(b)},inject:function(e,a){a=a||document;var b=document.createElement("style");b.type="text/css";b.textContent =e;a.getElementsByTagName("head")[0].appendChild(b)}}}();
 dat.utils.common=function(){var e=Array.prototype.forEach,a=Array.prototype.slice;return{BREAK:{},extend:function(b){this.each(a.call(arguments,1),function(a){for(var f in a)this.isUndefined(a[f])||(b[f]=a[f])},this);return b},defaults:function(b){this.each(a.call(arguments,1),function(a){for(var f in a)this.isUndefined(b[f])&&(b[f]=a[f])},this);return b},compose:function(){var b=a.call(arguments);return function(){for(var d=a.call(arguments),f=b.length-1;0<=f;f--)d=[b[f].apply(this,d)];return d[0]}},
     each:function(a,d,f){if(e&&a.forEach===e)a.forEach(d,f);else if(a.length===a.length+0)for(var c=0,p=a.length;c<p&&!(c in a&&d.call(f,a[c],c)===this.BREAK);c++);else for(c in a)if(d.call(f,a[c],c)===this.BREAK)break},defer:function(a){setTimeout(a,0)},toArray:function(b){return b.toArray?b.toArray():a.call(b)},isUndefined:function(a){return void 0===a},isNull:function(a){return null===a},isNaN:function(a){return a!==a},isArray:Array.isArray||function(a){return a.constructor===Array},isObject:function(a){return a===
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/dat.gui.min.js:13` (CWE-79)
```
dat.controllers.OptionController=function(e,a,b){var d=function(f,c,e){d.superclass.call(this,f,c);var k=this;this.__select=document.createElement("select");if(b.isArray(e)){var l={};b.each(e,function
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/dat.gui.min.js
+++ b/frontend/src/assets/private/dat.gui.min.js
@@ -11,5 +11,5 @@
         e&&(b.splice(e,1),a.className=b.join(" "))}}else a.className=void 0;return f},hasClass:function(a,d){return RegExp("(?:^|\\s+)"+d+"(?:\\s+|$)").test(a.className)||!1},getWidth:function(c){c=getComputedStyle(c);return a(c["border-left-width"])+a(c["border-right-width"])+a(c["padding-left"])+a(c["padding-right"])+a(c.width)},getHeight:function(c){c=getComputedStyle(c);return a(c["border-top-width"])+a(c["border-bottom-width"])+a(c["padding-top"])+a(c["padding-bottom"])+a(c.height)},getOffset:function(a){var d=
     {left:0,top:0};if(a.offsetParent){do d.left+=a.offsetLeft,d.top+=a.offsetTop;while(a=a.offsetParent)}return d},isActive:function(a){return a===document.activeElement&&(a.type||a.href)}};return f}(dat.utils.common);
-dat.controllers.OptionController=function(e,a,b){var d=function(f,c,e){d.superclass.call(this,f,c);var k=this;this.__select=document.createElement("select");if(b.isArray(e)){var l={};b.each(e,function(a){l[a]=a});e=l}b.each(e,function(a,c){var d=document.createElement("option");d.innerHTML=c;d.setAttribute("value",a);k.__select.appendChild(d)});this.updateDisplay();a.bind(this.__select,"change",function(){k.setValue(this.options[this.selectedIndex].value)});this.domElement.appendChild(this.__select)};
+dat.controllers.OptionController=function(e,a,b){var d=function(f,c,e){d.superclass.call(this,f,c);var k=this;this.__select=document.createElement("select");if(b.isArray(e)){var l={};b.each(e,function(a){l[a]=a});e=l}b.each(e,function(a,c){var d=document.createElement("option");d.textContent =c;d.setAttribute("value",a);k.__select.appendChild(d)});this.updateDisplay();a.bind(this.__select,"change",function(){k.setValue(this.options[this.selectedIndex].value)});this.domElement.appendChild(this.__select)};
     d.superclass=e;b.extend(d.prototype,e.prototype,{setValue:function(a){a=d.superclass.prototype.setValue.call(this,a);this.__onFinishChange&&this.__onFinishChange.call(this,this.getValue());return a},updateDisplay:function(){this.__select.value=this.getValue();return d.superclass.prototype.updateDisplay.call(this)}});return d}(dat.controllers.Controller,dat.dom.dom,dat.utils.common);
 dat.controllers.NumberController=function(e,a){var b=function(d,f,c){b.superclass.call(this,d,f);c=c||{};this.__min=c.min;this.__max=c.max;this.__step=c.step;a.isUndefined(this.__step)?this.__impliedStep=0==this.initialValue?1:Math.pow(10,Math.floor(Math.log(this.initialValue)/Math.LN10))/10:this.__impliedStep=this.__step;d=this.__impliedStep;d=d.toString();d=-1<d.indexOf(".")?d.length-d.indexOf(".")-1:0;this.__precision=d};b.superclass=e;a.extend(b.prototype,e.prototype,{setValue:function(a){void 0!==
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/dat.gui.min.js:23` (CWE-79)
```
dat.controllers.FunctionController=function(e,a,b){var d=function(b,c,e){d.superclass.call(this,b,c);var k=this;this.__button=document.createElement("div");this.__button.innerHTML=void 0===e?"Fire":e;
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/dat.gui.min.js
+++ b/frontend/src/assets/private/dat.gui.min.js
@@ -21,5 +21,5 @@
     document.createElement("div");this.__foreground=document.createElement("div");a.bind(this.__background,"mousedown",function(c){a.bind(window,"mousemove",y);a.bind(window,"mouseup",g);y(c)});a.addClass(this.__background,"slider");a.addClass(this.__foreground,"slider-fg");this.updateDisplay();this.__background.appendChild(this.__foreground);this.domElement.appendChild(this.__background)};p.superclass=e;p.useDefaultStyles=function(){b.inject(f)};d.extend(p.prototype,e.prototype,{updateDisplay:function(){var a=
     (this.getValue()-this.__min)/(this.__max-this.__min);this.__foreground.style.width=100*a+"%";return p.superclass.prototype.updateDisplay.call(this)}});return p}(dat.controllers.NumberController,dat.dom.dom,dat.utils.css,dat.utils.common,"/**\n * dat-gui JavaScript Controller Library\n * http://code.google.com/p/dat-gui\n *\n * Copyright 2011 Data Arts Team, Google Creative Lab\n *\n * Licensed under the Apache License, Version 2.0 (the \"License\");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n * http://www.apache.org/licenses/LICENSE-2.0\n */\n\n.slider {\n  box-shadow: inset 0 2px 4px rgba(0,0,0,0.15);\n  height: 1em;\n  border-radius: 1em;\n  background-color: #eee;\n  padding: 0 0.5em;\n  overflow: hidden;\n}\n\n.slider-fg {\n  padding: 1px 0 2px 0;\n  background-color: #aaa;\n  height: 1em;\n  margin-left: -0.5em;\n  padding-right: 0.5em;\n  border-radius: 1em 0 0 1em;\n}\n\n.slider-fg:after {\n  display: inline-block;\n  border-radius: 1em;\n  background-color: #fff;\n  border:  1px solid #aaa;\n  content: '';\n  float: right;\n  margin-right: -1em;\n  margin-top: -1px;\n  height: 0.9em;\n  width: 0.9em;\n}");
-dat.controllers.FunctionController=function(e,a,b){var d=function(b,c,e){d.superclass.call(this,b,c);var k=this;this.__button=document.createElement("div");this.__button.innerHTML=void 0===e?"Fire":e;a.bind(this.__button,"click",function(a){a.preventDefault();k.fire();return!1});a.addClass(this.__button,"button");this.domElement.appendChild(this.__button)};d.superclass=e;b.extend(d.prototype,e.prototype,{fire:function(){this.__onChange&&this.__onChange.call(this);this.__onFinishChange&&this.__onFinishChange.call(this,
+dat.controllers.FunctionController=function(e,a,b){var d=function(b,c,e){d.superclass.call(this,b,c);var k=this;this.__button=document.createElement("div");this.__button.textContent =void 0===e?"Fire":e;a.bind(this.__button,"click",function(a){a.preventDefault();k.fire();return!1});a.addClass(this.__button,"button");this.domElement.appendChild(this.__button)};d.superclass=e;b.extend(d.prototype,e.prototype,{fire:function(){this.__onChange&&this.__onChange.call(this);this.__onFinishChange&&this.__onFinishChange.call(this,
     this.getValue());this.getValue().call(this.object)}});return d}(dat.controllers.Controller,dat.dom.dom,dat.utils.common);
 dat.controllers.BooleanController=function(e,a,b){var d=function(b,c){d.superclass.call(this,b,c);var e=this;this.__prev=this.getValue();this.__checkbox=document.createElement("input");this.__checkbox.setAttribute("type","checkbox");a.bind(this.__checkbox,"change",function(){e.setValue(!e.__prev)},!1);this.domElement.appendChild(this.__checkbox);this.updateDisplay()};d.superclass=e;b.extend(d.prototype,e.prototype,{setValue:function(a){a=d.superclass.prototype.setValue.call(this,a);this.__onFinishChange&&
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/dat.gui.min.js:33` (CWE-79)
```
dat.GUI=dat.gui.GUI=function(e,a,b,d,f,c,p,k,l,q,n,r,y,g,h){function t(a,c,b,e){if(void 0===c[b])throw Error("Object "+c+' has no property "'+b+'"');e.color?c=new n(c,b):(c=[c,b].concat(e.factoryArgs)
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/dat.gui.min.js
+++ b/frontend/src/assets/private/dat.gui.min.js
@@ -31,5 +31,5 @@
     a.isNumber(c.g)&&a.isNumber(c.b)?{space:"RGB",r:c.r,g:c.g,b:c.b}:!1},write:function(a){return{r:a.r,g:a.g,b:a.b}}},HSVA_OBJ:{read:function(c){return a.isNumber(c.h)&&a.isNumber(c.s)&&a.isNumber(c.v)&&a.isNumber(c.a)?{space:"HSV",h:c.h,s:c.s,v:c.v,a:c.a}:!1},write:function(a){return{h:a.h,s:a.s,v:a.v,a:a.a}}},HSV_OBJ:{read:function(d){return a.isNumber(d.h)&&a.isNumber(d.s)&&a.isNumber(d.v)?{space:"HSV",h:d.h,s:d.s,v:d.v}:!1},write:function(a){return{h:a.h,s:a.s,v:a.v}}}}}];return function(){d=!1;
     var c=1<arguments.length?a.toArray(arguments):arguments[0];a.each(f,function(e){if(e.litmus(c))return a.each(e.conversions,function(e,f){b=e.read(c);if(!1===d&&!1!==b)return d=b,b.conversionName=f,b.conversion=e,a.BREAK}),a.BREAK});return d}}(dat.color.toString,dat.utils.common);
-dat.GUI=dat.gui.GUI=function(e,a,b,d,f,c,p,k,l,q,n,r,y,g,h){function t(a,c,b,e){if(void 0===c[b])throw Error("Object "+c+' has no property "'+b+'"');e.color?c=new n(c,b):(c=[c,b].concat(e.factoryArgs),c=d.apply(a,c));e.before instanceof f&&(e.before=e.before.__li);v(a,c);g.addClass(c.domElement,"c");b=document.createElement("span");g.addClass(b,"property-name");b.innerHTML=c.property;var q=document.createElement("div");q.appendChild(b);q.appendChild(c.domElement);e=u(a,q,e.before);g.addClass(e,m.CLASS_CONTROLLER_ROW);
+dat.GUI=dat.gui.GUI=function(e,a,b,d,f,c,p,k,l,q,n,r,y,g,h){function t(a,c,b,e){if(void 0===c[b])throw Error("Object "+c+' has no property "'+b+'"');e.color?c=new n(c,b):(c=[c,b].concat(e.factoryArgs),c=d.apply(a,c));e.before instanceof f&&(e.before=e.before.__li);v(a,c);g.addClass(c.domElement,"c");b=document.createElement("span");g.addClass(b,"property-name");b.textContent =c.property;var q=document.createElement("div");q.appendChild(b);q.appendChild(c.domElement);e=u(a,q,e.before);g.addClass(e,m.CLASS_CONTROLLER_ROW);
     g.addClass(e,typeof c.getValue());s(a,e,c);a.__controllers.push(c);return c}function u(a,d,c){var b=document.createElement("li");d&&b.appendChild(d);c?a.__ul.insertBefore(b,params.before):a.__ul.appendChild(b);a.onResize();return b}function s(a,d,b){b.__li=d;b.__gui=a;h.extend(b,{options:function(d){if(1<arguments.length)return b.remove(),t(a,b.object,b.property,{before:b.__li.nextElementSibling,factoryArgs:[h.toArray(arguments)]});if(h.isArray(d)||h.isObject(d))return b.remove(),t(a,b.object,b.property,
     {before:b.__li.nextElementSibling,factoryArgs:[d]})},name:function(a){b.__li.firstElementChild.firstElementChild.innerHTML=a;return b},listen:function(){b.__gui.listen(b);return b},remove:function(){b.__gui.remove(b);return b}});if(b instanceof l){var e=new k(b.object,b.property,{min:b.__min,max:b.__max,step:b.__step});h.each(["updateDisplay","onChange","onFinishChange"],function(a){var d=b[a],J=e[a];b[a]=e[a]=function(){var a=Array.prototype.slice.call(arguments);d.apply(b,a);return J.apply(e,a)}});
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/dat.gui.min.js:35` (CWE-79)
```
{before:b.__li.nextElementSibling,factoryArgs:[d]})},name:function(a){b.__li.firstElementChild.firstElementChild.innerHTML=a;return b},listen:function(){b.__gui.listen(b);return b},remove:function(){b
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/dat.gui.min.js
+++ b/frontend/src/assets/private/dat.gui.min.js
@@ -33,5 +33,5 @@
 dat.GUI=dat.gui.GUI=function(e,a,b,d,f,c,p,k,l,q,n,r,y,g,h){function t(a,c,b,e){if(void 0===c[b])throw Error("Object "+c+' has no property "'+b+'"');e.color?c=new n(c,b):(c=[c,b].concat(e.factoryArgs),c=d.apply(a,c));e.before instanceof f&&(e.before=e.before.__li);v(a,c);g.addClass(c.domElement,"c");b=document.createElement("span");g.addClass(b,"property-name");b.innerHTML=c.property;var q=document.createElement("div");q.appendChild(b);q.appendChild(c.domElement);e=u(a,q,e.before);g.addClass(e,m.CLASS_CONTROLLER_ROW);
     g.addClass(e,typeof c.getValue());s(a,e,c);a.__controllers.push(c);return c}function u(a,d,c){var b=document.createElement("li");d&&b.appendChild(d);c?a.__ul.insertBefore(b,params.before):a.__ul.appendChild(b);a.onResize();return b}function s(a,d,b){b.__li=d;b.__gui=a;h.extend(b,{options:function(d){if(1<arguments.length)return b.remove(),t(a,b.object,b.property,{before:b.__li.nextElementSibling,factoryArgs:[h.toArray(arguments)]});if(h.isArray(d)||h.isObject(d))return b.remove(),t(a,b.object,b.property,
-    {before:b.__li.nextElementSibling,factoryArgs:[d]})},name:function(a){b.__li.firstElementChild.firstElementChild.innerHTML=a;return b},listen:function(){b.__gui.listen(b);return b},remove:function(){b.__gui.remove(b);return b}});if(b instanceof l){var e=new k(b.object,b.property,{min:b.__min,max:b.__max,step:b.__step});h.each(["updateDisplay","onChange","onFinishChange"],function(a){var d=b[a],J=e[a];b[a]=e[a]=function(){var a=Array.prototype.slice.call(arguments);d.apply(b,a);return J.apply(e,a)}});
+    {before:b.__li.nextElementSibling,factoryArgs:[d]})},name:function(a){b.__li.firstElementChild.firstElementChild.textContent =a;return b},listen:function(){b.__gui.listen(b);return b},remove:function(){b.__gui.remove(b);return b}});if(b instanceof l){var e=new k(b.object,b.property,{min:b.__min,max:b.__max,step:b.__step});h.each(["updateDisplay","onChange","onFinishChange"],function(a){var d=b[a],J=e[a];b[a]=e[a]=function(){var a=Array.prototype.slice.call(arguments);d.apply(b,a);return J.apply(e,a)}});
     g.addClass(d,"has-slider");b.domElement.insertBefore(e.domElement,b.domElement.firstElementChild)}else if(b instanceof k){var f=function(d){return h.isNumber(b.__min)&&h.isNumber(b.__max)?(b.remove(),t(a,b.object,b.property,{before:b.__li.nextElementSibling,factoryArgs:[b.__min,b.__max,b.__step]})):d};b.min=h.compose(f,b.min);b.max=h.compose(f,b.max)}else b instanceof c?(g.bind(d,"click",function(){g.fakeEvent(b.__checkbox,"click")}),g.bind(b.__checkbox,"click",function(a){a.stopPropagation()})):
     b instanceof p?(g.bind(d,"click",function(){g.fakeEvent(b.__button,"click")}),g.bind(d,"mouseover",function(){g.addClass(b.__button,"hover")}),g.bind(d,"mouseout",function(){g.removeClass(b.__button,"hover")})):b instanceof n&&(g.addClass(d,"color"),b.updateDisplay=h.compose(function(a){d.style.borderLeftColor=b.__color.toString();return a},b.updateDisplay),b.updateDisplay());b.setValue=h.compose(function(d){a.getRoot().__preset_select&&b.isModified()&&D(a.getRoot(),!0);return d},b.setValue)}function v(a,
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/dat.gui.min.js:39` (CWE-79)
```
a.__ul.firstChild);g.addClass(b,"save-row");var d=document.createElement("span");d.innerHTML="&nbsp;";g.addClass(d,"button gears");var c=document.createElement("span");c.innerHTML="Save";g.addClass(c,
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/dat.gui.min.js
+++ b/frontend/src/assets/private/dat.gui.min.js
@@ -37,5 +37,5 @@
     b instanceof p?(g.bind(d,"click",function(){g.fakeEvent(b.__button,"click")}),g.bind(d,"mouseover",function(){g.addClass(b.__button,"hover")}),g.bind(d,"mouseout",function(){g.removeClass(b.__button,"hover")})):b instanceof n&&(g.addClass(d,"color"),b.updateDisplay=h.compose(function(a){d.style.borderLeftColor=b.__color.toString();return a},b.updateDisplay),b.updateDisplay());b.setValue=h.compose(function(d){a.getRoot().__preset_select&&b.isModified()&&D(a.getRoot(),!0);return d},b.setValue)}function v(a,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 d){var b=a.getRoot(),c=b.__rememberedObjects.indexOf(d.object);if(-1!=c){var e=b.__rememberedObjectIndecesToControllers[c];void 0===e&&(e={},b.__rememberedObjectIndecesToControllers[c]=e);e[d.property]=d;if(b.load&&b.load.remembered){b=b.load.remembered;if(b[a.preset])b=b[a.preset];else if(b[z])b=b[z];else return;b[c]&&void 0!==b[c][d.property]&&(c=b[c][d.property],d.initialValue=c,d.setValue(c))}}}function K(a){var b=a.__save_row=document.createElement("li");g.addClass(a.domElement,"has-save");a.__ul.insertBefore(b,
-    a.__ul.firstChild);g.addClass(b,"save-row");var d=document.createElement("span");d.innerHTML="&nbsp;";g.addClass(d,"button gears");var c=document.createElement("span");c.innerHTML="Save";g.addClass(c,"button");g.addClass(c,"save");var e=document.createElement("span");e.innerHTML="New";g.addClass(e,"button");g.addClass(e,"save-as");var f=document.createElement("span");f.innerHTML="Revert";g.addClass(f,"button");g.addClass(f,"revert");var q=a.__preset_select=document.createElement("select");a.load&&
+    a.__ul.firstChild);g.addClass(b,"save-row");var d=document.createElement("span");d.textContent ="&nbsp;";g.addClass(d,"button gears");var c=document.createElement("span");c.innerHTML="Save";g.addClass(c,"button");g.addClass(c,"save");var e=document.createElement("span");e.innerHTML="New";g.addClass(e,"button");g.addClass(e,"save-as");var f=document.createElement("span");f.innerHTML="Revert";g.addClass(f,"button");g.addClass(f,"revert");var q=a.__preset_select=document.createElement("select");a.load&&
     a.load.remembered?h.each(a.load.remembered,function(b,d){E(a,d,d==a.preset)}):E(a,z,!1);g.bind(q,"change",function(){for(var b=0;b<a.__preset_select.length;b++)a.__preset_select[b].innerHTML=a.__preset_select[b].value;a.preset=this.value});b.appendChild(q);b.appendChild(d);b.appendChild(c);b.appendChild(e);b.appendChild(f);if(w){var b=document.getElementById("dg-save-locally"),n=document.getElementById("dg-local-explain");b.style.display="block";b=document.getElementById("dg-local-storage");"true"===
     localStorage.getItem(document.location.href+".isLocal")&&b.setAttribute("checked","checked");var k=function(){n.style.display=a.useLocalStorage?"block":"none"};k();g.bind(b,"change",function(){a.useLocalStorage=!a.useLocalStorage;k()})}var r=document.getElementById("dg-new-constructor");g.bind(r,"keydown",function(a){!a.metaKey||67!==a.which&&67!=a.keyCode||A.hide()});g.bind(d,"click",function(){r.innerHTML=JSON.stringify(a.getSaveObject(),void 0,2);A.show();r.focus();r.select()});g.bind(c,"click",
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/dat.gui.min.js:40` (CWE-79)
```
a.load.remembered?h.each(a.load.remembered,function(b,d){E(a,d,d==a.preset)}):E(a,z,!1);g.bind(q,"change",function(){for(var b=0;b<a.__preset_select.length;b++)a.__preset_select[b].innerHTML=a.__prese
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/dat.gui.min.js
+++ b/frontend/src/assets/private/dat.gui.min.js
@@ -38,5 +38,5 @@
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 d){var b=a.getRoot(),c=b.__rememberedObjects.indexOf(d.object);if(-1!=c){var e=b.__rememberedObjectIndecesToControllers[c];void 0===e&&(e={},b.__rememberedObjectIndecesToControllers[c]=e);e[d.property]=d;if(b.load&&b.load.remembered){b=b.load.remembered;if(b[a.preset])b=b[a.preset];else if(b[z])b=b[z];else return;b[c]&&void 0!==b[c][d.property]&&(c=b[c][d.property],d.initialValue=c,d.setValue(c))}}}function K(a){var b=a.__save_row=document.createElement("li");g.addClass(a.domElement,"has-save");a.__ul.insertBefore(b,
     a.__ul.firstChild);g.addClass(b,"save-row");var d=document.createElement("span");d.innerHTML="&nbsp;";g.addClass(d,"button gears");var c=document.createElement("span");c.innerHTML="Save";g.addClass(c,"button");g.addClass(c,"save");var e=document.createElement("span");e.innerHTML="New";g.addClass(e,"button");g.addClass(e,"save-as");var f=document.createElement("span");f.innerHTML="Revert";g.addClass(f,"button");g.addClass(f,"revert");var q=a.__preset_select=document.createElement("select");a.load&&
-    a.load.remembered?h.each(a.load.remembered,function(b,d){E(a,d,d==a.preset)}):E(a,z,!1);g.bind(q,"change",function(){for(var b=0;b<a.__preset_select.length;b++)a.__preset_select[b].innerHTML=a.__preset_select[b].value;a.preset=this.value});b.appendChild(q);b.appendChild(d);b.appendChild(c);b.appendChild(e);b.appendChild(f);if(w){var b=document.getElementById("dg-save-locally"),n=document.getElementById("dg-local-explain");b.style.display="block";b=document.getElementById("dg-local-storage");"true"===
+    a.load.remembered?h.each(a.load.remembered,function(b,d){E(a,d,d==a.preset)}):E(a,z,!1);g.bind(q,"change",function(){for(var b=0;b<a.__preset_select.length;b++)a.__preset_select[b].textContent =a.__preset_select[b].value;a.preset=this.value});b.appendChild(q);b.appendChild(d);b.appendChild(c);b.appendChild(e);b.appendChild(f);if(w){var b=document.getElementById("dg-save-locally"),n=document.getElementById("dg-local-explain");b.style.display="block";b=document.getElementById("dg-local-storage");"true"===
     localStorage.getItem(document.location.href+".isLocal")&&b.setAttribute("checked","checked");var k=function(){n.style.display=a.useLocalStorage?"block":"none"};k();g.bind(b,"change",function(){a.useLocalStorage=!a.useLocalStorage;k()})}var r=document.getElementById("dg-new-constructor");g.bind(r,"keydown",function(a){!a.metaKey||67!==a.which&&67!=a.keyCode||A.hide()});g.bind(d,"click",function(){r.innerHTML=JSON.stringify(a.getSaveObject(),void 0,2);A.show();r.focus();r.select()});g.bind(c,"click",
     function(){a.save()});g.bind(e,"click",function(){var b=prompt("Enter a new preset name.");b&&a.saveAs(b)});g.bind(f,"click",function(){a.revert()})}function L(a){function b(f){f.preventDefault();e=f.clientX;g.addClass(a.__closeButton,m.CLASS_DRAG);g.bind(window,"mousemove",d);g.bind(window,"mouseup",c);return!1}function d(b){b.preventDefault();a.width+=e-b.clientX;a.onResize();e=b.clientX;return!1}function c(){g.removeClass(a.__closeButton,m.CLASS_DRAG);g.unbind(window,"mousemove",d);g.unbind(window,
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/dat.gui.min.js:41` (CWE-79)
```
localStorage.getItem(document.location.href+".isLocal")&&b.setAttribute("checked","checked");var k=function(){n.style.display=a.useLocalStorage?"block":"none"};k();g.bind(b,"change",function(){a.useLo
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/dat.gui.min.js
+++ b/frontend/src/assets/private/dat.gui.min.js
@@ -39,5 +39,5 @@
     a.__ul.firstChild);g.addClass(b,"save-row");var d=document.createElement("span");d.innerHTML="&nbsp;";g.addClass(d,"button gears");var c=document.createElement("span");c.innerHTML="Save";g.addClass(c,"button");g.addClass(c,"save");var e=document.createElement("span");e.innerHTML="New";g.addClass(e,"button");g.addClass(e,"save-as");var f=document.createElement("span");f.innerHTML="Revert";g.addClass(f,"button");g.addClass(f,"revert");var q=a.__preset_select=document.createElement("select");a.load&&
     a.load.remembered?h.each(a.load.remembered,function(b,d){E(a,d,d==a.preset)}):E(a,z,!1);g.bind(q,"change",function(){for(var b=0;b<a.__preset_select.length;b++)a.__preset_select[b].innerHTML=a.__preset_select[b].value;a.preset=this.value});b.appendChild(q);b.appendChild(d);b.appendChild(c);b.appendChild(e);b.appendChild(f);if(w){var b=document.getElementById("dg-save-locally"),n=document.getElementById("dg-local-explain");b.style.display="block";b=document.getElementById("dg-local-storage");"true"===
-    localStorage.getItem(document.location.href+".isLocal")&&b.setAttribute("checked","checked");var k=function(){n.style.display=a.useLocalStorage?"block":"none"};k();g.bind(b,"change",function(){a.useLocalStorage=!a.useLocalStorage;k()})}var r=document.getElementById("dg-new-constructor");g.bind(r,"keydown",function(a){!a.metaKey||67!==a.which&&67!=a.keyCode||A.hide()});g.bind(d,"click",function(){r.innerHTML=JSON.stringify(a.getSaveObject(),void 0,2);A.show();r.focus();r.select()});g.bind(c,"click",
+    localStorage.getItem(document.location.href+".isLocal")&&b.setAttribute("checked","checked");var k=function(){n.style.display=a.useLocalStorage?"block":"none"};k();g.bind(b,"change",function(){a.useLocalStorage=!a.useLocalStorage;k()})}var r=document.getElementById("dg-new-constructor");g.bind(r,"keydown",function(a){!a.metaKey||67!==a.which&&67!=a.keyCode||A.hide()});g.bind(d,"click",function(){r.textContent =JSON.stringify(a.getSaveObject(),void 0,2);A.show();r.focus();r.select()});g.bind(c,"click",
     function(){a.save()});g.bind(e,"click",function(){var b=prompt("Enter a new preset name.");b&&a.saveAs(b)});g.bind(f,"click",function(){a.revert()})}function L(a){function b(f){f.preventDefault();e=f.clientX;g.addClass(a.__closeButton,m.CLASS_DRAG);g.bind(window,"mousemove",d);g.bind(window,"mouseup",c);return!1}function d(b){b.preventDefault();a.width+=e-b.clientX;a.onResize();e=b.clientX;return!1}function c(){g.removeClass(a.__closeButton,m.CLASS_DRAG);g.unbind(window,"mousemove",d);g.unbind(window,
     "mouseup",c)}a.__resize_handle=document.createElement("div");h.extend(a.__resize_handle.style,{width:"6px",marginLeft:"-3px",height:"200px",cursor:"ew-resize",position:"absolute"});var e;g.bind(a.__resize_handle,"mousedown",b);g.bind(a.__closeButton,"mousedown",b);a.domElement.insertBefore(a.__resize_handle,a.domElement.firstElementChild)}function F(a,b){a.domElement.style.width=b+"px";a.__save_row&&a.autoPlace&&(a.__save_row.style.width=b+"px");a.__closeButton&&(a.__closeButton.style.width=b+"px")}
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/dat.gui.min.js:44` (CWE-79)
```
function B(a,b){var d={};h.each(a.__rememberedObjects,function(c,e){var f={};h.each(a.__rememberedObjectIndecesToControllers[e],function(a,d){f[d]=b?a.initialValue:a.getValue()});d[e]=f});return d}fun
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/dat.gui.min.js
+++ b/frontend/src/assets/private/dat.gui.min.js
@@ -42,5 +42,5 @@
     function(){a.save()});g.bind(e,"click",function(){var b=prompt("Enter a new preset name.");b&&a.saveAs(b)});g.bind(f,"click",function(){a.revert()})}function L(a){function b(f){f.preventDefault();e=f.clientX;g.addClass(a.__closeButton,m.CLASS_DRAG);g.bind(window,"mousemove",d);g.bind(window,"mouseup",c);return!1}function d(b){b.preventDefault();a.width+=e-b.clientX;a.onResize();e=b.clientX;return!1}function c(){g.removeClass(a.__closeButton,m.CLASS_DRAG);g.unbind(window,"mousemove",d);g.unbind(window,
     "mouseup",c)}a.__resize_handle=document.createElement("div");h.extend(a.__resize_handle.style,{width:"6px",marginLeft:"-3px",height:"200px",cursor:"ew-resize",position:"absolute"});var e;g.bind(a.__resize_handle,"mousedown",b);g.bind(a.__closeButton,"mousedown",b);a.domElement.insertBefore(a.__resize_handle,a.domElement.firstElementChild)}function F(a,b){a.domElement.style.width=b+"px";a.__save_row&&a.autoPlace&&(a.__save_row.style.width=b+"px");a.__closeButton&&(a.__closeButton.style.width=b+"px")}
-    function B(a,b){var d={};h.each(a.__rememberedObjects,function(c,e){var f={};h.each(a.__rememberedObjectIndecesToControllers[e],function(a,d){f[d]=b?a.initialValue:a.getValue()});d[e]=f});return d}function E(a,b,d){var c=document.createElement("option");c.innerHTML=b;c.value=b;a.__preset_select.appendChild(c);d&&(a.__preset_select.selectedIndex=a.__preset_select.length-1)}function D(a,b){var d=a.__preset_select[a.__preset_select.selectedIndex];d.innerHTML=b?d.value+"*":d.value}function G(a){0!=a.length&&
+    function B(a,b){var d={};h.each(a.__rememberedObjects,function(c,e){var f={};h.each(a.__rememberedObjectIndecesToControllers[e],function(a,d){f[d]=b?a.initialValue:a.getValue()});d[e]=f});return d}function E(a,b,d){var c=document.createElement("option");c.textContent =b;c.value=b;a.__preset_select.appendChild(c);d&&(a.__preset_select.selectedIndex=a.__preset_select.length-1)}function D(a,b){var d=a.__preset_select[a.__preset_select.selectedIndex];d.innerHTML=b?d.value+"*":d.value}function G(a){0!=a.length&&
     r(function(){G(a)});h.each(a,function(a){a.updateDisplay()})}e.inject(b);var z="Default",w;try{w="localStorage"in window&&null!==window.localStorage}catch(M){w=!1}var A,H=!0,x,C=!1,I=[],m=function(a){function b(){localStorage.setItem(document.location.href+".gui",JSON.stringify(c.getSaveObject()))}function d(){var a=c.getRoot();a.width+=1;h.defer(function(){a.width-=1})}var c=this;this.domElement=document.createElement("div");this.__ul=document.createElement("ul");this.domElement.appendChild(this.__ul);
         g.addClass(this.domElement,"dg");this.__folders={};this.__controllers=[];this.__rememberedObjects=[];this.__rememberedObjectIndecesToControllers=[];this.__listening=[];a=a||{};a=h.defaults(a,{autoPlace:!0,width:m.DEFAULT_WIDTH});a=h.defaults(a,{resizable:a.autoPlace,hideable:a.autoPlace});h.isUndefined(a.load)?a.load={preset:z}:a.preset&&(a.load.preset=a.preset);h.isUndefined(a.parent)&&a.hideable&&I.push(this);a.resizable=h.isUndefined(a.parent)&&a.resizable;a.autoPlace&&h.isUndefined(a.scrollable)&&
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/dat.gui.min.js:48` (CWE-79)
```
b);c.revert()}},width:{get:function(){return a.width},set:function(b){a.width=b;F(c,b)}},name:{get:function(){return a.name},set:function(b){a.name=b;q&&(q.innerHTML=a.name)}},closed:{get:function(){r
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/dat.gui.min.js
+++ b/frontend/src/assets/private/dat.gui.min.js
@@ -46,5 +46,5 @@
         g.addClass(this.domElement,"dg");this.__folders={};this.__controllers=[];this.__rememberedObjects=[];this.__rememberedObjectIndecesToControllers=[];this.__listening=[];a=a||{};a=h.defaults(a,{autoPlace:!0,width:m.DEFAULT_WIDTH});a=h.defaults(a,{resizable:a.autoPlace,hideable:a.autoPlace});h.isUndefined(a.load)?a.load={preset:z}:a.preset&&(a.load.preset=a.preset);h.isUndefined(a.parent)&&a.hideable&&I.push(this);a.resizable=h.isUndefined(a.parent)&&a.resizable;a.autoPlace&&h.isUndefined(a.scrollable)&&
         (a.scrollable=!0);var e=w&&"true"===localStorage.getItem(document.location.href+".isLocal");Object.defineProperties(this,{parent:{get:function(){return a.parent}},scrollable:{get:function(){return a.scrollable}},autoPlace:{get:function(){return a.autoPlace}},preset:{get:function(){return c.parent?c.getRoot().preset:a.load.preset},set:function(b){c.parent?c.getRoot().preset=b:a.load.preset=b;for(b=0;b<this.__preset_select.length;b++)this.__preset_select[b].value==this.preset&&(this.__preset_select.selectedIndex=
-            b);c.revert()}},width:{get:function(){return a.width},set:function(b){a.width=b;F(c,b)}},name:{get:function(){return a.name},set:function(b){a.name=b;q&&(q.innerHTML=a.name)}},closed:{get:function(){return a.closed},set:function(b){a.closed=b;a.closed?g.addClass(c.__ul,m.CLASS_CLOSED):g.removeClass(c.__ul,m.CLASS_CLOSED);this.onResize();c.__closeButton&&(c.__closeButton.innerHTML=b?m.TEXT_OPEN:m.TEXT_CLOSED)}},load:{get:function(){return a.load}},useLocalStorage:{get:function(){return e},set:function(a){w&&
+            b);c.revert()}},width:{get:function(){return a.width},set:function(b){a.width=b;F(c,b)}},name:{get:function(){return a.name},set:function(b){a.name=b;q&&(q.textContent =a.name)}},closed:{get:function(){return a.closed},set:function(b){a.closed=b;a.closed?g.addClass(c.__ul,m.CLASS_CLOSED):g.removeClass(c.__ul,m.CLASS_CLOSED);this.onResize();c.__closeButton&&(c.__closeButton.innerHTML=b?m.TEXT_OPEN:m.TEXT_CLOSED)}},load:{get:function(){return a.load}},useLocalStorage:{get:function(){return e},set:function(a){w&&
         ((e=a)?g.bind(window,"unload",b):g.unbind(window,"unload",b),localStorage.setItem(document.location.href+".isLocal",a))}}});if(h.isUndefined(a.parent)){a.closed=!1;g.addClass(this.domElement,m.CLASS_MAIN);g.makeSelectable(this.domElement,!1);if(w&&e){c.useLocalStorage=!0;var f=localStorage.getItem(document.location.href+".gui");f&&(a.load=JSON.parse(f))}this.__closeButton=document.createElement("div");this.__closeButton.innerHTML=m.TEXT_CLOSED;g.addClass(this.__closeButton,m.CLASS_CLOSE_BUTTON);this.domElement.appendChild(this.__closeButton);
             g.bind(this.__closeButton,"click",function(){c.closed=!c.closed})}else{void 0===a.closed&&(a.closed=!0);var q=document.createTextNode(a.name);g.addClass(q,"controller-name");f=u(c,q);g.addClass(this.__ul,m.CLASS_CLOSED);g.addClass(f,"title");g.bind(f,"click",function(a){a.preventDefault();c.closed=!c.closed;return!1});a.closed||(this.closed=!1)}a.autoPlace&&(h.isUndefined(a.parent)&&(H&&(x=document.createElement("div"),g.addClass(x,"dg"),g.addClass(x,m.CLASS_AUTO_PLACE_CONTAINER),document.body.appendChild(x),
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/dat.gui.min.js:49` (CWE-79)
```
((e=a)?g.bind(window,"unload",b):g.unbind(window,"unload",b),localStorage.setItem(document.location.href+".isLocal",a))}}});if(h.isUndefined(a.parent)){a.closed=!1;g.addClass(this.domElement,m.CLASS_M
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/dat.gui.min.js
+++ b/frontend/src/assets/private/dat.gui.min.js
@@ -47,5 +47,5 @@
         (a.scrollable=!0);var e=w&&"true"===localStorage.getItem(document.location.href+".isLocal");Object.defineProperties(this,{parent:{get:function(){return a.parent}},scrollable:{get:function(){return a.scrollable}},autoPlace:{get:function(){return a.autoPlace}},preset:{get:function(){return c.parent?c.getRoot().preset:a.load.preset},set:function(b){c.parent?c.getRoot().preset=b:a.load.preset=b;for(b=0;b<this.__preset_select.length;b++)this.__preset_select[b].value==this.preset&&(this.__preset_select.selectedIndex=
             b);c.revert()}},width:{get:function(){return a.width},set:function(b){a.width=b;F(c,b)}},name:{get:function(){return a.name},set:function(b){a.name=b;q&&(q.innerHTML=a.name)}},closed:{get:function(){return a.closed},set:function(b){a.closed=b;a.closed?g.addClass(c.__ul,m.CLASS_CLOSED):g.removeClass(c.__ul,m.CLASS_CLOSED);this.onResize();c.__closeButton&&(c.__closeButton.innerHTML=b?m.TEXT_OPEN:m.TEXT_CLOSED)}},load:{get:function(){return a.load}},useLocalStorage:{get:function(){return e},set:function(a){w&&
-        ((e=a)?g.bind(window,"unload",b):g.unbind(window,"unload",b),localStorage.setItem(document.location.href+".isLocal",a))}}});if(h.isUndefined(a.parent)){a.closed=!1;g.addClass(this.domElement,m.CLASS_MAIN);g.makeSelectable(this.domElement,!1);if(w&&e){c.useLocalStorage=!0;var f=localStorage.getItem(document.location.href+".gui");f&&(a.load=JSON.parse(f))}this.__closeButton=document.createElement("div");this.__closeButton.innerHTML=m.TEXT_CLOSED;g.addClass(this.__closeButton,m.CLASS_CLOSE_BUTTON);this.domElement.appendChild(this.__closeButton);
+        ((e=a)?g.bind(window,"unload",b):g.unbind(window,"unload",b),localStorage.setItem(document.location.href+".isLocal",a))}}});if(h.isUndefined(a.parent)){a.closed=!1;g.addClass(this.domElement,m.CLASS_MAIN);g.makeSelectable(this.domElement,!1);if(w&&e){c.useLocalStorage=!0;var f=localStorage.getItem(document.location.href+".gui");f&&(a.load=JSON.parse(f))}this.__closeButton=document.createElement("div");this.__closeButton.textContent =m.TEXT_CLOSED;g.addClass(this.__closeButton,m.CLASS_CLOSE_BUTTON);this.domElement.appendChild(this.__closeButton);
             g.bind(this.__closeButton,"click",function(){c.closed=!c.closed})}else{void 0===a.closed&&(a.closed=!0);var q=document.createTextNode(a.name);g.addClass(q,"controller-name");f=u(c,q);g.addClass(this.__ul,m.CLASS_CLOSED);g.addClass(f,"title");g.bind(f,"click",function(a){a.preventDefault();c.closed=!c.closed;return!1});a.closed||(this.closed=!1)}a.autoPlace&&(h.isUndefined(a.parent)&&(H&&(x=document.createElement("div"),g.addClass(x,"dg"),g.addClass(x,m.CLASS_AUTO_PLACE_CONTAINER),document.body.appendChild(x),
             H=!1),x.appendChild(this.domElement),g.addClass(this.domElement,m.CLASS_AUTO_PLACE)),this.parent||F(c,a.width));g.bind(window,"resize",function(){c.onResize()});g.bind(this.__ul,"webkitTransitionEnd",function(){c.onResize()});g.bind(this.__ul,"transitionend",function(){c.onResize()});g.bind(this.__ul,"oTransitionEnd",function(){c.onResize()});this.onResize();a.resizable&&L(this);c.getRoot();a.parent||d()};m.toggleHide=function(){C=!C;h.each(I,function(a){a.domElement.style.zIndex=C?-999:999;a.domElement.style.opacity=
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/dat.gui.min.js:55` (CWE-79)
```
b-20+"px"):(g.removeClass(a.domElement,m.CLASS_TOO_TALL),a.__ul.style.height="auto")}a.__resize_handle&&h.defer(function(){a.__resize_handle.style.height=a.__ul.offsetHeight+"px"});a.__closeButton&&(a
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/dat.gui.min.js
+++ b/frontend/src/assets/private/dat.gui.min.js
@@ -53,5 +53,5 @@
         2)})},addColor:function(a,b){return t(this,a,b,{color:!0})},remove:function(a){this.__ul.removeChild(a.__li);this.__controllers.slice(this.__controllers.indexOf(a),1);var b=this;h.defer(function(){b.onResize()})},destroy:function(){this.autoPlace&&x.removeChild(this.domElement)},addFolder:function(a){if(void 0!==this.__folders[a])throw Error('You already have a folder in this GUI by the name "'+a+'"');var b={name:a,parent:this};b.autoPlace=this.autoPlace;this.load&&this.load.folders&&this.load.folders[a]&&
     (b.closed=this.load.folders[a].closed,b.load=this.load.folders[a]);b=new m(b);this.__folders[a]=b;a=u(this,b.domElement);g.addClass(a,"folder");return b},open:function(){this.closed=!1},close:function(){this.closed=!0},onResize:function(){var a=this.getRoot();if(a.scrollable){var b=g.getOffset(a.__ul).top,d=0;h.each(a.__ul.childNodes,function(b){a.autoPlace&&b===a.__save_row||(d+=g.getHeight(b))});window.innerHeight-b-20<d?(g.addClass(a.domElement,m.CLASS_TOO_TALL),a.__ul.style.height=window.innerHeight-
-        b-20+"px"):(g.removeClass(a.domElement,m.CLASS_TOO_TALL),a.__ul.style.height="auto")}a.__resize_handle&&h.defer(function(){a.__resize_handle.style.height=a.__ul.offsetHeight+"px"});a.__closeButton&&(a.__closeButton.style.width=a.width+"px")},remember:function(){h.isUndefined(A)&&(A=new y,A.domElement.innerHTML=a);if(this.parent)throw Error("You can only call remember on a top level GUI.");var b=this;h.each(Array.prototype.slice.call(arguments),function(a){0==b.__rememberedObjects.length&&K(b);-1==
+        b-20+"px"):(g.removeClass(a.domElement,m.CLASS_TOO_TALL),a.__ul.style.height="auto")}a.__resize_handle&&h.defer(function(){a.__resize_handle.style.height=a.__ul.offsetHeight+"px"});a.__closeButton&&(a.__closeButton.style.width=a.width+"px")},remember:function(){h.isUndefined(A)&&(A=new y,A.domElement.textContent =a);if(this.parent)throw Error("You can only call remember on a top level GUI.");var b=this;h.each(Array.prototype.slice.call(arguments),function(a){0==b.__rememberedObjects.length&&K(b);-1==
         b.__rememberedObjects.indexOf(a)&&b.__rememberedObjects.push(a)});this.autoPlace&&F(this,this.width)},getRoot:function(){for(var a=this;a.parent;)a=a.parent;return a},getSaveObject:function(){var a=this.load;a.closed=this.closed;0<this.__rememberedObjects.length&&(a.preset=this.preset,a.remembered||(a.remembered={}),a.remembered[this.preset]=B(this));a.folders={};h.each(this.__folders,function(b,d){a.folders[d]=b.getSaveObject()});return a},save:function(){this.load.remembered||(this.load.remembered=
     {});this.load.remembered[this.preset]=B(this);D(this,!1)},saveAs:function(a){this.load.remembered||(this.load.remembered={},this.load.remembered[z]=B(this,!0));this.load.remembered[a]=B(this);this.preset=a;E(this,a,!0)},revert:function(a){h.each(this.__controllers,function(b){this.getRoot().load.remembered?v(a||this.getRoot(),b):b.setValue(b.initialValue)},this);h.each(this.__folders,function(a){a.revert(a)});a||D(this.getRoot(),!1)},listen:function(a){var b=0==this.__listening.length;this.__listening.push(a);
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/stats.min.js:3` (CWE-79)
```
i.innerHTML="FPS";a.appendChild(i);var c=document.createElement("div");c.id="fpsGraph";c.style.cssText="position:relative;width:74px;height:30px;background-color:#0ff";for(a.appendChild(c);74>c.childr
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/stats.min.js
+++ b/frontend/src/assets/private/stats.min.js
@@ -1,5 +1,5 @@
 // stats.js - http://github.com/mrdoob/stats.js
 var Stats=function(){var l=Date.now(),m=l,g=0,n=Infinity,o=0,h=0,p=Infinity,q=0,r=0,s=0,f=document.createElement("div");f.id="stats";f.addEventListener("mousedown",function(b){b.preventDefault();t(++s%2)},!1);f.style.cssText="width:80px;opacity:0.9;cursor:pointer";var a=document.createElement("div");a.id="fps";a.style.cssText="padding:0 0 3px 3px;text-align:left;background-color:#002";f.appendChild(a);var i=document.createElement("div");i.id="fpsText";i.style.cssText="color:#0ff;font-family:Helvetica,Arial,sans-serif;font-size:9px;font-weight:bold;line-height:15px";
-    i.innerHTML="FPS";a.appendChild(i);var c=document.createElement("div");c.id="fpsGraph";c.style.cssText="position:relative;width:74px;height:30px;background-color:#0ff";for(a.appendChild(c);74>c.children.length;){var j=document.createElement("span");j.style.cssText="width:1px;height:30px;float:left;background-color:#113";c.appendChild(j)}var d=document.createElement("div");d.id="ms";d.style.cssText="padding:0 0 3px 3px;text-align:left;background-color:#020;display:none";f.appendChild(d);var k=document.createElement("div");
+    i.textContent ="FPS";a.appendChild(i);var c=document.createElement("div");c.id="fpsGraph";c.style.cssText="position:relative;width:74px;height:30px;background-color:#0ff";for(a.appendChild(c);74>c.children.length;){var j=document.createElement("span");j.style.cssText="width:1px;height:30px;float:left;background-color:#113";c.appendChild(j)}var d=document.createElement("div");d.id="ms";d.style.cssText="padding:0 0 3px 3px;text-align:left;background-color:#020;display:none";f.appendChild(d);var k=document.createElement("div");
     k.id="msText";k.style.cssText="color:#0f0;font-family:Helvetica,Arial,sans-serif;font-size:9px;font-weight:bold;line-height:15px";k.innerHTML="MS";d.appendChild(k);var e=document.createElement("div");e.id="msGraph";e.style.cssText="position:relative;width:74px;height:30px;background-color:#0f0";for(d.appendChild(e);74>e.children.length;)j=document.createElement("span"),j.style.cssText="width:1px;height:30px;float:left;background-color:#131",e.appendChild(j);var t=function(b){s=b;switch(s){case 0:a.style.display=
         "block";d.style.display="none";break;case 1:a.style.display="none",d.style.display="block"}};return{REVISION:11,domElement:f,setMode:t,begin:function(){l=Date.now()},end:function(){var b=Date.now();g=b-l;n=Math.min(n,g);o=Math.max(o,g);k.textContent=g+" MS ("+n+"-"+o+")";var a=Math.min(30,30-30*(g/200));e.appendChild(e.firstChild).style.height=a+"px";r++;b>m+1E3&&(h=Math.round(1E3*r/(b-m)),p=Math.min(p,h),q=Math.max(q,h),i.textContent=h+" FPS ("+p+"-"+q+")",a=Math.min(30,30-30*(h/100)),c.appendChild(c.firstChild).style.height=
```

### [HIGH] Cross-site scripting (unsafe HTML sink) — `frontend/src/assets/private/stats.min.js:4` (CWE-79)
```
k.id="msText";k.style.cssText="color:#0f0;font-family:Helvetica,Arial,sans-serif;font-size:9px;font-weight:bold;line-height:15px";k.innerHTML="MS";d.appendChild(k);var e=document.createElement("div");
```
- **Why it matters:** Untrusted data reaches an HTML sink without contextual output encoding.
- **Fix:** Use textContent / auto-escaping templates and sanitise rich content with an allow-list sanitiser.
- **Verification plan:** Submit a benign marker tag as input and confirm it is rendered unescaped in the response DOM.

```diff
--- a/frontend/src/assets/private/stats.min.js
+++ b/frontend/src/assets/private/stats.min.js
@@ -2,5 +2,5 @@
 var Stats=function(){var l=Date.now(),m=l,g=0,n=Infinity,o=0,h=0,p=Infinity,q=0,r=0,s=0,f=document.createElement("div");f.id="stats";f.addEventListener("mousedown",function(b){b.preventDefault();t(++s%2)},!1);f.style.cssText="width:80px;opacity:0.9;cursor:pointer";var a=document.createElement("div");a.id="fps";a.style.cssText="padding:0 0 3px 3px;text-align:left;background-color:#002";f.appendChild(a);var i=document.createElement("div");i.id="fpsText";i.style.cssText="color:#0ff;font-family:Helvetica,Arial,sans-serif;font-size:9px;font-weight:bold;line-height:15px";
     i.innerHTML="FPS";a.appendChild(i);var c=document.createElement("div");c.id="fpsGraph";c.style.cssText="position:relative;width:74px;height:30px;background-color:#0ff";for(a.appendChild(c);74>c.children.length;){var j=document.createElement("span");j.style.cssText="width:1px;height:30px;float:left;background-color:#113";c.appendChild(j)}var d=document.createElement("div");d.id="ms";d.style.cssText="padding:0 0 3px 3px;text-align:left;background-color:#020;display:none";f.appendChild(d);var k=document.createElement("div");
-    k.id="msText";k.style.cssText="color:#0f0;font-family:Helvetica,Arial,sans-serif;font-size:9px;font-weight:bold;line-height:15px";k.innerHTML="MS";d.appendChild(k);var e=document.createElement("div");e.id="msGraph";e.style.cssText="position:relative;width:74px;height:30px;background-color:#0f0";for(d.appendChild(e);74>e.children.length;)j=document.createElement("span"),j.style.cssText="width:1px;height:30px;float:left;background-color:#131",e.appendChild(j);var t=function(b){s=b;switch(s){case 0:a.style.display=
+    k.id="msText";k.style.cssText="color:#0f0;font-family:Helvetica,Arial,sans-serif;font-size:9px;font-weight:bold;line-height:15px";k.textContent ="MS";d.appendChild(k);var e=document.createElement("div");e.id="msGraph";e.style.cssText="position:relative;width:74px;height:30px;background-color:#0f0";for(d.appendChild(e);74>e.children.length;)j=document.createElement("span"),j.style.cssText="width:1px;height:30px;float:left;background-color:#131",e.appendChild(j);var t=function(b){s=b;switch(s){case 0:a.style.display=
         "block";d.style.display="none";break;case 1:a.style.display="none",d.style.display="block"}};return{REVISION:11,domElement:f,setMode:t,begin:function(){l=Date.now()},end:function(){var b=Date.now();g=b-l;n=Math.min(n,g);o=Math.max(o,g);k.textContent=g+" MS ("+n+"-"+o+")";var a=Math.min(30,30-30*(g/200));e.appendChild(e.firstChild).style.height=a+"px";r++;b>m+1E3&&(h=Math.round(1E3*r/(b-m)),p=Math.min(p,h),q=Math.max(q,h),i.textContent=h+" FPS ("+p+"-"+q+")",a=Math.min(30,30-30*(h/100)),c.appendChild(c.firstChild).style.height=
         a+"px",m=b,r=0);return b},update:function(){l=this.end()}}};
```

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

_…and 7 more findings are listed in the PDF overview table and available through the agent._

---
_Findings come from the engine named above. Verification plans describe how a finding would be confirmed; no exploit was run. Patches are suggestions that must be reviewed and tested before merge. Test folders and test files (test, tests, spec, e2e, cypress, fixtures, *.spec.*, *.test.*) and vendored/build folders are not scanned._