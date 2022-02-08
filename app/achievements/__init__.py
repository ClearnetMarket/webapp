# coding=utf-8
__author__ = 'eeamesX'
from flask import Blueprint

achievements = Blueprint('achievements', __name__)

from . import views