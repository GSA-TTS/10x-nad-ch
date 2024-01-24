from .base import APP_ENV


if APP_ENV == 'development-local' or APP_ENV == 'test':
    from .development_local import *
elif APP_ENV == 'development-remote':
    from .development_remote import *
