from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.keras.layers import Rescaling
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

model = load_model("/app/models/corrected.keras")
class_names = ['no_damage', 'damage'] 

@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    print("GLOBAL ERROR HANDLER", flush=True)
    traceback.print_exc()
    return jsonify({"error": str(e)}), 500


@app.route('/summary', methods=['GET'])
def summary():
   return {
      "version": "v1",
      "name": "damage",
      "description": " ----- Categorize damage from hurricanes ------",
      "number_of_parameters": model.count_params()
   }

@app.route('/inference', methods=['POST'])
def predict():
    print("Hit /inference endpoint", flush=True)
    if 'image' not in request.files:
        return jsonify({
            "error": "Invalid request; pass a binary image file as a multi-part form under the image key."
        }), 400

    data = request.files['image']

    try:
        # load and preprocess image
        img = Image.open(data) ##.convert('RGB')
        img = img.resize((128, 128))  
        img_array = np.array(img) / 255.0  
        img_array = np.expand_dims(img_array, axis=0)
        
        print(f"Image array shape: {img_array.shape}")  # Add this line for debugging
        preds = model.predict(img_array)
        if(preds[0][0] > 0.5):
            predicted_class = "no_damage"
        else:
            predicted_class = "damage"

        return jsonify({
            "prediction": predicted_class
        })

    except Exception as e:
        print(f"Error during image prediction: {e}")  # Add this line to catch any exception
        return jsonify({
            "error": f"Failed to process image: {str(e)}"
        }), 500


if __name__ == '__main__':
    print(app.url_map)
    app.run(host='0.0.0.0', port=5000, debug=True)
