import logging
from flaskface.post.Routes import new_post, post_detail, post_delete, post_update

logging.basicConfig(filename='debugR.log', level=logging.INFO,
                    format='%(%asctime)s:%(name)s:%(message)s')


check_new_post = new_post
check_post_detail = post_detail
check_post_delete = post_delete
check_post_update = post_update

logging.info(f'New Post Data{check_new_post}')
logging.info(f'Detail Post Data{check_post_detail}')
logging.info(f'Delete Post Data{check_post_delete}')
logging.info(f'Update Post Data{check_post_update}')


