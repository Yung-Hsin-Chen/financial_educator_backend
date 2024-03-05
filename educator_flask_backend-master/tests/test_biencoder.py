import unittest

import os
import shutil
import sys
sys.path.append(os.path.abspath(""))

class test_biencoder(unittest.TestCase):  
    def test_a_biencoder_setup(self):
        self.biencoder_location = os.path.abspath("model/sentence_transformers/bi_encoder/distiluse-base-multilingual-cased-v1")
        if os.path.isdir(self.biencoder_location):
            shutil.rmtree(self.biencoder_location)
        
        self.embeddings_location = os.path.abspath("model/sentence_transformers/bi_encoder/embeddings.pkl")
        if os.path.isfile(self.embeddings_location):
            os.remove(self.embeddings_location)
        
        import model.sentence_transformers.bi_encoder.model

        self.assertTrue(os.path.isdir(self.biencoder_location))
        self.assertTrue(os.path.isfile(self.embeddings_location))

    def test_b_storing_biencoder_embeddings(self):
        from model.sentence_transformers.bi_encoder.model import model
        from model.sentence_transformers.bi_encoder.sentence_preparer import _store_embeddings_for_bi_encoder
        import pickle

        test_embeddings_location = os.path.abspath("tests/test_files/embeddings.pkl")
        if os.path.isfile(test_embeddings_location):
            os.remove(test_embeddings_location)
        
        _store_embeddings_for_bi_encoder(bi_encoder_model=model, 
            abs_filepath=os.path.abspath("tests/test_files/test_sentences.csv"), 
            save_location=os.path.abspath("tests/test_files/")
        )

        self.assertTrue(os.path.isfile(test_embeddings_location))

        with open("tests/test_files" + "/embeddings.pkl", "rb") as fIn:
            stored_data = pickle.load(fIn)
            sentence_topic_lists = stored_data["sentence_topic_lists"]
        
        self.assertEqual(sentence_topic_lists[0][0], "Are you alive?")

    def test_c_empty_transcription(self):
        from model.sentence_transformers.bi_encoder.model import get_topics_by_bi_encoder
        
        topic = get_topics_by_bi_encoder("")

        self.assertEqual(topic, "none")
    
    def test_d_random_transcription(self):
        from model.sentence_transformers.bi_encoder.model import get_topics_by_bi_encoder
        
        topic = get_topics_by_bi_encoder("Random stuff, I don't know.")

        self.assertEqual(topic, "none")

    def test_e_treshold_check(self):
        from model.sentence_transformers.bi_encoder.model import get_topics_by_bi_encoder
        
        topic = get_topics_by_bi_encoder("Aktien, ja.", treshold=0.99)

        self.assertEqual(topic, "none")

        topic2 = get_topics_by_bi_encoder("Aktien, ja.", treshold=0.3)

        self.assertNotEqual(topic2, "none")

        topic3 = get_topics_by_bi_encoder("Random stuff, I don't know.", treshold=0.6)

        self.assertEqual(topic3, "none")

if __name__ == '__main__':
    unittest.main()