# Security Overview

- JWT authentication for all endpoints (access/refresh tokens)
- Role Based Access Control (RBAC) enforced on API
- Passwords are hashed with bcrypt (passlib)
- Rate limiting with slowapi (per IP)
- Sensitive credentials/configuration via .env files
- Audit log for all critical actions (login, register, role change, etc.)
- Tenant isolation for all vector/database operations

## Recommendations

- Only expose necessary ports in production
- Use HTTPS in deployment
- Change SECRET_KEY and all credentials before production
- Regularly monitor audit logs and Prometheus metrics
```