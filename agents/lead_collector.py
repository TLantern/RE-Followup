"""
Load leads from `leads.csv` (headers: name,phone,interest).
"""
import csv, logging, os
logger = logging.getLogger(__name__)

def load_leads_from_csv(csv_path='leads.csv'):
    leads = []
    if not os.path.exists(csv_path):
        logger.error(f"CSV not found: {csv_path}")
        return leads
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            leads.append({'name': row.get('name'),'phone': row.get('phone'),'interest': row.get('interest')})
    logger.info(f"Loaded {len(leads)} leads")
    return leads