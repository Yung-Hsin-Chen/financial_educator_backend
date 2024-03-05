import csv
import pickle

def _store_embeddings_for_bi_encoder(bi_encoder_model, abs_filepath, save_location):
    """
    Will create pickled embeddings for a given Bi-Encoder by using the provided .csv file with ";" as delimiters.
    Arguments:
        bi_encoder_model: A Bi-Encoder model object from the "sentence_transformers" library.
        abs_filepath: A string. The absolute path of the location of the .csv file with the sentences + their topics as rows.
        save_location: A string. The absolute path of the location to save the embeddings.
    Returns:
        Nothing.
    """

    results = []
    with open(abs_filepath, "r", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=";")
        next(reader)
        for row in reader: # each row is a list
            results.append(row)

    sentences = [sentence[0] for sentence in results]
    embeddings = bi_encoder_model.encode(sentences)

    #Store sentences and embeddings
    with open(save_location + "/embeddings.pkl", "wb") as fOut:
        pickle.dump({"sentence_topic_lists": results, "embeddings": embeddings}, fOut, protocol=pickle.HIGHEST_PROTOCOL)