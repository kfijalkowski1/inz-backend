class DBException(Exception):
    def __init__(self, message):
        super().__init__(message)


# Exceptions text consts
BAD_WORKER_TYPE = "Zły typ pracownika"
USER_EXISTS = "Użytkownik o podanej nazwie już istnieje"
BAD_DEPARTMENT = "Zły dział"