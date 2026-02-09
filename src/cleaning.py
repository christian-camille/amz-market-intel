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
    # Create copy to avoid SettingWithCopy warnings
    df = df.copy()

    # Handle Missing Ratings/Reviews (New Arrivals)
    if 'product_rating' in df.columns:
        df['product_rating'] = df['product_rating'].fillna(0)
    if 'total_reviews' in df.columns:
        df['total_reviews'] = df['total_reviews'].fillna(0)

    # Fix Discount Percentage
    if 'discount_percentage' in df.columns and 'is_best_seller' in df.columns:
        df['discount_percentage_fixed'] = df.apply(extract_discount_from_badge, axis=1)
    
    # Badge Categorization & Tagging
    if 'is_best_seller' in df.columns:
        df['badge_category'] = df['is_best_seller'].apply(simplify_badge)
        
        # Boolean flags
        df['is_best_seller_flag'] = df['is_best_seller'].str.contains('Best Seller', case=False, na=False)
        df['is_amazons_choice'] = df['is_best_seller'].str.contains("Amazon's", case=False, na=False)
        
        urgency_keywords = ['Limited time deal', 'Ends in', 'Save']
        df['has_promo_tag'] = df['is_best_seller'].str.contains('|'.join(urgency_keywords), case=False, na=False)
        
    # New Arrival Signal
    # Conditions: 0 rating AND 0 reviews (after imputation)
    if 'product_rating' in df.columns and 'total_reviews' in df.columns:
        df['is_new_arrival'] = (df['product_rating'] == 0) & (df['total_reviews'] == 0)

    # Clean Buy Box
    if 'buy_box_availability' in df.columns:
        # Standardise to Yes/No
        df['buy_box_availability'] = df['buy_box_availability'].fillna('No').replace({'Add to cart': 'Yes'})
        # Create boolean flag
        df['has_buy_box'] = df['buy_box_availability'] == 'Yes'
        
    # Binning (Ranges)
    # Discount Range
    if 'discount_percentage_fixed' in df.columns:
        bins = [-1, 0, 5, 10, 20, 30, 50, 100]
        labels = ['No Discount', '0-5%', '5-10%', '10-20%', '20-30%', '30-50%', '50%+']
        # Convert to string to ensure PostgreSQL compatibility (ENUM or TEXT)
        df['discount_range'] = pd.cut(df['discount_percentage_fixed'], bins=bins, labels=labels).astype(str)
        # Fix 'nan' strings if any
        df['discount_range'] = df['discount_range'].replace('nan', None)

    # Rating Bin
    if 'product_rating' in df.columns:
        # We need to handle 0 separately or include it. 
        # Notebook logic: bins=[0, 3, 4, 4.5, 5], labels=['<3', '3-4', '4-4.5', '4.5+']
        # But 0 is 'New Arrival' typically. Let's include 0 in <3 or keep separate?
        # Notebook used: df[df['product_rating'] > 0] for plotting. 
        # Let's bin everything, users can filter 'New Arrivals'.
        # Custom binning to handle 0 properly might be safer, but pd.cut works ok.
        rate_bins = [-0.1, 2.99, 3.99, 4.49, 5.0]
        rate_labels = ['<3', '3-4', '4-4.5', '4.5+']
        df['rating_bin'] = pd.cut(df['product_rating'], bins=rate_bins, labels=rate_labels).astype(str)
        df['rating_bin'] = df['rating_bin'].replace('nan', None)

    # Encode 'is_sponsored' (Standardize)
    if 'is_sponsored' in df.columns:
        # Ensure it's consistent if needed, mostly it's already 'Sponsored'/'Organic' logic upstream or extracted.
        # Assuming current state is fine, but let's ensure no NaNs
        df['is_sponsored'] = df['is_sponsored'].fillna('Organic') 

    return df
