import datetime, os, logging

from flask import request
from logging.handlers import RotatingFileHandler
from app import create_app
from customlogger import get_logger



# def view_reload_time():
#     file_name = os.path.basename(__file__)
#     server_gmt_time  = datetime.datetime.now()
#     view_reload_time = [f'[{server_gmt_time.strftime("%d-%m-%Y %H:%M")}]']

#     colors_set = {'blue' : '[34m',
#                   'green': '[32m',
#                   'red'  : '[31m'}

#     paint_text = lambda text, color: f'\u001b{colors_set.get(color)}{text}\u001b[0m'

#     template_view = '\n{0}: {2} {1}'.format(
#                     paint_text('RELOAD', 'red'),
#                     paint_text(view_reload_time[0], 'green'),
#                     paint_text(file_name, 'blue'))
#     return template_view

# def start_logging(app):
#     if not os.path.exists('logs'):
#         os.mkdir('logs')

#     file_handler = RotatingFileHandler('logs/runner.log', maxBytes=1024, backupCount=5, encoding='UTF-8')
#     file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
#     file_handler.setLevel(logging.INFO)

#     app.logger.addHandler(file_handler)
#     app.logger.setLevel(logging.INFO)
#     app.logger.info('Worked/Logging: runner.py')
#     app.logger.info(view_reload_time())


if __name__ == '__main__':
    logger = get_logger(sreaming=True, name='FLASK_RUNNER')
    app    = create_app()
    # start_logging(app)
    # print(view_reload_time())

    with app.app_context():
        logger.info('runner is work')
        app.run()