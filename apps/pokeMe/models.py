# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib import messages
import bcrypt, re, datetime

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UsersManager(models.Manager):
    def reg(self, data):
    	errors = []

    	if len(data['name']) < 3:
    		errors.append("Name must be at least two characters long.")
    	if len(data['alias']) < 3:
    		errors.append("Alias must be at least two characters long.")
		if data['email'] == '':
			errors.append("Email may not be blank")
		if not EMAIL_REGEX.match(data['email']):
			errors.append("Please enter a valid email address.")
		try:
			Users.objects.get(e_mail=data['email'])
			errors.append("Email is already registered")
		except:
			pass
		if data['dob'] == '':
			errors.append("Birthday is required.")
		elif datetime.datetime.strptime(data['dob'], '%Y-%m-%d') >= datetime.datetime.now():
			errors.append("Birthday may not be in the future!!")
    	if len(data['pass']) < 8:
    		errors.append("Password must be at least eight characters long.")
    	if data['pass'] != data['c_pass']:
    		errors.append("Password does not match Confirm Password.")

    	if len(errors) == 0:
    		data['pass'] = bcrypt.hashpw(data['pass'].encode('utf-8'), bcrypt.gensalt())
    		new_user = Users.objects.create(n_ame=data['name'], a_lias=data['alias'], e_mail=data['email'], pass_word=data['pass'], birthday=data['dob'])
    		return {
    			'new': new_user,
    			'error_list': None
    		}
    	else:
    		return {
    			'new': None,
    			'error_list': errors
    		}

    def log(self, data):
        errors = []
        try:
        	user = Users.objects.get(e_mail=data['email'])
        	if bcrypt.hashpw(data['pass'].encode('utf-8'), user.pass_word.encode('utf-8')) != user.pass_word.encode('utf-8'):
        		errors.append("Incorrect password.")
        except:
        	errors.append("Email not registered.")
        if len(errors) == 0:
        	return {
        		'logged_user': user,
        		'list_errors': None
        	}
        else:
            return {
                'logged_user': None,
                'list_errors': errors
            }

class PokesManager(models.Manager):
    def poke(self,data):
        Pokes.objects.create(poke=True, user_id=data['user_id'])

class Users(models.Model):
    n_ame = models.CharField(max_length=255)
    a_lias = models.CharField(max_length=255)
    e_mail = models.CharField(max_length=255)
    pass_word = models.CharField(max_length=255)
    birthday = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UsersManager()

class Pokes(models.Model):
    poke = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(Users, related_name='user_pokes')
    objects = PokesManager()
