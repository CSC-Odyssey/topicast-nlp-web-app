import pandas as pd
import nltk
import re
import numpy as np
import gensim
import pyLDAvis.gensim_models
import pyLDAvis.gensim_models as gensimvis
import json

from collections import Counter
from nltk.corpus import stopwords
from gensim import corpora, models
from gensim.models import CoherenceModel
from collections import defaultdict

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


def preprocess_text(text, threshold=2):
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

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
    
    for num_topics in range(2, 10):
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
    print(f"Coherence Score: {coherence_score}")


    vis_data = pyLDAvis.gensim_models.prepare(lda_model, corpus, dictionary)

    topics = {}
    
    for i in range(len(vis_data.topic_coordinates)):
        topic_num = f"Topic {i+1}"
        topic_terms = [term for term, _ in lda_model.show_topic(i, topn=12)]
        topics[topic_num] = topic_terms

        if i == 2:  # stop after getting the top 3 topics
            break

    with open("topics.json", "w") as f:
        json.dump(topics, f)
    
    print("\n")


def initiate_topic_modelling(data):
    df = pd.from_dict(data)
    # Extract text data from content column and preprocess it
    df['preprocessed_content'] = df['content'].apply(preprocess_text)

    start_lda(df['preprocessed_content'])


if __name__ == '__main__':
    initiate_topic_modelling()