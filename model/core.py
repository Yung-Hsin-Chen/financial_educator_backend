from model.sentence_transformers.bi_encoder.model import get_topics_by_bi_encoder
from model.open_ai.model_openai import open_ai_qa
from model.util import detect_openai_command

def get_topics(transcription):
    """
    Returns the recognized financial topic(s)/subtopic(s)/subsubtopic(s) of a transcription by using the specified model.
    Arguments:
        transcription: A string to scan for topics/subtopics/subsubtopics.
    Returns:
        res: a string.
        If the result is gained by the openai model, res will be the transcription
        If the result is gained by bi-encoder model, res will be the topic.
        model: a string. Either "openai" or "biencoder"
        command_dict[command]: a string that tells the frontend to play the video/audio immediately or not.
        media_type: a string. Either "audio" or "video"
    """
    map_bool_to_str = {True: "true", False: "false"}
    transcription, command = detect_openai_command(transcription)
    model = "biencoder"
    media_type = "video"
    json_align = None
    if command == True:
        res = get_topics_by_bi_encoder(transcription, 0.8)
        if res == "none":
            res, json_align = open_ai_qa(transcription)
            model = "openai"
            media_type = "audio"
    else:
        res = get_topics_by_bi_encoder(transcription)
    return res, model, map_bool_to_str[command], media_type, json_align