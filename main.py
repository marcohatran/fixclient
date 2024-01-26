import socket
import time
import random
import datetime

class FixClient:
    def __init__(self, host, port, sender_comp_id, target_comp_id, reset_time):
        self.host = host
        self.port = port
        self.sender_comp_id = sender_comp_id
        self.target_comp_id = target_comp_id
        self.reset_time = reset_time
        self.sequence_number = 1
        self.orders = []
        self.total_volume = 0.0
        self.pnl = 0.0
        self.instrument_vwap = {}

    def log(self, message):
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        with open("fix_client.log", "a") as log_file:
            log_file.write(f"{timestamp} {message}\n")

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.log(f"Connected to {self.host}:{self.port}")

    def disconnect(self):
        self.socket.close()
        self.log("Disconnected")

    def send_message(self, message):
        self.socket.send(message.encode())
        self.log(f"Sent: {message}")

    def receive_message(self):
        data = self.socket.recv(1024).decode()
        self.log(f"Received: {data}")
        return data

    def parse_field(self, message, tag):
        try:
            start = message.index(f"{tag}=") + len(tag) + 1
            end = message.index("|", start)
            return message[start:end]
        except ValueError:
            return None

    def handle_execution_report(self, msg):
        # Example: Extract relevant fields from the execution report message
        exec_type = self.parse_field(msg, "150")
        order_id = self.parse_field(msg, "11")
        symbol = self.parse_field(msg, "55")
        quantity = float(self.parse_field(msg, "38"))
        price = float(self.parse_field(msg, "44"))

        if exec_type == "0":  # New Order - Filled
            self.total_volume += quantity * price
            if symbol not in self.instrument_vwap:
                self.instrument_vwap[symbol] = {"total_qty": 0, "total_value": 0.0}
            self.instrument_vwap[symbol]["total_qty"] += quantity
            self.instrument_vwap[symbol]["total_value"] += quantity * price

    def handle_reject(self, msg):
        # Example: Extract relevant fields from the reject message
        reject_reason = self.parse_field(msg, "58")
        order_id = self.parse_field(msg, "11")

    def handle_cancel_reject(self, msg):
        # Example: Extract relevant fields from the cancel reject message
        orig_cl_ord_id = self.parse_field(msg, "41")
        order_id = self.parse_field(msg, "11")


    def calculate_stats(self):
        # Example: Calculate PNL based on executed trades and total volume
        # You might need additional logic based on your specific requirements
        self.pnl = 0.0
        # Implement your PNL calculation logic here

        # Print or log the calculated stats
        print(f"Total Trading Volume: {self.total_volume} USD")
        print(f"PNL: {self.pnl} USD")
        print("VWAP for each instrument:")
        for symbol, vwap_data in self.instrument_vwap.items():
            if vwap_data["total_qty"] > 0:
                vwap = vwap_data["total_value"] / vwap_data["total_qty"]
                print(f"{symbol}: {vwap} USD")

    def run(self):
        try:
            self.connect()

            while True:
                for symbol in ["MSFT", "AAPL", "BAC"]:
                    side = random.choice(["1", "2", "5"])
                    order_id = random.randint(100000, 999999)
                    price = round(random.uniform(100.0, 200.0), 2)
                    quantity = random.randint(1, 100)
                    msg = (
                        f"8=FIX.4.2|35=D|34={self.sequence_number}|49={self.sender_comp_id}|56={self.target_comp_id}|"
                        f"11={order_id}|55={symbol}|54={side}|38={quantity}|44={price}|"
                    )
                    self.sequence_number += 1
                    self.send_message(msg)
                    self.orders.append(msg)
                    time.sleep(random.uniform(0.1, 1.0))

                    if random.random() < 0.2 and self.orders:
                        orig_order_id = self.parse_field(random.choice(self.orders), "11")
                        cancel_msg = (
                            f"8=FIX.4.2|35=F|34={self.sequence_number}|49={self.sender_comp_id}|56={self.target_comp_id}|"
                            f"11={random.randint(100000, 999999)}|41={orig_order_id}|55={symbol}|54={side}|"
                        )
                        self.sequence_number += 1
                        self.send_message(cancel_msg)
                        time.sleep(random.uniform(0.1, 1.0))

                response = self.receive_message()

                if "35=8" in response:
                    self.handle_execution_report(response)
                elif "35=3" in response:
                    self.handle_reject(response)
                elif "35=9" in response:
                    self.handle_cancel_reject(response)

                time.sleep(1)

        except Exception as e:
            self.log(f"Error: {e}")
        finally:
            self.disconnect()


if __name__ == "__main__":
    host = input("Enter Host: ")
    port = int(input("Enter Port: "))
    sender_comp_id = input("Enter SenderCompID: ")
    target_comp_id = input("Enter TargetCompID: ")
    reset_time = input("Enter Sequence Number Reset Time (e.g., 00:00 SGT): ")

    fix_client = FixClient(host, port, sender_comp_id, target_comp_id, reset_time)
    fix_client.run()
