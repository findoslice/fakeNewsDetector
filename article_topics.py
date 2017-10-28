from nltk.corpus import stopwords # pip3 instlal nltk
from nltk.stem.wordnet import WordNetLemmatizer
import string
import gensim # pip3 install Gensim
from gensim import corpora

# Main code from: https://www.analyticsvidhya.com/blog/2016/08/beginners-guide-to-topic-modeling-in-python/

# Present the article in a sentence per new line
doc_complete = open("text.txt", "r").readlines()

stop = set(stopwords.words('english'))
exclude = set(string.punctuation)
lemma = WordNetLemmatizer()

# Cleans the composed string from stop words (stop_free), puncuation (punc_free) and l
def clean(doc):
    stop_free = " ".join([i for i in doc.lower().split() if i not in stop])
    punc_free = ''.join(ch for ch in stop_free if ch not in exclude)
    normalized = " ".join(lemma.lemmatize(word) for word in punc_free.split())
    return normalized

# Use clean function on doc_complete
doc_clean = [clean(doc).split() for doc in doc_complete] 

# Matrix representation of a corpus using corpora
dictionary = corpora.Dictionary(doc_clean)

# Document - term matrix
doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean] 

# Training LDA model
Lda = gensim.models.ldamodel.LdaModel
ldamodel = Lda(doc_term_matrix, num_topics=3, id2word = dictionary, passes=50)

pairs = ldamodel.print_topics(num_topics=3, num_words=3)
pairs_dictionary = {}

for i in range(0, len(pairs)):
	for y in range(1, len(pairs[i])):
		pairs_split = pairs[i][y].split(" + ")
		for x in range(0, len(pairs_split)):
			pairs_split2 = pairs_split[x].split("*")
			pairs_split2[0] = float(pairs_split2[0])
			pairs_split2[1] = pairs_split2[1][1:(len(pairs_split2[1])-1)]
			pairs_dictionary[pairs_split2[1]] = pairs_split2[0]

# Decending
most_popular_topics = sorted(pairs_dictionary, key=pairs_dictionary.get, reverse=True)
print(most_popular_topics)