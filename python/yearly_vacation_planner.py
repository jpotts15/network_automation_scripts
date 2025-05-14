import datetime
from datetime import datetime, timedelta

# Target working hours per year
target_hours_min = 1864
target_hours_max = 1920


# Federal US holidays per OPM https://www.opm.gov/policy-data-oversight/pay-leave/federal-holidays/#url=2025
us_holidays = {
    "Independence Day": "2025-07-04",
    "Labor Day": "2025-09-01",
    "Columbus Day":"2025-10-13",
    "Veterans Day":"2025-11-11",
    "Thanksgiving": "2025-11-27",
    "Christmas Day": "2025-12-25",
    "New Year's Day": "2026-01-01",
    "Martin Luther King Jr. Day": "2026-01-19",
    "Presidents' Day": "2026-02-16",
    "Memorial Day": "2026-05-25",
}

# Function to generate fixed bi-monthly pay periods
def generate_fixed_pay_periods(start_date, end_date):
    pay_periods = []
    current_date = start_date
    
    while current_date < end_date:
        if current_date.day == 1:
            period_end = current_date + timedelta(days=14)
        else:  # it's the 16th
            next_month = (current_date.month % 12) + 1
            next_year = current_date.year + (1 if next_month == 1 else 0)
            period_end = datetime(next_year, next_month, 1) - timedelta(days=1)
        
        pay_periods.append((current_date.strftime("%Y-%m-%d"), period_end.strftime("%Y-%m-%d")))
        current_date = period_end + timedelta(days=1)
    
    return pay_periods

# Function to calculate working hours for a given period
def calculate_working_hours(start_date, end_date, overtime_hours):
    current_date = start_date
    working_hours = 0
    
    while current_date <= end_date:
        if current_date.weekday() < 5:  # Monday to Friday
            working_hours += 8  # Assuming an 8-hour workday
        current_date += timedelta(days=1)
    
    working_hours += overtime_hours
    return working_hours

def calculate_working_days(start_date, end_date):
    """Calculate the number of working days between two dates, excluding holidays."""
    start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
    total_days = (end - start).days + 1
    working_days = 0

    for day in range(total_days):
        current_day = start + timedelta(days=day)
        if current_day.weekday() < 5:
            working_days += 1

    return working_days

def calculate_vacation_hours(pay_periods, holidays, target_min, target_max):
    """Calculate available vacation hours while meeting target working hours."""
    total_working_days = 0

    for period in pay_periods:
        start_date, end_date = period
        total_working_days += calculate_working_days(start_date, end_date, holidays)

    total_working_hours = total_working_days * 8

    vacation_hours_min = max(0, total_working_hours - target_max)
    vacation_hours_max = max(0, total_working_hours - target_min)

    return vacation_hours_min, vacation_hours_max

def main():

    vacation_hours_min, vacation_hours_max = calculate_vacation_hours(pay_periods, us_holidays, target_hours_min, target_hours_max)

    print(f"Target Working Hours: {target_hours_min}-{target_hours_max} hours")
    print(f"Available Vacation Hours: {vacation_hours_min}-{vacation_hours_max} hours")
    print("\nMajor US Holidays:")
    for holiday, date in us_holidays.items():
        print(f"  {holiday}: {date}")

#if __name__ == "__main__":
#    main()

# Define start and end dates for pay periods
start_date = datetime.strptime("2025-06-01", "%Y-%m-%d")
end_date = datetime.strptime("2026-06-01", "%Y-%m-%d")

# Generate pay periods
pay_periods = generate_fixed_pay_periods(start_date, end_date)

# Calculate working hours for each period and print
totaler = 0
csver = ""
# Iterate over pay periods
for period in pay_periods:
    start_date = datetime.strptime(period[0], "%Y-%m-%d")
    end_date = datetime.strptime(period[1], "%Y-%m-%d")
    overtime_hours = 0  # Example input for overtime hours
    total_hours = calculate_working_hours(start_date, end_date, overtime_hours)
    totaler += total_hours
    print(f"Pay Period: {period[0]} to {period[1]}, Total Hours: {total_hours}")
    
    # Check if any holiday falls within this pay period
    holidays_in_period = []
    for holiday, holiday_date in us_holidays.items():
        holiday_datetime = datetime.strptime(holiday_date, "%Y-%m-%d")
        if start_date <= holiday_datetime <= end_date:
            holiday_day_of_week = holiday_datetime.strftime("%A")  # Get the day of the week
            holidays_in_period.append(f"{holiday}: {holiday_date} ({holiday_day_of_week})")
    csver += f"{period[0]},{period[1]},{total_hours}"
    # Print the holidays that occurred in this period
    if holidays_in_period:
        print(f"  Holidays in this period: {', '.join(holidays_in_period)}")
        csver += f",{holidays_in_period}"
    csver += "\n"
print(f'total hours: {totaler}')

with open('tmp.csv','w') as csv_out:
    csv_out.write(csver)