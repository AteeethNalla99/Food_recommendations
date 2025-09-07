import pandas as pd

df_encoded = pd.read_pickle('df_encoded.pkl')

def recommend_restaurants(location_input, online_order_input, book_table_input, cuisines_input, top_n=5):
    def normalize(name):
        return name.lower().replace('_', ' ').strip()

    # Location column
    possible_location_cols = [
        col for col in df_encoded.columns
        if col.lower() == f"location_{location_input.lower().replace(' ', '_')}"
    ]
    if not possible_location_cols:
        return []
    location_col = possible_location_cols[0]

    filtered_df = df_encoded[df_encoded[location_col] == 1]
    filtered_df = filtered_df[
        (filtered_df['online_order'] == online_order_input) &
        (filtered_df['book_table'] == book_table_input)
    ]

    cuisines_lookup = {normalize(col): col for col in df_encoded.columns}
    matched_cols = [cuisines_lookup[normalize(c)] for c in cuisines_input if normalize(c) in cuisines_lookup]

    if not matched_cols:
        return []

    filtered_df = filtered_df[filtered_df[matched_cols].sum(axis=1) > 0]
    filtered_df = filtered_df.sort_values(by=['rate', 'votes'], ascending=False)
    return filtered_df['name'].head(top_n).tolist()
