# Import necessary libraries
from flask import Flask, request, jsonify, render_template  # Flask web framework tools
import joblib  # For loading saved machine learning models
import pandas as pd  # For data manipulation

# Create a Flask application instance
app = Flask(__name__)

# Load machine learning models and data
model = joblib.load('recommendation_model.pkl')  # Load content-based recommendation model
vectorizer = joblib.load('vectorizer.pkl')  # Load text vectorizer for processing queries
svd_model = joblib.load("svd_model_amazon.pkl")  # Load collaborative filtering model (SVD)

# Load product data from CSV file
df = pd.read_csv("amazon.csv")  # Read the main dataset
products_df = df[['product_id', 'product_name']]  # Keep only product ID and name columns
products_df.drop_duplicates(inplace=True)  # Remove duplicate products

# Define route for the home page
@app.route('/')
def home():
    return render_template('index.html')  # Show the index.html template when someone visits the root URL

# Define route to get trending products
@app.route('/trending', methods=['GET'])
def trending():
    # Get top 12 products with most ratings
    top_products = df.sort_values(by='rating_count', ascending=False).head(12)

    # Prepare the trending products list
    trending_list = []
    for _, product in top_products.iterrows():  # Loop through each top product
        trending_list.append({
            'product_name': product['product_name'],  # Product name
            'img_link': product['img_link'],  # Image URL
            'product_link': product['product_link'],  # Product page URL
            'rating': product.get('rating', 'N/A'),  # Product rating or 'N/A' if missing
            'actual_price': product.get('actual_price', 'N/A'),  # Original price
            'discounted_price': product.get('discounted_price', 'N/A'),  # Discounted price
            'about_product': product.get('about_product', 'No description available.')  # Product description
        })

    return jsonify(trending_list)  # Return the list as JSON

# Define route to get product recommendations
@app.route('/recommend', methods=['POST'])
def recommend():
    query = request.form.get('query')  # Get search query from form data
    if not query:  # If no query was provided
        return jsonify([])  # Return empty list

    # Convert the query to numerical vector
    query_vec = vectorizer.transform([query])
    # Find similar products using the model
    distances, indices = model.kneighbors(query_vec, n_neighbors=5)

    # Set minimum similarity threshold (products more similar than this will be recommended)
    threshold = 0.7  # Can adjust this number - lower means more strict matching

    # Prepare recommendations list
    recommended = []
    for dist, idx in zip(distances[0], indices[0]):  # Check each recommended product
        if dist < threshold:  # Only include if similarity is above threshold
            row = df.iloc[idx]  # Get product details
            recommended.append({
                'product_name': row['product_name'],
                'img_link': row['img_link'],
                'product_link': row['product_link'],
                'rating': row.get('rating', 'N/A'),
                'actual_price': row.get('actual_price', 'N/A'),
                'discounted_price': row.get('discounted_price', 'N/A'),
                'about_product': row.get('about_product', 'No description available.')
            })

    return jsonify(recommended)  # Return recommendations as JSON

# Run the application if this script is executed directly
if __name__ == '__main__':
    app.run(debug=True)  # Start the Flask development server with debug mode on