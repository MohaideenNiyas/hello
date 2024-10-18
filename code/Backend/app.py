from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use the non-interactive backend for Matplotlib
import matplotlib.pyplot as plt
import yfinance as yf
import io
import base64

app = Flask(__name__)
CORS(app)  # This will allow cross-origin requests

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Route to get stock data
@app.route('/get_stock_data', methods=['POST'])
def get_stock_data():
    try:
        # Get the ticker from the request JSON
        ticker = request.json['ticker']  # Ensure you are using request.json
        
        stock = yf.Ticker(ticker)

        # Fetch historical data
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

        # Plot RSI
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
        rsi_plot = base64.b64encode(img_rsi.getvalue()).decode()

        # Plot Beta
        img_beta = io.BytesIO()
        plt.figure(figsize=(5, 5))
        plt.bar('Beta', beta, color='blue')
        plt.title('Beta')
        plt.ylim(0, max(beta + 0.5, 2))
        plt.savefig(img_beta, format='png')
        plt.close()
        img_beta.seek(0)
        beta_plot = base64.b64encode(img_beta.getvalue()).decode()

        # Plot P/E Ratios
        img_pe = io.BytesIO()
        pe_ratios = {'Trailing P/E': trailing_pe, 'Forward P/E': forward_pe}
        plt.figure(figsize=(5, 5))
        plt.bar(pe_ratios.keys(), pe_ratios.values(), color=['orange', 'cyan'])
        plt.title('P/E Ratios')
        plt.ylim(0, max(trailing_pe, forward_pe) + 10)
        plt.savefig(img_pe, format='png')
        plt.close()
        img_pe.seek(0)
        pe_plot = base64.b64encode(img_pe.getvalue()).decode()

        # Plot Price to Book Ratio
        img_pb = io.BytesIO()
        plt.figure(figsize=(5, 5))
        plt.bar('P/B Ratio', price_to_book, color='green')
        plt.title('Price to Book (P/B) Ratio')
        plt.ylim(0, max(price_to_book + 10, 20))
        plt.savefig(img_pb, format='png')
        plt.close()
        img_pb.seek(0)
        pb_plot = base64.b64encode(img_pb.getvalue()).decode()

        # Return the data as JSON
        return jsonify({
            'rsi_plot': rsi_plot,
            'beta_plot': beta_plot,
            'pe_plot': pe_plot,
            'pb_plot': pb_plot
        })
    except Exception as e:
        # Return error if something goes wrong
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
