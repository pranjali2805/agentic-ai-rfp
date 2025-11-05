import json
import pdfplumber
import re

class SalesAgent:
    """
    Sales Agent reads RFPs (JSON or PDF) and extracts product requirements.
    """

    def __init__(self, rfp_path: str):
        self.rfp_path = rfp_path
        self.rfp_data = None

    def load_rfp(self):
        """Load RFP JSON or parse PDF"""
        try:
            if self.rfp_path.endswith(".json"):
                with open(self.rfp_path, "r") as f:
                    self.rfp_data = json.load(f)
                print(f"✅ Loaded RFP (JSON): {self.rfp_data['title']}")
            elif self.rfp_path.endswith(".pdf"):
                self.rfp_data = self._parse_pdf_rfp()
                print(f"✅ Parsed RFP (PDF): {self.rfp_data['title']}")
            else:
                raise ValueError("Unsupported file format. Please upload JSON or PDF.")
        except Exception as e:
            print(f"❌ Error loading RFP file: {e}")

    def _parse_pdf_rfp(self):
        """Parse RFP details from PDF into structured format"""
        with pdfplumber.open(self.rfp_path) as pdf:
            text = "\n".join([page.extract_text() for page in pdf.pages if page.extract_text()])
            tables = []
            for page in pdf.pages:
                page_tables = page.extract_tables()
                if page_tables:
                    tables.extend(page_tables)

        # Extract metadata
        title = re.search(r"Project:\s*(.*)", text)
        client = re.search(r"Client:\s*(.*)", text)
        rfp_id = re.search(r"RFP ID:\s*(.*)", text)
        due_date = re.search(r"Due Date:\s*(.*)", text)

        # Extract items from tables
        items = []
        for table in tables:
            for row in table[1:]:  # Skip header row
                try:
                    item_id, desc, conductor, insulation, voltage, temp = row
                    items.append({
                        "item_id": item_id.strip(),
                        "description": desc.strip(),
                        "specs": {
                            "conductor_mm2": float(conductor),
                            "insulation": insulation.strip(),
                            "voltage_kv": float(voltage),
                            "temperature_rating_C": float(temp)
                        }
                    })
                except Exception:
                    continue

        return {
            "id": rfp_id.group(1) if rfp_id else "RFP-UNKNOWN",
            "title": title.group(1) if title else "Untitled RFP",
            "buyer": client.group(1) if client else "Unknown Client",
            "due_date": due_date.group(1) if due_date else "Unknown",
            "items": items
        }

    def display_rfp_summary(self):
        """Print RFP details (for human readability)"""
        if not self.rfp_data:
            print("No RFP data found. Please load first.")
            return

        print("\n📄 RFP Summary")
        print("-" * 50)
        print(f"RFP ID: {self.rfp_data['id']}")
        print(f"Title: {self.rfp_data['title']}")
        print(f"Buyer: {self.rfp_data['buyer']}")
        print(f"Due Date: {self.rfp_data['due_date']}")
        print("\nItems to be Supplied:")
        for item in self.rfp_data["items"]:
            print(f"  🔹 {item['item_id']}: {item['description']}")
            for spec_key, spec_value in item["specs"].items():
                print(f"     • {spec_key}: {spec_value}")
        print("-" * 50)

    def get_rfp_items(self):
        """Return list of items"""
        if not self.rfp_data:
            return []
        return self.rfp_data["items"]


# ---- Run for testing ----
if __name__ == "__main__":
    rfp_path = "data/Sample_RFP_Report.pdf"
    agent = SalesAgent(rfp_path)
    agent.load_rfp()
    agent.display_rfp_summary()
