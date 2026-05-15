"""
=============================================================
  E-COMMERCE DATA PIPELINE — Intern Assignment
  Estimated time: 2 days
  Tools: Python 3.10+, pandas, VS Code
=============================================================

SETUP (do this first in your terminal):
  python -m venv venv
  venv\\Scripts\\activate          # Windows
  source venv/bin/activate         # Mac / Linux
  pip install pandas

FILES:
  orders.csv    — 200 rows, sales transactions
  customers.csv — 50 rows,  customer master data

YOUR GOAL: build a clean, well-structured pipeline that
reads the raw data, fixes all quality issues, and outputs:
  -> cleaned_orders.csv
  -> cleaned_customers.csv
  -> merged_report.csv
=============================================================
"""

import pandas as pd


# =============================================================
# TASK 1 — Load the data
# =============================================================
# TODO: Read orders.csv and customers.csv into DataFrames.
#       Print the shape and first 5 rows of each.
#       Print df.info() to understand column types and nulls.


#problemi u orders.csv:
# unit_price 5null vrijednosti
#  discount_pct 32 null vrijednosti,
#  country 1 null vrijednost,status 27 null vr,
#  country 24 null vrijednosti, 
# status razlika pending i Pending,
# country skracenice US,USA umjesto punog naziva

#problemi u customers.csv:
#email 3 null vrijednosti
#phone 12 null vrijednosti
#segment 7 null vrijednosti
#lifetime_value 1 null vrijednost
#segment razlicit unos vip i VIP




# =============================================================
# TASK 2 — Create a DataCleaner class
# =============================================================
# Build a class called DataCleaner that wraps a DataFrame and
# exposes the cleaning methods below.
# Every method should return `self` so calls can be chained:
#   cleaner.standardize_text_columns().fill_nulls().fix_dates()

class DataCleaner:
    """
    Wraps a DataFrame and provides cleaning utilities.
    All mutating methods return self for method chaining.
    """

    def __init__(self, df: pd.DataFrame, name: str = "dataset"):
        """
        Store the DataFrame and a human-readable name.
        Make a copy so the original is never modified.
        """
        self.df = df.copy()
        self.name = name

    def report(self) -> None:
        """Print a short summary: shape, null counts, dtypes."""
        print(self.name)
        print("Shape: ", self.df.shape)
        print("Null counts:")
        print(self.df.isnull().sum())
        print("Data types:")
        print(self.df.dtypes)
        return self

    def standardize_text_columns(self, columns: list) -> "DataCleaner":
        """
        For each column in `columns`:
          - Strip leading/trailing whitespace
          - Convert to Title Case  (e.g. 'COMPLETED' -> 'Completed')
        Return self.
        """
        for col in columns:
            self.df[col] = self.df[col].str.strip().str.title()
        return self

    def normalize_country(self, column: str) -> "DataCleaner":
        """
        Map common country abbreviations/variants to a single
        canonical name, e.g.:
          'US', 'United States', 'USA'  -> 'United States'
          'DE'                           -> 'Germany'
          'FR'                           -> 'France'
          'UK', 'United Kingdom'         -> 'United Kingdom'
        Leave NaN values as NaN (handle them in fill_nulls).
        Return self.
        """
        country_map = {"US": "United States",
                       "USA": "United States",
                       "DE": "Germany",
                       "FR": "France",
                       "UK": "United Kingdom",
                       "United States": "United States",
                       "United Kingdom": "United Kingdom"
           
        }
        self.df[column]=self.df[column].map(lambda x:country_map.get(x,x) if pd.notna(x) else x)
        return self

    def fix_dates(self, column: str) -> "DataCleaner":
        """
        Parse `column` to datetime, handling mixed formats
        such as 'YYYY-MM-DD' and 'DD/MM/YYYY'.
        Store the result as a proper datetime column.
        Hint: pd.to_datetime(..., dayfirst=True, errors='coerce')
        Return self.
        """
        self.df[column]=pd.to_datetime(self.df[column],dayfirst=True,errors="coerce")
        return self

    def fill_nulls(self, strategy: dict) -> "DataCleaner":
        """
        Fill null values column-by-column based on a strategy dict.
        Example strategy:
          {
            'unit_price': 'median',
            'status':     'Unknown',
            'country':    'Unknown',
          }
        Supported strategies:
          'mean'   -> fill with column mean
          'median' -> fill with column median
          'mode'   -> fill with most frequent value
          any str  -> fill with that literal string / value
        Return self.
        """
        for col, strat in strategy.items():
            if strat=="mean":
                self.df[col]=self.df[col].fillna(self.df[col].mean())
            elif strat=="median":
                self.df[col]=self.df[col].fillna(self.df[col].median())
            elif strat=="mode":
                self.df[col]=self.df[col].fillna(self.df[col].mode()[0])
            else:
                self.df[col]=self.df[col].fillna(strat)
        return self

    def remove_duplicates(self, subset: list = None) -> "DataCleaner":
        """
        Drop duplicate rows.
        If `subset` is provided, only consider those columns.
        Print how many duplicates were removed.
        Return self.
        """
        before=len(self.df)
        self.df=self.df.drop_duplicates(subset=subset)
        print(before)
        after=len(self.df)
        print(after)
        print(f"Removed {before-after} duplicates.")
        return self

    def add_revenue_column(self,
                           price_col: str,
                           qty_col: str,
                           discount_col: str) -> "DataCleaner":
        """
        Add a new column 'revenue' calculated as:
          revenue = unit_price * quantity * (1 - discount_pct / 100)
        Where discount_pct is NaN, treat it as 0.
        Round to 2 decimal places.
        Return self.
        """
        discount=self.df[discount_col].fillna(0)
        self.df["revenue"]=self.df[price_col]*self.df[qty_col]*(1-discount/100)
        self.df["revenue"]=self.df["revenue"].round(2)
        return self

    def get(self) -> pd.DataFrame:
        """Return the cleaned DataFrame."""
        return self.df.copy()


