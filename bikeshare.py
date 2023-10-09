import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("We have information for the following US Cities: Chicago, New York City, Washington. Which city will you like to explore?")
        city = city.lower()
        if city in ['chicago', 'new york city', 'washington']:
            break
        else:
            print('Please enter a valid input! Available cities: Chicago, New York City, Washington')
    # get user input for month (all, january, february, ... , june)
    while True:
        month = input('We have information for the first six months of the year. If you want to see information for a particular month, e.g "January", enter the name of the month else enter "all"')
        month = month.lower()
        if month in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
            break
        else:
            print('Please enter a valid input! Available months: January - June or enter "all" ')
    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Which day (Monday to Sunday) will you like to get input for? Enter "All" for all days')
        day = day.lower()
        if day in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
            break
        else:
            print('Enter a valid day or enter "All" for all days!')
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data for specified city
    df = pd.read_csv(CITY_DATA[city])

    # convert Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    
    # extract month and day of week from Start Time
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()
    
    # filter by month or "all"
    if month != 'all':
        df = df[df['month'] == month.title()]
    # filter by day of week or "all"
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    highest_month = df['month'].mode()[0]
    print('Most commmon month: ', highest_month)

    # display the most common day of week
    highest_dow = df['day_of_week'].mode()[0]
    print('Most common day of the week: ', highest_dow)

    # Extracts hour from Start Time and displays the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    highest_hour = df['hour'].mode()[0]
    print('Most common hour: ', highest_hour)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    highest_start_station = df['Start Station'].mode()[0]
    print('Most commonly used start station: ', highest_start_station)

    # display most commonly used end station
    highest_end_station = df['End Station'].mode()[0]
    print('Most commonly used end station: ', highest_end_station)

    # display most frequent combination of start station and end station trip
    df['combo'] = df['Start Station'] + ' to ' + df['End Station']
    highest_combo = df['combo'].mode()[0]
    print('Most frequent combination of start station and end station trip: ', highest_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: ', total_travel_time, "minutes")

    # display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print('Average travel time: ', round(average_travel_time, 1), "minutes")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print("User Info: ", user_types)
    
    if city != 'washington':
        # Display counts of gender
        gender = df['Gender'].value_counts()
        print("Gender info: ", gender)

        # Display earliest, most recent, and most common year of birth
        earliest_yob = int(df['Birth Year'].min())
        print('Earliest year of birth: ', earliest_yob)

        most_recent_yob = int(df['Birth Year'].max())
        print('Most recent year of birth', most_recent_yob)

        mode_yob = int(df['Birth Year'].mode()[0])
        print('Most common year of birth: ', mode_yob)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw_data(df):
    """Displays the next five rows of data"""
    x = 0
    while True:
        user_input = y_or_n('Will you like to see individual user data? Enter yes or no')
        if user_input == 'yes':
            print(df[x:x+5])
            x += 5
        else:
            break
            
def y_or_n(query):
    """Input validation for yes/no"""
    while True:
        answer = input(query).lower()
        if answer not in ['yes', 'no']:
            print('Enter a valid input!')
        else:
            break
    return answer
        
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        view_raw_data(df)
        
        restart = y_or_n('Would you like to restart? Enter yes or no')
        if restart != 'yes':
            break
            

            

if __name__ == "__main__":
	main()
