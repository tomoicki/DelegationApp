#!/usr/bin/env python

from app.app import create_app
from logging.handlers import RotatingFileHandler
import logging
import os


if __name__ == '__main__':
    app = create_app()
    handler = RotatingFileHandler('console_output.log')
    app.logger.addHandler(handler)
    # app.run(debug=False)
    app.run(debug=False, host='0.0.0.0', port='5001')
