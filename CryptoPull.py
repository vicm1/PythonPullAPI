from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import re  # Regular expressions module
import datetime
import pandas as pd
import csv
import threading  # Allows graph and scraper to run together
import matplotlib.pyplot as plt
import matplotlib.animation as animation  

# File path
csv_file_path = r'PythonWebScrapers\Code\AmazonWebScraper\AmazonWebScraperDataset.csv'

def check_price():
    URL = 'https://www.amazon.com/Optimum-Nutrition-Standard-Delicious-Strawberry/dp/B000GIQT2O'

    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in background
    options.add_argument("--log-level=3")  # Suppress non-critical logs
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Suppress logging
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(URL)
    time.sleep(5)  # Wait for JavaScript to load

    try:
        title = driver.find_element(By.ID, "productTitle").text.strip()
    except:
        title = "Title not found"

    price = None
    price_selectors = [
        "corePriceDisplay_desktop_feature_div",
        "snsDetailPagePrice",
        "sns-base-price",
        "subscriptionPrice",
        "priceblock_ourprice"
    ]

    for selector in price_selectors:
        try:
            price_text = driver.find_element(By.ID, selector).text.strip()
            price_match = re.search(r'(\d+)[\s\-](\d+)\.?(\d+)?', price_text)
            
            if price_match:
                price = f"{price_match.group(1)}.{price_match.group(2)}"
                if price_match.group(3):
                    price += f"{price_match.group(3)}"
                price = float(price.replace("$", ""))
                break
        except:
            continue

    if price is None:
        price = "Price not found"

    today = datetime.date.today()
    current_time = datetime.datetime.now().strftime("%H:%M:%S")  # HH:MM:SS format

    print(f"Title: {title}")
    print(f"Price: ${price}")
    print(f"Date: {today}")
    print(f"Time: {current_time}")

    header = ['Title', 'Price', 'Date', 'Time']
    data = [title, f"${price}", today, current_time]

    with open(csv_file_path, 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

    driver.quit()

# **Graphing Function (Only Day & Month on X-axis)**
def animate(i):
    try:
        df = pd.read_csv(csv_file_path)
        df['DateTime'] = df['Date'] + ' ' + df['Time']  # Combine date and time
        df['DateTime'] = pd.to_datetime(df['DateTime'])  # Convert to datetime
        df['Price'] = df['Price'].replace('[\$,]', '', regex=True).astype(float)  # Convert price to float

        plt.cla()  # Clear the old plot
        plt.plot(df['DateTime'], df['Price'], marker='o', linestyle='-')

        plt.xlabel("Date")
        plt.ylabel("Price (USD)")
        plt.title("Amazon Price Tracker")

        # Format X-axis to show only Day & Month
        date_labels = df['DateTime'].dt.strftime('%b %d')  # Example: "Feb 04"
        plt.xticks(df['DateTime'], date_labels, rotation=45)

        plt.grid()
    except Exception as e:
        print("Error updating graph:", e)

# **Start Graphing in a Separate Thread**
def start_graph():
    fig = plt.figure()
    ani = animation.FuncAnimation(fig, animate, interval=5000)  # Update every 5 seconds
    plt.show()

# **Run Scraper in a Loop While Graph Updates**
def run_scraper():
    while True:
        check_price()
        time.sleep(10)  # Check price every 10 seconds

# **Start Both Processes**
threading.Thread(target=run_scraper, daemon=True).start()  # Run scraper in background
start_graph()  # Start graph (Main Thread)