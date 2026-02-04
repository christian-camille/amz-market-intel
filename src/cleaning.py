import pandas as pd
import re
import numpy as np

def extract_discount_from_badge(row):
    # Extract discount percentage from 'is_best_seller' badge text if the numeric
    # discount column is missing or zero.
    if pd.isna(row['discount_percentage']) or row['discount_percentage'] == 0:
        # Look for patterns like "Save 15%"
        match = re.search(r'Save (\d+)%', str(row['is_best_seller']))
        if match:
            return float(match.group(1))
    return row['discount_percentage']

def simplify_badge(val):
    # Categorise the 'is_best_seller' badge into broader groups.
    val_str = str(val)
    urgency_keywords = ['Limited time deal', 'Ends in', 'Save']
    
    if 'Best Seller' in val_str:
        return 'Best Seller'
    if "Amazon's" in val_str:
        return "Amazon's Choice"
    if any(k in val_str for k in urgency_keywords):
        return 'Promotional'
    return 'No Badge'

def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    # Apply standard cleaning and feature engineering steps to the Amazon Sales DataFrame.
    # Create copy to avoid SettingWithCopy warnings
    df = df.copy()

    # 1. Feature Recovery: Fix Discount Percentage
    if 'discount_percentage' in df.columns and 'is_best_seller' in df.columns:
        df['discount_percentage_fixed'] = df.apply(extract_discount_from_badge, axis=1)
    
    # 2. Badge Categorization
    if 'is_best_seller' in df.columns:
        df['badge_category'] = df['is_best_seller'].apply(simplify_badge)
        
        # Boolean flags
        df['is_best_seller_flag'] = df['is_best_seller'].str.contains('Best Seller', case=False, na=False)
        df['is_amazons_choice'] = df['is_best_seller'].str.contains("Amazon's", case=False, na=False)
        
    # 3. New Arrival Signal
    # Conditions: 0 rating AND 0 reviews
    if 'product_rating' in df.columns and 'total_reviews' in df.columns:
        df['is_new_arrival'] = (df['product_rating'] == 0) & (df['total_reviews'] == 0)

    # 4. Clean Buy Box
    if 'buy_box_availability' in df.columns:
        # Standardise to Yes/No
        df['buy_box_availability'] = df['buy_box_availability'].fillna('No').replace({'Add to cart': 'Yes'})
        # Create boolean flag
        df['has_buy_box'] = df['buy_box_availability'] == 'Yes'
        
    # 5. Encode 'is_sponsored'
    if 'is_sponsored' in df.columns:
        pass

    return df
