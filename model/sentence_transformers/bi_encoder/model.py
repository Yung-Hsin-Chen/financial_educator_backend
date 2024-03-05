import os
import pickle

from sentence_transformers import SentenceTransformer, util

from model.sentence_transformers.bi_encoder.sentence_preparer import _store_embeddings_for_bi_encoder

#Download/Load Model
bi_encoder_location = os.path.abspath("model/sentence_transformers/bi_encoder/")
modelName = "distiluse-base-multilingual-cased-v1"
if os.path.isdir(bi_encoder_location + "/" + modelName):
    model = SentenceTransformer(bi_encoder_location + "/" + modelName)
else:
    model = SentenceTransformer("sentence-transformers/" + modelName)
    model.save(bi_encoder_location + "/" + modelName)

#Prepare/Load Emebeddings
if not os.path.isfile(bi_encoder_location + "/embeddings.pkl"):
    print("Creating a file with the embeddings. This might take a moment.")
    absfilepath = os.path.abspath("model/sentence_transformers/pre_defined_sentences/sentences.csv")
    _store_embeddings_for_bi_encoder(model, absfilepath, bi_encoder_location)

with open(bi_encoder_location + "/embeddings.pkl", "rb") as fIn:
    stored_data = pickle.load(fIn)
    sentence_topic_lists = stored_data["sentence_topic_lists"]
    embeddings = stored_data["embeddings"]

sentences = [sentence[0] for sentence in sentence_topic_lists]

def get_topics_by_bi_encoder(transcription, treshold=0.6):
    """
    Returns the recognized financial topic(s) of a transcription by using a Bi-Encoder model.
    Arguments:
        transcription: A string to scan for topics.
        threshold: A float value. If no score is above this value, "none" will be returned as the topic.
    Returns:
        The topic(s) of the provided transcription (as a list in the future).
    """

    if not transcription == "":
        embedding = model.encode(transcription)
        cos_similarities = util.cos_sim(embeddings, embedding)

        #create list with similarity score and its index beforegsorting
        sentences_with_scores = []
        for i in range(len(cos_similarities)):
            sentences_with_scores.append([cos_similarities[i], i])

        sentences_with_scores = sorted(sentences_with_scores, key=lambda x: x[0], reverse=True)
        print("Highest score: {:.4f}".format(sentences_with_scores[0][0].item()))

        if sentences_with_scores[0][0] < treshold:
            return "none"

        # Take index of highest score and retrieve its topic
        return sentence_topic_lists[sentences_with_scores[0][1]][2]
    else:
        print("The provided transcription was empty.")
        return "none"