import pandas as pd
from ast import literal_eval
from joblib import load

from cdqa.utils.converter import filter_paragraphs, generate_squad_examples
from cdqa.retriever.tfidf_doc_ranker import predict_document_retriever
from cdqa.reader.bertqa_sklearn import BertProcessor, BertQA

df = pd.read_csv('data/bnpp_newsroom_v1.0/bnpp_newsroom-v1.0.csv', converters={'paragraphs': literal_eval})
df['paragraphs'] = df['paragraphs'].apply(filter_paragraphs)

article_vectorizer, article_tfidf_matrix = load('models/article_vectorizer.joblib'), load('models/article_tfidf_matrix.joblib') 

question = 'Who is the creator of Artificial Intelligence?'

article_indices = predict_document_retriever(question=question,
                                             paragraphs=None,
                                             vectorizer=article_vectorizer,
                                             tfidf_matrix=article_tfidf_matrix,
                                             top_n=3,
                                             metadata=df,
                                             verbose=True)

squad_examples = generate_squad_examples(question=question,
                                         article_indices=article_indices,
                                         metadata=df)

test_processor = BertProcessor(is_training=False)
test_examples, test_features = test_processor.fit_transform(X=squad_examples)
model = load('model.joblib') 
predictions = model.predict(X=test_features)

print(question)
print(predictions)