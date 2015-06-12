# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Copyright 2014, Cercle Informatique ASBL. All rights reserved.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or (at
# your option) any later version.
#
# This software was made by hast, C4, ititou at UrLab, ULB's hackerspace

from django.shortcuts import render

from telepathy.models import Thread
from documents.models import Document, Page
from users.models import User
from users.authBackend import NetidBackend

import settings


def index(request, p402=False):
    if not request.user.is_authenticated():
        context = auth_page_context(request)
        if p402:
            return render(request, "p402.html", context)
        else:
            return render(request, "index.html", context)
    else:
        return feed(request)


def auth_page_context(request):
    next_url = request.GET.get("next", "")

    def floor(num, r=1):
        r = 10 ** r
        return int((num // r) * r)

    return {
        "login_url": NetidBackend.login_url(next_url),
        "debug": settings.DEBUG,
        "documents": floor(Document.objects.count()),
        "pages": floor(Page.objects.count(), 2),
        "users": floor(User.objects.count()),
        "threads": floor(Thread.objects.count()),
    }


def feed(request):
    courses = request.user.followed_courses.all()
    documents = Document.objects.filter(course__in=courses)
    documents = documents.select_related('course').select_related('user')
    documents = documents.order_by('-id').filter(state="DONE")
    documents = documents[:20]

    context = {
        'documents': documents
    }
    return render(request, "home.html", context)
