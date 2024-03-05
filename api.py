import os

import flask
from flask import request, jsonify, render_template, abort
from flask_cors import CORS
from flasgger import Swagger, swag_from

from model.core import get_topics
from model.util import detect_stop_command, detect_resume_command

app = flask.Flask(__name__)
app.config["SWAGGER"] = {
    "title": "Educator API",
    "description": "API for the Educator Module.",
    "version": "1.0",
    "uiversion": 3,
    "openapi": "3.0.3"
}
swagger = Swagger(app)
cors = CORS(app)

@app.route("/", methods=["GET"])
def home():
    print(flask.request.host_url)
    return render_template("index.html")

# A testing-route for debugging purposes to see if requests work
@app.route("/api/v1/test", methods=["GET"])
def api_test():
    return jsonify({"message": "Test message. You got it!"})

# Evaluate Transcription
@app.route("/api/v1/models", methods=["POST"])
@swag_from("templates/api_doc.yml")
def api_models():
    if not request.data:
        print("Request is empty.")
        abort(400)

    request_data = request.get_json()

    json_align = None

    if "message" in request_data:
        message = request_data["message"]
        url = ""
        recognized_command = ""
        topic = ""
        media_type = ""
        instant_play = ""

        if "explanationState" in request_data and request_data["explanationState"] == "paused":
            recognized_command = detect_resume_command(message)
            if recognized_command == "":
                recognized_command = detect_stop_command(message)
        elif "explanationState" in request_data and request_data["explanationState"] == "playing":
            recognized_command = detect_stop_command(message)
        else:
            topic, model, instant_play, media_type, json_align = get_topics(message)
            get_url_dict = {"biencoder": topic, "openai": model}
            if not topic == "none":
                url_ending = _get_url_ending(get_url_dict[model])
                url = flask.request.host_url + url_ending
            else:
                media_type = "" #NOTE: get_topcis should probably already return an empty media_type if topic is "none"
                instant_play = ""
        
        response = jsonify({
            "message": "The API has received the following message: " + message,
            "topic": topic,
            "url": url,
            "align_url": json_align,
            "mediaType": media_type,
            "playInstantly": instant_play,
            "command": recognized_command})
            
        return response
    else:
        print("Error: No message field provided. Please specify a message.")
        return abort(400)

@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404_no_explanation.html", title = "404"), 404

@app.errorhandler(400)
def bad_request(error):
    return render_template("400_bad_request.html", title = "400"), 400

def _get_url_ending(topic):
    #NOTE: This check might need to be updated in the future, depending on the possible "topic" values
    if not topic == "" and not topic == "none":
        #This will look for all files within the upper directory to get the ending of the requested one
        #NOTE: This code could easily break if the folder structure assumptions (e.g. file name = topic name) are changed
        explanations_directory = os.path.abspath("static/explanations/")
        filenames = next(os.walk(explanations_directory), (None, None, []))[2]
        truncated_filenames = []
        for filename in filenames:
            truncated_filenames.append(filename[0:filename.rfind(".")])
        if topic in truncated_filenames:
            index_of_requested_resource = truncated_filenames.index(topic)
        else:
            print("File not found.")
            abort(404)
        file_ending = filenames[index_of_requested_resource][filenames[index_of_requested_resource].rfind("."):]

        if os.path.isfile(os.path.abspath("static/explanations/" + topic + file_ending)):
            return "static/explanations/" + topic + file_ending
        else:
            print("File not found.")
            abort(404)
    else:
        print("(Sub-)Topic is empty.")
        abort(500)

app.run()