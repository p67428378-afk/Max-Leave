from datetime import date

def get_public_holidays(start_date: date, end_date: date) -> list[date]:
    """
    Returns a list of hardcoded public holidays within a given date range.
    In a real-world application, this would fetch data from a database or an external API.
    """
    # Example public holidays (replace with actual company holidays)
    all_holidays = [
        date(2023, 1, 1),   # New Year's Day
        date(2023, 1, 16),  # Martin Luther King, Jr. Day
        date(2023, 2, 20),  # Presidents' Day
        date(2023, 5, 29),  # Memorial Day
        date(2023, 6, 19),  # Juneteenth
        date(2023, 7, 4),   # Independence Day
        date(2023, 9, 4),   # Labor Day
        date(2023, 10, 9),  # Columbus Day
        date(2023, 11, 10), # Veterans Day (observed)
        date(2023, 11, 23), # Thanksgiving Day
        date(2023, 11, 24), # Day after Thanksgiving
        date(2023, 12, 25), # Christmas Day
        date(2024, 1, 1),   # New Year's Day 2024
        date(2024, 1, 15),  # Martin Luther King, Jr. Day 2024
        date(2024, 2, 19),  # Presidents' Day 2024
        date(2024, 3, 29),  # Good Friday 2024
        date(2024, 5, 27),  # Memorial Day 2024
        date(2024, 6, 19),  # Juneteenth 2024
        date(2024, 7, 4),   # Independence Day 2024
        date(2024, 9, 2),   # Labor Day 2024
        date(2024, 10, 14), # Columbus Day 2024
        date(2024, 11, 11), # Veterans Day 2024
        date(2024, 11, 28), # Thanksgiving Day 2024
        date(2024, 11, 29), # Day after Thanksgiving 2024
        date(2024, 12, 25), # Christmas Day 2024
    ]

    # Filter holidays that fall within the requested date range
    return [holiday for holiday in all_holidays if start_date <= holiday <= end_date]

if __name__ == '__main__':
    # Example usage
    start = date(2023, 10, 1)
    end = date(2023, 11, 30)
    holidays_in_range = get_public_holidays(start, end)
    print(f"Public holidays between {start} and {end}:")
    for holiday in holidays_in_range:
        print(holiday)
