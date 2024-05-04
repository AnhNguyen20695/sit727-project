def convert_df_tolist(df):
    result = []
    for _, row in df.iterrows():
        result.append({col:row[col] for col in df.columns})
    return result