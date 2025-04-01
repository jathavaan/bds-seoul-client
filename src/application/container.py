from dependency_injector import containers, providers

from ..persistence import create_db_session
from ..application.services.author_service import AuthorRepositoryService
from ..application.services.quote_service import QuoteRepositoryService, QuoteService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.scraper.pipelines"])

    session = providers.Singleton(create_db_session)

    author_repository_service = providers.Singleton(
        AuthorRepositoryService,
        session=session
    )

    quote_repository_service = providers.Singleton(
        QuoteRepositoryService,
        session=session
    )

    quote_service = providers.Singleton(QuoteService)
