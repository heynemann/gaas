#!/usr/bin/python
# -*- coding: utf-8 -*-


def get_class(klass):
    module_name, class_name = klass.rsplit('.', 1)

    module = __import__(module_name)

    if '.' in module_name:
        module = reduce(getattr, module_name.split('.')[1:], module)

    return getattr(module, class_name)
