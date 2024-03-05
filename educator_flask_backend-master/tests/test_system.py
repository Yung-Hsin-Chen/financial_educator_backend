import unittest
import os

import sys
sys.path.append(os.path.abspath(""))

import requests

#This test class does full system tests, which also fully test the api.py module of the backend.
#NOTE: Due to complications with VScode and flask, you have to manually start the server before running this test
class test_system(unittest.TestCase):
    def test_debugging_route(self):
        response = requests.get("http://localhost:5000/api/v1/test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["message"], "Test message. You got it!")

    def test_home(self):
        response = requests.get("http://localhost:5000/")
        self.assertTrue("<title>Educator API Flask</title>" in response.text)

    def test_model_no_topic(self):
        response = requests.post("http://localhost:5000/api/v1/models", 
            json={"message": "Hi, ich heisse Özgür", "explanationState": ""}
        )
        self.assertEquals(response.json()["mediaType"], "")
        self.assertEquals(response.json()["message"], 
            "The API has received the following message: Hi, ich heisse Özgür"
        )
        self.assertEquals(response.json()["playInstantly"], "")
        self.assertEquals(response.json()["topic"], "none")
        self.assertEquals(response.json()["url"], "")
        self.assertEquals(response.json()["command"], "")

    
    def test_model_biencoder(self):
        response = requests.post("http://localhost:5000/api/v1/models", 
            json={"message": "Ich möchte Obligationen von Paragon kaufen", "explanationState": ""}
        )
        self.assertEquals(response.json()["mediaType"], "video")
        self.assertEquals(response.json()["message"], 
            "The API has received the following message: Ich möchte Obligationen von Paragon kaufen"
        )
        self.assertEquals(response.json()["playInstantly"], "false")
        self.assertEquals(response.json()["topic"], "Obligationen Erklärung")
        self.assertEquals(response.json()["url"], 
            "http://localhost:5000/static/explanations/Obligationen Erklärung.mp4"
        )
        self.assertEquals(response.json()["command"], "")

    def test_model_biencoder2(self):
        response = requests.post("http://localhost:5000/api/v1/models", 
            json={"message": "Aktien", "explanationState": ""}
        )
        #print(response.json())
        self.assertEquals(response.json()["mediaType"], "")
        self.assertEquals(response.json()["message"], 
            "The API has received the following message: Aktien"
        )
        self.assertEquals(response.json()["playInstantly"], "")
        self.assertEquals(response.json()["topic"], "none")
        self.assertEquals(response.json()["url"], "")
        self.assertEquals(response.json()["command"], "")

    def test_model_command_biencoder(self):
        response = requests.post("http://localhost:5000/api/v1/models", 
            json={"message": "Hey Moe, warum emittieren Unternehmen Aktien", "explanationState": ""}
        )
        self.assertEquals(response.json()["mediaType"], "video")
        self.assertEquals(response.json()["message"], 
            "The API has received the following message: Hey Moe, warum emittieren Unternehmen Aktien"
        )
        self.assertEquals(response.json()["playInstantly"], "true")
        self.assertEquals(response.json()["topic"], "Aktien Erklärung")
        self.assertEquals(response.json()["url"], "http://localhost:5000/static/explanations/Aktien Erklärung.mp4")
        self.assertEquals(response.json()["command"], "")

    def test_model_command_openai(self):
        openai_mp3_location = os.path.abspath("static/explanations/openai.mp3")
        if os.path.isfile(openai_mp3_location):
            os.remove(openai_mp3_location) 
        
        response = requests.post("http://localhost:5000/api/v1/models", 
            json={"message": "Hey Moe, was ist der Sinn des Lebens", "explanationState": ""}
        )
        self.assertEquals(response.json()["mediaType"], "audio")
        self.assertEquals(response.json()["message"], 
            "The API has received the following message: Hey Moe, was ist der Sinn des Lebens"
        )
        self.assertEquals(response.json()["playInstantly"], "true")
        self.assertEquals(response.json()["topic"], "was ist der Sinn des Lebens")
        self.assertEquals(response.json()["url"], "http://localhost:5000/static/explanations/openai.mp3")
        self.assertEquals(response.json()["command"], "")

        self.assertTrue(os.path.isfile(openai_mp3_location))

    def test_model_empty(self):
        response = requests.post("http://localhost:5000/api/v1/models")
        self.assertEquals(response.status_code, 400)

    def test_model_empty2(self):
        response = requests.post("http://localhost:5000/api/v1/models", 
            json={"message": "", "explanationState": ""}
        )
        self.assertEquals(response.json()["mediaType"], "")
        self.assertEquals(response.json()["message"], 
            "The API has received the following message: "
        )
        self.assertEquals(response.json()["playInstantly"], "")
        self.assertEquals(response.json()["topic"], "none")
        self.assertEquals(response.json()["url"], "")
        self.assertEquals(response.json()["command"], "")

    def test_model_no_message(self):
        response = requests.post("http://localhost:5000/api/v1/models", 
            json={"test": "test", "explanationState": ""}
        )
        self.assertEquals(response.status_code, 400)

    def test_model_long_message(self):
        response = requests.post("http://localhost:5000/api/v1/models", 
            json={"message": ("Diese Nachricht is absichtlich so lang, " 
            "um zu sehen, ob das System damit umgehen kann. " 
            "Aber mal schauen, ob das Model ein Limit hat, die Nachricht abschneidet und "
            "das richtige Thema erkennen kann. "
            "Noch mehr Fülltext hier. "
            "Das Model sollte nicht abstürzen. " 
            "Aber das Thema sollte am Schluss auch nicht erkannt werden. "
            "Auch wenn die Nachricht unter dem Limit ist, wird das Thema bei solch einem langen "
            "Text nicht erkannt. Ist dieser Test sinnvoll? "
            "Fillertext hier, da ich nicht mehr weiss, was ich schreiben soll. "
            "Ich würde gerne wissen, was Aktien sind. "),
                "explanationState": ""
            }
        )
        self.assertEquals(response.json()["topic"], "none")

    #NOTE: Wastes a lot of credits, Test deactivated for that reason. Test did not work due to openai issue.
    # def test_model_long_message_openai(self):
    #     response = requests.post("http://localhost:5000/api/v1/models", 
    #         json={"message": ("Hey Mo Diese Nachricht is absichtlich so lang, " 
    #         "um zu sehen, ob das System damit umgehen kann. " 
    #         "Aber mal schauen, ob das Model ein Limit hat, die Nachricht abschneidet und "
    #         "das richtige Thema erkennen kann. "
    #         "Noch mehr Fülltext hier. "
    #         "Das Model sollte nicht abstürzen. " 
    #         "Aber das Thema sollte am Schluss auch nicht erkannt werden. "
    #         "Auch wenn die Nachricht unter dem Limit ist, wird das Thema bei solch einem langen "
    #         "Text nicht erkannt. Ist dieser Test sinnvoll? "
    #         "Fillertext hier, da ich nicht mehr weiss, was ich schreiben soll. "
    #         "Ich würde gerne wissen, was Aktien sind. "),
    #            "explanationState": False
    #         }
    #     )
    #     self.assertEquals(response.json()["mediaType"], "audio")

    #NOTE: There is a specific sentence + subtopic within the .csv file for testing purposes.
    #The test topic should never be recognized under normal circumstances.
    #It's bad test design, but it's not worth refactoring the code for that.
    def test_non_existing_url_ending(self):
        response = requests.post("http://localhost:5000/api/v1/models", 
            json={"message": "dphgj s'rnm'hnjhr 4'hbhj' dorfib",
                "explanationState": ""
            }
        )
        self.assertEquals(response.status_code, 404)

    #NOTE: This could potentially break the whole package. Remove if that happens.
    def test_unusual_characters(self):
        response = requests.post("http://localhost:5000/api/v1/models", 
            json={"message": "読売新聞オンライン",
                "explanationState": ""
            }
        )
        self.assertEquals(response.json()["mediaType"], "")
        self.assertEquals(response.json()["message"], 
            "The API has received the following message: 読売新聞オンライン"
        )
        self.assertEquals(response.json()["playInstantly"], "")
        self.assertEquals(response.json()["topic"], "none")
        self.assertEquals(response.json()["url"], "")
        self.assertEquals(response.json()["command"], "")

    def test_stop_command_detection(self):
        response = requests.post("http://localhost:5000/api/v1/models", 
            json={"message": "Hey kannst, video irgendetwas irrelevantes stoppen",
                "explanationState": "playing"
            }
        )

        self.assertEquals(response.json()["mediaType"], "")
        self.assertEquals(response.json()["message"], 
            "The API has received the following message: Hey kannst, video irgendetwas irrelevantes stoppen"
        )
        self.assertEquals(response.json()["playInstantly"], "")
        self.assertEquals(response.json()["topic"], "")
        self.assertEquals(response.json()["url"], "")
        self.assertEquals(response.json()["command"], "stopExplanation")

        response2 = requests.post("http://localhost:5000/api/v1/models", 
            json={"message": "Hey kannst, video irgendetwas irrelevantes stoppen",
                "explanationState": "something random"
            }
        )

        self.assertEquals(response2.json()["mediaType"], "")
        self.assertEquals(response2.json()["message"], 
            "The API has received the following message: Hey kannst, video irgendetwas irrelevantes stoppen"
        )
        self.assertEquals(response2.json()["playInstantly"], "")
        self.assertEquals(response2.json()["topic"], "none")
        self.assertEquals(response2.json()["url"], "")
        self.assertEquals(response2.json()["command"], "")

    def test_pause_command_detection(self):
        response = requests.post("http://localhost:5000/api/v1/models", 
            json={"message": "Hey kannst, video irgendetwas irrelevantes pausieren",
                "explanationState": "playing"
            }
        )

        self.assertEquals(response.json()["mediaType"], "")
        self.assertEquals(response.json()["message"], 
            "The API has received the following message: Hey kannst, video irgendetwas irrelevantes pausieren"
        )
        self.assertEquals(response.json()["playInstantly"], "")
        self.assertEquals(response.json()["topic"], "")
        self.assertEquals(response.json()["url"], "")
        self.assertEquals(response.json()["command"], "pauseExplanation")

    def test_resume_command_detection(self):
        response = requests.post("http://localhost:5000/api/v1/models", 
            json={"message": "Hey kannst, video irgendetwas irrelevantes fortsetzen",
                "explanationState": "paused"
            }
        )

        self.assertEquals(response.json()["mediaType"], "")
        self.assertEquals(response.json()["message"], 
            "The API has received the following message: Hey kannst, video irgendetwas irrelevantes fortsetzen"
        )
        self.assertEquals(response.json()["playInstantly"], "")
        self.assertEquals(response.json()["topic"], "")
        self.assertEquals(response.json()["url"], "")
        self.assertEquals(response.json()["command"], "resumeExplanation")

if __name__ == '__main__':
    unittest.main()