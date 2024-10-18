from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive backend for Matplotlib
import matplotlib.pyplot as plt
import yfinance as yf
import io
import base64
import bcrypt
from config import Config
from models import mongo, create_user, find_user

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)  # This will allow cross-origin requests
mongo.init_app(app)  # Initialize MongoDB

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to register a user
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")
        preferred_stock = data.get("preferredStock")

        # Validate request data
        if not username or not password or not preferred_stock:
            return jsonify({"error": "Missing required fields"}), 400

        # Check if the user already exists
        if find_user(username):
            return jsonify({"error": "User already exists"}), 400

        # Create the new user
        user = create_user(username, password, preferred_stock)
        return jsonify({"message": "User registered successfully", "user": user}), 201

    except Exception as e:
        print(f"Error during registration: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Route to log in a user
@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        username = data.get("username")
        password = data.get("password")

        # Validate request data
        if not username or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Find the user in the database
        user = find_user(username)

        # Check if the user exists
        if not user:
            return jsonify({"error": "No user exists with this username. Please register."}), 404

        # Check if the password matches
        if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            return jsonify({"error": "Incorrect password. Please try again."}), 401

        # Successful login
        return jsonify({"message": "Login successful", "username": username}), 200

    except Exception as e:
        print(f"Error during login: {e}")
        return jsonify({"error": "Internal Server Error"}), 500

# Route to get stock data
@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    try:
        ticker = request.json['ticker']  # Get the ticker from the request JSON
        
        # Fetch stock data using yfinance
        stock = yf.Ticker(ticker)

        # Fetch historical data for the last month
        hist = stock.history(period='1mo', interval='1d')

        # Calculate daily price change
        hist['PriceChange'] = hist['Close'].diff()

        # Separate gains and losses
        hist['Gain'] = hist['PriceChange'].apply(lambda x: x if x > 0 else 0)
        hist['Loss'] = hist['PriceChange'].apply(lambda x: -x if x < 0 else 0)

        # Calculate average gain and loss over the past 14 days
        hist['AvgGain'] = hist['Gain'].rolling(window=14).mean()
        hist['AvgLoss'] = hist['Loss'].rolling(window=14).mean()

        # Calculate the RS and RSI
        hist['RS'] = hist['AvgGain'] / hist['AvgLoss']
        hist['RSI'] = 100 - (100 / (1 + hist['RS']))

        # Get stock info
        info = stock.info
        beta = info.get('beta', 0)
        trailing_pe = info.get('trailingPE', 0)
        forward_pe = info.get('forwardPE', 0)
        price_to_book = info.get('priceToBook', 0)

        # Convert to float if needed
        beta = float(beta) if isinstance(beta, (int, float)) else 0
        trailing_pe = float(trailing_pe) if isinstance(trailing_pe, (int, float)) else 0
        forward_pe = float(forward_pe) if isinstance(forward_pe, (int, float)) else 0
        price_to_book = float(price_to_book) if isinstance(price_to_book, (int, float)) else 0

        # Generate plots
        rsi_plot = create_rsi_plot(hist, ticker)
        beta_plot = create_beta_plot(beta)
        pe_plot = create_pe_plot(trailing_pe, forward_pe)
        pb_plot = create_pb_plot(price_to_book)

        # Return the plots as JSON
        return jsonify({
            'rsi_plot': rsi_plot,
            'beta_plot': beta_plot,
            'pe_plot': pe_plot,
            'pb_plot': pb_plot
        })

    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return jsonify({"error": str(e)}), 500

# Function to create RSI plot
def create_rsi_plot(hist, ticker):
    img_rsi = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.plot(hist.index, hist['RSI'], label='RSI', color='purple')
    plt.axhline(70, color='red', linestyle='--', label='Overbought')
    plt.axhline(30, color='green', linestyle='--', label='Oversold')
    plt.title(f'Relative Strength Index (RSI) for {ticker}')
    plt.legend()
    plt.savefig(img_rsi, format='png')
    plt.close()
    img_rsi.seek(0)
    return base64.b64encode(img_rsi.getvalue()).decode()

# Function to create Beta plot
def create_beta_plot(beta):
    img_beta = io.BytesIO()
    plt.figure(figsize=(5, 5))
    plt.bar('Beta', beta, color='blue')
    plt.title('Beta')
    plt.ylim(0, max(beta + 0.5, 2))
    plt.savefig(img_beta, format='png')
    plt.close()
    img_beta.seek(0)
    return base64.b64encode(img_beta.getvalue()).decode()

# Function to create P/E ratios plot
def create_pe_plot(trailing_pe, forward_pe):
    img_pe = io.BytesIO()
    pe_ratios = {'Trailing P/E': trailing_pe, 'Forward P/E': forward_pe}
    plt.figure(figsize=(5, 5))
    plt.bar(pe_ratios.keys(), pe_ratios.values(), color=['orange', 'cyan'])
    plt.title('P/E Ratios')
    plt.ylim(0, max(trailing_pe, forward_pe) + 10)
    plt.savefig(img_pe, format='png')
    plt.close()
    img_pe.seek(0)
    return base64.b64encode(img_pe.getvalue()).decode()

# Function to create P/B ratio plot
def create_pb_plot(price_to_book):
    img_pb = io.BytesIO()
    plt.figure(figsize=(5, 5))
    plt.bar('P/B Ratio', price_to_book, color='green')
    plt.title('Price to Book (P/B) Ratio')
    plt.ylim(0, max(price_to_book + 10, 20))
    plt.savefig(img_pb, format='png')
    plt.close()
    img_pb.seek(0)
    return base64.b64encode(img_pb.getvalue()).decode()

# Function to create a user
def create_user(username, password, preferred_stock):
    try:
        # Hash the password before saving
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user = {"username": username, "password": hashed.decode('utf-8'), "preferred_stock": preferred_stock}
        mongo.db.users.insert_one(user)
        return {"username": username, "preferred_stock": preferred_stock}
    except Exception as e:
        print(f"Error creating user: {e}")
        raise

# Function to find a user
def find_user(username):
    try:
        return mongo.db.users.find_one({"username": username})
    except Exception as e:
        print(f"Error finding user: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)