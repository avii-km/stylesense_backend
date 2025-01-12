"""
This module represents the Helth-Check controller end-point.

This end-point is not part of the specification and is configured
directly with Flask

Example:
    To open the end-point 'http://<host>:<port>/health'
"""

import json
from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import logging


@csrf_exempt
def home(request):
    if request.method == 'GET':
        logging.debug('GET Request')
    if request.method == 'POST':
        logging.debug('POST Request')
    return render(request, "index.html")


@csrf_exempt
def health(request, skip_auth_middleware_list):
    """
    Get the health of the service.

    Returns:
        Ok response
    """

    logging.debug(f"Entered health check DEBUG level Logs")
    logging.info(f"Entered health check INFO level Logs")
    return HttpResponse(json.dumps({'success': True}))
