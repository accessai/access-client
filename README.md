# Access Client

Python client to interact with acessai's various applications/services like access-face-vision

### Installation
```bash
pip install access-cleint
```

### Usage
```python
from access_client.face_vision.client import AFV

#instantiate by giving the host and port of the access-face-vision server
afv = AFV("http://localhost:5001")
```

Now we need to create a face-group. This is will be our face-index.
```python
afv.create_face_group(face_group_name="celebrities")

#Pass in the directory and face group name
afv.add_faces_to_face_group(dir="./samples/celebrities", face_group="celebrities")

# Directory structure
# **/Images/
#          A/
#           A_K_01.jpg
#           A_K_02.jpg
#          B/
#           B_S_01.jpg
#           B_S_02.jpg
```

Once faces are indexed we can run inference on it. 
```python
afv.parse(img_path="./samples/celebrities/Bill Gates/Bill_Gates.jpg", face_group="celebrities")
```