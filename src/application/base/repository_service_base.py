from sqlalchemy.orm import Session


class RepositoryServiceBase:
    session: Session

    def __init__(self, session: Session):
        self.session = session
