# 岛経管理システム — Frontend

React + TypeScript + Vite frontend for the Project Performance Management
training app. Talks to a FastAPI backend (see the project root for the backend
codebase; this folder only contains the frontend).

The app is in Japanese (customer name, project name, etc. are entered in
Japanese). UI labels stay in Japanese on purpose so the screens match the
spec / matching data.

## Getting started

```bash
npm install
npm run dev          # http://localhost:5173
```

The dev server expects the FastAPI backend to be running at
`VITE_API_BASE_URL` (default `http://localhost:8000`). Override it by editing
`.env`.

## Build

```bash
npm run build        # type-check (tsc -b) then produce dist/
npm run preview      # serve the production build locally
```

## Lint

```bash
npx oxlint
```

## Backend endpoints the frontend calls

All paths are relative to `VITE_API_BASE_URL`. Requests to everything except
`/auth/*` and `/health` require a JWT in the `Authorization` header
(`Bearer <idToken>`).

| Method | Path                                       | Purpose                                    |
| ------ | ------------------------------------------ | ------------------------------------------ |
| POST   | `/auth/login`                              | Exchange email + password for an `idToken` |
| POST   | `/auth/register`                           | Create a new account; on success returns `{ idToken }` (auto-login) |
| GET    | `/health`                                  | Readiness probe (`{ status, db }`)         |
| GET    | `/projects`                                | List projects (search + filter + paging)   |
| POST   | `/projects`                                | Create a project                           |
| GET    | `/projects/:id`                            | Get one project                            |
| PUT    | `/projects/:id`                            | Replace a project                          |
| DELETE | `/projects/:id`                            | Soft-delete a project                      |
| GET    | `/tech-tags`                               | Tech-tag autocomplete (`?q=`)              |

On `401` the frontend clears the stored token and redirects to `/login`.

## Auth model

Two endpoints, both unauthenticated:

- `POST /auth/login` — body `{ email, password }`, returns `{ idToken }`.
- `POST /auth/register` — body `{ email, password }`, returns `{ idToken }`
  (auto-login on success). If the backend does not return a token the
  frontend falls back to calling `/auth/login` automatically.

The token is stored in `localStorage` under `auth.idToken` and attached
to subsequent requests as `Authorization: Bearer <idToken>`. The frontend
also checks the `exp` claim and clears the stored token on expiry.

A logged-in user is described by `{ email, role }` decoded from the JWT
payload. `role` is either `"admin"` or `"member"`. New users registered
through `/auth/register` are created with `role = "member"`.

