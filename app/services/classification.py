from typing import List, Dict, Tuple
from collections import defaultdict

# Minimal mapping of NICE classes with simple keywords for MVP demonstration.
# This is NOT exhaustive and must be expanded/curated for production use.
NICE_CLASS_KEYWORDS: Dict[int, Tuple[str, List[str]]] = {
    1: ("Chemicals", ["chemical", "fertilizer", "adhesive", "salt"]),
    3: ("Cosmetics and Cleaning", ["cosmetic", "soap", "perfume", "shampoo", "detergent", "cleaning"]),
    5: ("Pharmaceuticals", ["pharmaceutical", "medicine", "supplement", "vitamin", "sanitary"]),
    9: ("Electronics and Software", ["software", "app", "computer", "camera", "sensor", "ai", "saas"]),
    16: ("Paper Goods; Printed Matter", ["book", "magazine", "stationery", "paper", "card"]),
    25: ("Clothing, Footwear, Headgear", ["clothing", "t-shirt", "shirt", "shoe", "cap", "hoodie", "fashion"]),
    30: ("Staple Foods", ["coffee", "tea", "bread", "chocolate", "snack", "spice"]),
    32: ("Beers and Non-alcoholic Beverages", ["juice", "soda", "water", "energy drink", "beer"]),
    33: ("Alcoholic Beverages", ["wine", "whisky", "vodka", "gin"]),
    35: ("Advertising; Retail Services", ["retail", "ecommerce", "marketing", "advertising", "online store", "marketplace"]),
    36: ("Financial Services", ["banking", "payment", "wallet", "insurance", "fintech"]),
    38: ("Telecommunications", ["telecom", "sms", "messaging", "isp", "network"]),
    41: ("Education; Training", ["education", "course", "training", "school", "workshop"]),
    42: ("Scientific and Technology Services", ["software development", "hosting", "cloud", "design", "engineering", "research"]),
        43: ("Food and Drink Services", ["restaurant", "cafe", "catering", "food truck"]),
    44: ("Medical; Beauty; Agriculture", ["clinic", "spa", "beauty", "salon", "agriculture"]),
    45: ("Legal and Security Services", ["legal", "security", "licensing", "ip services"]),
}


def suggest_classes(business_description: str, max_results: int = 4) -> List[tuple]:
    text = business_description.lower()
    scores = defaultdict(float)

    for class_no, (title, keywords) in NICE_CLASS_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[class_no] += 1.0

    # Basic heuristic normalization by keyword count
    ranked = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:max_results]
    suggestions: List[tuple] = []
    for class_no, score in ranked:
        title = NICE_CLASS_KEYWORDS[class_no][0]
        confidence = min(0.9, 0.5 + 0.1 * score)
        suggestions.append((class_no, title, confidence))
    return suggestions 