import datetime, os, logging

from logging.handlers import SMTPHandler, RotatingFileHandler
from app import app, cli


def view_reload_time():
    file_name = os.path.basename(__file__)
    server_gmt_time  = datetime.datetime.now()
    view_reload_time = [f'[{server_gmt_time.strftime("%d-%m-%Y %H:%M")}]']

    colors_set = {'blue' : '[34m',
                  'green': '[32m',
                  'red'  : '[31m'}

    paint_text = lambda text, color: f'\u001b{colors_set.get(color)}{text}\u001b[0m'

    template_view = '\n{0}: {2} {1}'.format(
                    paint_text('RELOAD', 'red'),
                    paint_text(view_reload_time[0], 'green'),
                    paint_text(file_name, 'blue'))
    return template_view

def start_logging():
    if not os.path.exists('logs'):
        os.mkdir('logs')

    file_handler = RotatingFileHandler('logs/runner.log', maxBytes=10240, backupCount=10, encoding='UTF-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Worked/Logging: runner.py')



if __name__ == '__main__':
    
    print(view_reload_time())
    start_logging()

    app.run()