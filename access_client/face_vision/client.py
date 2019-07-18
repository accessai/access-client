import os
import logging
from PIL import Image
import base64

import requests
from glob import glob


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EncodedImage(object):

    def __init__(self, img_b64_str, width, height, mode):
        self.img_b64_str = img_b64_str
        self.size = (width, height)
        self.mode = mode

    def to_json(self):
        return {
            "image": self.img_b64_str,
            "width": self.size[0],
            "height": self.size[1],
            "mode": self.mode
        }


class AFV(object):

    def __init__(self, host, timeout=4):

        if host[-1] == '/':
            host = host[:-1]

        self.host = host
        self.parse_url = self.host + "/afv/v1/parse/image"
        self.fg_url = self.host + "/afv/v1/facegroup"
        self.faceid_url = self.host + "/afv/v1/facegroup/faceid"
        self.faceids_url = self.host + "/afv/v1/facegroup/faceids"
        self.timeout = timeout

    def _encode_image(self, img_path: str) -> EncodedImage:
        img = Image.open(img_path)
        mode = img.mode
        width, height = img.size
        img_str = base64.encodebytes(img.tobytes()).decode('utf-8')
        return EncodedImage(img_str, width, height, mode)

    def _decode_image(self, img: EncodedImage) -> Image.Image:
        return Image.frombytes(img.mode, img.size, base64.decodebytes(img.img_b64_str))

    def parse(self, img_path: str, face_group) -> (dict, int):
        encoded_image = self._encode_image(img_path)
        req_json = encoded_image.to_json()
        req_json['face_group'] = face_group

        headers = {"ContentType": "application/json"}
        response = requests.post(self.parse_url, json=req_json, headers=headers, timeout=self.timeout)

        resp_json = response.json()
        return resp_json, response.status_code

    def create_face_group(self, face_group_name):
        headers = {"ContentType": "application/json"}
        response = requests.post(self.fg_url, json={'face_group': face_group_name}, headers=headers, timeout=self.timeout)

        resp_json = response.json()
        return resp_json, response.status_code

    def add_face_to_face_group(self, img_path, face_group):
        encoded_img = self._encode_image(img_path)

        headers = {"ContentType": "application/json"}
        req_json = encoded_img.to_json()
        req_json['face_group'] = face_group
        req_json['label'] = os.path.basename(img_path).split(".")[0]
        response = requests.put(self.faceid_url, json=req_json, headers=headers,
                                timeout=self.timeout)

        resp_json = response.json()
        logger.info(resp_json)

        return resp_json, response.status_code

    def add_faces_to_face_group(self, dir, face_group):
        images = glob(os.path.join(dir, "**/*.*"), recursive=True)

        results = []
        for img_path in images:

            if img_path.split(".")[-1].lower() not in ['jpg', 'jpeg']:
                logger.warning("Invalid image extension found. We support only jpeg/jpg images.")
                continue

            resp_json, status_code = self.add_face_to_face_group(img_path, face_group)

            results.append({"image": img_path, "response": resp_json, "status_code": status_code})

        return results

    def delete_face_group(self, face_group):
        headers = {"ContentType": "application/json"}
        response = requests.delete(self.fg_url, json={'face_group': face_group}, headers=headers,
                                 timeout=self.timeout)

        resp_json = response.json()
        return resp_json

    def delete_face_id(self, face_group, face_id):
        headers = {"ContentType": "application/json"}
        response = requests.delete(self.fg_url, json={'face_group': face_group, 'face_id': face_id}, headers=headers,
                                 timeout=self.timeout)

        resp_json = response.json()
        return resp_json

    def list_face_ids(self, face_group):
        headers = {"ContentType": "application/json"}
        response = requests.post(self.faceids_url, json={'face_group': face_group}, headers=headers,
                                 timeout=self.timeout)

        resp_json = response.json()
        return resp_json

