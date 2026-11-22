# Example input — fictional appointment booking service

## Scope
A public web client sends appointment requests to a web API. The API reads/writes appointment records in a backend database. A signed-in user can view their own appointments. No production credentials or external endpoint names are provided.

## Assets
- Personal appointment details.
- Session authentication state.
- Integrity of appointment ownership.

## Entry points
- Public web application and authenticated API requests (routes unspecified).

## Trust boundaries
- Internet client to backend API.
- Backend API to private database.

## Unknowns
Authorization checks, rate limits, authentication implementation, audit log retention, transport controls, and deployment configuration are not supplied. This description does **not** assert any control is missing.
