import logging
from flaskface.user.Routes import registers, login, logout, account, user_posts


logging.basicConfig(filename='debuglog.log', level=logging.WARNING,
                    format='%(asctime)s:%(name)s:%(message)s')

debug_registers = registers
debug_login = login
debug_logout = logout
debug_account = account
debug_userposts = user_posts

logging.warning(f'Register {debug_registers}')
logging.warning(f'Login {debug_login}')
logging.warning(f'Logout {debug_logout}')
logging.warning(f'Account {debug_account}')
logging.warning(f'User Post {debug_userposts}')