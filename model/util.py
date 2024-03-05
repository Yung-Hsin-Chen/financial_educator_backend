import os
import requests
import json
import re 
from aeneas.executetask import ExecuteTask
from aeneas.task import Task

def get_token():
    """
    This function gets a token which lasts for 10 minutes.
    Arguments:
        none
    Returns:
        access_token: a string of token.
    """
    token_url = "https://{}.api.cognitive.microsoft.com/sts/v1.0/issueToken".format(os.environ["azure_region"])
    headers = {
		'Ocp-Apim-Subscription-Key' : os.environ["azure_subscription"]
	}
    response = requests.post(token_url, headers=headers)
    access_token = str(response.text)
    return access_token

def save_audio(text):
    """
    This function takes texts, read it in Swiss German accent, 
    and save the audio file as azure_T2S.mp3 in explanations folder.
    Arguments:
        text: a string that needs to be read.
    Returns:
        None
    """
    token = get_token()
    out_path = os.path.abspath("static/explanations/openai.mp3")
    url = "https://{}.tts.speech.microsoft.com/cognitiveservices/v1".format(os.environ["azure_region"])
    header = {
		'Authorization': 'Bearer '+str(token),
		'Content-Type': 'application/ssml+xml',
		'X-Microsoft-OutputFormat': 'audio-24khz-160kbitrate-mono-mp3'
	}
    data = "<speak version='1.0' xml:lang='en-US'>\
				<voice xml:lang='de-CH' xml:gender='Female' name='de-CH-LeniNeural'>\
					{}\
				</voice>\
		    </speak>".format(text)
    try:
        response = requests.post(url, headers=header, data=data.encode("utf-8"))
        response.raise_for_status()
        with open(out_path, "wb") as file:
            file.write(response.content)
        response.close()
    except Exception as e:
        print("ERROR: ", e)
    return

def text_audio_align(text):
    """
    This function outputs the timestamp json file with the provided audio and txt files.
    Arguments:
        text: a string.
    Returns:
        None
    """
    text_lst = text.split(" ")
    with open(os.path.abspath("static/explanations/openai_response.txt"), "w") as f:
        for i in range(len(text_lst)):
            f.write(text_lst[i] + " ")
            if (i % 3 == 1) | (i == 1):
                f.write("\n")
    # create Task object
    config_string = u"task_language=deu|is_text_type=plain|os_task_file_format=json"
    task = Task(config_string=config_string)
    task.audio_file_path_absolute = os.path.abspath("static/explanations/openai.mp3")
    task.text_file_path_absolute = os.path.abspath("static/explanations/openai_response.txt")
    task.sync_map_file_path_absolute = os.path.abspath("static/explanations/word_audio_align.json")

    # process Task
    ExecuteTask(task).execute()

    # output sync map to file
    task.output_sync_map_file()

    with open("static/explanations/word_audio_align.json", "r") as json_file:
        json_align = json.load(json_file)
    for i in json_align["fragments"]:
        del i["children"]
        del i["id"]
        del i["language"]
    return json_align

def detect_openai_command(transcription):
    """
    This function process the input, transcription, and detect whether there is command "Hey Moe" 
    or other similar patterns in it.
    Arguments:
        transcription: a string.
    Returns:
        transcription: a string. If the model_indicator is "openai", transcription will be the string after command. 
        Otherwise, transcription will return the inpt, transcription.
        model_indicator: either "openai" or "biencoder". If command is detected, model_indicator will be "openai".
        Otherwiser, it will be "biencode".
    """
    pattern1 = r"Hey[\w,.]*\s"
    pattern2 = r"H[ei]y{0,1}l{0,1}[\s,]*M[\w,.]*\s"
    res = re.findall(pattern1, transcription, flags=re.IGNORECASE)
    res.extend(re.findall(pattern2, transcription, flags=re.IGNORECASE))
    # IF COMMAND IS FOUND IN THE TRANSCTIPTION, THEN RETURN THE TRANSCRIPTION AFTER THE COMMAND
    if res != []:
        start_idx = transcription.rfind(res[-1]) + len(res[-1])
        return (transcription[start_idx:], True)
    # IF THERE IS NO COMMAND FOUND IN THE TRANSCTIPTION, THEN RETURN THE WHOLE TRANSCRIPTION
    else:
        return (transcription, False)

