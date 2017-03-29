from __future__ import unicode_literals
from django.db import models
import re, bcrypt
import datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def register(self, data):

        errors = []
        for field in data:
            if len(data[field]) == 0:
                errors.append(field + " cannot be blank!")

        if len(data['first_name']) < 3:
            errors.append("First name must be at least 3 characters long")
        if len(data['username']) < 3:
            errors.append("Username must be at least 3 characters long")
        if not EMAIL_REGEX.match(data['email']):
            errors.append("PLEASE enter valid email")
        try:
            self.get(email=data['email'])
            errors.append("Email already registered")
        except:
            pass
        try:
            self.get(username=data['username'])
            errors.append("Alias already registered")
        except:
            pass
        if not data['first_name'].isalpha():
            errors.append("Name may only be letters")
        if not data['password'] == data['confirm']:
            errors.append("Passwords must match")
        if len(data['password']) < 8:
            errors.append("Password must be at least 8 characters long")
        if len(data['date']) < 8:
            errors.append("Please provide your birthday")
        if len(data['date']) >= 8:
            s = data['date']
            f = "%Y-%m-%d"
            date = datetime.datetime.strptime(s, f)
            if date > datetime.datetime.now():
                errors.append("Please select a valid birthday")
        if len(errors) != 0:
            return {'errors': errors}

        data['password'] = bcrypt.hashpw(data['password'].encode('utf8'), bcrypt.gensalt())
        user = self.create(first_name=data['first_name'], username=data['username'], email=data['email'], password=data['password'])

        return {'user': user}

    def login(self, data):
        errors = []
        try:
            user = self.get(username=data['username'])
            if bcrypt.hashpw(data['password'].encode('utf8'), user.password.encode('utf8')) == user.password.encode('utf8'):
                return {'user': user}
            errors.append('Wrong password')
        except:
            errors.append('Username not registered')
        return {'errors': errors}


class User(models.Model):
    first_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
