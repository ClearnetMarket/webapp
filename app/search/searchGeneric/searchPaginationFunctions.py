
from flask import request
from flask_paginate import Pagination


def paginationView(page,links,per_page,offset,inner_window,outer_window,total):
    pagination = get_pagination(page=page,
                                links=links,
                                per_page=per_page,
                                offset=offset,
                                inner_window=inner_window,
                                outer_window=outer_window,
                                # total number of results
                                total=total,
                                format_total=True,  # format total. example 1,024
                                format_number=True,  # turn on format flag
                                record_name='links'
                                )
    return pagination


def searchs():
    return True


def get_css_framework():
    return 'bootstrap4'


def get_link_size():
    return 'sm'


def show_single_page_or_not():
    return False


def get_page_items():

    page = int(request.args.get('page', 1))

    per_page = request.args.get('per_page')
    if not per_page:
        per_page = 20
    else:
        per_page = int(per_page)

    if page == 1:
        offset = 0
    else:
        offset = (page - 1) * per_page

    return page, per_page, offset


def get_pagination(**kwargs):
    kwargs.setdefault('record_name', 'repositories')

    return Pagination(css_framework=get_css_framework(),
                      link_size=get_link_size(),
                      show_single_page=show_single_page_or_not(),
                      **kwargs
                      )
