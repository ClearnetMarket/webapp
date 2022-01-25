# coding=utf-8
__author__ = 'eeamesX'
from flask import Blueprint

affiliate = Blueprint('affiliate', __name__)

from . import views