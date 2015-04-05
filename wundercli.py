#!/usr/bin/env python2

import random
import urllib2
import json
import requests
import sys


AUTH_FILE = 'wunderlist_auth.json'
auth_data_dict = {
	'client_id': '',
	'client_secret': '',
	'redirect_uri': '',
	'code': '',
	'access_token': ''
}
header_dict = {}

'''
  authenticate to wunderlist
'''
def oauth2_wunderlist():
	auth_data_dict['state'] = str(random.random())[2:]
	start_url = "https://www.wunderlist.com/oauth/authorize?client_id=%(client_id)s&redirect_uri=%(redirect_uri)s&state=%(state)s\n" % auth_data_dict

	access_token_dict = {}
	print 'Warning! Do no continue if "state" is not "%s"' % auth_data_dict['state']
	access_token_dict['code'] = raw_input(start_url)
	access_token_dict['client_id'] = auth_data_dict['client_id']
	access_token_dict['client_secret'] = auth_data_dict['client_secret']

	access_token_url = "https://www.wunderlist.com/oauth/access_token"

	access_token_data = requests.post(access_token_url, json=access_token_dict)

	if access_token_data.status_code == 200:
		access_token = json.loads(access_token_data.text)['access_token']
	else:
		sys.exit(access_token_data.status_code)

	auth_data_dict['access_token'] = access_token

'''
  find list by name
  return list id or error
'''
def find_list(list_name):
	list_info_url = "https://a.wunderlist.com/api/v1/lists"
	list_info_data = requests.get(list_info_url, headers=header_dict)

	if list_info_data.status_code != 200:
		sys.exit(list_info_data.status_code)

	# internaly inbox list is lowercase
	if list_name.lower() == 'inbox':
		list_name = 'inbox'

	for user_list in json.loads(list_info_data.text):
		if list_name == user_list['title']:
			print 'Found List: %s' % list_name
			return 0, user_list['id']

	return -1, 'No list found for: %s' % list_name

'''
  create list by name, does not check if exists
  return new list id
'''
def create_list(list_name):
	list_create_url = "https://a.wunderlist.com/api/v1/lists"
	list_create_json = {
		'title': list_name
	}
	list_create_data = requests.post(list_create_url, headers=header_dict, json=list_create_json)

	if list_create_data.status_code != 201:
		sys.exit(list_create_data.status_code)

	return json.loads(list_create_data.text)['id']

'''
  add task to list_id
  return new task id
'''
def add_task_to_list(list_id, task_title):
	task_create_url = "https://a.wunderlist.com/api/v1/tasks"
	task_create_json = {
		'list_id': list_id,
		'title': task_title
	}
	task_create_data = requests.post(task_create_url, headers=header_dict, json=task_create_json)

	if task_create_data.status_code != 201:
		sys.exit(task_create_data.status_code)

	return json.loads(task_create_data.text)['id']


'''
  save authorisation data to file
'''
def save_authorisation(file_name, auth_data_dict):
	with open(file_name, 'w') as auth_file:
		json.dump(auth_data_dict, auth_file, sort_keys=True, indent=4)

'''
  load authorisation data from file
'''
def load_authorisation(file_name):
	with open(file_name, 'r') as auth_file:
		return json.load(auth_file)

if __name__ == '__main__':
	import os.path

	if os.path.isfile(AUTH_FILE):
		auth_data_dict = load_authorisation(AUTH_FILE)

	if not 'access_token' in auth_data_dict:
		oauth2_wunderlist()
		save_authorisation(AUTH_FILE, auth_data_dict)

	header_dict['X-Access-Token'] = auth_data_dict['access_token']
	header_dict['X-Client-ID'] = auth_data_dict['client_id']

	list_name = raw_input('Enter name for list\n')
	error_code, list_id = find_list(list_name)

	if error_code != 0:
		print "Error: %d (%s)" % (error_code, list_id, )
		list_id = create_list(list_name)

	print 'Enter tasks to add to list:'
	task_list = []
	while True:
		last_input = raw_input()
		if not last_input:
			break
		task_list.append(last_input)

	print 'Adding tasks to list: %s (%s)' % (list_name, list_id, )
	for task in task_list:
		add_task_to_list(list_id, task)
