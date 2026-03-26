from main import analyze_startup

def collect_inputs():
    name = input("Startup name: ")
    sector = input("Sector: ")
    revenue = input("Monthly revenue (₹): ")
    users = input("Users: ")
    ask = input("Investment ask (₹): ")
    equity = input("Equity (%): ")

    print("\nDescribe your startup (what you do, story, problem, etc):")
    description = input("> ")

    return {
        "name": name,
        "sector": sector,
        "revenue": revenue,
        "users": users,
        "ask": ask,
        "equity": equity,
        "description": description
    }

def build_pitch(data):
    pitch = f"""
Startup: {data['name']}
Sector: {data['sector']}

Description:
{data['description']}

Metrics:
- Revenue: ₹{data['revenue']}
- Users: {data['users']}

Funding:
- Asking ₹{data['ask']} for {data['equity']}% equity
"""
    return pitch


# Step 1: collect user input
data = collect_inputs()

# Step 2: build pitch from input
pitch = build_pitch(data)

# Step 3: call AI
result = analyze_startup(pitch)

# Step 4: print result
print("\n--- TEST OUTPUT ---\n")
print(result)