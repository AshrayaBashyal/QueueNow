## QueueNow
QueueNow is a backend system for appointment booking and queue/token management designed for organizations such as clinics, offices, banks, and consultancies. It focuses on controlled staff access, predictable queue flow, and clean domain-driven architecture.

This project is built as a learning-first but production-grade system, following real-world backend practices rather than tutorial shortcuts.


## Project Goals
Provide a reliable appointment booking system
Manage daily queues using sequential tokens
Support invite-only staff access
Maintain clean separation of concerns
Be reusable as a module in larger systems 

## Scope (Current MVP)
Included:
User registration and JWT authentication
Organization creation
Invite-based staff membership
Role management (Admin, Staff)
Service management (what users book)
Time slot scheduling
Appointment booking, cancellation, rescheduling
Queue & token generation per service per day
Staff queue operations (call next, complete, no-show)

Explicitly Excluded (for now):
Payments
SMS
Email sending 
Background jobs (Celery, Redis)
Docker
Automated testing

These will be added incrementally in later phases.


## Project Structure
```
queuenow/
├── config/          # Django settings and routing
├── apps/            # Domain-driven apps (business logic)
├── core/            # Shared internal utilities and permissions
├── infrastructure/  # External integrations (email, cache) – later
├── tests/           # Test suites – later
```


## Staff Access Model
Organizations are created by users
Creator becomes Admin by default
Staff access is invite-only
Users accept or reject invites via dashboard
The last admin cannot be removed


## Development Approach
This project is built in phases:
Core domain logic (current)
Email handling
Async processing (Celery + Redis)
Testing
Docker & deployment

