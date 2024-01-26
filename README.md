Certainly! Here's the complete documentation in Markdown format:

markdown
Copy code
# FIX Client

This is a simple FIX (Financial Information eXchange) client written in Python. It connects to a FIX server, sends random orders, and calculates certain statistics related to the order flow.

## Requirements
- Python 3.x

## How to Run
1. Clone or download the repository to your local machine.
2. Open a terminal and navigate to the directory where the script is located.
3. Run the script with the following command:

   ```bash
   python fix_client.py
The script will start sending random orders to the specified FIX server.
Configuration
You can configure the FIX client by modifying the following parameters in the script:

host: The host address of the FIX server.
port: The port number to connect to the FIX server.
sender_comp_id: Sender's unique identifier.
target_comp_id: Target's unique identifier.
reset_time: Time to reset the sequence number (e.g., "00:00 SGT").
FIX Version
The client uses FIX version 4.2.

External Libraries
The script doesn't rely on any external libraries.

Logging
The script logs its activities to a file named fix_client.log in the same directory.

## Design Documentation
1. Overview
The FIX client is designed to interact with a FIX server, sending random orders and calculating specific statistics related to the order flow. The key components and design aspects include:

FixClient Class: Represents the FIX client, encapsulating the entire functionality.
Socket Connection: Establishes a TCP socket connection to the FIX server.
Order Generation: Generates and sends random orders for specified instruments (e.g., MSFT, AAPL, BAC).
Response Handling: Receives and processes execution reports, rejects, and cancel rejects from the server.
Statistics Calculation: Calculates total trading volume, profit and loss (PNL), and Volume Weighted Average Price (VWAP) for each instrument.
Logging: Logs activities to a file named fix_client.log.
2. Sequence Number Reset
The sequence number is reset when logging in for simplicity, as per the FIX protocol.

3. Order Generation and Cancellation
The client generates random buy/sell/short orders for specified instruments within a 5-minute period. Additionally, it randomly cancels orders within 5 minutes of sending.

4. Statistics Calculation
The client calculates and displays the following statistics:

Total Trading Volume: The sum of the product of order quantity and price for executed orders.
PNL (Profit and Loss): Currently set to zero, awaiting specific PNL calculation logic.
VWAP (Volume Weighted Average Price): Calculated for each instrument based on executed order quantities and prices.
Running the Code
Ensure you have Python 3.x installed on your system.

Open a terminal and navigate to the directory containing the script.

Run the script with the following command:

```python main.py```
python fix_client.py
The script will connect to the specified FIX server, send random orders, and calculate statistics.

Note: Make sure to configure the script based on your FIX server's details as mentioned in the Configuration section.

License
This code is provided under the MIT License.

Disclaimer
This script is a basic example for educational purposes. It may need adjustments for use in a production environment. Use it at your own risk.