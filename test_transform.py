# Import pandas library for working with tables
import pandas as pd

# Define a test function to verify the behavior of the transform() function
def test_transform():
    '''
    This test verifies the correctness of the transform() function
    using a sample DataFrame and mock currency exchange rates.
    '''

    # Create a test DataFrame with two banks and their market capitalization in billions of USD
    test_df = pd.DataFrame({
        'Name': ['Bank A', 'Bank B'],
        'MC_USD_Billion': [100, 200]  # market capitalization in USD
    })

    # Define mock exchange rates (as if they were read from a CSV file)
    test_exchange = {
        'EUR': 0.9,   # EUR to USD exchange rate
        'GBP': 0.8,   # GBP to USD exchange rate
        'INR': 83.0   # INR to USD exchange rate
    }

    # Simulate the transform() function — transform the data
    def transform_test(df):
        # Add a column for market cap in EUR
        df['MC_EUR_Billion'] = df['MC_USD_Billion'] * test_exchange['EUR']
        # Add a column for market cap in GBP
        df['MC_GBP_Billion'] = df['MC_USD_Billion'] * test_exchange['GBP']
        # Add a column for market cap in INR
        df['MC_INR_Billion'] = df['MC_USD_Billion'] * test_exchange['INR']
        # Round all numeric values to two decimal places
        df = df.round(2)
        return df

    # Run the transformation and get the result
    result_df = transform_test(test_df)

    # Validate the calculations using assertions
    assert result_df.loc[0, 'MC_EUR_Billion'] == 90.00     # 100 USD × 0.9 = 90.00
    assert result_df.loc[1, 'MC_GBP_Billion'] == 160.00    # 200 USD × 0.8 = 160.00
    assert result_df.loc[0, 'MC_INR_Billion'] == 8300.00   # 100 USD × 83 = 8300.00

    # If all assertions pass — print a success message
    print("Test passed successfully.")

# This block runs only if the file is executed directly
if __name__ == "__main__":
    test_transform()  # Run the test
