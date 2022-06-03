import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'smart.settings')


import django

django.setup()


# Fake Population script

import random

from base.models import User, Shop
from shop.models import Product

from faker import Faker

faker = Faker()


topics = ['search']



def add_topic():
    t = Topic.objects.get_or_create(top_name = random.choice(topics))[0]
    t.save()
    return t

def populate(N = 5):
    for entry in range(N):

        top = add_topic()

        #  create the data

        fake_url = fakegen.url()
        fake_date = fakegen.date()
        fake_name = fakegen.company()

        webpg = Webpage.objects.get_or_create()

