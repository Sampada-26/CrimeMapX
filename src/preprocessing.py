import pandas as pd
import numpy as np
from pathlib import Path


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

RAW_DATA = BASE_DIR / "data" / "raw" / "crime_dataset_india.csv"

PROCESSED_DIR = BASE_DIR / "data" / "processed"

PROCESSED_DATA = PROCESSED_DIR / "crime_data_processed.csv"


# ============================================================
# 1. LOAD DATA
# ============================================================

def load_data():

    df = pd.read_csv(RAW_DATA)

    print("\n========================================")
    print("DATASET LOADED SUCCESSFULLY")
    print("========================================")

    print("\nDataset Shape:")
    print(df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nData Types:")
    print(df.dtypes)

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nDuplicate Rows:")
    print(df.duplicated().sum())

    return df


# ============================================================
# 2. STANDARDIZE COLUMN NAMES
# ============================================================

def standardize_columns(df):

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    print("\n========================================")
    print("COLUMN NAMES STANDARDIZED")
    print("========================================")

    print(df.columns.tolist())

    return df


# ============================================================
# 3. REMOVE DUPLICATE ROWS
# ============================================================

def remove_duplicates(df):

    before = len(df)

    df = df.drop_duplicates()

    after = len(df)

    print("\n========================================")
    print("DUPLICATE ROW REMOVAL")
    print("========================================")

    print("Duplicate rows removed:", before - after)

    return df


# ============================================================
# 4. CHECK DUPLICATE REPORT NUMBERS
# ============================================================

def check_duplicate_report_numbers(df):

    duplicates = df["report_number"].duplicated().sum()

    print("\n========================================")
    print("REPORT NUMBER CHECK")
    print("========================================")

    print("Duplicate report numbers:", duplicates)

    return df


# ============================================================
# 5. FLEXIBLE DATE PARSER
# ============================================================

def parse_mixed_datetime(value):

    if pd.isna(value):
        return pd.NaT

    value = str(value).strip()

    # --------------------------------------------------------
    # First try DD-MM-YYYY HH:MM
    # --------------------------------------------------------

    result = pd.to_datetime(
        value,
        format="%d-%m-%Y %H:%M",
        errors="coerce"
    )

    if not pd.isna(result):
        return result

    # --------------------------------------------------------
    # If that fails, try MM-DD-YYYY HH:MM
    # --------------------------------------------------------

    result = pd.to_datetime(
        value,
        format="%m-%d-%Y %H:%M",
        errors="coerce"
    )

    if not pd.isna(result):
        return result

    # --------------------------------------------------------
    # Final fallback
    # --------------------------------------------------------

    return pd.to_datetime(
        value,
        errors="coerce"
    )


# ============================================================
# 6. CONVERT DATE COLUMNS
# ============================================================

def convert_dates(df):

    print("\n========================================")
    print("DATE CONVERSION")
    print("========================================")

    # --------------------------------------------------------
    # Show examples of the mixed formats
    # --------------------------------------------------------

    print("\nDate of Occurrence samples:")

    print(
        df["date_of_occurrence"]
        .iloc[[0, 15835, 15836, 15837, 15838]]
        .tolist()
    )

    print("\nTime of Occurrence samples:")

    print(
        df["time_of_occurrence"]
        .head(10)
        .tolist()
    )

    # --------------------------------------------------------
    # Convert Date Reported
    # --------------------------------------------------------

    df["date_reported"] = (
        df["date_reported"]
        .apply(parse_mixed_datetime)
    )

    # --------------------------------------------------------
    # Convert Date of Occurrence
    # --------------------------------------------------------

    df["date_of_occurrence"] = (
        df["date_of_occurrence"]
        .apply(parse_mixed_datetime)
    )

    # --------------------------------------------------------
    # Convert Date Case Closed
    # --------------------------------------------------------

    df["date_case_closed"] = (
        df["date_case_closed"]
        .apply(parse_mixed_datetime)
    )

    print("\nDate conversion completed.")

    print(
        "Date Reported missing:",
        df["date_reported"].isna().sum()
    )

    print(
        "Date of Occurrence missing:",
        df["date_of_occurrence"].isna().sum()
    )

    print(
        "Date Case Closed missing:",
        df["date_case_closed"].isna().sum()
    )

    return df


# ============================================================
# 7. CREATE TEMPORAL FEATURES
# ============================================================

def create_temporal_features(df):

    print("\n========================================")
    print("CREATING TEMPORAL FEATURES")
    print("========================================")

    df["year"] = (
        df["date_of_occurrence"]
        .dt.year
    )

    df["month"] = (
        df["date_of_occurrence"]
        .dt.month
    )

    df["month_name"] = (
        df["date_of_occurrence"]
        .dt.month_name()
    )

    df["day"] = (
        df["date_of_occurrence"]
        .dt.day
    )

    df["day_of_week"] = (
        df["date_of_occurrence"]
        .dt.day_name()
    )

    print("\nTemporal features created:")

    print("- year")
    print("- month")
    print("- month_name")
    print("- day")
    print("- day_of_week")

    return df


# ============================================================
# 8. CREATE TIME FEATURES
# ============================================================

def create_time_features(df):

    print("\n========================================")
    print("CREATING TIME FEATURES")
    print("========================================")

    # Time of Occurrence contains full datetime values.
    # Example:
    # 01-01-2020 01:11

    time_values = (
        df["time_of_occurrence"]
        .apply(parse_mixed_datetime)
    )

    df["occurrence_hour"] = (
        time_values.dt.hour
    )

    # --------------------------------------------------------
    # Convert hour into time periods
    # --------------------------------------------------------

    def get_time_period(hour):

        if pd.isna(hour):
            return "Unknown"

        elif hour < 6:
            return "Night"

        elif hour < 12:
            return "Morning"

        elif hour < 17:
            return "Afternoon"

        elif hour < 21:
            return "Evening"

        else:
            return "Night"

    df["time_period"] = (
        df["occurrence_hour"]
        .apply(get_time_period)
    )

    print("\nTime Period Distribution:")

    print(
        df["time_period"]
        .value_counts()
    )

    return df


# ============================================================
# 9. CREATE REPORTING DELAY
# ============================================================

def create_reporting_delay(df):

    print("\n========================================")
    print("CALCULATING REPORTING DELAY")
    print("========================================")

    df["reporting_delay_days"] = (
        df["date_reported"]
        - df["date_of_occurrence"]
    ).dt.total_seconds() / (24 * 60 * 60)

    # Negative values are invalid.
    # Keep the crime record but mark the calculated
    # metric as missing.

    df.loc[
        df["reporting_delay_days"] < 0,
        "reporting_delay_days"
    ] = np.nan

    print(
        "Valid reporting delay values:",
        df["reporting_delay_days"].notna().sum()
    )

    print(
        "Missing/invalid reporting delay values:",
        df["reporting_delay_days"].isna().sum()
    )

    return df


# ============================================================
# 10. CLEAN CATEGORICAL COLUMNS
# ============================================================

def clean_categorical_columns(df):

    print("\n========================================")
    print("CLEANING CATEGORICAL COLUMNS")
    print("========================================")

    categorical_columns = [

        "city",
        "crime_description",
        "victim_gender",
        "weapon_used",
        "crime_domain",
        "case_closed"
    ]

    for column in categorical_columns:

        df[column] = (
            df[column]
            .astype("string")
            .str.strip()
        )

    print("Categorical columns cleaned.")

    return df


# ============================================================
# 11. HANDLE MISSING VALUES
# ============================================================

def handle_missing_values(df):

    print("\n========================================")
    print("HANDLING MISSING VALUES")
    print("========================================")

    # Missing weapon information is treated as Unknown.
    # This is useful for Association Rule Mining.

    df["weapon_used"] = (
        df["weapon_used"]
        .fillna("Unknown")
    )

    print("\nMissing values after handling:")

    print(df.isnull().sum())

    return df


# ============================================================
# 12. CREATE AGE GROUP
# ============================================================

def create_age_group(df):

    print("\n========================================")
    print("CREATING AGE GROUPS")
    print("========================================")

    def categorize_age(age):

        if pd.isna(age):
            return "Unknown"

        elif age < 18:
            return "Minor"

        elif age <= 30:
            return "Young Adult"

        elif age <= 50:
            return "Adult"

        else:
            return "Senior"

    df["age_group"] = (
        df["victim_age"]
        .apply(categorize_age)
    )

    print("\nAge Group Distribution:")

    print(
        df["age_group"]
        .value_counts()
    )

    return df


# ============================================================
# 13. VALIDATE VICTIM AGE
# ============================================================

def validate_age(df):

    print("\n========================================")
    print("VALIDATING VICTIM AGE")
    print("========================================")

    invalid_age = (
        (df["victim_age"] < 0)
        |
        (df["victim_age"] > 100)
    )

    print(
        "Unrealistic victim ages:",
        invalid_age.sum()
    )

    return df


# ============================================================
# 14. VALIDATE POLICE DEPLOYMENT
# ============================================================

def validate_police_deployment(df):

    print("\n========================================")
    print("VALIDATING POLICE DEPLOYMENT")
    print("========================================")

    invalid_values = (
        df["police_deployed"] < 0
    )

    print(
        "Invalid police deployment values:",
        invalid_values.sum()
    )

    return df


# ============================================================
# 15. CREATE CASE RESOLUTION TIME
# ============================================================

def create_case_resolution_time(df):

    print("\n========================================")
    print("CALCULATING CASE RESOLUTION TIME")
    print("========================================")

    df["case_resolution_days"] = (
        df["date_case_closed"]
        - df["date_of_occurrence"]
    ).dt.total_seconds() / (24 * 60 * 60)

    # Negative values are invalid.
    # Keep the original crime record.

    df.loc[
        df["case_resolution_days"] < 0,
        "case_resolution_days"
    ] = np.nan

    print(
        "Valid case resolution values:",
        df["case_resolution_days"].notna().sum()
    )

    print(
        "Missing/invalid case resolution values:",
        df["case_resolution_days"].isna().sum()
    )

    return df


# ============================================================
# 16. VALIDATE REPORTING DELAY
# ============================================================

def validate_reporting_delay(df):

    print("\n========================================")
    print("VALIDATING REPORTING DELAY")
    print("========================================")

    negative_delay = (
        df["reporting_delay_days"] < 0
    )

    print(
        "Negative reporting delays:",
        negative_delay.sum()
    )

    return df


# ============================================================
# 17. VALIDATE CASE RESOLUTION
# ============================================================

def validate_case_resolution(df):

    print("\n========================================")
    print("VALIDATING CASE RESOLUTION TIME")
    print("========================================")

    negative_resolution = (
        df["case_resolution_days"] < 0
    )

    print(
        "Negative case resolution times:",
        negative_resolution.sum()
    )

    return df


# ============================================================
# 18. FINAL DATA VALIDATION
# ============================================================

def validate_data(df):

    print("\n========================================")
    print("FINAL DATA VALIDATION")
    print("========================================")

    print("\nDataset Shape:")

    print(df.shape)

    print("\nMissing Values:")

    print(df.isnull().sum())

    print("\nDuplicate Rows:")

    print(df.duplicated().sum())

    print("\nData Types:")

    print(df.dtypes)

    print("\nVictim Age Range:")

    print(
        df["victim_age"].min(),
        "to",
        df["victim_age"].max()
    )

    print("\nPolice Deployed Range:")

    print(
        df["police_deployed"].min(),
        "to",
        df["police_deployed"].max()
    )

    print("\nCase Status:")

    print(
        df["case_closed"]
        .value_counts()
    )

    print("\nCrime Domains:")

    print(
        df["crime_domain"]
        .value_counts()
    )

    print("\nNumber of Cities:")

    print(
        df["city"].nunique()
    )

    print("\nTime Periods:")

    print(
        df["time_period"]
        .value_counts()
    )

    print("\nAge Groups:")

    print(
        df["age_group"]
        .value_counts()
    )

    print("\nFinal Columns:")

    print(
        df.columns.tolist()
    )

    return df


# ============================================================
# 19. SAVE PROCESSED DATA
# ============================================================

def save_data(df):

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    df.to_csv(
        PROCESSED_DATA,
        index=False
    )

    print("\n========================================")
    print("PROCESSED DATASET SAVED")
    print("========================================")

    print("\nLocation:")

    print(PROCESSED_DATA)

    print("\nFinal Shape:")

    print(df.shape)


# ============================================================
# 20. MAIN PREPROCESSING PIPELINE
# ============================================================

def preprocess():

    print("\n")
    print("========================================")
    print("       CRIMEMAPX PREPROCESSING")
    print("========================================")

    # Load data
    df = load_data()

    # Standardize column names
    df = standardize_columns(df)

    # Remove duplicate rows
    df = remove_duplicates(df)

    # Check unique report numbers
    df = check_duplicate_report_numbers(df)

    # Convert dates
    df = convert_dates(df)

    # Create temporal features
    df = create_temporal_features(df)

    # Create time features
    df = create_time_features(df)

    # Calculate reporting delay
    df = create_reporting_delay(df)

    # Clean categorical data
    df = clean_categorical_columns(df)

    # Handle missing values
    df = handle_missing_values(df)

    # Create age groups
    df = create_age_group(df)

    # Validate age
    df = validate_age(df)

    # Validate police deployment
    df = validate_police_deployment(df)

    # Calculate case resolution time
    df = create_case_resolution_time(df)

    # Validate reporting delay
    df = validate_reporting_delay(df)

    # Validate case resolution
    df = validate_case_resolution(df)

    # Final validation
    df = validate_data(df)

    # Save processed data
    save_data(df)

    print("\n========================================")
    print("PREPROCESSING COMPLETED SUCCESSFULLY")
    print("========================================")

    return df


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    preprocess()