# =============================================================
# TASK 3 — Clean the orders dataset
# =============================================================
# Instantiate DataCleaner with orders_df.
# Chain the following steps:
#   1. report()                       (print before state)
#   2. standardize_text_columns()     for 'status' and 'category'
#   3. normalize_country()            for 'country'
#   4. fix_dates()                    for 'order_date'
#   5. fill_nulls()                   choose a sensible strategy
#   6. remove_duplicates()
#   7. add_revenue_column()
#   8. report()                       (print after state)
# Save the result to cleaned_orders.csv (no index).



# =============================================================
# TASK 4 — Clean the customers dataset
# =============================================================
# Instantiate DataCleaner with customers_df.
# Chain the steps that make sense for this dataset:
#   - standardize 'segment'
#   - fill nulls in 'last_name', 'email', 'lifetime_value'
#   - remove duplicates
# Save to cleaned_customers.csv (no index).



# =============================================================
# TASK 5 — Merge the two cleaned datasets
# =============================================================
# Merge cleaned_orders with cleaned_customers on 'customer_id'.
# Use a LEFT join (keep all orders, attach customer info).
# Print:
#   - Total number of rows in the merged result
#   - How many orders have no matching customer (if any)
# Save to merged_report.csv (no index).





# =============================================================
# TASK 6 — Analyse & summarise  (BONUS)
# =============================================================
# Using the merged DataFrame, answer these questions with code:
#
#  Q1. What is the total revenue per category?
#      (sorted descending)


#  Q2. Which country placed the most orders?
#  Q3. What is the average order value per customer segment?
#  Q4. Which month of 2023 had the highest total revenue?

#  Q5. List the top 5 customers by total revenue.


# =============================================================
# ENTRY POINT
# =============================================================
if __name__ == "__main__":
    print("Starting e-commerce pipeline...")
    orders_df = pd.read_csv("orders.csv")
    customers_df = pd.read_csv("customers.csv")
    print("Orders shape: ", orders_df.shape)
    print("First 5 rows of orders: ", orders_df.head())
    print("Orders info: ",orders_df.info())
    print("Orders nulls values ",orders_df.isnull().sum())
    print("Customers shape: ", customers_df.shape)
    print("First 5 rows of customers: ", customers_df.head())
    print("Customers info: ", customers_df.info())
    print("Customers nulls values ",customers_df.isnull().sum())
    orders_cleaner = DataCleaner(orders_df, "orders")
    orders_clean   = (orders_cleaner.standardize_text_columns(["status", "category"])
                  .normalize_country("country")
                  .fix_dates("order_date")
                  .fill_nulls({"unit_price": "median", "status": "Unknown", "country": "Unknown", "discount_pct":0})
                  .remove_duplicates()
                  .add_revenue_column("unit_price", "quantity", "discount_pct")
                  .get())
    orders_cleaner.report() 
    orders_clean.to_csv("cleaned_orders.csv", index=False)
    print("Sačuvano: cleaned_orders.csv")
    customers_cleaner = DataCleaner(customers_df, "customers")
    customers_clean=(customers_cleaner.standardize_text_columns(["segment"]).fill_nulls({"last_name":"Unknown", "email":"Unknown", "lifetime_value":"median"}).remove_duplicates().get())
    customers_cleaner.report()
    customers_clean.to_csv("cleaned_customers.csv", index=False)
    print("Sačuvano: cleaned_customers.csv")
    merged = orders_clean.merge(customers_clean, on="customer_id", how="left")
    print(f"Total rows in merged report: {len(merged)}")
    missing_customers = merged["first_name"].isnull().sum()
    print(f"Orders with no matching customer: {missing_customers}")
    merged.to_csv("merged_report.csv", index=False)
    print("Sačuvano: merged_report.csv")
    print("Total revenue per category:")
    print(merged.groupby("category")["revenue"].sum().sort_values(ascending=False))

    print("Country with most orders:")
    print(merged.groupby("country")["order_id"].count().idxmax())
    print("Average order value per customer segment:")
    print(merged.groupby("segment")["revenue"].mean())
    print("Month of 2023 with highest total revenue:")
    merged_2023=merged[merged["order_date"].dt.year==2023]
    print(merged_2023.groupby(merged_2023["order_date"].dt.month)["revenue"].sum().idxmax())
    print("Top 5 customers by total revenue:")
    print(merged.groupby(["customer_id", "first_name", "last_name"])["revenue"].sum().sort_values(ascending=False).head(5))



    print("Pipeline complete.")
