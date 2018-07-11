# -*- coding: utf-8 -*-
#
# Author: Roman Savchenko <r.sav4enko@gmail.com>
# Created: 2016-02-23
#
# Id: $Id$
import datetime

from base import BaseHandler


class IndexHandler(BaseHandler):
    allowed_methods = ('GET', )

    def get(self):
        return self.success({
            "current_time": datetime.datetime.now().isoformat()
        })