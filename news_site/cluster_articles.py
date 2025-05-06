import os
import re
import pandas as pd
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

# Load the dataset
data_folder = os.path.join("..", "news_scraper", "data")
csv_files = [f for f in os.listdir(data_folder) if f.endswith(".csv")]

all_data = []

# Initialize NLTK components
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

# Preprocess the text (remove punctuation, lowercase, remove stopwords, and stemming)
def preprocess_text(text):
    if pd.isnull(text):
        return ""
    text = text.lower()  # Convert to lowercase
    text = ''.join([char for char in text if char not in string.punctuation])  # Remove punctuation
    tokens = re.findall(r'\b\w+\b', text)  # Regex tokenization
    tokens = [word for word in tokens if word not in stop_words]  # Remove stopwords
    tokens = [stemmer.stem(word) for word in tokens]  # Apply stemming
    return ' '.join(tokens)

for file in csv_files:
    df = pd.read_csv(os.path.join(data_folder, file))
    df.columns = [col.lower().strip() for col in df.columns]

    if not all(col in df.columns for col in ['title', 'url', 'category']):
        print(f"Skipping {file} due to missing required columns.")
        continue

    title = df['title'].fillna("")
    url = df['url'].fillna("")
    category = df['category'].fillna("")
    source = file.split("_")[0]

    # Consolidate categories
    category = category.replace("Arts", "Arts/Culture/Celebrities")
    category = category.replace("Culture", "Arts/Culture/Celebrities")
    category = category.replace("Celebrities", "Arts/Culture/Celebrities")
    category = category.replace("Sport", "Sports")

    # Preprocess text fields
    df['processed_title'] = title.apply(preprocess_text)
    if 'description' in df.columns:
        df['processed_description'] = df['description'].fillna("").apply(preprocess_text)
        df['text_to_cluster'] = df['processed_title'] + " " + df['processed_description']
    else:
        df['text_to_cluster'] = df['processed_title']

    combined = pd.DataFrame({
        "title": title,
        "url": url,
        "category": category.str.strip().str.title(),
        "source": source.title(),
        "text_to_cluster": df['text_to_cluster']
    })

    all_data.append(combined)

# Combine all articles into one DataFrame
final_df = pd.concat(all_data, ignore_index=True)

# Vectorize the text using TF-IDF
vectorizer = TfidfVectorizer(max_features=5000, stop_words='english')
X = vectorizer.fit_transform(final_df['text_to_cluster'])

# Apply KMeans clustering
n_clusters = 4  # Based on four expected categories
kmeans = KMeans(n_clusters=n_clusters, random_state=42)
final_df['cluster'] = kmeans.fit_predict(X)

# Save clustered articles
final_df.to_csv("clustered_articles.csv", index=False)
print("✅ Clustering complete. File saved as clustered_articles.csv")