def detect_stop_command(transcription):
    """
    This function processes the transcription and detects if it contains the stop/pause explanation command.
    Arguments:
        transcription: a string.
    Returns:
        recognized_command: "stopExplanation"/"pauseExplanation" as a string. If no command is detected, an empty string is returned.
    """
    recognized_command = ""

    video_stop_pattern = r"(?:Video|Audio|Wiedergabe|Erklär).*(?:stop|abbrech|beend|zurück)|(?:stop|abbrech|beend|zurück).*(?:Video|Audio|Wiedergabe|Erklär)"
    video_stop_pattern2 = r"Hör.*(?:Video|Audio|Wiedergabe|Erklär).*auf|Hör.*auf.*(?:Video|Audio|Wiedergabe|Erklär)"
    video_stop_pattern3 = r"Brech.*(?:Video|Audio|Wiedergabe|Erklär).*ab|Brech.*ab.*(?:Video|Audio|Wiedergabe|Erklär)"
    video_stop_res = re.findall(video_stop_pattern, transcription, flags=re.IGNORECASE)
    video_stop_res.extend(re.findall(video_stop_pattern2, transcription, flags=re.IGNORECASE))
    video_stop_res.extend(re.findall(video_stop_pattern3, transcription, flags=re.IGNORECASE))
    if video_stop_res != []:
        recognized_command = "stopExplanation"
        return recognized_command

    video_pause_pattern = r"(?:Video|Audio|Wiedergabe|Erklär).*(?:anhalt|paus)|(?:paus|anhalt).*(?:Video|Audio|Wiedergabe|Erklär)"
    video_pause_pattern2 = r"Halt.*(?:Video|Audio|Wiedergabe|Erklär).*an|Halt.*an.*(?:Video|Audio|Wiedergabe|Erklär)"
    video_pause_res = re.findall(video_pause_pattern, transcription, flags=re.IGNORECASE)
    video_pause_res.extend(re.findall(video_pause_pattern2, transcription, flags=re.IGNORECASE))
    if video_pause_res != []:
        recognized_command = "pauseExplanation"
        return recognized_command


    return recognized_command

def detect_resume_command(transcription):
    """
    This function processes the transcription and detects if it contains the resume explanation command.
    Arguments:
        transcription: a string.
    Returns:
        recognized_command: "resumeExplanation" as a string. If no command is detected, an empty string is returned.
    """
    recognized_command = ""

    pattern = r"(?:Video|Audio|Wiedergabe|Erklär).*(?:start|fort.*setz|fort.*führ|fort.*fahr)|(?:start|fort.*setz|fort.*führ|fort.*fahr).*(?:Video|Audio|Wiedergabe|Erklär)"
    pattern2 = r"(?:Setz|führ|fahr).*(?:Video|Audio|Wiedergabe|Erklär).*fort"
    pattern3= r"mach.*(?:Video|Audio|Wiedergabe|Erklär).*weiter|mach.*weiter.*(?:Video|Audio|Wiedergabe|Erklär)"
    res = re.findall(pattern, transcription, flags=re.IGNORECASE)
    res.extend(re.findall(pattern2, transcription, flags=re.IGNORECASE))
    res.extend(re.findall(pattern3, transcription, flags=re.IGNORECASE))
    if res != []:
        recognized_command = "resumeExplanation"
        return recognized_command

    return recognized_command

def umlaut_replace(ans):
    """
    This function replace umlaut with string.
    Arguments:
        ans: a string of answer provided by openai model.
    Returns:
        ans: a string with umlaut replaced.
    """
    encode_dict = {b"\xa4": "ae", b"\x84": "Ae", b"\xbc": "ue", b"\x9c": "Ue", b"\xb6": "oe", b"\x96": "Oe", b"\x9f": "ss", b"\xc3": ""}
    ans = ans.encode()
    ans = [bytes([b]) for b in ans]
    ans = "".join([ encode_dict[char] if char in encode_dict.keys() else char.decode("utf-8") for char in ans ])
    return ans

def delete_unfinished_sentence(ans, transcription):
    """
    This function remove the unfinished sentence in the end of a paragraph.
    Arguments:
        ans: a string of multiple sentences with/without an unfinished sentence in the end.
        transcription: a string.
    Returns:
        ans: a string of multiple sentences without unfinished sentence.
        transcription: a string
    """
    if ans[-1] != ".":
        ans = ans[:ans.rfind(".")+1]
    try:
        assert ans != ""
    except:
        transcription = "none"
    return ans, transcription
