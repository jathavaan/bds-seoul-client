# Architecture and design patterns

To ensure that codebase is scalable, understandable, debuggable and easy to navigate multiple architectural design
choices have been made. Our project structure is heavily inspired by Clean Architecture and divides the codebase into
layers. There are four layers:

- Domain
- Application
- Persistence
- Scraper (presentation)

where the applicatoin and persistence layer are on the same level.