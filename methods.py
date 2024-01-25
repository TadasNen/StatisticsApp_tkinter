from geopy.distance import geodesic
import requests
import json





def remove_columns(df):
    """
    Removes specified columns from a DataFrame and returns the updated DataFrame.

    Parameters:
    - df (pd.DataFrame): The DataFrame from which columns should be removed.

    Returns:
    - pd.DataFrame: The updated DataFrame.
    """
    columns_to_remove = ['Unnamed: 0', 'street', 'city', 'state', 'zip', 'city_pop', 'unix_time', 'trans_num']
    try:
        updated_df = df.drop(columns=columns_to_remove, errors='ignore')
        return updated_df
    except Exception as e:
        raise e


def update_column_names(df):
    """
    Update sepcific column names of a DataFrame that user uploaded. Works only with base design that was used to
    write a code and resembles financial institution extracted files.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - pd.DataFrame: The DataFrame with updated column names.
    """

    # Variable with all column names and their new name counterparts
    column_names = {'trans_date_trans_time': 'Date and Time', 'cc_num': 'Card Number', 'merchant': 'Store',
                    'category': 'Store Industry', 'amt': 'Amount, EUR', 'first': 'First name', 'last': 'Last name',
                    'gender': 'Gender', 'street': 'Address', 'city': 'City', 'zip': 'ZIP code',
                    'lat': 'Latitude Person',
                    'long': 'Longitude Preson', 'city_pop': 'City population', 'job': 'Job', 'dob': 'Date of Birth',
                    'trans_num': 'Transaction ID', 'unix_time': 'Unix time', 'merch_lat': 'Latitude Store',
                    'merch_long': 'Longitude Store', 'is_fraud': 'Fraud'}
    # Updates existing columns, if there aren't matching names, it will skip
    updated_df = df.rename(columns=column_names)
    return updated_df


def distance(df):
    """
    Calculate the distance between persons and merchants using their coordinates provided in original dataset.

    Parameters:
    - df (pd.DataFrame): DataFrame containing columns 'lat', 'long', 'merch_lat', 'merch_long'.

    Returns:
    - updated_df (pd.DataFrame): DataFrame with added 'Distance' column and removed coordinate columns.
    """
    # Extract coordinates from DataFrame
    person_coords = list(zip(df['lat'], df['long']))
    merchant_coords = list(zip(df['merch_lat'], df['merch_long']))
    # Calculate distances
    distances = [geodesic(person, merchant).kilometers for person, merchant in zip(person_coords, merchant_coords)]
    # Add 'Distance' column to DataFrame
    df.insert(10, 'Distance, km', distances)
    # Delete coordinate columns
    updated_df = df.drop(['lat', 'long', 'merch_lat', 'merch_long'], axis=1)
    return updated_df


def process_values(df):
    """
    Process merchant names in the DataFrame by amending values in the 'merchant' column to not contain 'fraud_' part,
    creating a new 'Name' column consisting of values from 'first' and 'last' columns and dropping them.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - updated_df (pd.DataFrame): The DataFrame with the specified modifications.
    """
    # Amend values in the 'merchant' column
    df['merchant'] = df['merchant'].apply(lambda x: x.replace('fraud_', '') if x.startswith('fraud_') else x)
    # Create a new 'Name' column by joining 'first' and 'last' with space
    df.insert(4, 'Name', df['first'] + ' ' + df['last'])
    # Drop 'first' and 'last' columns
    updated_df = df.drop(['first', 'last'], axis=1)
    return updated_df


def split_datetime(df):
    """
    Split the 'trans_date_trans_time' column into separate 'Date' and 'Time' columns,
    and drop the original column.

    Parameters:
    - df (pd.DataFrame): The input DataFrame.

    Returns:
    - updated_df (pd.DataFrame): The DataFrame with the specified modifications.
    """
    try:
        # Check if 'trans_date_trans_time' column exists in the DataFrame
        if 'trans_date_trans_time' in df.columns:
            # Split 'trans_date_trans_time' into 'Date' and 'Time'
            split_values = df['trans_date_trans_time'].str.split(' ', expand=True)

            # Assign 'Date' and 'Time' columns separately
            df.insert(0, 'Date', split_values[0])
            df.insert(1, 'Time', split_values[1])

            # Drop the original 'trans_date_trans_time' column
            updated_df = df.drop(['trans_date_trans_time'], axis=1)

            return updated_df
        else:
            raise ValueError("'trans_date_trans_time' column not found in the DataFrame.")
    except Exception as e:
        raise e


