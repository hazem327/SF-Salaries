import pandas as pd


print("Loading Salaries.csv...")
df = pd.read_csv('Salaries.csv', low_memory=False)
print(f"Original shape: {df.shape[0]:,} rows, {df.shape[1]} columns")


cols_to_check = [col for col in df.columns if col != 'Id']
dups_count = df.duplicated(subset=cols_to_check).sum()
print(f"\nDuplicates found (ignoring Id): {dups_count}")


df = df.drop_duplicates(subset=cols_to_check, keep='first')
print(f"Rows after removing duplicates: {len(df):,}")


print("\nCleaning null values...")


placeholders = ['Not Provided', 'Not provided', '']
df = df.replace(placeholders, None)


if 'Notes' in df.columns:
    df = df.drop(columns=['Notes'])
    print(" - Dropped 'Notes' column (was 100% null)")


if 'Status' in df.columns:
    df['Status'] = df['Status'].fillna('Unknown')


pay_columns = ['BasePay', 'OvertimePay', 'OtherPay', 'Benefits', 'TotalPay', 'TotalPayBenefits']
for col in pay_columns:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')


if 'Benefits' in df.columns:
    df['Benefits'] = df['Benefits'].fillna(0.0)


df_cleaned = df.dropna(subset=['EmployeeName', 'BasePay'])


output_filename = 'cleaned_Salaries.csv'
df_cleaned.to_csv(output_filename, index=False)

print("\n" + "=" * 45)
print(f"SUCCESS: Cleaned dataset saved to '{output_filename}'")
print(f"Final shape: {df_cleaned.shape[0]:,} rows, {df_cleaned.shape[1]} columns")
print("\nRemaining null count per column:")
print(df_cleaned.isnull().sum())
print("=" * 45)

