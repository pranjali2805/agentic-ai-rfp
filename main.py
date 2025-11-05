from sales_agent import SalesAgent
from technical_agent import TechnicalAgent
from pricing_agent import PricingAgent
from report_generator import ReportGenerator
import pandas as pd

class MasterAgent:
    """
    Orchestrates all worker agents and generates final report.
    """

    def __init__(self):
        self.rfp_path = "data/sample_rfp.json"
        self.sku_path = "data/mock_skus.csv"
        self.tech_output = "data/technical_matches.csv"
        self.pricing_output = "data/final_pricing_summary.csv"

    def run(self):
        print("\nStarting Agentic AI RFP Automation...\n")

        # 1️⃣ Sales Agent
        sales = SalesAgent(self.rfp_path)
        sales.load_rfp()
        rfp_items = sales.get_rfp_items()

        # 2️⃣ Technical Agent
        tech = TechnicalAgent(self.sku_path)
        tech.load_sku_data()
        matches_df = tech.match_rfp_items(rfp_items)
        matches_df.to_csv(self.tech_output, index=False)
        print(f"Technical matches saved to {self.tech_output}")

        # 3️⃣ Pricing Agent
        pricing = PricingAgent(self.tech_output)
        pricing.load_matches()
        top_df = pricing.select_top_matches()
        final_df = pricing.calculate_costs(top_df, quantity_per_item=100)
        final_df.to_csv(self.pricing_output, index=False)
        print(f"Pricing summary saved to {self.pricing_output}")

        # 4️⃣ Report Generator
        ppt = ReportGenerator("Industrial Cable Supply (Demo)", final_df)
        ppt.add_title_slide()
        ppt.add_process_flow()
        ppt.add_match_summary()
        ppt.add_pricing_summary()
        ppt.add_conclusion_slide()
        ppt.save_ppt("data/AsianPaints_RFP_Report.pptx")

        print("\nWorkflow completed successfully!\n")

if __name__ == "__main__":
    MasterAgent().run()
