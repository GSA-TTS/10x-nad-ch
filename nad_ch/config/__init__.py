from .base import APP_ENV


if APP_ENV == "dev_local":
    from .development_local import *
elif APP_ENV == "dev_remote":
    from .development_remote import *
elif APP_ENV == "test":
    from .test import *
