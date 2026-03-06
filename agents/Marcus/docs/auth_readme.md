Auth decision summary

- Refresh token transport: HttpOnly Secure cookie, SameSite=Lax, path=/api/v1/auth/refresh
- Access token: short-lived (15min) returned in response body; frontend keeps in-memory
- Cookie name: refresh_token
- CORS: allow_credentials=True; allowed origins: http://localhost:3000 (update per env)
- Error format: { code: string, message: string, field_errors?: [{field, message}] }
- Pagination metadata: total_count
- Endpoints implemented in OpenAPI: /auth/login, /auth/refresh, /auth/logout, /auth/signup, /users/me
- Notes: backend sets refresh cookie; frontend must call endpoints with credentials included (fetch credentials: 'include')
