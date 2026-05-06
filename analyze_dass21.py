import pandas as pd

df = pd.read_excel('DATA PENELITIAN.xlsx', header=None)

# Extract actual data (skip header rows)
data = df.iloc[3:56, [1, 2, 3, 4, 5, 6, 7]]
data.columns = ['Responden', 'HR_test1', 'HR_test2', 'Temp_test1', 'Temp_test2', 'DASS21_Score', 'Stress_Category']

print("DATA ANALYSIS:")
print(data.to_string())
print("\n" + "="*80)
print("\nDASS-21 SCORE vs STRESS CATEGORY RELATIONSHIP:")
print("="*80)

# Group by category
for cat in sorted(data['Stress_Category'].unique()):
    if pd.notna(cat):
        subset = data[data['Stress_Category'] == cat]
        scores = subset['DASS21_Score'].astype(int)
        print(f"\nCategory {cat}:")
        print(f"  Score range: {scores.min()} - {scores.max()}")
        print(f"  Respondents: {subset['Responden'].tolist()}")
        print(f"  Scores: {scores.tolist()}")

print("\n" + "="*80)
print("\nDASS-21 SCORING CATEGORIES (Standard):")
print("="*80)
print("""
DASS-21 Stress Severity Labels:
- Category 0: Normal (0-14)
- Category 1: Mild (15-18)
- Category 2: Moderate (19-25)
- Category 3: Severe (26-33)
- Category 4: Extremely Severe (34+)

Note: DASS-21 scores are multiplied by 2 to get DASS-42 equivalent
""")

print("\n" + "="*80)
print("VERIFICATION:")
print("="*80)

# Verify the categorization
for idx, row in data.iterrows():
    if pd.notna(row['DASS21_Score']) and pd.notna(row['Stress_Category']):
        score = int(row['DASS21_Score'])
        cat = int(row['Stress_Category'])
        
        # Determine expected category
        if score <= 14:
            expected = 0
        elif score <= 18:
            expected = 1
        elif score <= 25:
            expected = 2
        elif score <= 33:
            expected = 3
        else:
            expected = 4
        
        match = "✓" if expected == cat else "✗"
        print(f"{row['Responden']}: Score={score}, Category={cat}, Expected={expected} {match}")
