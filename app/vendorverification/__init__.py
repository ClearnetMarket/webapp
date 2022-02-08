# coding=utf-8

from flask import Blueprint

vendorverification = Blueprint('vendorverification', __name__)

from . import views