def card_type_generate(cc_num):
    """
    Determines the card type based on the card number stored in dataframe uploaded by user.

    Parameters:
    - cc_num (str): Credit card number.

    Returns:
    - str: Card type ('Visa', 'Mastercard', 'AMEX', 'Discover', 'N/A').
    """
    try:
        if len(cc_num) >= 13 and len(cc_num) <= 16 and int(cc_num[0]) == 4:
            return 'Visa'
        elif len(cc_num) == 16 and int(cc_num[0]) == 5:
            return 'Mastercard'
        elif len(cc_num) == 15 and (int(cc_num[0:2]) == 34 or int(cc_num[0:2])) == 37:
            return 'AMEX'
        elif len(cc_num) == 16 and int(cc_num[0]) == 6:
            return 'Discover'
        else:
            return 'N/A'
    except Exception as e:
        raise e


def card_issuer_industry(cc_num):
    """
    Determines the card issuer industry based on the first digit of the card number sdored in dataframe.

    Parameters:
    - cc_num (str): Credit card number.

    Returns:
    - str: Card issuer industry.
    """
    try:
        if int(cc_num[0]) == 0:
            return 'ISO/TC 68 nec'
        elif int(cc_num[0]) == 1:
            return 'Airlines'
        elif int(cc_num[0]) == 2:
            return 'Airlines, financial, nec'
        elif int(cc_num[0]) == 3:
            return 'Travel and entertainment'
        elif int(cc_num[0]) == 4:
            return 'Banking and financial'
        elif int(cc_num[0]) == 5:
            return 'Banking and financial'
        elif int(cc_num[0]) == 6:
            return 'Merchandising and banking/financial'
        elif int(cc_num[0]) == 7:
            return 'Petroleum, nec'
        elif int(cc_num[0]) == 8:
            return 'Healthcare, telecommunications, nec'
        elif int(cc_num[0]) == 9:
            return 'Government issued'
        else:
            return 'Invalid number'

    except Exception as e:
        raise e


def card_type_assign(df):
    """
    Assigns card type and card issuer industry to a DataFrame based on the 'cc_num' column.

    Parameters:
    - df (pd.DataFrame): Input DataFrame containing a 'cc_num' column.

    Returns:
    - pd.DataFrame: Updated DataFrame with 'Type' and 'Card Industry' columns.
    """
    cache = {}
    try:
        # Create new columns with empty values
        df.insert(3, 'Type', '')
        df.insert(4, 'Card Industry', '')

        for index, row in df.iterrows():
            cc_num = row['cc_num']

            # Check if the result for the current cc_num is in the cache
            if cc_num in cache:
                cc_type, card_industry = cache[cc_num]
            else:
                # Otherwise, calculate the card type and card industry
                cc_type = card_type_generate(cc_num)
                card_industry = card_issuer_industry(cc_num)
                cache[cc_num] = (cc_type, card_industry)

            # Update the 'Type' and 'Card Industry' columns in the DataFrame
            df.at[index, 'Type'] = cc_type
            df.at[index, 'Card Industry'] = card_industry

    except Exception as e:
        raise e

    finally:
        # Clear the cache before returning
        cache.clear()

    return df





# def update_cc_info(df):
#     api_url = "https://api.freebinchecker.com/bin/{bin}"
#
#     try:
#         df.insert(3, 'Scheme', '')
#         df.insert(4, 'Type', '')
#         df.insert(5, 'Issuer', '')
#         df.insert(6, 'Country', '')
#         df.insert(7, 'Currency', '')
#
#         cache = {}
#
#         unique_bins = df['cc_num'].astype(str).str[:6].unique()
#
#         for bin_number in unique_bins:
#             if bin_number in cache:
#                 bin_info = cache[bin_number]
#             else:
#                 bin_url = api_url.format(bin=bin_number)
#                 response = requests.get(bin_url)
#
#                 if response.status_code == 200:
#                     try:
#                         bin_info = response.json()
#                         cache[bin_number] = bin_info
#                     except json.JSONDecodeError:
#                         bin_info = {}
#                 else:
#                     bin_info = {}

#             rows_to_update = df['cc_num'].astype(str).str.startswith(bin_number)

#             df.loc[rows_to_update, 'Scheme'] = bin_info.get('card', {}).get('scheme', '')
#             df.loc[rows_to_update, 'Type'] = bin_info.get('card', {}).get('type', '')
#             df.loc[rows_to_update, 'Issuer'] = bin_info.get('issuer', {}).get('name', '')
#             df.loc[rows_to_update, 'Country'] = bin_info.get('country', {}).get('name', '')
#             df.loc[rows_to_update, 'Currency'] = bin_info.get('country', {}).get('currency', '')
#
#         return df
#     except Exception as e:
#         raise e
#     finally:
#         del cache
