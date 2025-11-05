import pandas as pd

class TechnicalAgent:
    """
    Technical Agent is responsible for matching RFP product specs
    with available SKUs in the company database and generating a
    match score for each SKU.
    """

    def __init__(self, sku_data_path: str):
        self.sku_data_path = sku_data_path
        self.sku_df = None

    def load_sku_data(self):
        """Load SKU data from CSV"""
        try:
            self.sku_df = pd.read_csv(self.sku_data_path)
            print(f"Loaded {len(self.sku_df)} SKUs successfully.")
        except Exception as e:
            print(f" Error loading SKU data: {e}")

    def spec_match_score(self, rfp_specs: dict, sku_specs: dict):
        """
        Calculate match score between RFP specs and SKU specs.
        Simple rule-based:
        - Exact match for categorical (e.g., insulation)
        - Tolerance match (±10%) for numeric specs
        """
        matched = 0
        total = len(rfp_specs)
        for k, v in rfp_specs.items():
            sku_v = sku_specs.get(k)
            if sku_v is None:
                continue
            # Numeric comparison
            if isinstance(v, (int, float)) and isinstance(sku_v, (int, float)):
                tolerance = max(0.1, 0.1 * abs(v))
                if abs(v - sku_v) <= tolerance:
                    matched += 1
            else:
                # String comparison (case insensitive)
                if str(v).lower() == str(sku_v).lower():
                    matched += 1
        return round((matched / total) * 100, 2)

    def match_rfp_items(self, rfp_items: list, top_k=3):
        """
        For each RFP item, calculate match scores and return top-k matches.
        """
        results = []
        for item in rfp_items:
            scores = []
            for _, sku in self.sku_df.iterrows():
                sku_specs = {
                    "conductor_mm2": sku["conductor_mm2"],
                    "insulation": sku["insulation"],
                    "voltage_kv": sku["voltage_kv"],
                    "temperature_rating_C": sku["temperature_rating_C"]
                }
                score = self.spec_match_score(item["specs"], sku_specs)
                scores.append({
                    "item_id": item["item_id"],
                    "item_description": item["description"],
                    "sku": sku["sku"],
                    "product_name": sku["product_name"],
                    "match_score": score,
                    "unit_price": sku["unit_price"]
                })
            # Sort by score (desc), price (asc)
            top_matches = sorted(scores, key=lambda x: (-x["match_score"], x["unit_price"]))[:top_k]
            results.extend(top_matches)

        return pd.DataFrame(results)

# ---- Run for testing ----
if __name__ == "__main__":
    from sales_agent import SalesAgent

    # Load RFP items
    sales = SalesAgent("data/sample_rfp.json")
    sales.load_rfp()
    rfp_items = sales.get_rfp_items()

    # Run Technical Agent
    tech = TechnicalAgent("data/mock_skus.csv")
    tech.load_sku_data()
    result_df = tech.match_rfp_items(rfp_items, top_k=3)

    print("\n Top Matches for Each Item:\n", result_df)
    result_df.to_csv("data/technical_matches.csv", index=False)
    print("\nSaved results to data/technical_matches.csv")
