import unittest

import os
import sys
sys.path.append(os.path.abspath(""))

class test_other(unittest.TestCase): 
    def test_empty_transcription_core(self):
        from model.core import get_topics
        
        topic, model, instant_play, media_type = get_topics("")

        self.assertEqual(topic, "none")
        self.assertEqual(model, "biencoder")
        self.assertEqual(instant_play, "false")
        self.assertEqual(media_type, "video") #NOTE: Questionable result.
    
    def test_recognize_stop_video(self):
        from model.util import detect_stop_command

        recognized_command1 = detect_stop_command("Video Stoppen")
        recognized_command2 = detect_stop_command("Stopp          erklärung.")
        recognized_command3 = detect_stop_command("WiedergabeStoppen")
        recognized_command4 = detect_stop_command("hi, audio irgendetwas irrelevantes abbrechen, oder.")
        recognized_command5 = detect_stop_command("Höre mit dem Erklären auf.")
        recognized_command6 = detect_stop_command("Brech die wiedergabe ab")
        
        recognized_command_negative1 = detect_stop_command("Stoppen wir mit den Aktien.")
        recognized_command_negative2 = detect_stop_command("Brechen wir dann damit ab.")

        self.assertEqual(recognized_command1, "stopExplanation")
        self.assertEqual(recognized_command2, "stopExplanation")
        self.assertEqual(recognized_command3, "stopExplanation")
        self.assertEqual(recognized_command4, "stopExplanation")
        self.assertEqual(recognized_command5, "stopExplanation")
        self.assertEqual(recognized_command6, "stopExplanation")
        self.assertEqual(recognized_command_negative1, "")
        self.assertEqual(recognized_command_negative2, "")
    
    def test_recognize_pause_video(self):
        from model.util import detect_stop_command

        recognized_command1 = detect_stop_command("Video pausieren")
        recognized_command2 = detect_stop_command("Pausier          erklärung.")
        recognized_command3 = detect_stop_command("WiedergabeAnhalten")
        recognized_command4 = detect_stop_command("hi, audio irgendetwas irrelevantes anhalten, oder.")
        recognized_command5 = detect_stop_command("Halte die Erklärung an.")
        
        recognized_command_negative1 = detect_stop_command("Halten wir mit den Aktien an.")
        recognized_command_negative2 = detect_stop_command("Pausieren wir das Gespräch.")

        self.assertEqual(recognized_command1, "pauseExplanation")
        self.assertEqual(recognized_command2, "pauseExplanation")
        self.assertEqual(recognized_command3, "pauseExplanation")
        self.assertEqual(recognized_command4, "pauseExplanation")
        self.assertEqual(recognized_command5, "pauseExplanation")
        self.assertEqual(recognized_command_negative1, "")
        self.assertEqual(recognized_command_negative2, "")

    def test_recognize_resume_video(self):
        from model.util import detect_resume_command

        recognized_command1 = detect_resume_command("Video fortsetzen")
        recognized_command2 = detect_resume_command("Starte          erklärung.")
        recognized_command3 = detect_resume_command("WiedergabeFort fahren")
        recognized_command4 = detect_resume_command("hi, audio irgendetwas irrelevantes fortführen, oder.")
        recognized_command5 = detect_resume_command("Fahre mit der Erklären fort.")
        recognized_command6 = detect_resume_command("Mache mit der Erklärung weiter")
        
        recognized_command_negative1 = detect_resume_command("Kannst du bitte weitermachen?")
        recognized_command_negative2 = detect_resume_command("Starten wir mit Ihrem Portfolio.")
        recognized_command_negative3 = detect_resume_command("Können Sie mit dem fort   fahren?")

        self.assertEqual(recognized_command1, "resumeExplanation")
        self.assertEqual(recognized_command2, "resumeExplanation")
        self.assertEqual(recognized_command3, "resumeExplanation")
        self.assertEqual(recognized_command4, "resumeExplanation")
        self.assertEqual(recognized_command5, "resumeExplanation")
        self.assertEqual(recognized_command6, "resumeExplanation")
        self.assertEqual(recognized_command_negative1, "")
        self.assertEqual(recognized_command_negative2, "")
        self.assertEqual(recognized_command_negative3, "")

if __name__ == '__main__':
    unittest.main()