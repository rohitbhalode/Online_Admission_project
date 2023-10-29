
import logging
from werkzeug.serving import WSGIRequestHandler

logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Define a logger with the root name
logger = logging.getLogger('werkzeug')
logger.setLevel(logging.ERROR)

WSGIRequestHandler.handler_class = lambda *args, **kwargs: logging.StreamHandler()