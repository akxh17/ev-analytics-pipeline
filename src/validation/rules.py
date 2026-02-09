class AmazonSalesRules:
    def __init__(self):
        # -------------------------
        # Valid categorical values
        # -------------------------
        self.product_categories = {
            "Beauty",
            "Fashion",
            "Books",
            "Electronics",
            "Sports",
            "Home & Kitchen",
        }

        self.customer_regions = {
            "Asia",
            "North America",
            "Middle East",
            "Europe",
        }

        self.payment_methods = {
            "Wallet",
            "UPI",
            "Debit Card",
            "Cash on Delivery",
            "Credit Card",
        }

        # -------------------------
        # Numeric column rules
        # -------------------------
        self.numeric_rules = {
            "price": {"min": 0.01},
            "discount_percentage": {"min": 0, "max": 99, "default": 0},
            "quantity_sold": {"min": 1},
            "rating": {"min": 0, "max": 5},
            "review_count": {"min": 0, "default": 0},
        }
