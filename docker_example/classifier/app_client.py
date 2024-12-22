import os
import json
import time
import copy
import app_config
import logging
import service
from service import launch_task
from rq import Queue
from rq.job import Job
from rq.registry import FailedJobRegistry, StartedJobRegistry
from redis import Redis
from flask import Flask, jsonify, abort, make_response, request


if not os.path.exists('logs'):
    os.makedirs('logs')
    
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/logs.log'),
        logging.StreamHandler()
    ]
)


logging.info('Инициализация редиса')
redis_conn = Redis(host=app_config.REDIS_HOST, port=app_config.REDIS_PORT)
queue = Queue(app_config.REDIS_WORKER_NAME, connection=redis_conn, default_timeout=app_config.REDIS_JOB_TTL)

app = Flask(__name__)


# def process_unfinished_jobs():
#     logging.info("Checking for unfinished jobs...")
#     # This registry holds jobs that were started but interrupted

#     for job_id in queue.started_registry.get_job_ids():
#         job = queue.fetch_job(job_id)
#         if job and not job.is_finished and not job.is_failed:
#             logging.info(f"Re-enqueuing unfinished job {job.id}")
#             # Re-enqueue the unfinished job
#             queue.enqueue(job.func, *job.args, **job.kwargs, job_id=job.id)
#         else:
#             logging.info(f"Job {job.id} was not re-enqued")

# def get_jobs_from_redis():
#     """ Retrieve all jobs that were in started or queued state before restart """
#     job_ids = []

#     # Query Redis directly for jobs that are started or queued
#     all_jobs = redis_conn.keys("rq:job:*")  # Get all job keys from Redis
#     for job_key in all_jobs:
#         print
#         job = queue.fetch_job(job_key.decode())
#         if job and (job.get_status() in ["started", "queued"]):
#             job_ids.append(job.id)


# with app.app_context():
#     """Восстанавливаем состояние после падения системы."""
#     def recover_jobs():
#         get_jobs_from_redis()
#         process_unfinished_jobs()

def get_response(dict, status=200):
    return make_response(jsonify(dict), status)

def get_job_response(job_id):
    return get_response({'ok': job_id})

@app.route('/api/classifier/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    
    required_keys = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
    for key in required_keys:
        if key not in data:
            return jsonify({'ok': -1, 'message': f"Missing key: '{key}'"})

    job = queue.enqueue(launch_task, data, 'v1.0', result_ttl=app_config.REDIS_JOB_TTL)
    return get_job_response(job.get_id())


def get_process_response(process_status, status=200):
    return get_response({
        'status': process_status
    }, status)


@app.route('/api/classifier/analyze_status/<id_>')
def status(id_):
    job = queue.fetch_job(id_)

    if (job is None):
        return get_process_response(-1, 404)

    if (job.is_failed):
        return get_process_response(-2, 500)

    if (job.is_finished):
        return get_process_response(1)
    
    return get_process_response(0, 202)


@app.route('/api/classifier/get_result/<id_>')
def result(id_):
    job = queue.fetch_job(id_)
    
    if job is None:
        return get_process_response(-1, 404)

    if job.is_failed:
        return get_process_response(-2, 500)

    if job.is_finished:
        job_result = copy.deepcopy(job.result)
        result = job_result
    
        return get_response(result)

    return get_process_response(0, 202)


@app.route('/api/classifier/all_jobs', methods=['GET'])
def all_jobs():
    
    all_job_keys = redis_conn.keys("rq:job:*")  # Get all job keys from Redis
    all_jobs = []

    for job_key in all_job_keys:
        try:
            # Decode the Redis key and fetch the job
            job_id = job_key.decode().split(":")[-1]
            job = queue.fetch_job(job_id)
            if job:
                all_jobs.append({
                    "id": job.id,
                    "status": job.get_status(),
                    "created_at": str(job.created_at) if job.created_at else None,
                    "enqueued_at": str(job.enqueued_at) if job.enqueued_at else None,
                    "started_at": str(job.started_at) if job.started_at else None,
                    "ended_at": str(job.ended_at) if job.ended_at else None,
                })
        except Exception as e:
            logging.error(f"Error fetching job {job_key}: {e}")

    return get_response({"jobs": all_jobs})

    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'code': 'PAGE_NOT_FOUND'}), 404)

@app.errorhandler(500)
def server_error(error):
    return make_response(jsonify({'code': 'INTERNAL_SERVER_ERROR'}), 500)

if __name__ == '__main__':
    app.run(debug=True, host=app_config.APP_HOST, port=app_config.APP_PORT)