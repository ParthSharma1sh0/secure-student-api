# Security Decisions

## 1. JWT Authentication

I chose JWT Bearer authentication because the API is a REST API and needs a simple way to authenticate requests without storing server-side sessions.

## 2. Password Hashing

Passwords are never stored directly. Argon2 is used to hash passwords before they are stored in the database.

## 3. Role-Based Authorization

Two roles are used:

- Student
- Admin

Authenticated students can view records, while administrative operations such as creating, updating and deleting records require the Admin role.

## 4. Input Validation

Pydantic schemas validate incoming student data.

For example:

- Name has length limits.
- Email must have a valid email format.
- Year must be between 1 and 6.

Invalid requests are rejected before database operations are performed.

## 5. Sensitive Information

Password hashes are never returned through the API.

The API uses response models so that only required student information is returned.

## Security Trade-off

The API uses a simple role-based authorization model rather than implementing a more complex permission system.

This keeps the project small and understandable while still demonstrating authentication, authorization and resource protection.
