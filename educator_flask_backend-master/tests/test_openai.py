import unittest
import os

import sys
sys.path.append(os.path.abspath(""))
from model.open_ai.content import load_files
from model.open_ai.model_openai import load_read_file, open_ai_qa
from model.util import get_token, save_audio, detect_openai_command
from model.core import get_topics

os.environ["openai_api_key"] = "YOUR OPENAI API KEY"
os.environ["azure_region"] = "YOUR AZURE REGION"
os.environ["azure_subscription"] = "YOUR AZURE SUBSCRIPTION"

class test_openai(unittest.TestCase):

    def test_load_file(self):
        """
        check if load_files() create document.txt in the explanations folder
        """
        doc_path = os.path.abspath("static/explanations/document.txt")
        if os.path.exists(doc_path):
            os.remove(doc_path)
        load_files()  
        self.assertEqual(os.path.exists(doc_path), True, "Should create document.txt in the explanations folder.")

    def test_load_read_file_type(self):
        """
        check if load_read_file() output a list 
        """
        content = load_read_file()
        self.assertEqual(type(content), list, "Type should be list.")
        self.assertTrue(content[0])

    def test_load_read_file_content(self):
        """
        check if load_read_file() reads the content into the output, i.e., output != False
        """
        content = load_read_file()
        self.assertTrue(content[0], "There should be contents inside the string.")

    def test_get_token_create(self):
        """
        check if get_token create a new token
        """
        token = get_token()
        self.assertEqual(type(token), str, "Should create a string, token.")

    def test_get_token_content(self):
        """
        check if get_token create a new token
        """
        token = get_token()
        self.assertTrue(token, "Should create a token which has non-zero length.")

    def test_save_audio(self):
        """
        check if save_audio(text) can create an audio file in explanations folder
        """
        audio_path = os.path.abspath("static/explanations/openai.mp3")
        if os.path.exists(audio_path):
            os.remove(audio_path)
        save_audio("This is a unit test.")
        self.assertTrue(os.path.exists(audio_path), "Should create openai.mp3 in explanations folder")

    def test_command_detection_true_case(self):
        """
        check if command_detection can recognise "Hey Moe" and other similar patterns
        """
        self.assertTrue(detect_openai_command("Hey Moe ")[1])
        self.assertTrue(detect_openai_command("Hey Mol ")[1])
        self.assertTrue(detect_openai_command("Hey Mom ")[1])
        self.assertTrue(detect_openai_command("Hey Mom, ")[1])
        self.assertTrue(detect_openai_command("Hey Moe. ")[1])
        self.assertTrue(detect_openai_command("He more ")[1])
        self.assertTrue(detect_openai_command("Hey, Moe, ")[1])
        self.assertTrue(detect_openai_command("hey Moe ")[1])
        self.assertTrue(detect_openai_command("he more ")[1])
        self.assertTrue(detect_openai_command("hey moe ")[1])

    def test_command_detection_output(self):
        """
        check the output of command_detection
        """
        res = detect_openai_command("Hey Moe, ")
        self.assertEqual(type(res[0]), str, "The first return value should be string type.")
        self.assertEqual(type(res[1]), bool, "The second return value should be boolean type.")

    def test_open_ai_qa(self):
        """
        check if open_ai_qa creates document.txt and audio.mp3 successfully,
        and outputs the transcription
        """
        doc_path = os.path.abspath("static/explanations/document.txt")
        if os.path.exists(doc_path):
            os.remove(doc_path)
        audio_path = os.path.abspath("static/explanations/openai.mp3")
        if os.path.exists(audio_path):
            os.remove(audio_path)
        trans = open_ai_qa("What is your name?")
        self.assertTrue(trans, "Should be content in transcription")
        self.assertTrue(os.path.exists(audio_path), "audio should be created")
        self.assertTrue(os.path.exists(doc_path), "document should be created")

    def test_get_topics_case_1(self):
        """
        case_1: no "Hey Moe"
        use biencoder directly
        """
        file_lst = [filename[:filename.rfind(".")] for filename in os.listdir(os.path.abspath("static/explanations")) if filename[-1] == "4"]
        res, model, bool, media_type = get_topics("What is a stock?")
        self.assertIn(res, file_lst, "res should come from one of the predefined topics")
        self.assertEqual(model, "biencoder", "model should be 'biencoder'")
        self.assertEqual(bool, "false", "playInstantly should be false")
        self.assertEqual(media_type, "video", "media_type should be video.")

    def test_get_topics_case_2(self):
        """
        case_2: "Hey Moe" exists
        biencoder returns an answer
        """
        file_lst = [filename[:filename.rfind(".")] for filename in os.listdir(os.path.abspath("static/explanations")) if filename[-1] == "4"]
        res, model, bool, media_type = get_topics("Hey Moe, what is a stock?")
        self.assertIn(res, file_lst, "res should come from one of the predefined topics")
        self.assertEqual(model, "biencoder", "model should be 'biencoder'")
        self.assertEqual(bool, "true", "playInstantly should be true")
        self.assertEqual(media_type, "video", "media_type should be video.")

    def test_get_topics_case_3(self):
        """
        case_2: "Hey Moe" exists
        biencoder returns none
        openai returns an answer
        """
        transcription = "Hey Moe, what is the best pizzeria in the world?"
        transcription_wo_command = "what is the best pizzeria in the world?"
        res, model, bool, media_type = get_topics(transcription)
        self.assertEqual(res, transcription_wo_command, "res should be the transcription without command part")
        self.assertEqual(model, "openai", "model should be 'openai'")
        self.assertEqual(bool, "true", "playInstantly should be true")
        self.assertEqual(media_type, "audio", "media_type should be audio.")


if __name__ == '__main__':
    unittest.main()