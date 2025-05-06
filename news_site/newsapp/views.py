import pandas as pd
from django.shortcuts import render

def home(request):
    # Load the clustered articles CSV file
    df = pd.read_csv('clustered_articles.csv')

    # Get unique cluster IDs
    clusters = df['cluster'].unique()
    clusters.sort()

    # Get selected cluster from URL (or default to 0)
    selected_cluster = int(request.GET.get('cluster', 0))

    # Filter the articles based on the selected cluster
    filtered_articles = df[df['cluster'] == selected_cluster]

    # Add category and source class to each article for CSS styling
    for index, article in filtered_articles.iterrows():
        # Creating class names for category and source to avoid invalid CSS characters
        article['category_class'] = article['category'].title().replace('/', '')
        article['source_class'] = article['source'].lower()

    # Prepare context for rendering the template
    context = {
    'clusters': clusters,
    'selected_cluster': selected_cluster,
    'articles': filtered_articles.to_dict(orient='records'),
    'cluster_class': f"cluster-{selected_cluster}"
}


    return render(request, 'home.html', context)
