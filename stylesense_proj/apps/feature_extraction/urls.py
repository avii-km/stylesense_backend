from django.urls import path, include
from stylesense_proj.apps.feature_extraction import views
from django.conf import settings
CONFIGS = getattr(settings, "CONFIGS", {})

urlpatterns = [
    path('extract_features/', views.extract_features,

             {"session_data": {},
                 "skip_auth_middleware_list": [],
              "pre_login_url_name_list": ["login"],
              "params": {"session_conf": {}, "db_connection_obj": CONFIGS.get("MYSQL_DB_CONFIG"),
                     "auth_project": 'stylesense'}}, name="view_all_cf"),


    path('get_feedback/', views.get_feedback,

         {"session_data": {},
          "skip_auth_middleware_list": [],
          "pre_login_url_name_list": ["login"],
          "params": {"session_conf": {}, "db_connection_obj": CONFIGS.get("MYSQL_DB_CONFIG"),
                     "auth_project": 'stylesense'}}, name="view_all_cf"),

]