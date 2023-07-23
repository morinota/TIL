class MyError(Exception):
    pass


class NotFoundError(MyError):
    def __init__(self, entity_id: str) -> None:
        self.entity_id = entity_id
