class CommonBaseException(Exception):
    HTTP_STATUS_CODE = 400

    def __init__(self, *args: object, toast=False, http_status_code=0):
        self.toast = toast
        if http_status_code:
            self.HTTP_STATUS_CODE = http_status_code

        super().__init__(*args)


class ServerException(CommonBaseException):
    HTTP_STATUS_CODE = 500


class ClientException(CommonBaseException):
    HTTP_STATUS_CODE = 400


class SessionExpireException(ClientException):
    HTTP_STATUS_CODE = 401


class AuthException(ClientException):
    pass
