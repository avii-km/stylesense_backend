import json
import logging
import traceback
from pymongo import MongoClient
import base64
import io

import torch
from torchvision import models, transforms

from stylesense_proj.apps.feature_extraction.services.ontology import all as ALL_PRODS

import numpy as np
from PIL import Image


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class FeatureExtractor(object, metaclass=Singleton):

    def __init__(self):
        self.model = None
        self.get_emb_model()

    def get_emb_model(self):
        if self.model is None:
            model = models.resnet50(pretrained=True)
            model.eval()
            self.model = model


    def get_emb_for_img(self, img_bin):

        preprocess = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        try:
            image = Image.open(io.BytesIO(img_bin)).convert('RGB')
            input_tensor = preprocess(image).unsqueeze(0)
            with torch.no_grad():
                embedding = self.model(input_tensor).squeeze().tolist()
            return embedding
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            return []


    def classify_prod_using_mongo(self, emb, entity):
        try:
            MONGO_URI = "mongodb+srv://laptopsahil123:sahilmongo12@cluster0.asnbdyu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
            DATABASE_NAME = "styluminya_v2"
            client = MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            col = db[entity]


            all_data = col.find()
            # print("len of doc", len(list(all_data)))
            mx_sim = 0
            best = ''
            for dt in all_data:

                try:
                    a = dt.get('img_emb')
                    if a and len(a) == 0:
                        continue
                    A_np = np.array(a)
                    B_np = np.array(emb)

                    # Compute cosine similarity
                    sim = np.dot(A_np, B_np) / (np.linalg.norm(A_np) * np.linalg.norm(B_np))
                    if sim > mx_sim:
                        best = dt.get('feature_value')
                        mx_sim = sim

                except Exception as e:
                    logging.error(f'err : {e}, log_key : ')
                    continue

            all_best = set()
            all_best.add(best)
            for dt in all_data:

                try:
                    a = dt.get('img_emb')
                    if a and len(a) == 0:
                        continue
                    A_np = np.array(a)
                    B_np = np.array(emb)

                    # Compute cosine similarity
                    sim = np.dot(A_np, B_np) / (np.linalg.norm(A_np) * np.linalg.norm(B_np))
                    if sim > 0.80:
                        all_best.add(dt.get('feature_value'))

                except Exception as e:
                    logging.error(f'err : {e}, log_key : ')
                    continue

            return list(all_best)

        except Exception as e:
            logging.error(f'e : {e}')

    def classify_prod_using_mongo_v2(self, emb, entity):
        try:
            import time
            MONGO_URI = "mongodb+srv://laptopsahil123:sahilmongo12@cluster0.asnbdyu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
            DATABASE_NAME = "styluminya_v3"
            client = MongoClient(MONGO_URI)
            db = client[DATABASE_NAME]
            col = db[entity]

            all_data = col.find()
            y = list(all_data)
            mx_sim = 0
            best = ''
            best_img = ''
            for dt in y:

                try:
                    a = dt.get('img_emb')
                    if a and len(a) == 0:
                        continue
                    A_np = np.array(a)
                    B_np = np.array(emb)

                    # Compute cosine similarity
                    sim = np.dot(A_np, B_np) / (np.linalg.norm(A_np) * np.linalg.norm(B_np))
                    if sim > mx_sim:
                        best = dt.get('feature_value')
                        best_img = dt.get('image_link')
                        mx_sim = sim

                except Exception as e:
                    logging.error(f'err : {e}, log_key : ')
                    continue

            all_recom = set()
            all_recom.add(best_img)
            yield f" {json.dumps({'success': True, 'event': 'message', 'message_type': 'related_products', 'message_data': best_img})}\n\n"

            for dt in y:
                try:
                    a = dt.get('img_emb')
                    if a and len(a) == 0:
                        continue
                    A_np = np.array(a)
                    B_np = np.array(emb)

                    # Compute cosine similarity
                    sim = np.dot(A_np, B_np) / (np.linalg.norm(A_np) * np.linalg.norm(B_np))
                    if sim > 0.88:
                        yield f" {json.dumps( {'success': True, 'event': 'message', 'message_type': 'related_products', 'message_data': dt.get('image_link')} )}\n\n"

                        all_recom.add(dt.get('image_link'))

                except Exception as e:
                    logging.error(f'err : {e}, log_key : ')
                    continue


            return best, mx_sim, list(all_recom)

        except Exception as e:
            logging.error(f'e : {e}')


    def convert_base64_to_image(self,base64_string, output_file):
        try:
            # Check if the string contains a MIME type and strip it if necessary
            if base64_string.startswith('data:image/'):
                base64_string = base64_string.split(',')[1]  # Remove metadata

            # Decode the Base64 string
            image_data = base64.b64decode(base64_string)

            # Write the decoded data to an image file
            with open(output_file, 'wb') as img_file:
                img_file.write(image_data)

            return {'success': True}
        except Exception as e:
            logging.error(f'')
            return {'success': False}


    def process_feature_extraction(self, session_data, body, params):
        import time
        try:

            logging.info(f'enter into process_feature_extraction')


            prod_image_bin_data = body.get('prod_img_bin_data')

            decoded_data = base64.b64decode(prod_image_bin_data)

            prod_emb =  self.get_emb_for_img(decoded_data)


            yield f" {json.dumps( {'success': True, 'event': 'stream started'} )}\n\n"


            prod_cat = self.classify_prod_using_mongo(prod_emb, 'all_products' )
            logging.info(f'prod_cat : {prod_cat}')

            prod_ft_list = {}

            for prod in prod_cat:
                # print(prod)

                features = ALL_PRODS[prod]
                ft_list = []
                for ft in features:

                    a = yield from self.classify_prod_using_mongo_v2(prod_emb, f"{prod}__{ft.replace(' ', '_')}" if prod in ('Dresses', 'Earrings', 'Shirts') else f"{prod}__{ft.replace(' ', '_').lower()}" )
                    # print(ft, a[0])
                    ft_list.append({ 'feature_name': ft , 'feature_value': a[0], 'confidence_score': a[1] })
                    yield from f" {json.dumps({'success': True, 'event': 'message', 'product_category' : prod,   'product_feature': ft_list[-1]})}\n\n"

                prod_ft_list[prod] = ft_list

                yield f" {json.dumps({'success': True, 'event': 'stream closed'})}\n\n"



        except Exception as e:
            logging.error(f'error is : {traceback.format_exc()}, log_key : process_feature_extraction')
            yield f" {json.dumps({'success': False})}\n\n"
            time.sleep(1)  # Simulate a delay






