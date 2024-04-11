from flask import Flask, request
import tensorflow as tf
import numpy as np
import os
import requests
from tensorflow.keras.layers.experimental.preprocessing import Rescaling


app = Flask(__name__)

model = tf.keras.models.load_model('models/CNN_1.keras')

@app.route('/models/buildings/v1', methods=['GET'])
def model_info():
    return {
        "version": "v1",
        "name": "buildings",
        "description": "Classify images of buildings as containing damage or not containing damage",
        "number_of_parameters": 1193458
    }

def preprocess_input(url):
    """
    Converts user-provided input, an image file, into an array that can be used with the model.
    This function could raise an exception.
    """
    # converting the image file
    name = 'test/image.jpg'

    if not os.path.exists('test/test'):
        os.makedirs('test/test')

    response = requests.get(url)
    image_content = response.content

    with open('test/test/image.jpg', 'wb') as f:
        f.write(image_content)

    path = 'test'
    img_height = 150
    img_width = 150

    data = tf.keras.utils.image_dataset_from_directory(
        path,
        batch_size = 1,
        seed = 123,
        image_size = (img_height, img_width)
    )

    rescale = Rescaling(scale=1.0/255)

    # then add an extra dimension
    return data.map(lambda image, label:(rescale(image), label))

@app.route('/models/buildings/v1', methods=['POST'])
def classify_clothes_image():
    url = request.json.get('url')
    if not url:
        return {"error": "The `url` field is required"}, 404
    try:
        data = preprocess_input(url)
        results = model.predict(data).tolist()
    except Exception as e:
        return {"error": f"Could not process the `url` field; details: {e}"}, 404
    return { "result": {"damaged confidence score": results[0][0], 'not damaged confidence score': results[0][1]}}


# start the development server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')