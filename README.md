# CrimeMapX

### Association Rule Mining and Interactive Visualization of Crime Patterns

Problem Statement:
Crime datasets contain large amounts of information about crime types, occurrence times, victim demographics, weapons, case status, and locations. However, raw crime data is difficult to interpret and does not directly reveal frequently occurring relationships between these attributes. There is a need for a data mining system that can preprocess and analyze historical crime data, discover meaningful associations among crime characteristics, and present crime patterns through an interactive geographical visualization. CrimeMapX aims to address this problem using Association Rule Mining and interactive map-based visualization to identify and explore significant patterns in historical crime data.

**CrimeMapX** is a data mining and visualization project that analyzes historical crime data to identify **frequent crime patterns and associations** and presents the findings through an **interactive crime map and visual analytics**.

The project applies data preprocessing, exploratory analysis, temporal analysis, and **Association Rule Mining using the Apriori algorithm** to discover relationships between crime characteristics such as crime type, crime domain, time of occurrence, victim demographics, weapons used, and case status.

---

## 🎯 Objectives

The main objectives of CrimeMapX are:

* To preprocess and clean historical crime data.
* To analyze crime patterns across different time periods and categories.
* To identify frequently occurring combinations of crime characteristics.
* To discover meaningful associations using the **Apriori algorithm**.
* To visualize crime distributions using an **interactive map**.
* To present crime trends and discovered patterns through an intuitive dashboard/visualization interface.
* To transform raw crime data into meaningful and interpretable information.

---

## 📊 Dataset

The project uses a historical crime dataset containing information about reported crime incidents.

### Dataset Attributes

| Attribute            | Description                                 |
| -------------------- | ------------------------------------------- |
| `Report Number`      | Unique identifier for the crime report      |
| `Date Reported`      | Date on which the crime was reported        |
| `Date of Occurrence` | Date on which the crime occurred            |
| `Time of Occurrence` | Time at which the crime occurred            |
| `City`               | City where the crime was reported           |
| `Crime Code`         | Code associated with the crime              |
| `Crime Description`  | Description/type of crime                   |
| `Victim Age`         | Age of the victim                           |
| `Victim Gender`      | Gender of the victim                        |
| `Weapon Used`        | Weapon involved in the crime, if applicable |
| `Crime Domain`       | Broad category/domain of the crime          |
| `Police Deployed`    | Number of police personnel deployed         |
| `Case Closed`        | Indicates whether the case was closed       |
| `Date Case Closed`   | Date on which the case was closed           |

---

## Project Structure
CrimeMapX/
│
├── data/
│   ├── raw/
│   │   └── crime_data.csv
│   │
│   └── processed/
│
├── src/
│   └── preprocessing.py
│
├── notebooks/
│   └── exploration.ipynb
│
├── outputs/
│   ├── figures/
│   ├── maps/
│   └── results/
│
├── main.py
├── requirements.txt
└── README.md


## 🔄 Project Workflow

```text
Raw Crime Dataset
       │
       ▼
Data Preprocessing
       │
       ├── Data Cleaning
       ├── Missing Value Handling
       ├── Duplicate Removal
       ├── Date/Time Processing
       └── Feature Engineering
       │
       ▼
Exploratory & Crime Analysis
       │
       ├── Temporal Analysis
       ├── Crime Category Analysis
       ├── Demographic Analysis
       └── City-wise Analysis
       │
       ▼
Transaction Transformation
       │
       ▼
Apriori Association Rule Mining
       │
       ├── Frequent Itemsets
       └── Association Rules
       │
       ▼
Interactive Crime Visualization
       │
       ├── Interactive Map
       ├── Crime Trends
       └── Association Results
       │
       ▼
Crime Insights
```

---

## 🧹 Data Preprocessing

The raw dataset is processed before analysis to improve data quality and consistency.

The preprocessing stage includes:

* Removing duplicate records.
* Checking and handling missing values.
* Standardizing column names and categorical values.
* Converting date columns into appropriate datetime formats.
* Extracting useful temporal features such as:

  * Year
  * Month
  * Day
  * Day of Week
  * Hour
  * Time Period
* Creating meaningful age groups from victim age.
* Validating numerical attributes such as victim age and police deployment.
* Handling categorical attributes such as crime description, crime domain, gender, and weapon used.
* Creating derived features such as reporting delay and case resolution time where applicable.

---

## 🔎 Crime Analysis

CrimeMapX performs multiple forms of exploratory analysis to understand crime patterns.

### Temporal Analysis

Crime occurrences are analyzed based on:

* Year
* Month
* Day of Week
* Hour
* Time Period

This helps identify periods during which certain types of crimes occur more frequently.

### Crime Category Analysis

The project analyzes:

* Crime Description
* Crime Domain
* Crime Code
* Weapon Used
* Case Status

This provides an overview of the distribution of different crime categories.

### Demographic Analysis

Crime patterns are also examined based on:

* Victim Age
* Age Group
* Victim Gender

