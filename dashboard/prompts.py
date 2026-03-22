import random
import json

PROMPTS = {
    'A': {
        'name': 'Understand "What’s Going On"',
        'icon': 'fa-brain',
        'color': 'primary',
        'prompts': [
            "You are my Chief of Staff. Look at this data and explain in simple business language what this data is about and what story it tells. Keep it under 10 bullet points.",
            "From this data, what are the top 10 things I, as CEO, should know right now? Prioritize by business impact (high to low).",
            "Summarize this data in a one-page CEO briefing: context, key numbers, key trends, and any red flags.",
            "Group the data into logical business buckets (for example: products, regions, channels, customer segments) and explain how each bucket is performing.",
            "If you had to explain this dataset to a non-technical board member, how would you describe it in 5 bullets?",
            "Create a simple health report: traffic light style (green = healthy, yellow = watch, red = problem) for the main metrics in this file.",
            "Identify the 5 most important KPIs that naturally emerge from this dataset, explain each KPI in plain English, and give their current values and trend.",
            "What are the biggest positive surprises and negative surprises you see in this data compared to what a typical business of this type might expect?",
            "Is this dataset complete enough to make decisions? List clearly what is missing or poor-quality from a CEO decision-making perspective.",
            "Convert this data into a monthly business review outline that I could walk through with my leadership team."
        ]
    },
    'B': {
        'name': 'Spot Problems and Risks',
        'icon': 'fa-shield-alt',
        'color': 'red-500',
        'prompts': [
            "Scan this data like a risk auditor. What potential problems, leakages, or risks do you see that may require immediate attention?",
            "Highlight any abnormal patterns, outliers, or sudden changes that could indicate fraud, errors, or operational issues.",
            "Show me the top 10 rows, customers, products, or transactions that worry you the most and explain why.",
            "Identify where we might be losing money or margin. Show specific examples and estimate the potential impact if the issue continues for 12 months.",
            "Find any negative trends (declines, increases in cost, rising churn, delayed payments). Rank them from most dangerous to least.",
            "Are there concentration risks (for example, too much revenue or cost tied to a single customer, vendor, or region)? Highlight them with numbers.",
            "Show me any situations in this data where we are giving too much discount, too much credit period, or selling unprofitable deals.",
            "If you were my CRO (Chief Risk Officer), what 5 alerts would you set up based on this file to protect the business?",
            "List potential data quality issues (missing values, duplicates, inconsistent formats) that could distort my decisions, and suggest how to fix them.",
            "If a regulator or auditor looked at this data, what questions might they ask us? List them."
        ]
    },
    'C': {
        'name': 'Revenue and Growth',
        'icon': 'fa-chart-line',
        'color': 'emerald-500',
        'keywords': ['revenue', 'profit', 'margin', 'growth', 'sales', 'cost', 'amount', 'price'],
        'prompts': [
            "From this sheet, break down revenue, cost, and profit (if possible) by product, customer, and region, and show who is driving our results.",
            "Identify our top 10 revenue drivers and our bottom 10 (loss-making or tiny contributors). Suggest actions for each group.",
            "Show whether our revenue is growing, flat, or declining over time. Call out any months or quarters that are particularly strong or weak.",
            "Analyze our margins (if cost data exists). Who are our most profitable customers, products, or regions and who are the worst?",
            "If we had to cut 10% of our product or customer portfolio with minimum impact on profit, what should we cut based on this data?",
            "Estimate our revenue run rate for the next 12 months based only on trends in this file. Explain assumptions in simple terms.",
            "Spot any seasonality or cyclic patterns in our revenue or transactions. Explain how this should influence hiring, inventory, and marketing.",
            "Are we over-dependent on any one customer, product, or region for our revenue or margin? Quantify that dependency.",
            "Show the relationship between discounts, volume, and margin in this dataset and tell me if our discounting strategy looks healthy or risky.",
            "If we want to grow revenue by 30% next year, which 3-5 levers in this data look most promising and realistic?"
        ]
    },
    'D': {
        'name': 'Customers and Retention',
        'icon': 'fa-users',
        'color': 'indigo-500',
        'keywords': ['customer', 'churn', 'retention', 'user', 'client', 'email', 'name'],
        'prompts': [
            "Segment our customers using the data available (for example: by revenue, frequency, geography, industry). Describe each segment in business language.",
            "Identify our top 20 customers by revenue and by profit. Show whether their business with us is growing or shrinking over time.",
            "Find customers who are at risk of churn based on reduced activity, smaller order sizes, delayed payments, or longer gaps between purchases.",
            "Highlight any 'hidden gems'—small customers who are growing quickly and could become strategic accounts.",
            "If you were our Head of Customer Success, what 5 customer groups would you prioritize and what specific actions would you recommend for each?",
            "Analyze customer lifetime value using the available data (even approximately). Who are our high-LTV and low-LTV customers?",
            "Show any correlation between customer type/segment and late payments, churn, or high support costs.",
            "Based on this sheet alone, what are 5 practical ideas to improve retention and increase revenue from existing customers?",
            "Create a simple RFM-style view (Recency, Frequency, Monetary) of customers using this data and explain the key insights in plain English.",
            "Summarize customer behavior trends over time: Are they buying more often, spending more, or becoming less active?"
        ]
    },
    'E': {
        'name': 'Operations and Forecasts',
        'icon': 'fa-cogs',
        'color': 'amber-500',
        'keywords': ['operation', 'forecast', 'stock', 'inventory', 'process', 'delivery', 'payment', 'cash', 'date', 'time'],
        'prompts': [
            "Look for operational bottlenecks in this data: delays, backlogs, slow-moving items, or any field that indicates inefficiency. Describe them clearly.",
            "Identify any patterns in payment delays, credit periods, or overdue invoices. Estimate how this is affecting our cash flow.",
            "If this data includes inventory or delivery information, tell me where we are over-stocked, under-stocked, or frequently late.",
            "Based on this dataset, forecast the next 3-6 months for the main metrics (revenue, orders, tickets, etc.) and explain the forecast in simple terms.",
            "Compare planned vs actual (if both exist). Where are we consistently under-performing or over-spending?",
            "If you were my COO, what top 5 process improvements would you suggest from this data to save cost or speed up delivery?",
            "Find any repeated errors or recurring issues in the data (for example, repeated refunds, cancellations, failed deliveries) and quantify their impact.",
            "Show 3-5 scenarios: conservative, realistic, and aggressive projections, using trends from this sheet. Explain what must be true for each scenario.",
            "Translate this data into a simple, visual dashboard description: which charts, numbers, and alerts should appear on my CEO dashboard?",
            "Suggest a minimal KPI stack (5-8 metrics) I should review weekly based on this file, and for each KPI give a healthy range and a danger range."
        ]
    }
}

