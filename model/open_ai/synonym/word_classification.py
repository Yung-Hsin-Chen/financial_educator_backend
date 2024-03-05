from pkg_resources import NullProvider
import spacy
import os
import re

def load_word_lst():
    global pic_lst
    global nlp
    nlp = spacy.load('en_core_web_lg')
    pic_lst = [nlp(filename[:filename.rfind(".")]) for filename in os.listdir(os.path.abspath("static/figures"))]
    return

def find_image_class(sentence):
    i = 0

    try: 
        assert nlp in globals()
        assert pic_lst in globals()
        sentence_nlp = nlp(sentence)
    except:
        load_word_lst() 
        sentence_nlp = nlp(sentence)

    noun_lst = [chunk for chunk in sentence_nlp.noun_chunks]
    if noun_lst != []:
        while i < len(noun_lst):
            j = 0
            while j < len(pic_lst):
                score = noun_lst[i].similarity(pic_lst[j][0])
                j += 1
                if score >= 0.5:
                    return pic_lst[j-1][0].text
            i += 1
    return "none"
    
def transcription_processing(transcription):
    fig_lst = []
    trans_lst = re.split(r"[.!?]", transcription)
    print(trans_lst)
    for sentence in trans_lst:
        fig = find_image_class(sentence)
        if fig != "none":
            print(f"fig: ", fig)
            fig_lst.append(fig)
    return fig_lst
