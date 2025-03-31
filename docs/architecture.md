# Architecture and design patterns

To ensure that codebase is scalable, understandable, debuggable and easy to navigate multiple architectural design
choices have been made. Our project structure is heavily inspired by Clean Architecture and divides the codebase into
layers. There are four layers:

- Domain
- Application
- Persistence
- Scraper (presentation)

where the presentation and persistence layer are on the same level.

<div align="center">
  <img src="https://miro.medium.com/v2/resize:fit:339/1*JWzL8VcHl13x0J5rDUZWzA.png" alt="Clean architecture"/>
</div>


## Clean architecture

> [!TIP]
> It is recommended that you have a basic understanding of Clean Architecture before proceding

A rule of thumb is to not import anything from an outer layer.

### Domain layer
The domain layer is the innermost layer and is not dependent on any other layer. The content in the domain layer can be viewed as the core building blocks in the codebase. Most of the code and logic is built ontop of these code bulidng blocks. 

## Application layer
The application layer contains the main logic.
