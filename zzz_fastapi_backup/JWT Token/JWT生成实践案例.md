，围绕 FastAPI + PostgreSQL 后端 与 HTML+TypeScript 前端的分离架构，使用短期 Access Token + HttpOnly Refresh Token、Refresh Token 轮换与撤销策略。会包含接口设计、数据库表、JWT 内容与校验、前端存储策略、CORS/Cookie 配置、安全注意点以及在 Windows 上的部署/调试提示。

概览（目标）

登录：前端提交 username/password → 后端验证（bcrypt/argon2）→ 成功后
在响应体返回短期 access_token（JWT）
在 Set-Cookie 中设置 httpOnly、Secure、SameSite 的 refresh_token（JWT 或 opaque id）
访问受保护资源（/api/me）：前端在 Authorization: Bearer <access_token> 发送请求；后端验证 access_token
Access token 过期后：前端调用 /api/refresh（携带 httpOnly refresh cookie）换取新的 access_token（并返回新的 refresh cookie，实现 refresh 轮换）；后端对 refresh token 做撤销/轮换检查
登出：调用 /api/logout，使当前 refresh token 撤销并可选择使所有 token 失效（例如通过 user.token_version++）
主要设计要点（要合理且安全）

Access token：短期（5–15 分钟），用于每次 API 请求，放在内存里（避免 localStorage）并加到 Authorization header。
Refresh token：长期（7–30 天），必须放在 httpOnly cookie（防 XSS），并设置 Secure（生产中）、SameSite（Lax/Strict）以降低 CSRF 风险。
Refresh token 轮换（推荐）：每次使用 refresh 生成新的 refresh token，同时在 DB 标记旧 token 为已替换/revoked。若检测到 reuse（已撤销的 refresh 被再次使用），说明 token 泄漏，后端应撤销该用户所有 refresh token 并强制登出/通知。
撤销策略：在 DB 中保存 refresh token 的状态（revoked），并保存 jti / token id，用于撤销与检测重放。Access token 在校验时可携带 token_version 或检查用户状态以实现快速失效（例如密码变更、管理员强制登出时）。
密码只存哈希（bcrypt/argon2），给出盐与强成本参数。
JWT 签名：小型项目可用对称 HS256；生产建议 RS256（公/私钥）或至少安全地把 secret 存在环境变量或密钥管理服务。
接口设计（REST）

POST /api/login
Request JSON: { "username": "...", "password": "..." }
Response: 200 OK，Body: { "access_token": "", "token_type": "bearer", "expires_in": 900 }
Set-Cookie: refresh_token=; HttpOnly; Secure; SameSite=Lax; Path=/api/refresh; Expires=...
POST /api/refresh
Request: cookie 中自动带 refresh_token
Response: 新 access_token（body）+ 新 refresh_token（Set-Cookie） — 实现轮换
POST /api/logout
Request: cookie 中带 refresh_token 或 Authorization header 带 access token
Response: 200，后端撤销当前 refresh token（并删除 cookie）
Set-Cookie: refresh_token=; HttpOnly; Expires=过去时间（清空）
GET /api/me
Request: Authorization: Bearer <access_token>
Response: 用户信息（仅当 access token 验证通过）
JWT 内容（access token）

使用标准 claim：
sub: 用户 id
iat: 签发时间
exp: 过期时间（短）
iss: issuer
aud: audience（可选）
token_version（或 custom claim）：当前用户 token_version，用来快速使历史 token 失效（可选）
不要放敏感信息（密码、完整个人信息）
Refresh Token 设计

两种主流方式：
Refresh token 也是 JWT，含 jti（唯一 id）并把 jti 存到 DB；验证时检查 jti 是否未撤销且未过期。
Refresh token 为随机 opaque string（更安全），在 DB 中存储其 hash（类似 session id），验证时查 DB。
推荐使用 opaque id 或 JWT+DB 映射，便于撤销与轮换检测。
数据库表设计（示例 SQL）