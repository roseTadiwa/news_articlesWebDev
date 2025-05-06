import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Path to CSVs
DATA_DIR = os.path.join(os.path.dirname(__file__), '../../news_scraper/data')

def load_and_merge_data():
    all_files = [f for f in os.listdir(DATA_DIR) if f.endswith('.csv')]
    dfs = []

    for filename in all_files:
        path = os.path.join(DATA_DIR, filename)
        df = pd.read_csv(path)
        
        # Standardize column names if needed
        df.columns = [col.strip().lower() for col in df.columns]
        
        # Ensure required columns exist
        if {'title', 'description', 'url', 'category'}.issubset(df.columns):
            df['source'] = filename.split('_')[0]
            dfs.append(df)
        else:
            print(f"Skipping file (missing columns): {filename}")

    return pd.concat(dfs, ignore_index=True)

def preprocess_and_cluster(df, num_clusters=4):
    vectorizer = TfidfVectorizer(stop_words='english')
    X = vectorizer.fit_transform(df['title'].astype(str) + ' ' + df['description'].astype(str))
    
    model = KMeans(n_clusters=num_clusters, random_state=42)
    df['cluster'] = model.fit_predict(X)
    
    return df

def main():
    df = load_and_merge_data()
    df = preprocess_and_cluster(df)
    df.to_csv('clustered_articles.csv', index=False)
    print("Clustering complete. Saved to 'clustered_articles.csv'.")

if __name__ == '__main__':
    main()
