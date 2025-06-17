import time
import pandas as pd
import numpy as np

CITY_DATA = {
    'chicago': 'chicago.csv',
    'new york': 'new_york_city.csv',
    'washington': 'washington.csv'
}

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.
    """
    print('\nHello! Let\'s explore some US bikeshare data!')

    while True:
        city = input('\nWhich city would you like to analyze? (Chicago, New York, or Washington): ').lower()
        if city in CITY_DATA:
            break
        print("Invalid input. Please enter Chicago, New York, or Washington.")

    months = ['all'] + MONTHS
    while True:
        month = input('\nWhich month? (all, January, ..., June): ').lower()
        if month in months:
            break
        print("Invalid input. Please enter a valid month or 'all'.")

    days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input('\nWhich day? (all, Monday, ..., Sunday): ').lower()
        if day in days:
            break
        print("Invalid input. Please enter a valid day or 'all'.")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name().str.lower()
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        month_index = MONTHS.index(month) + 1
        df = df[df['month'] == month_index]

    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    most_common_month = df['month'].mode()[0]
    print(f'Most Common Month: {MONTHS[most_common_month - 1].title()}')

    most_common_day = df['day_of_week'].mode()[0].title()
    print(f'Most Common Day of Week: {most_common_day}')

    most_common_hour = df['hour'].mode()[0]
    print(f'Most Common Start Hour: {most_common_hour}')

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    print(f'Most Common Start Station: {df["Start Station"].mode()[0]}')
    print(f'Most Common End Station: {df["End Station"].mode()[0]}')

    df['Trip'] = df['Start Station'] + ' to ' + df['End Station']
    print(f'Most Common Trip: {df["Trip"].mode()[0]}')

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    total = df['Trip Duration'].sum()
    mean = df['Trip Duration'].mean()

    days = total // 86400
    hours = (total % 86400) // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60
    print(f'Total Travel Time: {int(days)}d {int(hours)}h {int(minutes)}m {int(seconds)}s')

    print(f'Mean Travel Time: {int(mean // 60)} minutes, {int(mean % 60)} seconds')

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    print('\nCounts of User Types:')
    for user_type, count in df['User Type'].value_counts().items():
        print(f'{user_type}: {count}')

    if 'Gender' in df.columns:
        print('\nCounts of Gender:')
        for gender, count in df['Gender'].value_counts().items():
            print(f'{gender}: {count}')
    else:
        print('\nGender data not available.')

    if 'Birth Year' in df.columns:
        print(f'\nEarliest Birth Year: {int(df["Birth Year"].min())}')
        print(f'Most Recent Birth Year: {int(df["Birth Year"].max())}')
        print(f'Most Common Birth Year: {int(df["Birth Year"].mode()[0])}')
    else:
        print('\nBirth year data not available.')

    print(f"\nThis took {time.time() - start_time:.2f} seconds.")
    print('-'*40)


def display_data(df):
    """Displays 5 rows of data at a time based on user input."""
    start_loc = 0
    while True:
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no: ').lower()
        if view_data != 'yes':
            break

        print(df.iloc[start_loc:start_loc + 5].to_string(index=False))
        start_loc += 5


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no: ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
