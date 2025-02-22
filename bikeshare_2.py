import time
import datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze. If an invalid month and/or day are entered, the value(s) are defaulted to 'all'.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Enter the city you are interested in viewing bike share data for. You can review data for Chicago, Washington, or New York City: ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("Enter which month of data you would like to analyze. The options are: All or any month from January through June: ").lower()
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        #month = months.index(month) + 1
        if month not in months:
            print("\n***Incorrect value entered for the month ({}). No month filter applied to subsequent analysis.***\n".format(month.title()))
            month = 'all'

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Enter which day of the week to perform the analysis on. The options are: All or a specific day from Monday through Sunday: ").lower()
    if day != 'all':
        # filter by day of week to create the new dataframe
        days = ['sunday','monday','tuesday','wednesday','thursday','friday','saturday']
        if day not in days:
            print("\n***Incorrect value entered for the day ({}). No day of the week filter applied to subsequent analysis.***\n".format(day.title()))
            day = 'all'


    print('-'*40)
    return city, month, day


def filter_data(df, month, day):
    """
    Apply filters by month and day if applicable.

    Args:
        df - dataframe containing the selected city data
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        dff - Pandas DataFrame containing city data filtered by month and day
    """
    # convert the Start Time column to datetime
    dff = df
    dff['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns to use for filtering
    dff['month'] = dff['Start Time'].dt.month_name()
    dff['day_of_week'] = dff['Start Time'].dt.strftime('%A')

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        dff = dff[dff['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        dff = dff[dff['day_of_week'] == day.title()]

    return dff


def time_stats(df,dff,city,month,day):
    """Displays statistics on the most frequent times of travel. Data is not filtered to user filter inputs

    Args:
        df - dataframe containing the selected city data, unfiltered
        dff - dataframe containing the selected city data, filtered by month and day (if user entered a specific month and day)
        (str) city - name of the city for the data loaded
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('\nCalculating The Most Frequent Times of Travel in {}...\n'.format(city.title()))
    start_time = time.time()

    # Calculate counts of users by month on unfiltered dataset
    user_month_count = df['month'].value_counts()
    # Setup the bar graph to display the user counts by month
    user_month_count.plot(kind='bar')
    plt.xlabel('Month')
    plt.ylabel('Count')
    plt.title('Count of Users by Month')
    plt.show()

    # test if filtered by month before calculating the most common month
    if dff['month'].nunique() > 1:
        # display the most common month
        common_month = df['month'].mode()[0]
        print('\nThe most common month for bike travel is...\n {}'.format(common_month.title()))
    else:
        common_month = month

    # test if filtered by day of the week before calculating the most common day of the week
    if dff['day_of_week'].nunique() > 1:
        # display the most common day of week
        common_day = df['day_of_week'].mode()[0]
        print('\nThe most common day of the week in {} for bike travel is...\n {}'.format(common_month.title(), common_day.title()))
    else:
        common_day = day

    # extract hour from the Start Time column to create an hour column
    dff['hour'] = dff['Start Time'].dt.strftime('%I:00 %p')
    # find the most common hour
    common_hour = dff['hour'].mode()[0]
    # display the most common hour of the day
    print('\nThe most common hour of the day on a {} in {} for bike travel is...\n {}'.format(common_day.title(), common_month.title(), common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(dff,city,month,day):
    """Displays statistics on the most popular stations and trip.

      Args:
        dff - dataframe containing the selected city data, filtered by month and day (if user entered a specific month and day)
        (str) city - name of the city for the data loaded
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nCalculating The Most Popular Stations and Trip in {} in the month of: {} on day(s): {}...\n'.format(city.title(),month.title(),day.title()))
    start_time = time.time()

    # find the most common start station
    common_start_station = dff['Start Station'].mode()[0]
    # display most commonly used start station
    print('\nThe most common start station for bike travel is...\n {}'.format(common_start_station))

    # find the most common end station
    common_end_station = dff['End Station'].mode()[0]
    # display most commonly used end station
    print('\nThe most common end station in for bike travel is...\n {}'.format(common_end_station))

    # display most frequent combination of start station and end station trip
    common_combo_station = (dff['Start Station'] + ' to ' + dff['End Station']).mode()[0]
    print('\nThe most common combination of start and end stations in a trip for bike travel is...\n {}'.format(common_combo_station))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(dff,city,month,day):
    """Displays statistics on the total and average trip duration.

      Args:
        dff - dataframe containing the selected city data, filtered by month and day (if user entered a specific month and day)
        (str) city - name of the city for the data loaded
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    if month != 'all':
        print('\nCalculating Trip Duration in {} in the month of: {} on day(s): {}...\n'.format(city.title(),month.title(),day.title()))
        start_time = time.time()

        # calculate total travel time only if data has been filtered by month and day
        total_travel_time = dff['Trip Duration'].sum()
        total_days = int(total_travel_time/1440)
        total_hours = int((total_travel_time - (total_days * 1440))/60)
        total_mins = int(total_travel_time - (total_days * 1440) - (total_hours * 60))
    
        # display total travel time
        print('\nThe total travel time for bike travel for this day is...\n {} days, {} hours, and {} minutes'.format(total_days,total_hours,total_mins))

        if day != 'all':
            # find the average travel time
            avg_travel_time = dff['Trip Duration'].mean()
            avg_days = int(avg_travel_time/1440)
            avg_hours = int((avg_travel_time- (avg_days * 1440))/60)
            avg_mins = int(avg_travel_time - (avg_days * 1440) - (avg_hours * 60))
            # display mean travel time
            print('\nThe average travel time for bike travel is...\n {} days, {} hours, and {} minutes'.format(avg_days,avg_hours,avg_mins))
        else:
            print('\nThe average trip duration statistics need to be performed on a specific month and day.\n')

        print("\nThis took %s seconds." % (time.time() - start_time))

    else:
        print('\nTo review trip duration statistics a specific month must be selected.\n')
    
    print('-'*40)


def user_stats(dff,city,month,day):
    """Displays statistics on bikeshare users. Gender stats only applicable to Chicago and New York City.
      Args:
        dff - dataframe containing the selected city data, filtered by month and day (if user entered a specific month and day)
        (str) city - name of the city for the data loaded
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    print('\nCalculating User Stats in {} in the month of: {} on day: {}...\n'.format(city.title(),month.title(),day.title()))
    start_time = time.time()
    today = datetime.date.today()

    # Calculate counts of user types
    user_type_count = dff['User Type'].value_counts()
    # Setup the bar graph to display the user types
    user_type_count.plot(kind='bar')
    plt.xlabel('User Type')
    plt.ylabel('Count')
    plt.title('Count of User Types')
    plt.show()

    # Display counts of user types
    print('\nThe summary count for each User Type is...\n {}\n'.format(user_type_count))

    # Calculate and display counts of gender if city is not Washington
    if city != 'washington':
        gender_count = dff['Gender'].fillna('Unknown').value_counts()
        
        # Setup the bar graph to display the user types
        gender_count.plot(kind='bar')
        plt.xlabel('Gender')
        plt.ylabel('Count')
        plt.title('Count of Users by Gender')
        plt.show()       

        print('\nThe summary count for gender of each user is...\n {}\n'.format(gender_count))

        # Calculate and display earliest, most recent, and most common year of birth
        earliest_birth = int(dff['Birth Year'].min())
        oldest_age = int(today.strftime("%Y"))-earliest_birth
        print('\nThe oldest user on this day is {} years old and was born in {}.\n'.format(oldest_age, earliest_birth))

        latest_birth = int(dff['Birth Year'].max())
        youngest_age = int(today.strftime("%Y"))-latest_birth
        print('\nThe youngest user on this day is {} years old and was born in {}.\n'.format(youngest_age,latest_birth))
        
        common_birth_year = int(dff['Birth Year'].mode()[0])
        common_age = int(today.strftime("%Y"))-common_birth_year
        print('\nThe most common age of users on this day is {} and born in {}.\n'.format(common_age,common_birth_year))

        birth_year_cnt = dff['Birth Year'].value_counts()
        print('\nThe number of {} year old users for this day is: {}\n'.format(common_age,birth_year_cnt[common_birth_year]))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def view_raw_data(df, city):
    """Displays raw bikeshare data for the selected city.
    Args:
    df - dataframe containing the selected city data, raw data, unfiltered)
    (str) city - name of the city for the data loaded
    """   
    print('\nReviewing raw bikeshare data for {}.\n'.format(city.title()))
    nextrows = input('\nWould you like to see the first 5 rows of raw data? Enter yes or no.\n')

    while nextrows.lower() != 'yes' and nextrows.lower() != 'no':
        print("\n{} is invalid input. Expected response is yes or no.".format(nextrows))
        nextrows = input('\nWould you like to see the first 5 rows of raw data? Enter yes or no.\n')   

    i = 0
    rows = len(df.index)
    while nextrows.lower() == 'yes' and i < rows-1:
        print(df.loc[i:i+4,:])
        i += 5
        nextrows = input('\nWould you like to see the next 5 rows of raw data? Enter yes or no.\n')
        if nextrows.lower() != 'yes':
            break

def main():
    while True:
        city, month, day = get_filters()
        try:
            # load data file into a dataframe based on the city the user entered
            df = pd.read_csv(CITY_DATA[city])
            # apply filters to the dataframe
            dff = filter_data(df,month,day)
            # run time stats to the filtered data
            time_stats(df,dff,city,month,day)
            # run station stats to the filtered data
            station_stats(dff,city,month,day)
            # run trip duration stats to the filtered data
            trip_duration_stats(dff,city,month,day)
            # run user stats to the filtered data
            user_stats(dff,city,month,day)
            view_raw_data(df,city)
  
        except KeyError:
            print("{} is not a valid city. The city must be Chicago, Washington, or New York City.".format(city.title()))
        except FileNotFoundError:
            print("File '{}', for selected city: {}, is not found in the current directory.".format(CITY_DATA[city],city.title()))
        finally:
            restart = input('\nWould you like to restart? Enter yes or no.\n')
            if restart.lower() == 'no':
                break
            elif restart.lower() != 'no' and restart.lower() != 'yes':
                print("\n{} is invalid input. Next time enter yes or no.\n".format(restart))
                break
            else:
                print("Restarting..........")

if __name__ == "__main__":
	main()
