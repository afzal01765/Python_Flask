from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, VideoUnavailable, NoTranscriptFound

# For test Url
#  http://127.0.0.1:5000/api/youtube-to-text?video_id=dQw4w9WgXcQ

app = Flask(__name__)

@app.route('/api/youtube-to-text', methods=['GET'])
def youtube_to_text():
    video_id = request.args.get('video_id')  # Get the video ID from the query parameter

    if not video_id:
        return jsonify({"error": "Missing required parameter: video_id"}), 400

    try:
        # Fetch the transcript for the given video ID
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine the transcript text into a single string
        transcript_text = ' '.join([entry['text'] for entry in transcript])

        return jsonify({"transcript": transcript_text}), 200

    except TranscriptsDisabled:
        return jsonify({"error": "Transcripts are disabled for this video."}), 403
    except VideoUnavailable:
        return jsonify({"error": "The requested video is unavailable or does not exist."}), 404
    except NoTranscriptFound:
        return jsonify({"error": "No transcript found for this video."}), 404
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)