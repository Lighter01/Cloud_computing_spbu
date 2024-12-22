# backend/app.py
import os
import logging
import copy
from rq import Queue
from redis import Redis
from flask import Flask, jsonify, request
import service
from service import launch_task

# Setup logging
if not os.path.exists('logs'):
    os.makedirs('logs')
    
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('logs/logs.log'), logging.StreamHandler()]
)

# Setup Redis
REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)
print(f"REDIS_HOST: {REDIS_HOST}, REDIS_PORT: {REDIS_PORT}")
logging.info(f"REDIS_HOST: {REDIS_HOST}, REDIS_PORT: {REDIS_PORT}")
redis_conn = Redis(host=REDIS_HOST, port=int(REDIS_PORT))
queue = Queue('classifier_rest_api', connection=redis_conn)

app = Flask(__name__)

def get_response(data, status=200):
    return jsonify(data), status

@app.route('/api/classifier/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    required_keys = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    for key in required_keys:
        if key not in data:
            return jsonify({'ok': -1, 'message': f"Missing key: '{key}'"})
    job = queue.enqueue(launch_task, data, 'v1.0', result_ttl=3600)
    return get_response({'ok': job.get_id()})

@app.route('/api/classifier/analyze_status/<id_>', methods=['GET'])
def status(id_):
    job = queue.fetch_job(id_)
    if job is None:
        return get_response({'status': -1}, 404)
    if job.is_failed:
        return get_response({'status': -2}, 500)
    if job.is_finished:
        return get_response({'status': 1})
    return get_response({'status': 0}, 202)

@app.route('/api/classifier/get_result/<id_>', methods=['GET'])
def result(id_):
    job = queue.fetch_job(id_)
    if job is None:
        return get_response({'status': -1}, 404)
    if job.is_failed:
        return get_response({'status': -2}, 500)
    if job.is_finished:
        return get_response(job.result)
    return get_response({'status': 0}, 202)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9995)
