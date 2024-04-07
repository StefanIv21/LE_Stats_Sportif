"This module initializes the webserver."
import threading
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool
from .mylogging import configure_logger

webserver = Flask(__name__)
webserver.logger = configure_logger()
webserver.tasks_runner = ThreadPool(webserver.logger)
webserver.data_ingestor = DataIngestor(
    "./nutrition_activity_obesity_usa_subset.csv",
    webserver.logger)
webserver.job_counter = 1

from app import routes