### City-wise Analysis

Crime counts and categories are analyzed based on the available city information.

---

# 🔗 Association Rule Mining

The main data mining technique used in CrimeMapX is **Association Rule Mining**.

### Algorithm: Apriori

The **Apriori algorithm** is used to identify frequently occurring combinations of crime-related attributes and generate association rules.

For example, a transaction may contain:

```text
{Theft, Property Crime, Night, Male, No Weapon}
```

Apriori identifies combinations of such attributes that occur frequently in the dataset.

### Example Rule

```text
Night + Theft → No Weapon
```

The actual rules generated by the project will depend on the dataset and selected thresholds.

---

## 📈 Association Rule Metrics

The generated rules are evaluated using:

### Support

Measures how frequently an itemset occurs in the dataset.

```text
Support(A → B) =
Transactions containing A and B
--------------------------------
Total Transactions
```

### Confidence

Measures how frequently B occurs when A occurs.

```text
Confidence(A → B) =
Support(A ∪ B)
----------------
Support(A)
```

### Lift

Measures how strongly A and B are associated compared with their independent occurrence.

```text
Lift(A → B) =
Confidence(A → B)
-----------------
Support(B)
```

Rules with meaningful support, confidence, and lift values are selected for further interpretation.

---

# 🗺️ Interactive Crime Map

CrimeMapX includes an **interactive map** to visualize crime distribution geographically.

The map uses the location information available in the dataset to provide an interactive view of crime distribution.

Users can explore crime information by location and view relevant crime statistics and categories.

> **Note:** The current dataset contains city information but does not provide incident-level latitude and longitude coordinates. Therefore, the map represents crime distribution at the available geographic level and is not used for incident-level hotspot detection.

---

## 📊 Visualization

The project can provide visualizations such as:

* Crime distribution by category
* Crime trends over time
* Crime distribution by time period
* Crime distribution by victim demographics
* Weapon usage analysis
* Case closure analysis
* City-wise crime distribution
* Association rule visualizations
* Interactive geographic crime visualization

---

## 🛠️ Technologies Used

* **Python**
* **Pandas** – Data preprocessing and manipulation
* **NumPy** – Numerical operations
* **Matplotlib** – Data visualization
* **Seaborn** – Statistical visualization
* **Scikit-learn** – Data preprocessing and supporting analysis
* **MLxtend** – Apriori and association rule mining
* **Folium** – Interactive map visualization
* **Jupyter Notebook** – Development and analysis

---

## 📁 Project Structure

```text
CrimeMapX/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── preprocessing.ipynb
│   ├── crime_analysis.ipynb
│   └── association_rules.ipynb
│
├── src/
│   ├── preprocessing.py
│   ├── association.py
│   └── visualization.py
│
├── outputs/
│   ├── figures/
│   ├── maps/
│   └── reports/
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

## 🚀 Methodology

CrimeMapX follows the following data mining methodology:

1. **Data Collection**

   * Obtain the historical crime dataset.

2. **Data Preprocessing**

   * Clean, transform, validate, and prepare the data.

3. **Feature Engineering**

   * Extract temporal and categorical features useful for analysis.

4. **Exploratory Crime Analysis**

   * Analyze temporal, categorical, demographic, and geographic patterns.

5. **Transaction Formation**

   * Convert relevant categorical crime attributes into transaction-style data for association mining.

6. **Association Rule Mining**

   * Apply the Apriori algorithm.
   * Generate frequent itemsets.
   * Generate association rules.
   * Evaluate rules using support, confidence, and lift.

7. **Interactive Visualization**

   * Present crime distribution through an interactive map.
   * Display crime trends and discovered associations through visualizations.

8. **Pattern Interpretation**

   * Identify and interpret meaningful relationships within the crime dataset.

---

## 💡 Expected Outcomes

CrimeMapX aims to provide insights such as:

* Frequently occurring crime categories.
* Common combinations of crime characteristics.
* Relationships between crime type and time period.
* Associations between crime characteristics and victim demographics.
* Relationships involving weapon usage and crime categories.
* City-wise crime distribution.
* Temporal crime trends.
* Interactive exploration of available geographic crime information.

The project focuses on **discovering patterns and relationships in historical crime data rather than predicting individual crime incidents**.

---

## 🔮 Future Scope

Possible future enhancements include:

* Adding incident-level latitude and longitude data.
* Developing neighborhood-level crime hotspot analysis.
* Integrating real-time crime data where publicly available.
* Adding advanced association rule algorithms.
* Developing a more comprehensive interactive dashboard.
* Incorporating predictive machine learning models.
* Adding additional geographic and socioeconomic datasets.
* Deploying CrimeMapX as a web application.

---

## 👥 Project Team

**CrimeMapX**

A Data Mining project focused on crime pattern analysis, association rule mining, and interactive visualization.
1. Sampada Kaginkar
2. Vidisha Mankar
3. Mousam Patra
---

## 📜 License

This project is intended for **academic and educational purposes**.
