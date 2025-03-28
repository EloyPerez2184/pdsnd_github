import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['all', 'january', 'february', 'march', 'april', 'may', 'june']
days = ['all', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while(True):
        city = input('Please type one of the following city (Chicago, New York City or Washington) names to access that city\'s data:\n').lower()
        try: 
            CITY_DATA[city]
        except:
            print("Please enter a city from the list...\n\n")
        else:
            break
            
    # TO DO: get user input for month (all, january, february, ... , june)
    while(True):
        month = input('Please type month (all, january, february, ... , june) to see that city\'s corresponding data:\n').lower()
        if month in months: 
            break
        else:
            print("Please enter a correct month or 'all'.\n\n")
    

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while(True):
        day = input('Please type day (all, monday, tuesday, ... , sunday) to see that city\'s month corresponding data:\n').lower()
        if day in days:
            break
        else:
            print("Please enter a correct day or 'all'. \n\n")
    
    print('-'*50)
    return (city, month, day)


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
    df = pd.read_csv(CITY_DATA[city])
    
    #Change to DateTime for manipulation
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    #Columns addded for fitlering day and months 
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = months.index(month)
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]
        
    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Args:
        (dataframe) df - the chosen filtered data from intial input. 
    """
    
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month:', months[popular_month].title())

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('Most Popular Start Day:', popular_day.title())

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def station_stats(df):
    """Displays statistics on the most popular stations and trip.
    Args:
        (dataframe) df - the chosen filtered data from intial input. 
    """

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('Most Popular Start Station:', popular_start_station.title())

    
    # TO DO: display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('Most Popular End Station:', popular_end_station.title())

    # TO DO: display most frequent combination of start station and end station trip
    df['combistation'] = df['Start Station']+'/' + df['End Station']
    popular_combistation = df['combistation'].mode()[0]
    print('Most Popular Start/End Station pairing:', popular_combistation)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
       Args:
        (dataframe) df - the chosen filtered data from intial input.     
    """

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()
    
    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    print('Total Travel Time: {} hours {} minutes {} seconds'.format(total_duration//3600, (total_duration//60)%60, total_duration%60))
    
    # TO DO: display mean travel time
    popular_duration = df['Trip Duration'].mode()[0]
    print('Average Travel Time: {} hours {} minutes {} seconds'.format(popular_duration//3600, (popular_duration//60)%60, popular_duration%60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)


def user_stats(df):
    """Displays statistics on bikeshare users.
    Args:
        (dataframe) df - the chosen filtered data from intial input. 
    """

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    #Filters out NA values and switches to Other 
    df['User Type'] = df['User Type'].fillna('Other')
    
    print("User Type Count")
    
    user_count = df['User Type'].value_counts()
    for unique_user in df['User Type'].unique():
        print(unique_user +": "+ str(int(user_count[unique_user])))
    
    # TO DO: Display counts of gender
    #Switched NA values into Undisclosed because not everyone might want to disclose their gender
    print("\nGender Count")
    
    try:
        df['Gender'] = df['Gender'].fillna('Undisclosed') 
        gender_count = df['Gender'].value_counts()
        
        for gender in df['Gender'].unique():
            print(str(gender) +": "+ str(int(gender_count[gender]))) 
     
    #one of the data files had no Gender data column
    except KeyError:
        print("----No Gender Data Available----")
        
    # TO DO: Display earliest, most recent, and most common year of birth
    print("\nBirth Year Stats")
    
    try:
        print("User Base Oldest Birth Year: " + str(int(df['Birth Year'].min())))
        print("User Base Common Birth Year: " + str(int(df['Birth Year'].mode())))
        print("User Base Newest Birth Year: " + str(int(df['Birth Year'].max())))
        
    #One of the data files had no birthyear data column    
    except KeyError:  
        print("----No Birth Year Data Available----")
        
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*50)

def data_show(df):
    """Displays 5 rows worth of data.
    Args:
        (dataframe) df - the chosen filtered data from intial input. 
    """
    #intialized variables for tracking    
    count = 0
    #Dropped columns used for filtering, to make sure we see raw data, display is done at end so those columns are no longder needed
    df = df.drop(['hour', 'month','day_of_week','combistation'], axis = 1) 
    data_preview = input("Output first 5 rows of selected data?\n").lower()
    
    while(data_preview in ['yes', 'ye', 'y']):
       print(df.iloc[(count*5):5*(count+1)])
       count+=1
       data_preview = input("\nOutput the next 5 rows of current data?\n")
          
          
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        data_show(df)
       
        restart = input('\nEnter yes if you would like to restart?\n')
        if restart.lower() not in ['yes' , 'y' , 'ye']:  #Did 2 variations because they were the most common mistakes I made
            break

if __name__ == "__main__":
	main()