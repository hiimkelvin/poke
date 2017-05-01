# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Count
from .models import Users, Pokes

def index(request):
    # Users.objects.all().delete()
    return render(request, 'pokeMe/index.html')

def register(request):
	context = {
		'name': request.POST['name'],
        'alias': request.POST['alias'],
        'email': request.POST['email'],
		'pass': request.POST['password'],
		'c_pass': request.POST['confirm_pw'],
        'dob': request.POST['dob'],
	}
	reg_results = Users.objects.reg(context)
	if reg_results['new'] != None:

		request.session['users_id'] = reg_results['new'].id
		request.session['users_name'] = reg_results['new'].n_ame
		return redirect('/pokes')
	else:
		for error_str in reg_results['error_list']:
			messages.add_message(request, messages.ERROR, error_str)
		return redirect('/')

def login(request):
    context = {
        'email': request.POST['email'],
        'pass': request.POST['password'],
    }
    results = Users.objects.log(context)
    if results['list_errors'] != None:
        for error in results['list_errors']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('/')
    else:
        request.session['users_id'] = results['logged_user'].id
        request.session['users_name'] = results['logged_user'].n_ame
        return redirect('/pokes')

def homepage(request):
    if 'users_id' not in request.session:
        messages.add_message(request, messages.ERROR, 'You must be logged in to view that page.')
        return redirect('/')

    user = Users.objects.get(id=request.session['users_id'])
    context ={
        'other_users': Users.objects.all(),
    }
    return render(request, 'pokeME/pokes.html', context)

def poking(request, user_id):
    pokes = Pokes.objects.get(id=user_id)
    users = Users.objects.get(id=request.session['users_id'])
    context = {
        'user_id': users,
        'pokes_id': pokes,
    }
    Pokes.objects.poke(context)
    return redirect('/pokes')

def logout(request):
	request.session.clear()
	return redirect('/')
