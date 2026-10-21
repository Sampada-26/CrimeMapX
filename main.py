"""
CrimeMapX - Main Execution Pipeline
Author: [Your Name]
Description: Runs association rule mining and generates interactive visualizations.
"""

from src.association import run_association_mining
from src.visualization import generate_interactive_map

def main():
    print("=" * 50)
    print("Starting CrimeMapX Pipeline...")
    print("=" * 50)
    
    # Step 1: Run Association Rule Mining (Apriori)
    print("\n[1/2] Running Apriori Association Rule Mining...")
    try:
        rules = run_association_mining('data/processed/crime_data_processed.csv')
        print(f"-> Successfully generated {len(rules)} association rules.")
        print("-> Results saved to outputs/results/association_rules.csv")
    except Exception as e:
        print(f"-> Error during association mining: {e}")

    # Step 2: Generate Interactive Crime Map
    print("\n[2/2] Generating Interactive Crime Map...")
    try:
        generate_interactive_map('data/processed/crime_data_processed.csv')
        print("-> Interactive map saved to outputs/maps/interactive_crime_map.html")
    except Exception as e:
        print(f"-> Error during map generation: {e}")

    print("\n" + "=" * 50)
    print("CrimeMapX Pipeline Completed Successfully!")
    print("=" * 50)

if __name__ == "__main__":
    main()