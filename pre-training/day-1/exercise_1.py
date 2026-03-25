# Personal profile details
full_name = "Aneeq Duraiz"
current_age = 29
coffee_drinker = False
monthly_pay = 10000000.0

# Display profile summary
coffee_status = "Yes" if coffee_drinker else "No"
print("Name:", full_name)
print("Age:", current_age)
print("Drinks Coffee:", coffee_status)
print(f"Salary: Rs. {monthly_pay}")

# Calculate years left until retirement
retire_at = 60
retirement_gap = retire_at - current_age
print(f"Years to retirement: {retirement_gap}")

# Estimate weekly coffee spending
daily_cups = 3
price_per_cup = 150
week_days = 7
if coffee_drinker:
    weekly_spend = daily_cups * price_per_cup * week_days
else:
    weekly_spend = 0
print(f"Weekly coffee budget: Rs. {weekly_spend}")

