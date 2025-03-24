from dependency_injector import containers, providers

from ..persistence import create_db_session


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(modules=["src.scraper.pipelines"])

    session = providers.Factory(create_db_session)
