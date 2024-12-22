import app_config

import logging
import pandas as pd
import numpy as np

import os
from os import walk
from datetime import datetime
import time
from lib.predictor import get_model, predict


ROOT_DIR = os.path.dirname(os.path.abspath(__file__)) 


logging.info('Загрузка обученной модели')
MODEL = get_model(f'{ROOT_DIR}/{app_config.MODEL_PATH}')

def launch_task(data: list, 
                api: str) -> dict:

    '''
        Запуск задачи на классификацию контрактов.
        
        Параметры
        ------------
        
        data: dict
            словарь с данными
        
        api: str
            Версия API 
            
        Возвращает
        ------------
        
        results: dict
            Словарь с успешными результатами классификации ("results") и теми, которые не удалось выгрузить из API ("fail_contracts")
        
    '''
    digit = predict(data, MODEL)
    time.sleep(50)
    
    if api == 'v1.0':
        res_dict = {'result':  digit}
        return res_dict
    else:
        res_dict = {'error': 'API doesnt exist'}
        return res_dict
