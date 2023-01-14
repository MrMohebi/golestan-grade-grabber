

# captcha solver cloned from https://github.com/mdhi2000/captcha-solver
# see more there

import base64
from time import time
from PIL import Image
import requests
from io import BytesIO
import numpy as np
from joblib import load
import bottle
from bottle import response, request

app = bottle.app()


class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers[
                'Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors


def split_images_y(img):
    imgs = []
    start = 0
    start_found = False
    end = 0
    for (idy, y) in enumerate(img[0]):

        tmp = img[
              :,
              idy
              ].flatten()
        if start_found:
            # print("end - start",start - end)
            if list(tmp).count(1) < 2:
                start_found = False
                end = idy
                imgs.append(img[
                            :,
                            start:end
                            ])
        else:
            if not list(tmp).count(1) < 2:
                start_found = True
                start = idy
    return imgs


def split_images_x(img):
    imgs = []
    start = 0
    start_found = False
    end = 0
    for (idx, x) in enumerate(img):

        tmp = img[
              idx,
              :
              ].flatten()
        if start_found:
            if list(tmp).count(1) < 2:
                start_found = False
                end = idx
                imgs.append(img[
                            start:end,
                            :
                            ])
        else:
            if not list(tmp).count(1) < 2:
                start_found = True
                start = idx
    return imgs


def main(img=None):
    clf = load("edu.pkl")

    id = str(time())
    if img is None:
        res = requests.get(
            'https://eduold.uk.ac.ir/Forms/AuthenticateUser/captcha.aspx')
        img = Image.open(BytesIO(res.content)).convert("HSV")
    start_time = time()

    src_img = img.convert("RGB")
    img = img.convert('L')

    np_img = np.array(img)

    np_img[46:50, 45:80] = 255
    np_img[46:50, 85:95] = 255
    np_img[46:50, 100:140] = 255

    np_img = np.where(np_img > np.mean(np_img) - 5, 0, 1)

    for _ in range(3):
        for (idx, x) in enumerate(np_img):
            for (idy, y) in enumerate(x):
                if 0 < idx < len(np_img) - 1 and 0 < idy < len(x) - 1 and y == 1:
                    tmp = np_img[
                          idx - 1:idx + 2,
                          idy - 1:idy + 2
                          ].flatten()
                    if list(tmp).count(1) - 1 < 4:
                        np_img[idx, idy] = 0

    imgs = []

    for img in split_images_y(np_img):
        imgs.append(split_images_x(img))

    arr = []

    for (idx, x) in enumerate(imgs):
        for (idy, y) in enumerate(x):
            if len(y) >= 6 and len(y[0]) >= 3 and list(img.flatten()).count(1) > 15:
                pil_img = Image.fromarray(
                    (y * 255).astype(np.uint8), mode="L").resize((32, 32), Image.Resampling.LANCZOS).convert("1")
                arr.append(np.array(pil_img).reshape((1024, -1)).flatten())

    prediction = ''.join(clf.predict(np.array(arr)))
    print(time() - start_time)
    print(prediction)
    return prediction


@app.route('/edu', method=['POST'])
def edu():
    try:
        r = request
        base64data = r.forms.get('img')
        img = Image.open(BytesIO(base64.b64decode(base64data))).resize((140, 50))
        result = {"captcha": main(img), "status": "OK"}
        print(result)
        return result
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}


app.install(EnableCors())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="8000", debug=True)
# main()
