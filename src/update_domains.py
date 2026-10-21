import pandas as pd
import os

def remap_crime_domains(file_path='C:\\Users\\Vidisha Mankar\\Desktop\\DMBIPROJECT\\CrimeMapX\\data\\processed\\crime_data_processed.csv'):
    print("Loading processed dataset...")
    df = pd.read_csv(file_path)
    
    # Define a mapping dictionary from crime_description to new balanced crime_domains
    domain_mapping = {
        # Property & Financial Crimes
        'BURGLARY': 'Property & Financial Crime',
        'VANDALISM': 'Property & Financial Crime',
        'FRAUD': 'Property & Financial Crime',
        'IDENTITY THEFT': 'Property & Financial Crime',
        'COUNTERFEITING': 'Property & Financial Crime',
        'VEHICLE - STOLEN': 'Property & Financial Crime',
        'SHOPLIFTING': 'Property & Financial Crime',
        'EXTORTION': 'Property & Financial Crime',
        
        # Violent Crimes
        'DOMESTIC VIOLENCE': 'Violent & Personal Crime',
        'FIREARM OFFENSE': 'Violent & Personal Crime',
        'ROBBERY': 'Violent & Personal Crime',
        'KIDNAPPING': 'Violent & Personal Crime',
        'SEXUAL ASSAULT': 'Violent & Personal Crime',
        'ASSAULT': 'Violent & Personal Crime',
        'HOMICIDE': 'Violent & Personal Crime',
        
        # Public Order, Cyber & Substantive Offenses
        'PUBLIC INTOXICATION': 'Public Order & Cyber',
        'CYBERCRIME': 'Public Order & Cyber',
        'ILLEGAL POSSESSION': 'Public Order & Cyber',
        'ARSON': 'Public Order & Cyber',
        'DRUG OFFENSE': 'Public Order & Cyber',
        
        # Traffic & Safety
        'TRAFFIC VIOLATION': 'Traffic & Regulatory'
    }
    
    # Apply the mapping to rewrite 'crime_domain' based on 'crime_description'
    if 'crime_description' in df.columns:
        df['crime_domain'] = df['crime_description'].map(domain_mapping).fillna(df['crime_domain'])
    
    # Save the updated dataset back
    df.to_csv(file_path, index=False)
    print("Successfully re-mapped crime domains!")
    
    # Print new distribution to verify
    print("\nNew Crime Domain Breakdown:")
    print(df['crime_domain'].value_counts())

if __name__ == "__main__":
    remap_crime_domains()