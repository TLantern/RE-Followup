"""
Load leads from `leads.csv` (headers: name,phone,interest).
"""
import csv, logging, os
logger = logging.getLogger(__name__)

def load_leads_from_csv(csv_path=None):
    if csv_path is None:
        # Look for leads.csv in the project root (parent directory)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_path = os.path.join(os.path.dirname(current_dir), 'leads.csv')
    
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