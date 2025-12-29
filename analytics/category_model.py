import pandas as pd
from sklearn.linear_model import LogisticRegression
from analytics.db import engine

def train():
    df = pd.read_sql("SELECT merchant, category FROM txn_categories", engine)
    from sklearn.feature_extraction.text import TfidfVectorizer
    X = TfidfVectorizer().fit_transform(df.merchant)
    y = df.category
    model = LogisticRegression().fit(X,y)
    import joblib
    joblib.dump((model,X.vectorizer),"models/category.pkl")
