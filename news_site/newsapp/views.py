import pandas as pd
from django.shortcuts import render

# Load the clustered data
df = pd.read_csv("clustered_articles.csv")

# Ensure proper data formatting
df = df[df["cluster"].apply(lambda x: str(x).isdigit())]  # Keep only numeric cluster labels
df["cluster"] = df["cluster"].astype(int)

def cluster_list(request):
    cluster_ids = sorted(df['cluster'].unique())
    clusters = [{"cluster_id": cluster_id} for cluster_id in cluster_ids]
    return render(request, "cluster_list.html", {"clusters": clusters})


    
def articles_by_cluster(request, cluster_id):
    cluster_id = int(cluster_id)  # Ensure it's an integer
    filtered = df[df['cluster'] == cluster_id]
    articles = filtered.to_dict(orient="records")

    return render(request, "cluster_articles.html", {
        "cluster_id": cluster_id + 1,  # So template shows Cluster 1 instead of 0
        "articles": articles
    })

