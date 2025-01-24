from flask import Flask, request, jsonify
import fal_client
import os

os.environ["FAL_KEY"] = "YOUR_API_KEY"

app = Flask(__name__)

def on_queue_update(update):
    if isinstance(update, fal_client.InProgress):
        for log in update.logs:
            print(log["message"])

@app.route("/text_to_speech", methods=["POST"])
def text_to_speech():
    try:
        data = request.get_json()
        if 'input' not in data:
            return jsonify({"Error": "Text is required"})

        input_text = data['input']
        result = fal_client.subscribe(
            "fal-ai/playai/tts/v3",
            arguments={
                "input": input_text,
                "voice": "Jennifer (English (US)/American)",
                "response_format": "url"
            },
            with_logs=True,
            on_queue_update=on_queue_update,
        )
        audio_url = result['audio']['url']

        if audio_url:

            return jsonify({"Audio URL": audio_url})

        return jsonify({"Error": "Failed to generate audio"})

    except Exception as e:

        return jsonify({"Error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
