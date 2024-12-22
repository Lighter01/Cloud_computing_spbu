#!/bin/bash
rq worker classifier_rest_api --path /app & python app.py