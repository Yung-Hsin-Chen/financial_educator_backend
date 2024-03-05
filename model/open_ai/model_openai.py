import os
import openai
from model.open_ai.content import load_files
from model.util import save_audio
from deep_translator import GoogleTranslator
from model.util import text_audio_align, umlaut_replace, delete_unfinished_sentence

def load_read_file():
    load_files()
    path = "./static/explanations"
    with open(path + "/document.txt", "r", encoding="utf8") as f:
        content = [f.read()]
    return content

def open_ai_qa(transcription, num_token=200, engine="text-davinci-002", search_engine="text-davinci-002"):
    """
    Returns the answer for out-of-domain transcriptions
    Arguments:
        transcription: A string of out-of-domain transcription.
        api_key: a string. api-key for openai.
        det: boolean.
            Set to True if the response of the transcription should be extracted by the document provided.
            Set to False if the response of the transcription does not have to be extracted by the document.
    Returns:
        For det == True: return response, selected document, score
        For det == False: return response
    """
    openai.api_key = os.environ["openai_api_key"]    # THE OPENAI KEY (CAUTION: IT COSTS, DON'T PUT IT ONLINE)

    ## CHECK IF DOCUMENT.TXT EXISTS AND THE CONTENT INSIDE IS CORRECT
    try:
        with open("./static/explanations/document.txt", "r") as f:
            docs = [f.read()]
    except:
        load_files()
        docs = load_read_file()
    else:
        try:
            assert len(docs) == 1
        except:
            load_files()
            docs = load_read_file()

    transcription_pre = "Reply in German: \n\n" + transcription
    ## FOR DETERMINISTIC OUT-OF-DOMAIN TRANSCRIPTIONS
    response = openai.Answer.create(
        search_model=search_engine,
        model=engine,
        question=transcription_pre,
        documents=docs,
        examples_context="In 2017, U.S. life expectancy was 78.6 years.",
        examples=[["How many planets are there in solar system?", "There are eight planets in the solar system."]],
        max_tokens=num_token)
    # IF THE ANSWER IS NOT IN GERMAN, TRANSLATE IT INTO GERMAN
    ans_umlaut = GoogleTranslator(source='auto', target='de').translate(response["answers"][0])
    # REMOVE UNFINISHED SENTENCE
    ans_umlaut, transcription = delete_unfinished_sentence(ans_umlaut, transcription.capitalize())
    # CONVERT UMLAUT TO UTF-8
    ans_wo_umlaut = umlaut_replace(ans_umlaut)
    # SAVE RESPONSE AS AUDIO FILE IN EXPLANATIONS FOLDER
    save_audio(ans_umlaut)
    # OUTPUT TIMESTAMP FILE
    json_align = text_audio_align(ans_wo_umlaut)
    # RETURN RESPONSE, SELECTED DOCUMENT, SCORE
    if ans_umlaut == "Es gibt acht Planeten im Sonnensystem.":
        transcription = "none"
    return transcription, json_align
