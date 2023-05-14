import pandas as pd
import nltk
import re
import numpy as np
import gensim
import pyLDAvis.gensim_models
import pyLDAvis.gensim_models as gensimvis
import json

from multiprocessing import Process, Manager
from collections import Counter
from nltk.corpus import stopwords
from gensim import corpora, models
from gensim.models import CoherenceModel
from collections import defaultdict

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from baguio_mc import mc_navigate_scrape_website
from baguio_news import bn_navigate_scrape_website


def preprocess_text(text, threshold=2):
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']
    html_tags = ["!DOCTYPE", "html", "head", "title", "body", "h1", "h2", "h3", "h4", "h5", "p", "br", "hr", "!--...--", "span", "rgb", "style", "label", "input", "textarea", "button", "select"]
    common_words = ["baguio", "color", "city"]

    # Instantiate stop words
    stop_words = stopwords.words('english')
    stop_words.extend(months)
    stop_words

    # Lowercase
    text = text.lower()
    # Remove numbers and punctuation
    text = re.sub(r'[^a-zA-Z]+', ' ', text)
    # Remove months and people names
    
    # Tokenize words
    tokens = word_tokenize(text)
    tokens = [token for token in tokens if token not in common_words]
    tokens = [token for token in tokens if token not in html_tags]
    # Remove stop words
    tokens = [token for token in tokens if token not in stop_words]
    # Remove short words
    tokens = [token for token in tokens if len(token) > 2]

    word_counts = Counter(tokens)
    filtered_words = [word for word in text.split() if word_counts[word] >= threshold]

    # Join tokens back into a string
    text = ' '.join(filtered_words)
    return text


def get_optimal_num_topics(articles):
    texts = [doc.split() for doc in articles]
    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]
    
    coherence_scores = defaultdict(list)
    
    for num_topics in range(2, 7):
        lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)
        coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_score = coherence_model_lda.get_coherence()
        coherence_scores[num_topics].append(coherence_score)

    optimal_num_topics = max(coherence_scores, key=lambda k: np.mean(coherence_scores[k]))
    return optimal_num_topics


def start_lda(preprocessed_content):
    # get the optimal number of topics for this date
    optimal_num_topics = get_optimal_num_topics(preprocessed_content)

    # create the dictionary and corpus
    texts = [doc.split() for doc in preprocessed_content]

    dictionary = corpora.Dictionary(texts)
    corpus = [dictionary.doc2bow(text) for text in texts]

    # create the LDA model
    lda_model = models.LdaModel(corpus, num_topics=optimal_num_topics, id2word=dictionary, passes=10)

    # calculate the coherence score for the model
    coherence_model_lda = CoherenceModel(model=lda_model, texts=texts, dictionary=dictionary, coherence='c_v')
    coherence_score = coherence_model_lda.get_coherence()

    vis_data = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)

    topics = {}
    
    for i in range(len(vis_data.topic_coordinates)):
        topic_num = f"Topic {i+1}"
        topic_terms = [term for term, _ in lda_model.show_topic(i, topn=20)]
        topics[topic_num] = topic_terms

        if i == 4:  # stop after getting the top 3 topics
            break

    return [topics, {"coherence_score" : coherence_score}]


def initiate_topic_modelling(date, website_str):
    data = {}

    manager = Manager()
    return_dict = manager.dict()

    if website_str == "both":
        p1 = Process(target=bn_navigate_scrape_website, args=(str(date), return_dict))
        p2 = Process(target=mc_navigate_scrape_website, args=(str(date), return_dict))
        p1.start()
        p2.start()
        p1.join()
        p2.join()

        merged_dict = {k: return_dict['baguio_news'].get(k, []) + return_dict['baguio_mc'].get(k, []) for k in set(return_dict['baguio_news'].keys()) | set(return_dict['baguio_mc'].keys())}
        data.update(merged_dict)
    
    elif website_str == "baguio_news":
        p1 = Process(target=bn_navigate_scrape_website, args=(str(date), return_dict))
        p1.start()
        p1.join()
        data.update(return_dict['baguio_news'])

    elif website_str == "baguio_mc":
        p2 = Process(target=mc_navigate_scrape_website, args=(str(date), return_dict))
        p2.start()
        p2.join()
        data.update(return_dict['baguio_mc'])
    
    else:
        return "Unknown website"

    df = pd.DataFrame.from_dict(data)
    # Extract text data from content column and preprocess it
    df['preprocessed_content'] = df['content'].apply(preprocess_text)

    preprocessed_content = start_lda(df['preprocessed_content'])
    return [preprocessed_content[0], preprocessed_content[1]]


