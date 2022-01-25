# coding=utf-8
__author__ = 'eeamesX'
from flask import Blueprint

admin = Blueprint('admin', __name__)

from . import views