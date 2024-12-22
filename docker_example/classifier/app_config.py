MODEL_PATH = 'lib/models/model.pkl' # Путь до модели

# Настройки хоста сервиса
APP_HOST = '0.0.0.0'
APP_PORT = '9995' # Порт для сервиса классификации

# Настройки хоста Redis
REDIS_HOST = 'redis' # Хост, где расположен Redis
REDIS_PORT = 6379
REDIS_WORKER_NAME = 'classifier_rest_api' # Воркер для app_client.py
REDIS_JOB_TTL = 60 * 60 # Срок жизни хранения результата в секундах: 1 час
