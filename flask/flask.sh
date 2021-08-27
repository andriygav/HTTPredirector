#!/bin/bash
gunicorn --bind 0.0.0.0:$PORT "server:init('$1', '$2')" --threads $THREADS