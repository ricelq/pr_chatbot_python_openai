# This file is part of the Prodeimat project
# @Author: Ricel Quispe

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import delete

db = SQLAlchemy()
migrate = Migrate()