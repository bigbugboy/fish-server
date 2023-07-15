import typing

import settings
from common.app import ExtensionMixin
from common.extensions.jwtext import Jwt

jwt = Jwt(**settings.JWT)


EXTENSIONS: typing.List[ExtensionMixin] = [
    jwt,
]
