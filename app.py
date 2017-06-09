

from flask import Flask,jsonify,abort, request, make_response
from flask.ext.httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

clients =[
	{
		'id':1,
		'login': 'Gabriel',
		'password': 'python'
	},
	{
		'id':2,
		'login': 'Joao',
		'password': '123'
	}
]

@auth.get_password
def get_password(username):
	for client in clients:
		if username == client['login']:
			return client['password'] 
	return None

@auth.error_handler
def unauthorized():
	return make_response(jsonify({'error': 'Acces Denied'}),401)

app = Flask(__name__)
#Our database
tasks = [
		{
		'id': 1,
		'title': u'Buy groceries',
		'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
		'done': False,
		'client_id': 1        	
	},
        {
		'id': 2,
		'title': u'Learn Python',
		'description': u'Need to find a good Python tutorial on the web', 
		'done': False,
       		'client_id': 2
	 }
]
#our route for errors
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({'error':  'Not found'}), 404)

#the function to GET methods from dataase
@app.route('/todo/api/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
	task = [task for task in tasks if task['id'] == task_id] 
	if len(task) == 0:
		abort(404)	
	return jsonify({'task':task[0]})

#remeber thic could be used with, forms, db, etc
#inserting new task

@app.route('/todo/api/tasks', methods=['POST'])
@auth.login_required
def create_task():
	if not request.json or not 'title' in request.json:
	#if dont get nothing or the title is empty, the BAD request
		abort(400)
	task = {
		'id': tasks[-1]['id'] +1,
		'title': request.json['title'],
		#get the description if is empty set it to ""
		'description': request.json.get('description',""),
		'done': False
	}
	tasks.append(task)
	#if everthing whent ok then we send the task+ created code
	return jsonify({'task':task}), 201

def valide(task):
	if len(task) == 0:
		abort(404)
	if not request.json:
		abort(400)
	if 'title' in request.json and type(request.json['title']) != unicode:
		abort(400)
	if 'description' in request.json and type(request.json['description']) is not unicode:
		abort(400)
	if 'done' in request.json and type(request.json['done']) is not bool:
		abort(400)
	return True

#update	
@app.route('/todo/api/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
	task = [task for task in tasks if task['id'] == task_id]
	if valide(task):
		task[0]['title'] 
#delete
@app.route('/todo/api/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
	if task_id not in tasks['id']:
		abort(404)
	task = [task for task in tasks if task['id'] == task_id]
	tasks.remove(task[0])
if __name__ == '__main__':
	app.run(debug=True)

