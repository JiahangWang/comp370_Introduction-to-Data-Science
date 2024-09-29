import pandas as pd

file_path = 'taylor_swift_news.csv'
data = pd.read_csv(file_path, encoding='ISO-8859-1')

data['publishedAt'] = pd.to_datetime(data['publishedAt'])
data_sorted = data.sort_values(by='publishedAt')

# Function to sample 20 items or return the group if it has fewer than 20 items
def sample_or_all(group):
    n = min(len(group), 20)
    return group.sample(n)

data_grouped = data_sorted.groupby(data_sorted['publishedAt'].dt.date).apply(sample_or_all)

# Reset the index as 'apply' function returns multi-index dataframe
data_grouped.reset_index(drop=True, inplace=True)

output_path = 'processed_news_data.csv'
data_grouped.to_csv(output_path, index=False)

print("Data processed and saved to:", output_path)
