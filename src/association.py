import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

def run_association_mining(file_path=r'C:\Users\Vidisha Mankar\Desktop\DMBIPROJECT\CrimeMapX\data\processed\crime_data_processed.csv'):
    print(f"Loading processed dataset for Association Rule Mining from: {file_path}")
    df = pd.read_csv(file_path)
    
    # Select your categorical columns for market basket analysis
    features = ['crime_domain', 'weapon_used', 'time_period', 'day_of_week', 'city']
    available_features = [f for f in features if f in df.columns]
    basket_df = df[available_features].dropna()
    
    # One-hot encode the categorical variables
    print("One-hot encoding features...")
    df_encoded = pd.get_dummies(basket_df)
    
    # Apply Apriori algorithm with lower support to capture rules
    print("Running Apriori algorithm...")
    frequent_itemsets = apriori(df_encoded, min_support=0.002, use_colnames=True)
    
    # Generate association rules based on confidence (20% threshold)
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.2)
    
    # Sort by lift to find the strongest correlations
    if not rules.empty:
        rules = rules.sort_values(by="lift", ascending=False)
    
    print(f"Generated {len(rules)} association rules.")
    return rules

if __name__ == "__main__":
    rules = run_association_mining()
    if not rules.empty:
        print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(10))
    else:
        print("No rules generated.")