import requests
import sys

#Данные авторизации в API Trello
auth_params = {
	'key': "08afb3a8cef8676d01e67d63c012961f",
	'token': "175029f01f071872e6e969c327b77b038ce60fbd7e2024ce17f4f527eaa0f381", }

#Адрес, на котором расположен API Trello
#Именно туда отправлять HTTP запросы ROvqbd26
base_url = "https://api.trello.com/1/{}"
board_id = "ROvqbd26"

def read():
	#Получим данные всех колонок на доске
	column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

	#Теперь выведем название каждой колонки и всех заданий, которые к ней относятся
	for column in column_data:
		print(column['name'])
		#Получим данные всех задач в колонке и перечислим все названия
		task_data = requests.get(base_url.format('list') + '/' + column['id'] + '/cards', params=auth_params).json()
		if not task_data:
			print('\t' + 'Нет задач!')
			continue
		for task in task_data:
			print('\t' + task['name'])

def create(name, column_name):
	#Получаем данные всех колонок на доске
	column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

	#Перебером данные обо всех колонках, пока не найдем колонку, которая нам нужна
	for column in column_data:
		if column['name'] == column_name:
			#Создаем задачу с именем _name_ в найденой колонке
			requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})
			break

def move(name, column_name):
	#Получим данные всех колонок на доске
	column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

	#Среди всех колонок нужно найти задачу по имени и получить её id
	task_id = None
	for column in column_data:
		column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
		for task in column_tasks:
			if task['name'] == name:
				task_id = task['id']
				break
		if task_id:
			break
	#Теперь, когда у нас есть id задачи, которую мы хотим переместить
	#Переберем данные обо всех колонках, пока не найдем ту, в которую мы будем перемещать задачу
	for column in column_data:
		if column['name'] == column_name:
			#И выполним запрос к API для перемещения задачи в нужную колонку
			requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
			break

if __name__ == "__main__":
	if len(sys.argv) <= 2:
		read()
	elif sys.argv[1] == 'create':
		create(sys.argv[2], sys.argv[3])
	elif sys.argv[1] == 'move':
		move(sys.argv[2], sys.argv[3])