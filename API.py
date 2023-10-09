from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

# Load data from the Excel file into dataframes
item_df = pd.read_excel('data.xlsx', sheet_name='ItemInven')
discount_df = pd.read_excel('data.xlsx', sheet_name='Discount')

# Merge data based on DiscountCode
merged_df = item_df.merge(discount_df, on='DiscountCode')

@app.route('/api/items', methods=['GET'])
def get_items():
    items = []

    for _, row in merged_df.iterrows():
        item = {
            'ItemID': int(row['ItemID']),
            'ItemName': row['ItemName'],
            'ItemPrice(RM)': float(row['ItemPrice(RM)']),
            'DiscountCode': row['DiscountCode'],
            'Discount%': row['Discount%']
        }

        # Calculate the DiscountPrice
        item_price = item['ItemPrice(RM)']
        discount_percentage = float(item['Discount%'][:-1]) / 100
        discount_price = item_price * discount_percentage

        item['DiscountPrice'] = discount_price

        items.append(item)

    return jsonify(items)

if __name__ == '__main__':
    app.run(debug=True)
