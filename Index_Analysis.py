import plotly.express as px
import yfinance as yf
import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels import regression
import statsmodels.api as sm
from datetime import date
# Set page configuration
st.set_page_config(layout="wide", page_title="Integrated Stock/Index Analysis Dashboard")
# Tabs for separate functionalities
tab1, tab2, tab3 = st.tabs(["Tab 1: Nifty Indices Analysis", "Tab 2: Nifty Falls and Recovery Analysis","Tab 3: Stock vs Nifty/Sectoral Comparison"])




# Tab 1: First code logic
with tab1:
    st.title("📈 Nifty Indices Percentage Change Dashboard")
    st.write("""
        This dashboard provides a detailed analysis of the percentage changes in various Nifty indices and their constituent stocks over a user-defined period.
        You can select the number of days for which you want to see the percentage change. The dashboard displays the percentage
        change sorted from most negative to positive and provides a visual representation using bar and line charts.
    """)
    # tab1_data = []  # Example variable specific to Tab 1




    nifty_200_stocks = [
        "RELIANCE.NS", "HDFCBANK.NS", "INFY.NS", "ICICIBANK.NS", "TCS.NS", "KOTAKBANK.NS", "HINDUNILVR.NS", "SBIN.NS",
        "BAJFINANCE.NS", "BHARTIARTL.NS", "HCLTECH.NS", "ASIANPAINT.NS", "ITC.NS", "AXISBANK.NS", "LT.NS", "MARUTI.NS",
        "HDFCLIFE.NS", "NESTLEIND.NS", "WIPRO.NS", "M&M.NS", "TITAN.NS", "SUNPHARMA.NS", "ULTRACEMCO.NS", "POWERGRID.NS",
        "TATAMOTORS.NS", "ADANIPORTS.NS", "DABUR.NS", "JSWSTEEL.NS", "INDUSINDBK.NS", "HINDALCO.NS", "GRASIM.NS",
        "DIVISLAB.NS", "TATASTEEL.NS", "BAJAJFINSV.NS", "BPCL.NS", "SHREECEM.NS", "HEROMOTOCO.NS", "BRITANNIA.NS",
        "CIPLA.NS", "TECHM.NS", "TATACONSUM.NS", "GAIL.NS", "DRREDDY.NS", "UPL.NS", "EICHERMOT.NS", "DMART.NS",
        "COALINDIA.NS", "IOC.NS", "BANDHANBNK.NS", "BIOCON.NS", "GODREJCP.NS", "SIEMENS.NS", "MGL.NS", "CONCOR.NS",
        "DLF.NS", "CUB.NS", "SBILIFE.NS", "GUJGASLTD.NS", "PAGEIND.NS", "BAJAJ-AUTO.NS", "INDIGO.NS", "TATAPOWER.NS",
        "MINDTREE.NS", "SRF.NS", "IDFCFIRSTB.NS", "MARICO.NS", "CHOLAFIN.NS", "PIIND.NS", "HAL.NS", "PFIZER.NS",
        "TRENT.NS", "ACC.NS", "NTPC.NS", "BEL.NS", "VOLTAS.NS", "AARTIIND.NS", "AMBUJACEM.NS", "ZEEL.NS", "JINDALSTEL.NS",
        "BANKBARODA.NS", "NAM-INDIA.NS", "APOLLOHOSP.NS", "HAVELLS.NS", "GMRINFRA.NS", "IRCTC.NS", "ABCAPITAL.NS",
        "ICICIPRULI.NS", "MANAPPURAM.NS", "BOSCHLTD.NS", "ASHOKLEY.NS", "NAVINFLUOR.NS", "MPHASIS.NS", "INDHOTEL.NS",
        "HONAUT.NS", "SUNTV.NS", "ATGL.NS", "AUROPHARMA.NS", "GLAND.NS", "OBEROIRLTY.NS", "BATAINDIA.NS", "ZYDUSLIFE.NS",
        "PETRONET.NS", "WHIRLPOOL.NS", "COFORGE.NS", "ESCORTS.NS", "ALKEM.NS", "TATAELXSI.NS", "EMAMILTD.NS", "DEEPAKNTR.NS",
        "AMARAJABAT.NS", "TVSMOTOR.NS","LTIM.NS", "SHRIRAMCIT.NS", "MUTHOOTFIN.NS", "IEX.NS"
    ]








    nifty_indices = {
        "Nifty 50": "^NSEI",
        "Nifty Bank": "^NSEBANK",
        "Nifty IT": "^CNXIT",
        "Nifty Auto": "^CNXAUTO",
        "Nifty Metal": "^CNXMETAL",
        "Nifty Pharma": "^CNXPHARMA"
    }




    sector_stocks = {
        "IT": ["INFY.NS", "TCS.NS", "HCLTECH.NS", "WIPRO.NS","LTIM.NS"],  
        "Banking": ["HDFCBANK.NS", "ICICIBANK.NS", "AXISBANK.NS", "KOTAKBANK.NS", "SBIN.NS"],
        "Auto": ["MARUTI.NS", "TATAMOTORS.NS", "M&M.NS", "BAJAJ-AUTO.NS"],
        "Pharma": ["SUNPHARMA.NS", "DRREDDY.NS", "CIPLA.NS", "DIVISLAB.NS"],
        "Finance": ["BAJFINANCE.NS", "HDFCLIFE.NS", "ICICIPRULI.NS", "SBILIFE.NS"],
        "Auto": ["M&M.NS", "MARUTI.NS", "TATAMOTORS.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS"]

    }








    def calculate_percentage_change(ticker, days):
        try:
            # Fetch sufficient historical data to include at least `days` trading days
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days * 3)  # Fetch extra days to cover non-trading days
            data = yf.download(ticker, start=start_date, end=end_date)
            
            if data.empty:
                return None, None, None, None

            # Ensure we use the last `days` trading days
            if len(data) >= days:
                filtered_data = data.tail(days)
            else:
                filtered_data = data  # Use all available days if less than required

            # Calculate percentage change
            percentage_change = ((filtered_data['Close'].iloc[-1] - filtered_data['Close'].iloc[0]) / filtered_data['Close'].iloc[0]) * 100
            current_price = filtered_data['Close'].iloc[-1]
            start_date = filtered_data.index[0].date()
            return percentage_change, filtered_data, start_date, current_price
        except Exception as e:
            st.warning(f"Failed to fetch data for {ticker}: {e}")
            return None, None, None, None






    # Function to get the current percentage change from the previous close
    def get_current_percentage_change(ticker):
        try:
            data = yf.download(ticker, period='5d', interval='1d')
            if data.empty or len(data) < 2:
                return None
            current_change = ((data['Close'].iloc[-1] - data['Close'].iloc[-2]) / data['Close'].iloc[-2]) * 100
            return current_change
        except Exception as e:
            st.warning(f"Failed to fetch current data for {ticker}: {e}")
            return None




    # Function to get the 52-week high and percentage below 52-week high
    def get_52_week_high(ticker):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            data = yf.download(ticker, start=start_date, end=end_date)
            if data.empty:
                return None, None
            high_52_week = data['Close'].max()
            current_price = data['Close'].iloc[-1]
            percentage_below_52_week_high = ((current_price - high_52_week) / high_52_week) * 100
            return high_52_week, percentage_below_52_week_high
        except Exception as e:
            st.warning(f"Failed to fetch 52-week high data for {ticker}: {e}")
            return None, None




    # Function to get the all-time high and percentage below all-time high
    def get_all_time_high(ticker):
        try:
            data = yf.download(ticker, period='max')
            if data.empty:
                return None, None
            all_time_high = data['Close'].max()
            current_price = data['Close'].iloc[-1]
            percentage_below_ath = ((current_price - all_time_high) / all_time_high) * 100
            return all_time_high, percentage_below_ath
        except Exception as e:
            st.warning(f"Failed to fetch all-time high data for {ticker}: {e}")
            return None, None




    # Function to fetch historical data and normalize it
    def fetch_and_normalize_data(ticker, days):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            data = yf.download(ticker, start=start_date, end=end_date)
            if data.empty:
                return None, None, None
            normalized_data = (data['Close'] / data['Close'].iloc[0]) * 100
            return normalized_data, data.index, data['Close']
        except Exception as e:
            st.warning(f"Failed to fetch data for {ticker}: {e}")
            return None, None, None




    # Function to calculate daily percentage changes
    def calculate_daily_percentage_changes(data):
        daily_changes = data.pct_change() * 100
        return daily_changes




    # Function to calculate the overall percentage change for the selected range
    def calculate_overall_percentage_change(data):
        overall_change = ((data.iloc[-1] - data.iloc[0]) / data.iloc[0]) * 100
        return overall_change




    # Function to calculate beta and correlation with Nifty 50
    def calculate_beta_and_correlation(ticker):
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            nifty50_data = yf.download("^NSEI", start=start_date, end=end_date)['Close']
            index_data = yf.download(ticker, start=start_date, end=end_date)['Close']
            if nifty50_data.empty or index_data.empty:
                return None, None
            returns_nifty50 = nifty50_data.pct_change().dropna()
            returns_index = index_data.pct_change().dropna()
            aligned_data = returns_nifty50.align(returns_index, join='inner')
            returns_nifty50, returns_index = aligned_data[0], aligned_data[1]
            covariance = np.cov(returns_nifty50, returns_index)[0, 1]
            beta = covariance / returns_nifty50.var()
            correlation = covariance / (returns_nifty50.std() * returns_index.std())
            return beta, correlation
        except Exception as e:
            st.warning(f"Failed to fetch beta and correlation data for {ticker}: {e}")
            return None, None


    def calculate_percentage_difference_from_nifty50(nifty50_data, index_data):
        differences = index_data / nifty50_data
        return differences


    # Function to color negative values light red and positive values light green
    def color_times_of_nifty50(value):
        if isinstance(value, str):
            return ''
        if value < 1:
            return 'background-color: lightcoral;'
        else:
            return 'background-color: lightgreen;'


    # Function to get market cap of a stock
    def get_market_cap(ticker):
        try:
            stock = yf.Ticker(ticker)
            market_cap = stock.info.get('marketCap')
            return market_cap
        except Exception as e:
            st.warning(f"Failed to fetch market cap for {ticker}: {e}")
            return None


    days = st.sidebar.slider("Select number of days for percentage change calculation:", 1, 30, 7)


    # Fetch Nifty 50 data for comparison
    _, nifty50_data, _, nifty50_current_price = calculate_percentage_change("^NSEI", days)


    # Fetch data for all indices and stocks
    percentage_changes = {}
    historical_data = {}
    start_dates = {}
    current_prices = {}
    current_percentage_changes = {}
    high_52_weeks = {}
    percent_below_52_week_highs = {}
    all_time_highs = {}
    percent_below_aths = {}
    percentage_difference_from_nifty50 = {}
    market_caps = {}




    for index, ticker in nifty_indices.items():
        change, data, start_date, current_price = calculate_percentage_change(ticker, days)
        current_change = get_current_percentage_change(ticker)
        high_52_week, percent_below_52_week_high = get_52_week_high(ticker)
        all_time_high, percent_below_ath = get_all_time_high(ticker)
        market_cap = get_market_cap(ticker)
   
        if change is not None:
            percentage_changes[index] = change
            historical_data[index] = data
            start_dates[index] = start_date
            current_prices[index] = current_price
            current_percentage_changes[index] = current_change
            high_52_weeks[index] = high_52_week
            percent_below_52_week_highs[index] = percent_below_52_week_high
            all_time_highs[index] = all_time_high
            percent_below_aths[index] = percent_below_ath
            market_caps[index] = market_cap
            if nifty50_data is not None and data is not None:
                aligned_nifty50_data, aligned_index_data = nifty50_data['Close'].align(data['Close'], join='inner')
                percentage_difference_from_nifty50[index] = calculate_percentage_difference_from_nifty50(aligned_nifty50_data, aligned_index_data)




    # Calculate one-week and one-month percentage changes
    one_week_changes = {}
    one_month_changes = {}
    for index, ticker in nifty_indices.items():
        one_week_changes[index], _, _, _ = calculate_percentage_change(ticker, 7)
        one_month_changes[index], _, _, _ = calculate_percentage_change(ticker, 30)




    # Fetch stock data within each sector and calculate percentage changes
    sector_stock_changes = {sector: {} for sector in sector_stocks}
    sector_market_caps = {sector: {} for sector in sector_stocks}




    for sector, stocks in sector_stocks.items():
        for stock in stocks:
            stock_change, stock_data, _, stock_current_price = calculate_percentage_change(stock, days)
            one_week_stock_change, _, _, _ = calculate_percentage_change(stock, 7)
            one_month_stock_change, _, _, _ = calculate_percentage_change(stock, 30)
            stock_high_52_week, stock_percent_below_52_week_high = get_52_week_high(stock)
            stock_all_time_high, stock_percent_below_ath = get_all_time_high(stock)
            stock_market_cap = get_market_cap(stock)
       
            sector_stock_changes[sector][stock] = {
                "Selected Period Change": stock_change,
                "One Week Change": one_week_stock_change,
                "One Month Change": one_month_stock_change,
                "Current Price": stock_current_price,
                "52 Week High": stock_high_52_week,
                "52 Week High % Below": stock_percent_below_52_week_high,
                "All-Time High": stock_all_time_high,
                "ATH % Below": stock_percent_below_ath,
                "Market Cap": stock_market_cap
            }
            sector_market_caps[sector][stock] = stock_market_cap




    # Display the main data
    table_data = {
        "Index/Stock": [],
        "Category": [],
        "Start Date": [],
        "End Date": [],
        "Current Price": [],
        "Current % Change": [],
        "Selected Period Change (%)": [],
        "One Week Change (%)": [],
        "One Month Change (%)": [],
        "52 Week High": [],
        "52 Week High % Below": [],
        "All-Time High": [],
        "ATH % Below": [],
        "Market Cap": [],
        "Times of Nifty 50": []
    }




    end_date = datetime.now().date()




    for index in sorted(percentage_changes, key=percentage_changes.get):
        table_data["Index/Stock"].append(index)
        table_data["Category"].append("Index")
        table_data["Start Date"].append(start_dates.get(index, "N/A") if start_dates.get(index) else "N/A")
        table_data["End Date"].append(end_date)
        table_data["Current Price"].append(f"{current_prices.get(index, 0.0):.2f}" if current_prices.get(index) is not None else "N/A")
        table_data["Current % Change"].append(f"{current_percentage_changes.get(index, 0.0):.2f}%" if current_percentage_changes.get(index) is not None else "N/A")
        table_data["Selected Period Change (%)"].append(f"{percentage_changes.get(index, 0.0):.2f}%" if percentage_changes.get(index) is not None else "N/A")
        table_data["One Week Change (%)"].append(f"{one_week_changes.get(index, 0.0):.2f}%" if one_week_changes.get(index) is not None else "N/A")
        table_data["One Month Change (%)"].append(f"{one_month_changes.get(index, 0.0):.2f}%" if one_month_changes.get(index) is not None else "N/A")
        table_data["52 Week High"].append(f"{high_52_weeks.get(index, 0.0):.2f}" if high_52_weeks.get(index) is not None else "N/A")
        table_data["52 Week High % Below"].append(f"{percent_below_52_week_highs.get(index, 0.0):.2f}%" if percent_below_52_week_highs.get(index) is not None else "N/A")
        table_data["All-Time High"].append(f"{all_time_highs.get(index, 0.0):.2f}" if all_time_highs.get(index) is not None else "N/A")
        table_data["ATH % Below"].append(f"{percent_below_aths.get(index, 0.0):.2f}%" if percent_below_aths.get(index) is not None else "N/A")
        table_data["Market Cap"].append(f"{market_caps.get(index, 0.0):.2f}" if market_caps.get(index) is not None else "N/A")
        if index != "Nifty 50" and index in percentage_difference_from_nifty50:
            ratio = percentage_difference_from_nifty50[index].iloc[-1]
            table_data["Times of Nifty 50"].append(f"{ratio:.2f}" if ratio is not None else "N/A")
        else:
            table_data["Times of Nifty 50"].append("N/A")








    # Include individual stock data within its sector
    for sector, stocks in sector_stock_changes.items():
        for stock, changes in stocks.items():
            table_data["Index/Stock"].append(stock)
            table_data["Category"].append(f"{sector} - Stock")
            table_data["Start Date"].append(start_dates.get(stock, "N/A") if start_dates.get(stock) else "N/A")
            table_data["End Date"].append(end_date)
            table_data["Current Price"].append(f"{changes['Current Price']:.2f}" if changes['Current Price'] is not None else "N/A")
            table_data["Current % Change"].append("N/A")  # This metric is not applicable to stocks
            table_data["Selected Period Change (%)"].append(f"{changes['Selected Period Change']:.2f}%" if changes['Selected Period Change'] is not None else "N/A")
            table_data["One Week Change (%)"].append(f"{changes['One Week Change']:.2f}%" if changes['One Week Change'] is not None else "N/A")
            table_data["One Month Change (%)"].append(f"{changes['One Month Change']:.2f}%" if changes['One Month Change'] is not None else "N/A")
            table_data["52 Week High"].append(f"{changes['52 Week High']:.2f}" if changes['52 Week High'] is not None else "N/A")
            table_data["52 Week High % Below"].append(f"{changes['52 Week High % Below']:.2f}%" if changes['52 Week High % Below'] is not None else "N/A")
            table_data["All-Time High"].append(f"{changes['All-Time High']:.2f}" if changes['All-Time High'] is not None else "N/A")
            table_data["ATH % Below"].append(f"{changes['ATH % Below']:.2f}%" if changes['ATH % Below'] is not None else "N/A")
            table_data["Market Cap"].append(f"{changes['Market Cap']:.2f}" if changes['Market Cap'] is not None else "N/A")
            if nifty50_data is not None and changes['Selected Period Change'] is not None:
                ratio = changes['Selected Period Change'] / percentage_changes["Nifty 50"]
                table_data["Times of Nifty 50"].append(f"{ratio:.2f}" if ratio is not None else "N/A")
            else:
                table_data["Times of Nifty 50"].append("N/A")



    # Adding custom CSS for compact and subtle card layout
    st.markdown("""
        <style>
        .card {
            background: #f9f9f9; /* Light grey background for a professional look */
            color: #333; /* Dark text for readability */
            border-radius: 8px;
            padding: 15px;
            margin: 10px 5px;
            box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1); /* Subtle shadow */
            text-align: center;
        }
        .card h3 {
            margin: 5px 0;
            font-size: 1.2rem;
            font-weight: bold;
        }
        .card .metric {
            font-size: 1.6rem;
            font-weight: bold;
            margin: 10px 0;
        }
        .card .delta {
            font-size: 1rem;
            margin-top: 5px;
            color: #ff4d4d; /* Negative values in red */
        }
        .card .delta.positive {
            color: #4caf50; /* Positive values in green */
        }
        </style>
    """, unsafe_allow_html=True)

    # Display summary of the most negative index in the last month
    if table_data["Index/Stock"]:
        # Filter only indices (not stocks) from the table_data
        indices_only = [
            i for i in range(len(table_data["Category"])) if table_data["Category"][i] == "Index"
        ]
        
        if indices_only:
            # Extract monthly percentage changes for indices
            monthly_changes = [
                float(table_data["One Month Change (%)"][i].strip('%'))
                for i in indices_only if table_data["One Month Change (%)"][i] != "N/A"
            ]
            
            # Find the most negative change
            min_monthly_change = min(monthly_changes)
            most_negative_index_pos = indices_only[
                monthly_changes.index(min_monthly_change)
            ]
            
            # Get the index name and its one-week change
            most_negative_index = table_data["Index/Stock"][most_negative_index_pos]
            index_monthly_change = table_data["One Month Change (%)"][most_negative_index_pos]
            index_one_week_change = table_data["One Week Change (%)"][most_negative_index_pos]

            # Find the stocks in the most negative sector
            sector_name = most_negative_index.split(" ")[1]  # Extract sector name from index name
            stocks_in_sector = sector_stocks.get(sector_name, [])
            
            # Filter stocks data
            stocks_data = [
                (i, table_data["Index/Stock"][i])
                for i in range(len(table_data["Category"]))
                if table_data["Index/Stock"][i] in stocks_in_sector and table_data["One Month Change (%)"][i] != "N/A"
            ]

            if stocks_data:
                # Extract monthly changes for stocks in the sector
                stock_monthly_changes = [
                    float(table_data["One Month Change (%)"][i].strip('%')) for i, _ in stocks_data
                ]

                # Find the most negative stock in the sector
                most_negative_stock_pos = stocks_data[
                    stock_monthly_changes.index(min(stock_monthly_changes))
                ][0]
                most_negative_stock = table_data["Index/Stock"][most_negative_stock_pos]
                stock_monthly_change = table_data["One Month Change (%)"][most_negative_stock_pos]
                stock_one_week_change = table_data["One Week Change (%)"][most_negative_stock_pos]

                # Create a visually appealing card layout with two columns
                st.markdown("### Summary: Most Negative Performance")
                col1, col2 = st.columns(2)

                # Card for the most negative index
                with col1:
                    st.markdown(f"""
                    <div class="card">
                        <h3>📉 Most Negative Index</h3>
                        <div class="metric">{most_negative_index}</div>
                        <div class="delta">1 Month Change: <span class="delta">{index_monthly_change}</span></div>
                        <div class="delta positive">1 Week Change: <span>{index_one_week_change}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                # Card for the most negative stock in the sector
                with col2:
                    st.markdown(f"""
                    <div class="card">
                        <h3>🏚️ Most Negative Stock</h3>
                        <div class="metric">{most_negative_stock}</div>
                        <div class="delta">1 Month Change: <span class="delta">{stock_monthly_change}</span></div>
                        <div class="delta positive">1 Week Change: <span>{stock_one_week_change}</span></div>
                    </div>
                    """, unsafe_allow_html=True)

                # Add a horizontal divider for clarity
                st.markdown("<hr>", unsafe_allow_html=True)



        st.subheader("Percentage Change Data")

        # Function to clean and convert percentage strings to float
        def clean_percentage(value):
            if isinstance(value, str) and "%" in value:
                return float(value.strip('%'))
            return value

        # Clean up percentage columns in table_data
        percentage_columns = [
            "Selected Period Change (%)", "Current % Change",
            "One Week Change (%)", "One Month Change (%)",
            "52 Week High % Below", "ATH % Below"
        ]

        for col in percentage_columns:
            # Ensure all values in these columns are numeric
            table_data[col] = [clean_percentage(val) for val in table_data[col]]

        # Display indices with expandable stock details
        for index in sorted(percentage_changes, key=percentage_changes.get):
            idx = table_data['Index/Stock'].index(index)
            one_week_change = table_data['One Week Change (%)'][idx]
            
            # Plain text title for the expander
            expander_title = f"{index} - One Week Change: {one_week_change:.2f}%"

            # Display the expander
            with st.expander(expander_title, expanded=False):
                # Show the one-week change in color inside the expander
                if one_week_change < 0:
                    styled_change = f"<span style='color: red; font-weight: bold;'>{one_week_change:.2f}%</span>"
                else:
                    styled_change = f"<span style='color: green; font-weight: bold;'>{one_week_change:.2f}%</span>"

                st.markdown(
                    f"<p style='font-size:18px;'>One Week Change: {styled_change}</p>",
                    unsafe_allow_html=True
                )

                # Prepare the data for display in the expander
                df_index = pd.DataFrame({
                    "Index/Stock": [index],
                    "Category": ["Index"],
                    "Start Date": [table_data["Start Date"][idx]],
                    "End Date": [table_data["End Date"][idx]],
                    "Current Price": [table_data["Current Price"][idx]],
                    "Current % Change": [table_data["Current % Change"][idx]],
                    "Selected Period Change (%)": [table_data["Selected Period Change (%)"][idx]],
                    "One Week Change (%)": [table_data["One Week Change (%)"][idx]],
                    "One Month Change (%)": [table_data["One Month Change (%)"][idx]],
                    "52 Week High": [table_data["52 Week High"][idx]],
                    "52 Week High % Below": [table_data["52 Week High % Below"][idx]],
                    "All-Time High": [table_data["All-Time High"][idx]],
                    "ATH % Below": [table_data["ATH % Below"][idx]],
                    "Market Cap": [table_data["Market Cap"][idx]],
                    "Times of Nifty 50": [table_data["Times of Nifty 50"][idx]]
                })
                
                # Display the dataframe inside the expander
                st.dataframe(df_index)

           
                if index in sector_stock_changes:
                    stock_table_data = {
                        "Stock": [],
                        "Selected Period Change (%)": [],
                        "One Week Change (%)": [],
                        "One Month Change (%)": [],
                        "Current Price": [],
                        "52 Week High": [],
                        "52 Week High % Below": [],
                        "All-Time High": [],
                        "ATH % Below": [],
                        "Market Cap": [],
                        "Times of Nifty 50": []
                    }
               
                    for stock, changes in sector_stock_changes[index].items():
                        stock_table_data["Stock"].append(stock)
                        stock_table_data["Selected Period Change (%)"].append(f"{changes['Selected Period Change']:.2f}%" if changes['Selected Period Change'] is not None else "N/A")
                        stock_table_data["One Week Change (%)"].append(f"{changes['One Week Change']:.2f}%" if changes['One Week Change'] is not None else "N/A")
                        stock_table_data["One Month Change (%)"].append(f"{changes['One Month Change']:.2f}%" if changes['One Month Change'] is not None else "N/A")
                        stock_table_data["Current Price"].append(f"{changes['Current Price']:.2f}" if changes['Current Price'] is not None else "N/A")
                        stock_table_data["52 Week High"].append(f"{changes['52 Week High']:.2f}" if changes['52 Week High'] is not None else "N/A")
                        stock_table_data["52 Week High % Below"].append(f"{changes['52 Week High % Below']:.2f}%" if changes['52 Week High % Below'] is not None else "N/A")
                        stock_table_data["All-Time High"].append(f"{changes['All-Time High']:.2f}" if changes['All-Time High'] is not None else "N/A")
                        stock_table_data["ATH % Below"].append(f"{changes['ATH % Below']:.2f}%" if changes['ATH % Below'] is not None else "N/A")
                        stock_table_data["Market Cap"].append(f"{changes['Market Cap']:.2f}" if changes['Market Cap'] is not None else "N/A")
                        if nifty50_data is not None and changes['Selected Period Change'] is not None:
                            ratio = changes['Selected Period Change'] / percentage_changes["Nifty 50"]
                            stock_table_data["Times of Nifty 50"].append(f"{ratio:.2f}" if ratio is not None else "N/A")
                        else:
                            stock_table_data["Times of Nifty 50"].append("N/A")
               
                    stock_df_table = pd.DataFrame(stock_table_data)
                    styled_stock_table = stock_df_table.style.applymap(color_times_of_nifty50, subset=['Times of Nifty 50'])
               
                    st.dataframe(styled_stock_table)




                    # Pie chart for market cap weightage
                    st.subheader(f"Market Cap Weightage for {index}")
                    fig_pie = px.pie(
                        data_frame=stock_df_table,
                        names="Stock",
                        values="Market Cap",
                        title=f"Market Cap Weightage of Stocks in {index}"
                    )
                    st.plotly_chart(fig_pie)




# Function to calculate daily percentage changes
def calculate_daily_changes(data):
    return data.pct_change() * 100




# Function to compute expected daily change for indices based on Nifty
def compute_expected_changes(nifty_changes, correlations):
    expected_changes = {}
    for index, correlation in correlations.items():
        if correlation is not None:
            expected_changes[index] = nifty_changes * correlation
        else:
            expected_changes[index] = [None] * len(nifty_changes)
    return expected_changes




# Fetch Nifty 50 data
nifty_data = yf.download("^NSEI", start=datetime.now() - timedelta(days=150), end=datetime.now())
if not nifty_data.empty:
    nifty_daily_changes = calculate_daily_changes(nifty_data['Close'])



# Sidebar for selecting indices
st.sidebar.header("Select Indices for Analysis")

# Multiselect for comparison indices (exclude Nifty 50)
selected_indices = st.sidebar.multiselect(
    "Select Indices for Comparison with Nifty 50(Default)",
    [index for index in nifty_indices.keys() if index != "Nifty 50"],  # Exclude "Nifty 50"
    default=[]  # Default to no additional indices
)

# Dropdown for selecting the detailed analysis index
selected_index = st.sidebar.selectbox("Select Index for Detailed Analysis", list(nifty_indices.keys()))

# Fetch data for the selected index (independent of comparison indices)
selected_ticker = nifty_indices[selected_index]
selected_data = yf.download(selected_ticker, start=datetime.now() - timedelta(days=150), end=datetime.now())

# Perform detailed analysis for the selected index
if not selected_data.empty:
    st.subheader(f"Detailed Analysis for {selected_index}")

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=selected_data.index,
        y=selected_data['Close'],
        mode='lines+markers',
        name=selected_index,
        hoverinfo='text',
        hovertext=[
            f"Date: {date}<br>Close: {close:.2f}"
            for date, close in zip(selected_data.index, selected_data['Close'])
        ]
    ))
    fig_line.update_layout(
        title=f"Historical Data for {selected_index} (Last 150 Days)",
        xaxis_title="Date",
        yaxis_title="Closing Price",
        hovermode='x unified'
    )
    st.plotly_chart(fig_line)
else:
    st.warning(f"Data for {selected_index} is not available.")

# Fetch data for comparison indices (including Nifty 50 as default)
nifty_data = yf.download("^NSEI", start=datetime.now() - timedelta(days=150), end=datetime.now())
if not nifty_data.empty:
    nifty_daily_changes = calculate_daily_changes(nifty_data['Close'])

if selected_indices or not nifty_data.empty:
    st.subheader("Comparison of Selected Indices")

    correlations = {}
    index_data = {}
    actual_changes = {}

    # Fetch data for additional selected indices
    for index in selected_indices:
        index_ticker = nifty_indices[index]
        index_data[index] = yf.download(index_ticker, start=datetime.now() - timedelta(days=150), end=datetime.now())
        if not index_data[index].empty:
            actual_changes[index] = calculate_daily_changes(index_data[index]['Close'])
            _, correlation = calculate_beta_and_correlation(index_ticker)
            correlations[index] = correlation

    # Compute expected changes for selected indices
    expected_changes = compute_expected_changes(nifty_daily_changes, correlations)

    # Prepare DataFrame for comparison
    comparison_table = {
        "Date": nifty_data.index.strftime("%Y-%m-%d"),
        "Nifty 50 Actual Change (%)": nifty_daily_changes,
    }

    for index in selected_indices:
        comparison_table[f"{index} Correlation with Nifty"] = [correlations.get(index, None)] * len(nifty_daily_changes)
        comparison_table[f"{index} Expected Change (%)"] = expected_changes.get(index, [None] * len(nifty_daily_changes))
        comparison_table[f"{index} Actual Change (%)"] = actual_changes.get(index, [None] * len(nifty_daily_changes))

    # Convert to DataFrame
    comparison_df = pd.DataFrame(comparison_table)

    # Display the comparison table inside an expander
    with st.expander("Comparison Table"):
        st.dataframe(comparison_df)

    # Plot actual vs expected changes for selected indices
    for index in selected_indices:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=comparison_df["Date"],
            y=comparison_df[f"{index} Actual Change (%)"],
            mode='lines+markers',
            name=f"{index} Actual Change (%)"
        ))
        fig.add_trace(go.Scatter(
            x=comparison_df["Date"],
            y=comparison_df[f"{index} Expected Change (%)"],
            mode='lines+markers',
            name=f"{index} Expected Change (%)"
        ))
        fig.update_layout(
            title=f"Actual vs Expected Daily Changes for {index}",
            xaxis_title="Date",
            yaxis_title="Percentage Change",
            legend_title="Change Type"
        )
        st.plotly_chart(fig)

    # Plot comparison for the last 7 days
    st.subheader("Comparison of Actual Changes: Nifty 50 vs Selected Indices (Last 7 Days)")

    # Filter data for the last 7 days
    last_7_days_nifty = nifty_daily_changes.tail(7)
    comparison_data = {"Date": nifty_data.index[-7:].strftime("%Y-%m-%d")}
    comparison_data["Nifty 50 Actual Change (%)"] = last_7_days_nifty.values

    for index in selected_indices:
        if index in actual_changes:
            last_7_days_index = actual_changes[index].tail(7)
            comparison_data[f"{index} Actual Change (%)"] = last_7_days_index.values

    # Create a DataFrame for plotting
    last_7_days_df = pd.DataFrame(comparison_data)

    # Plotting
    fig_last_7 = go.Figure()
    fig_last_7.add_trace(go.Scatter(
        x=last_7_days_df["Date"],
        y=last_7_days_df["Nifty 50 Actual Change (%)"],
        mode="lines+markers",
        name="Nifty 50 Actual Change (%)"
    ))
    for index in selected_indices:
        if f"{index} Actual Change (%)" in last_7_days_df.columns:
            fig_last_7.add_trace(go.Scatter(
                x=last_7_days_df["Date"],
                y=last_7_days_df[f"{index} Actual Change (%)"],
                mode="lines+markers",
                name=f"{index} Actual Change (%)"
            ))

    fig_last_7.update_layout(
        title="Last 7 Days Actual Percentage Change Comparison",
        xaxis_title="Date",
        yaxis_title="Percentage Change",
        legend_title="Indices",
        hovermode="x unified"
    )
    st.plotly_chart(fig_last_7)




    # Corrected Function: display_top_gainers_losers
    def display_top_gainers_losers(title, stocks):
        st.sidebar.markdown(f"### {title}")
        table_data = []
        for stock, data in stocks:
            stock_high_52_week, stock_percent_below_52_week_high = get_52_week_high(stock)
            stock_all_time_high, stock_percent_below_ath = get_all_time_high(stock)
            table_data.append([
                stock,
                f"{data['Current Price']:.2f}" if data['Current Price'] is not None else "N/A",
                f"{data['Change']:.2f}%" if data['Change'] is not None else "N/A",
                f"{stock_high_52_week:.2f}" if stock_high_52_week is not None else "N/A",
                f"{stock_all_time_high:.2f}" if stock_all_time_high is not None else "N/A"
            ])
        df = pd.DataFrame(table_data, columns=["Stock", "Current Price", "Change (%)", "52 Week High", "All-Time High"])
        styled_df = df.style.applymap(color_positive_negative, subset=['Change (%)'])
        st.sidebar.table(styled_df)
    # Function to color positive and negative values
    def color_positive_negative(val):
        if isinstance(val, str):
            val = val.replace('%', '')
        try:
            val = float(val)
        except ValueError:
            pass
        color = 'green' if val > 0 else 'red'
        return f'color: {color}'




    # Function to calculate percentage change for today
    def calculate_today_change(ticker):
        try:
            # Fetch today's data
            today = datetime.now().strftime('%Y-%m-%d')
            data = yf.download(ticker, period='1d', interval='1d')  # Fetch one day of data
            if data.empty:
                return None, None
            # Calculate today's change as (Close - Open) / Open * 100
            change = ((data['Close'].iloc[-1] - data['Open'].iloc[-1]) / data['Open'].iloc[-1]) * 100
            current_price = data['Close'].iloc[-1]
            return change, current_price
        except Exception as e:
            st.warning(f"Failed to fetch data for {ticker}: {e}")
            return None, None








    # Calculate today's changes for Nifty 200 stocks
    def get_nifty_200_today_changes():
        stock_changes = {}
        for stock in nifty_200_stocks:
            change, current_price = calculate_today_change(stock)
            if change is not None:
                stock_changes[stock] = {
                    "Change": change,
                    "Current Price": current_price
                }
        return stock_changes




    # Update in get_nifty_200_today_changes function
    def get_nifty_200_today_changes():
        stock_changes = {}
        for stock in nifty_200_stocks:
            change, current_price = calculate_today_change(stock)
            if change is not None and current_price is not None:
                stock_changes[stock] = {
                    "Change": change,
                    "Current Price": current_price
                }
        return stock_changes
    # Get today's changes for Nifty 200
    nifty_200_today_changes = get_nifty_200_today_changes()




    # Sort stocks by today's percentage change
    sorted_nifty_200_today_changes = sorted(nifty_200_today_changes.items(), key=lambda x: x[1]['Change'] if x[1]['Change'] is not None else float('-inf'))
    top_5_losers_nifty_200 = sorted_nifty_200_today_changes[:5]
    top_5_gainers_nifty_200 = sorted_nifty_200_today_changes[-5:][::-1]




    st.sidebar.subheader("Top 5 Gainers and Losers in Nifty 200 for Today")
    display_top_gainers_losers("Top 5 Gainers", top_5_gainers_nifty_200)
    display_top_gainers_losers("Top 5 Losers", top_5_losers_nifty_200)




    st.subheader("Sector Stock Performance")




    for sector, stocks in sector_stocks.items():
        with st.expander(f"{sector} Sector Performance", expanded=False):
            # Prepare data for each sector
            sector_stocks_data = []
            for stock in stocks:
                stock_info = yf.Ticker(stock).info




                # Append stock data only if it exists in sector_stock_changes
                if stock in sector_stock_changes[sector]:
                    sector_stocks_data.append({
                        "Stock Name": stock_info.get("shortName", "N/A"),  # Stock name
                        "Current Price (₹)": sector_stock_changes[sector][stock]["Current Price"],
                        "Selected Period Change (%)": sector_stock_changes[sector][stock]["Selected Period Change"],
                        "One Week Change (%)": sector_stock_changes[sector][stock]["One Week Change"],
                        "One Month Change (%)": sector_stock_changes[sector][stock]["One Month Change"]
                    })
           
            # Create DataFrame for display
            sector_df = pd.DataFrame(sector_stocks_data)
            if not sector_df.empty:
                st.dataframe(sector_df)
            else:
                st.write("No data available for this sector.")




    # Function to calculate percentage deviation
    def calculate_percentage_deviation(actual, expected):
        if expected == 0 or pd.isna(expected):  # Handle division by zero or NaN
            return None
        deviation = ((actual - expected) / abs(expected)) * 100
        return deviation




    # Function to calculate cumulative return
    def calculate_cumulative_return(data, days):
        if len(data.dropna()) < days:  # Ensure there are enough non-NaN values
            return None
        return (np.prod(1 + data.tail(days).dropna() / 100) - 1) * 100




    # Function to calculate summary statistics
    def calculate_summary_statistics(data):
        data = data.dropna()  # Remove NaN values
        stats = {
            "Average Deviation (%)": np.mean(data),
            "Maximum Positive Deviation (%)": np.max(data),
            "Maximum Negative Deviation (%)": np.min(data),
            "Standard Deviation (%)": np.std(data),
            "Total Observations": len(data)
        }
        return stats




    # Prepare data for the difference table and cumulative returns
    if selected_indices:
        diff_table = {
            "Date": comparison_df["Date"]
        }
        cumulative_table = {
            "Index": [],
            "1 Week Actual Return (%)": [],
            "1 Week Expected Return (%)": [],
            "1 Week Difference (%)": [],
            "1 Month Actual Return (%)": [],
            "1 Month Expected Return (%)": [],
            "1 Month Difference (%)": [],
            "3 Month Actual Return (%)": [],
            "3 Month Expected Return (%)": [],
            "3 Month Difference (%)": []
        }
        summary_statistics = {}

        for index in selected_indices:
            if index != "Nifty 50":  # Exclude Nifty 50 from differences
                # Calculate the difference
                diff_col = comparison_df[f"{index} Actual Change (%)"] - comparison_df[f"{index} Expected Change (%)"]
                diff_table[f"{index} Difference (%)"] = diff_col
                diff_table[f"{index} Actual (%)"] = comparison_df[f"{index} Actual Change (%)"]
                diff_table[f"{index} Expected (%)"] = comparison_df[f"{index} Expected Change (%)"]

                # Calculate cumulative returns
                actual_cumulative_7 = calculate_cumulative_return(comparison_df[f"{index} Actual Change (%)"], 7)
                expected_cumulative_7 = calculate_cumulative_return(comparison_df[f"{index} Expected Change (%)"], 7)
                difference_7 = (
                    actual_cumulative_7 - expected_cumulative_7
                    if actual_cumulative_7 is not None and expected_cumulative_7 is not None
                    else None
                )

                actual_cumulative_30 = calculate_cumulative_return(comparison_df[f"{index} Actual Change (%)"], 30)
                expected_cumulative_30 = calculate_cumulative_return(comparison_df[f"{index} Expected Change (%)"], 30)
                difference_30 = (
                    actual_cumulative_30 - expected_cumulative_30
                    if actual_cumulative_30 is not None and expected_cumulative_30 is not None
                    else None
                )

                actual_cumulative_90 = calculate_cumulative_return(comparison_df[f"{index} Actual Change (%)"], 90)
                expected_cumulative_90 = calculate_cumulative_return(comparison_df[f"{index} Expected Change (%)"], 90)
                difference_90 = (
                    actual_cumulative_90 - expected_cumulative_90
                    if actual_cumulative_90 is not None and expected_cumulative_90 is not None
                    else None
                )

                # Add to cumulative table
                cumulative_table["Index"].append(index)
                cumulative_table["1 Week Actual Return (%)"].append(actual_cumulative_7)
                cumulative_table["1 Week Expected Return (%)"].append(expected_cumulative_7)
                cumulative_table["1 Week Difference (%)"].append(difference_7)
                cumulative_table["1 Month Actual Return (%)"].append(actual_cumulative_30)
                cumulative_table["1 Month Expected Return (%)"].append(expected_cumulative_30)
                cumulative_table["1 Month Difference (%)"].append(difference_30)
                cumulative_table["3 Month Actual Return (%)"].append(actual_cumulative_90)
                cumulative_table["3 Month Expected Return (%)"].append(expected_cumulative_90)
                cumulative_table["3 Month Difference (%)"].append(difference_90)

        # Convert difference and cumulative tables to DataFrames
        diff_table_df = pd.DataFrame(diff_table)
        cumulative_table_df = pd.DataFrame(cumulative_table)

        # Display the difference table inside an expander
        st.subheader("Difference Between Expected and Actual Changes")
        with st.expander("📊 View Difference Table", expanded=False):
            st.dataframe(diff_table_df, use_container_width=True)

        # Display the cumulative returns table inside another expander
        st.subheader("Cumulative Returns")
        with st.expander("📈 View Cumulative Returns Table", expanded=False):
            st.dataframe(cumulative_table_df, use_container_width=True)



        st.subheader("Cumulative Returns")

        # Helper function to safely format values
        def safe_format(value, fallback="N/A"):
            return f"{value:.2f}" if value is not None else fallback

        # Custom function for professional-styled metric cards with hover effects
        def styled_card(title, value, color, description, icon=None):
            return f"""
            <div style="
                border: 2px solid {color};
                border-radius: 12px;
                padding: 15px;
                margin: 10px;
                background-color: #ffffff;
                text-align: center;
                box-shadow: 0px 4px 8px rgba(0,0,0,0.2);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            "
                onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0px 6px 12px rgba(0,0,0,0.3)';"
                onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0px 4px 8px rgba(0,0,0,0.2)';"
            >
                <h4 style="margin: 0; color: {color};">{icon if icon else ''} {title}</h4>
                <p style="font-size: 24px; font-weight: bold; margin: 10px 0; color: {color};">{value}</p>
                <p style="font-size: 14px; color: #777;">{description}</p>
            </div>
            """

        # Helper function to safely format values
        def safe_format(value, fallback="N/A"):
            return f"{value:.2f}" if value is not None else fallback

        # Custom function for professional-styled metric cards
        def styled_card(title, value, gradient, description, icon=None):
            return f"""
            <div style="
                background: {gradient};
                border-radius: 15px;
                padding: 20px;
                margin: 15px;
                color: #ffffff;
                text-align: center;
                box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
                transition: transform 0.3s ease, box-shadow 0.3s ease;
            "
                onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 8px 20px rgba(0, 0, 0, 0.3)';"
                onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 6px 15px rgba(0, 0, 0, 0.2)';"
            >
                <h4 style="margin-bottom: 10px; font-size: 18px;">{icon if icon else ''} {title}</h4>
                <p style="font-size: 32px; font-weight: bold; margin: 5px 0;">{value}</p>
                <p style="font-size: 14px; opacity: 0.85; margin-top: 10px;">{description}</p>
            </div>
            """

        # Iterate through the cumulative table to display returns for each index
        for index in cumulative_table_df["Index"]:
            # Add an expander for each index
            with st.expander(f"📊 {index} Cumulative Returns", expanded=True):
                st.markdown(f"## {index} Performance Overview")

                # Define time periods and column mappings
                time_periods = [
                    ("1 Week", "1 Week Actual Return (%)", "1 Week Expected Return (%)"),
                    ("1 Month", "1 Month Actual Return (%)", "1 Month Expected Return (%)"),
                    ("3 Month", "3 Month Actual Return (%)", "3 Month Expected Return (%)"),
                ]

                for period, actual_col, expected_col in time_periods:
                    st.markdown(f"### {period} Cumulative Data")

                    # Create card-style layout using columns
                    col1, col2, col3 = st.columns(3, gap="large")

                    # Fetch values
                    actual_value_raw = cumulative_table_df.loc[cumulative_table_df['Index'] == index, actual_col].values[0]
                    expected_value_raw = cumulative_table_df.loc[cumulative_table_df['Index'] == index, expected_col].values[0]

                    # Use safe_format to ensure valid fallback values
                    actual_value = safe_format(actual_value_raw)
                    expected_value = safe_format(expected_value_raw)

                    # Calculate the difference and handle `N/A` case
                    if actual_value_raw is not None and expected_value_raw is not None:
                        difference_value_raw = abs(expected_value_raw - actual_value_raw)
                        difference_value = safe_format(difference_value_raw)
                        if actual_value_raw < expected_value_raw:
                            difference_gradient = "linear-gradient(135deg, #4CAF50, #81C784)"  # Green gradient
                            difference_text = f"Undervalued: Potential to move up by {difference_value}%"
                        else:
                            difference_gradient = "linear-gradient(135deg, #F44336, #E57373)"  # Red gradient
                            difference_text = f"Overvalued: Potential to move down by {difference_value}%"
                    else:
                        difference_value = "N/A"
                        difference_gradient = "linear-gradient(135deg, #9E9E9E, #BDBDBD)"  # Grey gradient
                        difference_text = "Difference not available"

                    # Define gradients for other cards
                    actual_gradient = "linear-gradient(135deg, #2196F3, #64B5F6)"  # Blue gradient
                    expected_gradient = "linear-gradient(135deg, #FF9800, #FFB74D)"  # Orange gradient

                    # Apply enhanced card styling with hover and shadow effects
                    col1.markdown(
                        styled_card(
                            "Actual Return (%)",
                            actual_value,
                            gradient=actual_gradient,
                            description=f"Performance over {period}",
                            icon="📈"
                        ),
                        unsafe_allow_html=True
                    )

                    col2.markdown(
                        styled_card(
                            "Expected Return (%)",
                            expected_value,
                            gradient=expected_gradient,
                            description="Estimated based on trends",
                            icon="📊"
                        ),
                        unsafe_allow_html=True
                    )

                    col3.markdown(
                        styled_card(
                            "Difference (%)",
                            difference_value,
                            gradient=difference_gradient,
                            description=difference_text,
                            icon="⚖️"
                        ),
                        unsafe_allow_html=True
                    )

# Tab 2: Second code logic
with tab2:
    st.title("📊 Nifty and Bank Nifty Index Analysis")
    st.write("""
        Analyze continuous falls until a new peak, single-day fall statistics, and next-day movement breakdown for selected indices.
    """)


    # Sidebar for index selection
    index_mapping = {
        "Nifty 50": "^NSEI",
        "Bank Nifty": "^NSEBANK"
    }


    # Fetch and cache data
    @st.cache_data
    def get_index_data(ticker, start_date, end_date):
        data = yf.download(ticker, start=start_date, end=end_date)
        data = data[['Low', 'Close']].dropna()
        return data

    # Analyze continuous falls until new peak with gains and recovery days
    @st.cache_data
    def analyze_falls_with_recovery(index_data):
        peak_price = index_data['Low'].iloc[0]
        peak_date = index_data.index[0]
        max_fall_reached = 0
        fall_started = False
        ongoing_correction = {}

        fall_ranges = {'5-10%': 0, '10-15%': 0, '15-20%': 0, '20-25%': 0, '25-30%': 0, '30%+': 0}
        max_falls = {key: 0 for key in fall_ranges.keys()}  # Store max fall per range
        recovery_stats = {key: {"Total Gain (%)": 0, "Days to Recover": []} for key in fall_ranges.keys()}

        for i in range(1, len(index_data)):
            current_price = index_data['Low'].iloc[i]
        
            if current_price < peak_price:
                fall_started = True
                current_fall = ((current_price - peak_price) / peak_price) * 100
                max_fall_reached = min(max_fall_reached, current_fall)
            else:
                if fall_started:
                    if -10 <= max_fall_reached < -5:
                        range_label = '5-10%'
                    elif -15 <= max_fall_reached < -10:
                        range_label = '10-15%'
                    elif -20 <= max_fall_reached < -15:
                        range_label = '15-20%'
                    elif -25 <= max_fall_reached < -20:
                        range_label = '20-25%'
                    elif -30 <= max_fall_reached < -25:
                        range_label = '25-30%'
                    elif max_fall_reached < -30:
                        range_label = '30%+'
                    else:
                        range_label = None

                    if range_label:
                        fall_ranges[range_label] += 1
                        max_falls[range_label] = min(max_falls[range_label], max_fall_reached)
                    
                        # Calculate total gain and recovery days
                        gain = ((current_price - peak_price) / peak_price) * 100
                        recovery_days = (index_data.index[i] - peak_date).days
                        recovery_stats[range_label]["Total Gain (%)"] += gain
                        recovery_stats[range_label]["Days to Recover"].append(recovery_days)

                peak_price = current_price
                peak_date = index_data.index[i]
                max_fall_reached = 0
                fall_started = False

        # Check for ongoing correction
        if fall_started:
            ongoing_correction = {
                "Current Fall (%)": round(max_fall_reached, 2),
                "Days Since Peak": (index_data.index[-1] - peak_date).days,
                "Peak Date": peak_date,
                "Current Price": current_price,
            }


        # Process recovery stats
        for key in recovery_stats.keys():
            total_recoveries = len(recovery_stats[key]["Days to Recover"])
            if total_recoveries > 0:
                recovery_stats[key]["Average Days to Recover"] = np.mean(recovery_stats[key]["Days to Recover"])
                recovery_stats[key]["Max Days to Recover"] = np.max(recovery_stats[key]["Days to Recover"])
            else:
                recovery_stats[key]["Average Days to Recover"] = 0
                recovery_stats[key]["Max Days to Recover"] = 0

        return fall_ranges, max_falls, recovery_stats, ongoing_correction

    # Analyze single-day falls with specific ranges
    @st.cache_data
    def analyze_single_day_fall_ranges(index_data):
        index_data['Daily Change (%)'] = index_data['Close'].pct_change() * 100
        single_day_falls = index_data['Daily Change (%)'].dropna()
        ranges = {
            '1-2%': (-2, -1),
            '2-3%': (-3, -2),
            '3-4%': (-4, -3),
            '4%+': (-float('inf'), -4)
        }
        total_trades = len(single_day_falls)  # Total number of trading days
        fall_summary = []
        for range_label, (lower, upper) in ranges.items():
            occurrence_count = single_day_falls[(single_day_falls > lower) & (single_day_falls <= upper)].count()
            percentage = (occurrence_count / total_trades) * 100
            fall_summary.append({
                'Range': range_label,
                'Occurrences': occurrence_count,
                'Percentage (%)': round(percentage, 2),
                'Total Trades': total_trades
            })
        return pd.DataFrame(fall_summary)


    # Analyze multi-day movements
    @st.cache_data
    def calculate_multi_day_movements(index_data):
        index_data['Daily Change (%)'] = index_data['Close'].pct_change() * 100
        single_day_falls = index_data['Daily Change (%)'].dropna()


        thresholds = [1, 2, 3]
        detailed_movements = {}


        for threshold in thresholds:
            fall_data = single_day_falls[single_day_falls <= -threshold]
            movements = {}

            for day_delta in [1, 2, 3]:
                day_movements = {'Movement Range': [], 'Occurrences': [], 'Percentage (%)': []}
                next_day_ranges = {'Positive': 0, 'Negative': 0}




                for date in fall_data.index:
                    target_day = date + pd.Timedelta(days=day_delta)
                    if target_day in index_data.index:
                        target_day_change = index_data.loc[target_day, 'Daily Change (%)']
                        if target_day_change > 0:
                            next_day_ranges['Positive'] += 1
                        elif target_day_change < 0:
                            next_day_ranges['Negative'] += 1

                for movement_type, count in next_day_ranges.items():
                    percentage = (count / len(fall_data)) * 100
                    day_movements['Movement Range'].append(f"{movement_type}")
                    day_movements['Occurrences'].append(count)
                    day_movements['Percentage (%)'].append(round(percentage, 2))


                movements[f"{day_delta} Day After"] = pd.DataFrame(day_movements)

            detailed_movements[f"{threshold}% Fall"] = movements
        return detailed_movements

    # Fetch the ticker for the selected index
    try:
        ticker = nifty_indices[selected_index]
    except KeyError:
        st.error(f"Selected index '{selected_index}' is not available in nifty_indices. Please check your selection.")
        st.stop()

    # Fetch data for the selected index
    index_data = get_index_data(ticker, "1998-01-01", pd.Timestamp.today().strftime('%Y-%m-%d'))

    # Perform analysis on the selected index
    fall_ranges_counts, max_falls, recovery_stats, ongoing_correction = analyze_falls_with_recovery(index_data)
    fall_ranges_summary = analyze_single_day_fall_ranges(index_data)
    detailed_multi_day_movements = calculate_multi_day_movements(index_data)

    # Prepare data for display
    fall_ranges_df = pd.DataFrame({
        "Range": list(fall_ranges_counts.keys()),
        "Occurrences": list(fall_ranges_counts.values()),
        "Max Fall (%)": [abs(max_falls[key]) for key in fall_ranges_counts.keys()],
        "Total Gain (%)": [recovery_stats[key]["Total Gain (%)"] for key in fall_ranges_counts.keys()],
        "Average Days to Recover": [recovery_stats[key]["Average Days to Recover"] for key in fall_ranges_counts.keys()],
        "Max Days to Recover": [recovery_stats[key]["Max Days to Recover"] for key in fall_ranges_counts.keys()],
    })

    # Display the analysis results
    st.subheader(f"Continuous Falls Analysis for {selected_index}")
    st.dataframe(fall_ranges_df)


    # Highlight ongoing correction
    ongoing_range = None
    if "Current Fall (%)" in ongoing_correction:
        current_fall = abs(ongoing_correction["Current Fall (%)"])
        if 5 <= current_fall < 10:
            ongoing_range = '5-10%'
        elif 10 <= current_fall < 15:
            ongoing_range = '10-15%'
        elif 15 <= current_fall < 20:
            ongoing_range = '15-20%'
        elif 20 <= current_fall < 25:
            ongoing_range = '20-25%'
        elif 25 <= current_fall < 30:
            ongoing_range = '25-30%'
        elif current_fall >= 30:
            ongoing_range = '30%+'

    # Display data and visualizations
    st.write(f"### Continuous Falls Analysis for {selected_index}")
    fig = px.bar(
        fall_ranges_df,
        x="Range",
        y="Occurrences",
        title="Continuous Falls by Range",
        text="Occurrences",
        hover_data=["Max Fall (%)", "Total Gain (%)", "Average Days to Recover", "Max Days to Recover"]
    )
    st.plotly_chart(fig)

    st.write("#### Recovery Statistics After Falls")
    if ongoing_range:
        st.write(f"##### Ongoing Correction: {ongoing_range}")
        st.write("#### Ongoing Correction Details:")
        st.markdown(f"""
        - **Current Fall (%)**: {ongoing_correction["Current Fall (%)"]:.2f}%
        - **Days Since Peak**: {ongoing_correction["Days Since Peak"]}
        - **Peak Date**: {ongoing_correction["Peak Date"].strftime('%Y-%m-%d')}
        - **Current Price**: ₹{ongoing_correction["Current Price"]:.2f}
        """)

    def highlight_row(row):
        if row["Range"] == ongoing_range:
            return ['background-color: lightgreen'] * len(row)
        return [''] * len(row)

    st.dataframe(fall_ranges_df.style.apply(highlight_row, axis=1))

    # Fixing single-day fall analysis to avoid redundancy
    st.write(f"### Single-Day Fall Analysis for {selected_index}")

    # Use expanders to separate DataFrame and charts
    with st.expander("View Single-Day Fall Statistics Table", expanded=True):
        st.dataframe(fall_ranges_summary)

    with st.expander("View Single-Day Fall Statistics Charts", expanded=False):
        fig = px.bar(fall_ranges_summary, x="Range", y="Occurrences",
                    title="Single-Day Fall Occurrences by Range", text="Occurrences")
        st.plotly_chart(fig)

        fig_percentages = px.bar(fall_ranges_summary, x="Range", y="Percentage (%)",
                                title="Percentage of Total Trades by Fall Range", text="Percentage (%)")
        st.plotly_chart(fig_percentages)

    # Multi-Day Movement Analysis
    st.write(f"### Multi-Day Movement Analysis for {selected_index}")


    for threshold, movement_data in detailed_multi_day_movements.items():
        with st.expander(f"Details for {threshold} Fall", expanded=False):
            for day, movement_table in movement_data.items():
                st.write(f"#### {day}")
                st.dataframe(movement_table)



with tab3:
    st.title("📊 Stock Comparison With Indexes")
    st.write("📊 Compare and analyze the performance of a stock against 🏦 Nifty50 and its 📈 respective sector index")


    # Function to calculate beta
    def calculate_beta(stock_returns, market_returns):
        X = sm.add_constant(market_returns)
        model = regression.linear_model.OLS(stock_returns, X).fit()
        beta = model.params[1]
        return beta

    # Fetch historical data
    def fetch_data(stock_symbol, start_date, end_date):
        stock_data = yf.download(stock_symbol, start=start_date, end=end_date)
        stock_data['Returns'] = stock_data['Adj Close'].pct_change()
        return stock_data

    # Calculate correlation and beta
    def analyze_pair(stock_b, benchmark, start_date, end_date):
        stock_b_data = fetch_data(stock_b, start_date, end_date)
        benchmark_data = fetch_data(benchmark, start_date, end_date)
        data = pd.concat([stock_b_data['Adj Close'], benchmark_data['Adj Close']], axis=1).dropna()
        data.columns = [stock_b, benchmark]
        correlation = data[stock_b].corr(data[benchmark])
        return correlation, data


    # Full Nifty 50 stocks with their sectors
    nifty_50_stocks = {
        'TCS.NS': '^CNXIT',
        'RELIANCE.NS': '^CNXENERGY',
        'HDFCBANK.NS': '^NSEBANK',
        'INFY.NS': '^CNXIT',
        'HINDUNILVR.NS': '^CNXCONSUMER',
        'ITC.NS': '^CNXCONSUMER',
        'LT.NS': '^CNXINFRA',
        'SBIN.NS': '^NSEBANK',
        'ICICIBANK.NS': '^NSEBANK',
        'BHARTIARTL.NS': '^CNXTELECOM',
        'MARUTI.NS': '^CNXAUTO',
        'ASIANPAINT.NS': '^CNXCONSUMER',
        # Add more stocks and sectors as needed
    }

    # Function to map stock to its relevant sector index
    def map_stock_to_sector(stock_symbol):
        return nifty_50_stocks.get(stock_symbol, '^NSEI')  # Default to Nifty 50 if no sector found

    # Streamlit dashboard
    st.title("Stock Price Analysis with Nifty 50 and Relevant Sector Index")

    # Select stock symbol for analysis
    stock_b = st.selectbox("Select Stock", list(nifty_50_stocks.keys()))
    benchmark = '^NSEI'
    sector_benchmark = map_stock_to_sector(stock_b)

    # Fixed start and end dates for calculations
    start_date = pd.to_datetime('2010-01-01')
    end_date = pd.to_datetime(date.today())

    # Display selected stock and sector
    st.write(f"**Selected Stock:** {stock_b}")
    st.write(f"**Sector Index:** {sector_benchmark}")

    # Analyze and display results
    if st.button("Analyze"):
        correlation_benchmark, data_benchmark = analyze_pair(stock_b, benchmark, start_date, end_date)
        correlation_sector_benchmark, data_sector_benchmark = analyze_pair(stock_b, sector_benchmark, start_date, end_date)

        last_7_trading_days = data_benchmark.tail(7).index

        expected_prices_nifty = []
        expected_prices_sector = []
        cumulative_returns_nifty = []
        cumulative_returns_sector = []

        for i in range(-7, 0):
            nifty_return = (data_benchmark[benchmark].iloc[i] / data_benchmark[benchmark].iloc[i-7]) - 1
            sector_return = (data_sector_benchmark[sector_benchmark].iloc[i] / data_sector_benchmark[sector_benchmark].iloc[i-7]) - 1

            expected_stock_return_nifty = correlation_benchmark * nifty_return
            expected_stock_return_sector = correlation_sector_benchmark * sector_return

            expected_price_nifty = data_benchmark[stock_b].iloc[i-7] * (1 + expected_stock_return_nifty)
            expected_price_sector = data_benchmark[stock_b].iloc[i-7] * (1 + expected_stock_return_sector)

            expected_prices_nifty.append(expected_price_nifty)
            expected_prices_sector.append(expected_price_sector)
            cumulative_returns_nifty.append(nifty_return)
            cumulative_returns_sector.append(sector_return)

        last_7_days = pd.DataFrame({
            "Date": last_7_trading_days,
            "Start Date for Cumulative Return": [data_benchmark.index[i-7].strftime("%Y-%m-%d") for i in range(-7, 0)],
            "Nifty Price": data_benchmark[benchmark].tail(7).values,
            "Stock Price": data_benchmark[stock_b].tail(7).values,
            "Sector Index Price": data_sector_benchmark[sector_benchmark].tail(7).values,
            "Cumulative Return (Nifty)": [f"{x:.2%}" for x in cumulative_returns_nifty],
            "Cumulative Return (Sector)": [f"{x:.2%}" for x in cumulative_returns_sector],
            "Expected Stock Price (Nifty)": expected_prices_nifty,
            "Difference (Nifty)": data_benchmark[stock_b].tail(7).values - expected_prices_nifty,
            "Expected Stock Price (Sector)": expected_prices_sector,
            "Difference (Sector)": data_benchmark[stock_b].tail(7).values - expected_prices_sector,
        })

        latest_date = last_7_days["Date"].iloc[-1]
        one_week_before_latest_date = last_7_days[last_7_days["Date"] <= latest_date - pd.Timedelta(days=7)]["Date"].iloc[0]

        start_date_cumulative = one_week_before_latest_date.strftime("%Y-%m-%d")
        end_date_cumulative = latest_date.strftime("%Y-%m-%d")
        start_date_stock_price = last_7_days[last_7_days["Date"] == one_week_before_latest_date]["Stock Price"].iloc[0]
        latest_stock_price = last_7_days[last_7_days["Date"] == latest_date]["Stock Price"].iloc[0]
        latest_expected_price_nifty = last_7_days[last_7_days["Date"] == latest_date]["Expected Stock Price (Nifty)"].iloc[0]
        latest_expected_price_sector = last_7_days[last_7_days["Date"] == latest_date]["Expected Stock Price (Sector)"].iloc[0]

        percent_diff_nifty = ((latest_stock_price - latest_expected_price_nifty) / latest_expected_price_nifty) * 100
        percent_diff_sector = ((latest_stock_price - latest_expected_price_sector) / latest_expected_price_sector) * 100
        percent_diff_start_to_latest_nifty = ((start_date_stock_price - latest_expected_price_nifty) / latest_expected_price_nifty) * 100
        percent_diff_start_to_latest_sector = ((start_date_stock_price - latest_expected_price_sector) / latest_expected_price_sector) * 100

        # Display Last 7 Trading Days Data Table
        st.subheader("Last 7 Trading Days Data Table")
        with st.expander("View Detailed Data"):
            st.write(last_7_days)

        # Display results using professional card layout
        st.subheader("1-Week Cumulative Comparison")
        col1, col2 = st.columns(2)

        def create_card(
            title,
            start_date,
            end_date,
            start_price,
            actual_price,
            expected_price,
            actual_date,
            percent_diff,
            percent_diff_start,
            comparison_type,
        ):
            # Determine colors and messages for Weekly and Daily differences
            color_weekly = "green" if percent_diff_start < 0 else "red"
            potential_weekly = f"<span style='color:{color_weekly};'>weekly Potential to move {'up'  if percent_diff_start < 0 else 'down'} by {abs(percent_diff_start):.2f}%</span>"

            color_daily = "green" if percent_diff < 0 else "red"
            potential_daily = f"<span style='color:{color_daily};'>daily Potential to move {'up' if percent_diff < 0 else 'down'} by {abs(percent_diff):.2f}%</span>"

            # Label for expected stock price
            expected_label = (
                f"Expected Stock Price w.r.t. Nifty on {actual_date}"
                if comparison_type == "Nifty"
                else f"Expected Stock Price w.r.t. Sector on {actual_date}"
            )

            # Construct the card content
            return f"""
            <div style="border-radius: 10px; background-color: #f4f4f4; padding: 15px; margin: 10px;">
                <h3 style="text-align: center; color: {'blue' if comparison_type == 'Sector' else 'black'};">{title}</h3>
                <p><b>Start Date:</b> {start_date}</p>
                <p><b>End Date:</b> {end_date}</p>
                <p><b>Actual Stock Price on {start_date}:</b> ₹{start_price:.2f}</p>
                <p><b>Actual Stock Price on {actual_date}:</b> ₹{actual_price:.2f}</p>
                <p><b>{expected_label}:</b> ₹{expected_price:.2f}</p>
                <p><b>% Difference (Weekly {start_date} - {end_date}):</b> {percent_diff_start:.2f}%</p>
                <p><b>% Difference (Daily {actual_date}):</b> {percent_diff:.2f}%</p>
                <p><b>{potential_weekly}</b></p>
                <p><b>{potential_daily}</b></p>
            </div>
            """






        with col1:
            nifty_card = create_card(
                title="Stock vs Nifty",
                start_date=start_date_cumulative,
                end_date=end_date_cumulative,
                start_price=start_date_stock_price,
                actual_price=latest_stock_price,
                expected_price=latest_expected_price_nifty,
                actual_date=latest_date.strftime("%Y-%m-%d"),
                percent_diff=percent_diff_nifty,
                percent_diff_start=percent_diff_start_to_latest_nifty,
                comparison_type="Nifty"
            )
            st.markdown(nifty_card, unsafe_allow_html=True)


        with col2:
            sector_card = create_card(
                title="Stock vs Sector",
                start_date=start_date_cumulative,
                end_date=end_date_cumulative,
                start_price=start_date_stock_price,
                actual_price=latest_stock_price,
                expected_price=latest_expected_price_sector,
                actual_date=latest_date.strftime("%Y-%m-%d"),
                percent_diff=percent_diff_sector,
                percent_diff_start=percent_diff_start_to_latest_sector,
                comparison_type="Sector"
            )
            st.markdown(sector_card, unsafe_allow_html=True)


