import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

def run_association_mining(input_path='data/processed/crime_data_processed.csv'):
    df = pd.read_csv(input_path)
    
    # Select categorical columns for transactions
    features = ['Crime Domain', 'Time Period', 'Victim Gender', 'Weapon Used', 'Age Group']
    df_subset = df[features].dropna()
    
    transactions = df_subset.values.tolist()
    
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_encoded = pd.DataFrame(te_ary, columns=te.columns_)
    
    # Apply Apriori
    frequent_itemsets = apriori(df_encoded, min_support=0.05, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.6)
    rules = rules.sort_values(by="lift", ascending=False)
    
    # Save results
    rules.to_csv('outputs/results/association_rules.csv', index=False)
    print("Association rules mined and saved to outputs/results/association_rules.csv")
    return rules

if __name__ == "__main__":
    run_association_mining()