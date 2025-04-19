import pandas as pd
from typing import List, Dict

class SpreadsheetManager:
    def save_to_excel(self, data: List[Dict], filename: str = "output.xlsx"):
        """Save data to Excel file"""
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Data saved to {filename}")
        return True