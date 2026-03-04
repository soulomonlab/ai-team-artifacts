openapi: 3.0.2
info:
  title: Product MVP API
  version: "1.0.0"
  description: |
    Minimal OpenAPI v1 spec for onboarding and core task flow for MVP.
servers:
  - url: /api/v1
paths:
  /users:
    post:
      summary: Create user (signup)
      tags: [auth]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserCreate'
      responses:
        '201':
          description: User created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/UserResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
  /auth/login:
    post:
      summary: Login and receive access token
      tags: [auth]
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserLogin'
      responses:
        '200':
          description: Auth token
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AuthResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'
  /tasks:
    get:
      summary: List tasks (paginated)
      tags: [tasks]
      parameters:
        - in: query
          name: page
          schema:
            type: integer
            minimum: 1
            default: 1
        - in: query
          name: size
          schema:
            type: integer
            minimum: 1
            maximum: 100
            default: 20
      security:
        - bearerAuth: []
      responses:
        '200':
          description: Paginated list of tasks
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskListResponse'
        '401':
          $ref: '#/components/responses/Unauthorized'
    post:
      summary: Create a task
      tags: [tasks]
      security:
        - bearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskCreate'
      responses:
        '201':
          description: Task created
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskResponse'
        '400':
          $ref: '#/components/responses/BadRequest'
  /tasks/{task_id}:
    get:
      summary: Get task
      tags: [tasks]
      security:
        - bearerAuth: []
      parameters:
        - in: path
          name: task_id
          required: true
          schema:
            type: integer
      responses:
        '200':
          description: Task
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskResponse'
        '404':
          $ref: '#/components/responses/NotFound'
    patch:
      summary: Update task (partial)
      tags: [tasks]
      security:
        - bearerAuth: []
      parameters:
        - in: path
          name: task_id
          required: true
          schema:
            type: integer
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/TaskUpdate'
      responses:
        '200':
          description: Updated task
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/TaskResponse'
        '404':
          $ref: '#/components/responses/NotFound'
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
  schemas:
    UserCreate:
      type: object
      required: [email, password, name]
      properties:
        email:
          type: string
          format: email
        password:
          type: string
          description: Use strong password rules; min 8 chars
        name:
          type: string
    UserLogin:
      type: object
      required: [email, password]
      properties:
        email:
          type: string
          format: email
        password:
          type: string
    AuthResponse:
      type: object
      properties:
        access_token:
          type: string
        token_type:
          type: string
          example: Bearer
        expires_in:
          type: integer
          description: seconds until expiry
    UserResponse:
      type: object
      properties:
        id:
          type: integer
        email:
          type: string
        name:
          type: string
    TaskCreate:
      type: object
      required: [title]
      properties:
        title:
          type: string
        description:
          type: string
        due_date:
          type: string
          format: date-time
        meta:
          type: object
          description: Arbitrary JSON metadata
    TaskUpdate:
      type: object
      properties:
        title:
          type: string
        description:
          type: string
        due_date:
          type: string
          format: date-time
        status:
          type: string
          enum: [todo, in_progress, done]
    TaskResponse:
      type: object
      properties:
        id:
          type: integer
        title:
          type: string
        description:
          type: string
        status:
          type: string
        created_at:
          type: string
          format: date-time
        updated_at:
          type: string
          format: date-time
        due_date:
          type: string
          format: date-time
    TaskListResponse:
      type: object
      properties:
        page:
          type: integer
        size:
          type: integer
        total:
          type: integer
        items:
          type: array
          items:
            $ref: '#/components/schemas/TaskResponse'
  responses:
    BadRequest:
      description: Bad request
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    Unauthorized:
      description: Missing or invalid auth
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    NotFound:
      description: Resource not found
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
  schemas:
    Error:
      type: object
      properties:
        code:
          type: string
        message:
          type: string
        details:
          type: object

examples:
  UserCreateExample:
    value:
      email: alice@example.com
      password: securePass123
      name: Alice
  TaskCreateExample:
    value:
      title: "Finish onboarding flow"
      description: "Implement API + frontend for onboarding"
      due_date: "2026-03-10T12:00:00Z"

# Examples (request/response)

## Signup (POST /users)
Request:
{
  "email": "alice@example.com",
  "password": "securePass123",
  "name": "Alice"
}

Response 201:
{
  "id": 1,
  "email": "alice@example.com",
  "name": "Alice"
}

## Login (POST /auth/login)
Request:
{
  "email": "alice@example.com",
  "password": "securePass123"
}

Response 200:
{
  "access_token": "<jwt>",
  "token_type": "Bearer",
  "expires_in": 3600
}

## Create Task (POST /tasks)
Request (Bearer auth):
{
  "title": "Finish onboarding flow",
  "description": "Implement API + frontend for onboarding",
  "due_date": "2026-03-10T12:00:00Z"
}

Response 201:
{
  "id": 10,
  "title": "Finish onboarding flow",
  "description": "Implement API + frontend for onboarding",
  "status": "todo",
  "created_at": "2026-03-04T09:00:00Z",
  "updated_at": "2026-03-04T09:00:00Z",
  "due_date": "2026-03-10T12:00:00Z"
}

# Notes / Decisions
- API versioning: /api/v1 prefix
- Auth: JWT bearer tokens
- Error format: {code, message, details}
- Pagination: page/size, size max 100
- Allow task.meta as JSON for flexible fields

# Next steps
- Implement FastAPI skeleton and schemas in output/code/backend/ on branch feature/api-skeleton
- #ai-frontend: consume these endpoints; expect /auth/login for auth flow
- #ai-qa: create test cases for auth, create/list tasks, pagination, invalid payloads
