import matplotlib.pyplot as plt
import os
from core.config import settings
from datetime import datetime

def generate_finance_report(data, user_id):
    """
    Generates a pie chart for expenses by category.
    data: list of tuples (category, total_amount)
    """
    if not data:
        return None
        
    categories = [row[0] for row in data]
    amounts = [row[1] for row in data]
    
    plt.figure(figsize=(10, 6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title(f"Xarajatlar tahlili - {datetime.now().strftime('%Y-%m-%d')}")
    
    report_path = os.path.join(settings.REPORTS_DIR, f"report_{user_id}_{int(datetime.now().timestamp())}.png")
    plt.savefig(report_path)
    plt.close()
    
    return report_path
