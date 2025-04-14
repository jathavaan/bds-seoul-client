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

### Application layer
The application layer contains the business logic. This could be everything from interacting with the database to string manipulation. This can only be independent of the domain layer.

> [!IMPORTANT]
> Services that access the database, also know as repository services have to extend the class `RepositoryServiceBase`
> ```python
> from sqlalchemy.orm import Session
>
> from ...base import RepositoryServiceBase
>
>
> class QuoteRepositoryService(RepositoryServiceBase):
>   def __init__(self, session: Session):
>     super().__init__(session)
> ```

This layer also handles the dependency injection. We use the `dependency-injector` Python package to ensure that the [singleton pattern](https://www.geeksforgeeks.org/singleton-design-pattern/) is maintained and to inject dependencies in services and other places where they are needed.

### Persistence layer
The persistence layer is the outmost layer, along with the presentation layer. This layer connects to the database, and carries the logic for creating a database session. It also contains the migration scripts created from Alembic.

### Presentation layer
This is the outmost layer and is the codebase's access point from external resources. In our case we call it the scraper layer as this layer contains the spiders. This will not contain any real logic and will for the most part use methods and services defined in the applicaiton layer.

## Dependency injection
Dependency injection simply put is passing external dependencies as a parameter in a class constructor or in the function defintion. For instance in the codeblock below `QuoteRepositoryService` is dependent on `session`. 
 
```python
class QuoteRepositoryService(RepositoryServiceBase):
    def __init__(self, session: Session):
        super().__init__(session)
```

It is therefore passed through the constructor (injected), instead of instantiating it in the constructor like this

```python
class QuoteRepositoryService(RepositoryServiceBase):
    def __init__(self):
        session = Session()
        super().__init__(session)
```

Combining dependency injection with the singleton pattern avoid excess instances of classes and ensure that there are not multiple database sessions activated at the same time.

When a new service or any other dependency is created, it can simply be added in [`container.py`](./src/application/container.py) like this

```python
session = providers.Factory(create_db_session)

quote_repository_service = providers.Factory(
    QuoteRepositoryService,
    session=session
)

quote_service = providers.Factory(QuoteService)
```

Note how `session` is passed as a parameter when defining `quote_repository_service` but not for `quote_service`. This is because the latter is not dependent on a database session. When using a service elsewhere simply import the service from the container class.
