from flask import Flask, request, jsonify
import time
import json
from pathlib import Path
from urllib.request import urlretrieve
import requests

app = Flask(__name__)
API_KEY = 'YOUR_API_KEY'

headers = {

    'x-api-key': API_KEY,
}

data = {
    "enhancements": ["denoise", "deblur", "light"],
    "width": 2000
}

data_dumped = {"parameters": json.dumps(data)}

@app.route('/enhance_image', methods=['POST'])

def enhance_image():

    if 'image' not in request.files:
        return jsonify({"error": "No image file found in the request"})

    image_file = request.files['image']

    local_file_path = f"./{image_file.filename}"
    image_file.save(local_file_path)

    try:
        with open(local_file_path, 'rb') as f:
            response = requests.post(
                'https://deep-image.ai/rest_api/process_result',
                headers=headers,
                files={'image': f},
                data=data_dumped
            )

        if response.status_code == 200:
            response_json = response.json()

            if response_json.get('status') == 'complete':
                p = Path(response_json['result_url'])
                urlretrieve(response_json['result_url'], p.name)
                return jsonify({"download_url": p.name})

            elif response_json['status'] in ['received', 'in_progress']:
                while response_json['status'] == 'in_progress':
                    response = requests.get(
                        f'https://deep-image.ai/rest_api/result/{response_json["job"]}',
                        headers=headers
                    )
                    response_json = response.json()
                    time.sleep(1)

                if response_json['status'] == 'complete':
                    p = Path(response_json['result_url'])
                    urlretrieve(response_json['result_url'], p.name)
                    return jsonify({"download_url": p.name})
        else:
            return jsonify({"error": f"API Error: {response.status_code}", "details": response.text})
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
