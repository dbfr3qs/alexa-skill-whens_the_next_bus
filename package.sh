#!/bin/bash
if [ -e "lambda_handler.zip" ];
then
    rm -f lambda_handler.zip
fi
zip -r lambda_handler.zip next_bus.py ./bus -x */__pycache__/*