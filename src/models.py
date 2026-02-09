from sqlalchemy import Column, Integer, String, Float, Date, DateTime, Boolean, DECIMAL, Text
from src.db import Base
from datetime import date

class AmazonSales(Base):
    __tablename__ = "amazon_sales"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_date = Column(Date, default=date.today, index=True)
    
    product_title = Column(Text)
    product_rating = Column(Float)
    total_reviews = Column(Integer)
    purchased_last_month = Column(Integer)
    discounted_price = Column(DECIMAL(10, 2))
    original_price = Column(DECIMAL(10, 2))
    discount_percentage = Column(Float)
    
    # Categorical/Text fields
    is_best_seller = Column(String)
    is_sponsored = Column(String)
    has_coupon = Column(String)
    buy_box_availability = Column(String)
    
    # Engineered Features (Persisted for Power BI Consistency)
    discount_percentage_fixed = Column(Float)
    badge_category = Column(String)
    is_best_seller_flag = Column(Boolean)
    is_amazons_choice = Column(Boolean)
    has_promo_tag = Column(Boolean)
    is_new_arrival = Column(Boolean)
    has_buy_box = Column(Boolean)
    discount_range = Column(String)
    rating_bin = Column(String)
    
    # Metadata
    delivery_date = Column(String)
    sustainability_tags = Column(String)
    product_image_url = Column(Text)
    product_page_url = Column(Text)
    data_collected_at = Column(DateTime)
    product_category = Column(String, index=True)

    def __repr__(self):
        return f"<AmazonSales(id={self.id}, title={self.product_title[:20]}...)>"