def get_suggested_prompts(dataset):
    """Pick 5 dynamic prompts based on dataset context"""
    try:
        cols = json.loads(dataset.columns_json)
        col_names = " ".join([c['name'].lower() for c in cols])
    except:
        col_names = ""

    score = {'C': 0, 'D': 0, 'E': 0}
    for cat in ['C', 'D', 'E']:
        for kw in PROMPTS[cat].get('keywords', []):
            if kw in col_names:
                score[cat] += 1
    
    # Sort categories by score
    sorted_cats = sorted(score.items(), key=lambda x: x[1], reverse=True)
    
    selected_prompts = []
    
    # 1. Always pick 1 from High-level (A)
    p_a = random.choice(PROMPTS['A']['prompts'])
    selected_prompts.append({'text': p_a, 'icon': PROMPTS['A']['icon'], 'color': PROMPTS['A']['color']})
    
    # 2. Always pick 1 from Risks (B)
    p_b = random.choice(PROMPTS['B']['prompts'])
    selected_prompts.append({'text': p_b, 'icon': PROMPTS['B']['icon'], 'color': PROMPTS['B']['color']})
    
    # 3. Pick 3 more based on relevant categories
    # Top 3 categories from C, D, E
    relevant_cats = [c[0] for c in sorted_cats]
    
    for cat_id in relevant_cats:
        p = random.choice(PROMPTS[cat_id]['prompts'])
        selected_prompts.append({'text': p, 'icon': PROMPTS[cat_id]['icon'], 'color': PROMPTS[cat_id]['color']})
        if len(selected_prompts) >= 5:
            break
            
    return selected_prompts
