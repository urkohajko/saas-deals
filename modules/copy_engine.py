CATEGORY_TAGS = {
    "AI": ["#AI", "#ArtificialIntelligence", "#SaaS"],
    "Marketing": ["#MarketingTools", "#SaaS", "#Growth"],
    "Productivity": ["#Productivity", "#SaaS", "#Tools"],
}

def generate_hashtags(category):
    tags = CATEGORY_TAGS.get(category, ["#SaaS", "#Deals"])
    return " ".join(tags)
