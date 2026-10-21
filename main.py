import os
from pathlib import Path
from src.association import run_association_mining
from src.visualization import generate_crime_map

def main():
    print("==========================================")
    print("      STARTING CRIMEMAPX PIPELINE         ")
    print("==========================================")
    
    project_root = Path(__file__).resolve().parent
    processed_path = project_root / "data" / "processed" / "crime_data_processed.csv"
    
    if not os.path.exists(processed_path):
        print(f"Error: Processed dataset not found at {processed_path}. Please run preprocessing first.")
        return

    # Step 1: Run Association Rule Mining
    print("\n--- STEP 1: Running Association Rule Mining ---")
    try:
        rules = run_association_mining(processed_path)
        print("Top 5 Association Rules Discovered:")
        print(rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(5))
        
        # Optionally save rules to outputs
        results_dir = project_root / "outputs" / "results"
        results_dir.mkdir(parents=True, exist_ok=True)
        rules_path = results_dir / "association_rules.csv"
        rules.to_csv(rules_path, index=False)
        print(f"Association rules saved to {rules_path}")
    except Exception as e:
        print(f"Error during association rule mining: {e}")

    # Step 2: Generate Interactive Visualizations / Map
    print("\n--- STEP 2: Generating Visualizations ---")
    try:
        map_path = project_root / "outputs" / "maps" / "crime_map.html"
        generate_crime_map(processed_path, map_path)
    except Exception as e:
        print(f"Error during map generation: {e}")

    print("\n==========================================")
    print("      CRIMEMAPX PIPELINE COMPLETED        ")
    print("==========================================")

if __name__ == "__main__":
    main()