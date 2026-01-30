"""
Budget Calculator Tool
Estimates trip costs based on destination and duration.
"""


def calculate_budget(query: str) -> str:
    """
    Calculate estimated trip budget.
    
    Args:
        query: Budget query like "budget for Paris 5 days" or "cost of Tokyo trip"
    
    Returns:
        Budget breakdown as formatted string
    """
    query_lower = query.lower()
    
    # Try to extract days
    days = 3  # default
    for word in query_lower.split():
        if word.isdigit():
            days = int(word)
            break
    
    # City cost tiers (daily estimates in INR)
    expensive_cities = ["paris", "london", "tokyo", "new york", "sydney", "dubai"]
    moderate_cities = ["bangkok", "singapore", "bali", "istanbul", "rome"]
    budget_cities = ["delhi", "mumbai", "goa", "jaipur", "kerala", "vietnam", "nepal"]
    
    # Determine tier
    daily_cost = 8000  # default moderate
    tier = "Moderate"
    
    for city in expensive_cities:
        if city in query_lower:
            daily_cost = 15000
            tier = "Premium"
            break
    
    for city in budget_cities:
        if city in query_lower:
            daily_cost = 4000
            tier = "Budget-Friendly"
            break
    
    # Calculate costs
    accommodation = daily_cost * 0.4 * days
    food = daily_cost * 0.25 * days
    transport = daily_cost * 0.2 * days
    activities = daily_cost * 0.15 * days
    total = accommodation + food + transport + activities
    
    return (
        f"💰 Budget Estimate ({days} days, {tier} tier):\n\n"
        f"🏨 Accommodation: ₹{accommodation:,.0f}\n"
        f"🍽️ Food & Dining: ₹{food:,.0f}\n"
        f"🚗 Local Transport: ₹{transport:,.0f}\n"
        f"🎯 Activities & Sightseeing: ₹{activities:,.0f}\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 Total Estimate: ₹{total:,.0f}\n\n"
        f"💡 Note: This excludes flight costs. Prices may vary based on season and preferences."
    )
