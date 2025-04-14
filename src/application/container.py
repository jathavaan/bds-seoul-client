from dependency_injector import containers, providers

from src.persistence import create_db_session
from src.application.services.author_service import AuthorRepositoryService
from src.application.services.quote_service import QuoteRepositoryService, QuoteService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.scraper.pipelines"])

    session = providers.Factory(create_db_session)

    author_repository_service = providers.Factory(
        AuthorRepositoryService,
        session=session
    )

    quote_repository_service = providers.Factory(
        QuoteRepositoryService,
        session=session
    )

    quote_service = providers.Factory(QuoteService)
