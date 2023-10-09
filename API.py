from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load the Excel sheets into dataframes
item_df = pd.read_excel('SampleData.xlsx', sheet_name='ItemInven')
discount_df = pd.read_excel('SampleData.xlsx', sheet_name='Discount')

# Function to calculate the discount price
def calculate_discount(item_price, discount_percentage):
    discount_price = item_price * (1 - discount_percentage)
    return round(discount_price, 2)

# API endpoint to get all items with discount prices
@app.route('/get_discounted_items', methods=['GET'])
def get_discounted_items():
    items = []

    for index, row in item_df.iterrows():
        item_id = row['ItemID']
        item_name = row['ItemName']
        item_price = row['ItemPrice(RM)']
        discount_code = row['DiscountCode']

        # Find the discount percentage for the given code
        discount_percentage = discount_df.loc[discount_df['DiscountCode'] == discount_code, 'Discount%'].values[0]

        # Calculate the discount price
        discount_price = calculate_discount(item_price, discount_percentage)

        item = {
            'ItemID': item_id,
            'ItemName': item_name,
            'ItemPrice': item_price,
            'DiscountCode': discount_code,
            'DiscountPrice': discount_price
        }
        items.append(item)

    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True)






