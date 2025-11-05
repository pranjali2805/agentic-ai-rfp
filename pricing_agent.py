import pandas as pd

class PricingAgent:
    """
    Pricing Agent calculates final cost of selected SKUs,
    including product unit price, quantity, and testing costs.
    """

    def __init__(self, matches_path: str):
        self.matches_path = matches_path
        self.matches_df = None

        # Define test cost table (mock data)
        self.test_costs = {
            "Tensile Test": 500,
            "Insulation Resistance": 300,
            "Voltage Withstand Test": 400,
            "Armor Integrity Test": 350
        }

    def load_matches(self):
        """Load matches CSV from Technical Agent"""
        try:
            self.matches_df = pd.read_csv(self.matches_path)
            print(f"Loaded matches file with {len(self.matches_df)} rows.")
        except Exception as e:
            print(f" Error loading matches: {e}")

    def select_top_matches(self):
        """
        Select the best SKU (top-1) for each RFP item.
        """
        if self.matches_df is None:
            print("Please load matches first.")
            return None

        top_df = (
            self.matches_df.sort_values(["item_id", "match_score", "unit_price"],
                                        ascending=[True, False, True])
            .groupby("item_id")
            .head(1)
            .reset_index(drop=True)
        )
        print(f"Selected {len(top_df)} top matches (1 per item).")
        return top_df

    def calculate_costs(self, selected_df, quantity_per_item=100):
        """
        Add total cost calculation for each item.
        Formula: total = (unit_price × quantity) + (test_cost × quantity)
        """
        results = []
        for _, row in selected_df.iterrows():
            sku_name = row["product_name"]
            qty = quantity_per_item
            unit_price = row["unit_price"]

            # Simple logic: if 'Armour' in name → add Armor Integrity Test
            tests = ["Tensile Test", "Insulation Resistance", "Voltage Withstand Test"]
            if "Armour" in sku_name or "Armour" in row["sku"]:
                tests.append("Armor Integrity Test")

            total_test_cost = sum(self.test_costs[t] for t in tests)
            material_cost = qty * unit_price
            total_cost = material_cost + total_test_cost * qty

            results.append({
                "item_id": row["item_id"],
                "item_description": row["item_description"],
                "sku": row["sku"],
                "product_name": sku_name,
                "match_score": row["match_score"],
                "quantity": qty,
                "unit_price": unit_price,
                "material_cost": material_cost,
                "tests": ", ".join(tests),
                "tests_cost_per_unit": total_test_cost,
                "total_cost": total_cost
            })

        df = pd.DataFrame(results)
        print(" Pricing calculation completed.")
        return df

# ---- Run for testing ----
if __name__ == "__main__":
    pricing = PricingAgent("data/technical_matches.csv")
    pricing.load_matches()

    top_df = pricing.select_top_matches()
    final_df = pricing.calculate_costs(top_df, quantity_per_item=100)

    print("\nFinal Pricing Summary:\n", final_df)
    final_df.to_csv("data/final_pricing_summary.csv", index=False)
    print("\n Saved results to data/final_pricing_summary.csv")
