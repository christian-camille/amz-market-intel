import pandas as pd
import os
from datetime import date
from src.db import engine, Base
from src.models import AmazonSales
from src.cleaning import clean_sales_data
from sqlalchemy.orm import Session

def migrate():
    print("Starting data migration (Time-Series Enabled)...")
    try:
        Base.metadata.drop_all(bind=engine)
        print("Dropped existing tables to enforce new schema.")
    except Exception as e:
        print(f"Warning dropping tables: {e}")

    Base.metadata.create_all(bind=engine)
    
    # Read CSV
    csv_path = os.path.join("data", "amazon_products_sales_data_cleaned.csv")
    if not os.path.exists(csv_path):
        print(f"Error: CSV file not found at {csv_path}")
        return

    print(f"Reading data from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    
    print("Applying data cleaning...")
    df = clean_sales_data(df)
    
    today = date.today()
    df['snapshot_date'] = today
    
    model_columns = [c.name for c in AmazonSales.__table__.columns if c.name != 'id']
    df_to_upload = df[df.columns.intersection(model_columns)]

    print(f"Uploading {len(df_to_upload)} rows for snapshot date: {today}...")
    
    try:
        with Session(engine) as session:
            rows_deleted = session.query(AmazonSales).filter(AmazonSales.snapshot_date == today).delete()
            if rows_deleted:
                print(f"Removed {rows_deleted} existing rows for today to avoid duplicates.")
            
            session.commit()

        df_to_upload.to_sql(AmazonSales.__tablename__, engine, if_exists='append', index=False)
        print("Data upload completed successfully.")
        
    except Exception as e:
        print(f"Error uploading data: {e}")

if __name__ == "__main__":
    migrate()
