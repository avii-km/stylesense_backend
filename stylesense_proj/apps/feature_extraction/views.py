import json, logging
import traceback
import http
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from stylesense_proj.apps.feature_extraction.services.feature_extractor import FeatureExtractor
from django.http import StreamingHttpResponse

feature_extractor_obj = FeatureExtractor()



@csrf_exempt
def extract_features(request, session_data, skip_auth_middleware_list, pre_login_url_name_list, params):
    try:
        try:
            body = json.loads(request.body.decode('utf-8'))
        except:
            body = {}

        stream = feature_extractor_obj.process_feature_extraction(session_data, body, params)

        response = StreamingHttpResponse(stream, content_type="text/event-stream")
        response['Cache-Control'] = 'no-cache'
        return response

        # return StreamingHttpResponse(stream, content_type="json/event-stream")
        # resp = feature_extractor_obj.process_feature_extraction(session_data, body, params)
        # return HttpResponse(json.dumps(resp, default=str), status=http.HTTPStatus.OK, content_type="application/json")
    except Exception as exp:
        logging.error(f"Error in processing make cf_live, err: {traceback.format_exc()}, log_key: deactivate_cf")
        return HttpResponse(json.dumps({'success': False}, default=str), status=http.HTTPStatus.OK,
                            content_type="application/json")
@csrf_exempt
def get_feedback(request, session_data, skip_auth_middleware_list, pre_login_url_name_list, params):
    try:
        try:
            body = json.loads(request.body.decode('utf-8'))
            print("body here")
        except:
            body = {}
        resp = {'success': True, 'message': 'thanks for feedback'}
        return HttpResponse(json.dumps(resp, default=str), status=http.HTTPStatus.OK, content_type="application/json")
    except Exception as exp:
        logging.error(f"Error in processing make cf_live, err: {traceback.format_exc()}, log_key: deactivate_cf")
        return HttpResponse(json.dumps({'success': False}, default=str), status=http.HTTPStatus.OK,
                            content_type="application/json")


