import re

class SupplyChainChatbot:
    def __init__(self):
        self.greetings = ['hello', 'hi', 'hey', 'greetings']
        self.farewells = ['bye', 'goodbye', 'see you', 'exit']
        self.commands = {
            'inventory': self.check_inventory,
            'order status': self.order_status,
            'shipment': self.shipment_status,
            'help': self.help_message
        }
        self.inventory_data = {
            'product 1': 100,
            'product 2': 50,
            'product 3': 0
        }
        self.orders = {
            '1001': 'shipped',
            '1002': 'processing',
            '1003': 'delivered'
        }
        self.shipments = {
            'shipment1': 'in transit',
            'shipment2': 'delivered',
            'shipment3': 'delayed'
        }

    def respond(self, message):
        message = message.lower()
        if any(greet in message for greet in self.greetings):
            return "Hello! How can I assist you with your supply chain today?"
        if any(farewell in message for farewell in self.farewells):
            return "Goodbye! Have a great day."
        for command in self.commands:
            if command in message:
                return self.commands[command](message)
        return "I'm sorry, I didn't understand that. You can ask about inventory, order status, or shipment."

    def check_inventory(self, message):
        for item in self.inventory_data:
            if item in message:
                qty = self.inventory_data[item]
                if qty > 0:
                    return f"The inventory for {item} is {qty} units."
                else:
                    return f"Sorry, {item} is currently out of stock."
        return "Please specify the product you want to check inventory for."

    def order_status(self, message):
        order_numbers = re.findall(r'\b\d{4}\b', message)
        if order_numbers:
            order_num = order_numbers[0]
            status = self.orders.get(order_num, None)
            if status:
                return f"Order {order_num} is currently {status}."
            else:
                return f"No information found for order {order_num}."
        return "Please provide a valid 4-digit order number."

    def shipment_status(self, message):
        for shipment in self.shipments:
            if shipment in message:
                status = self.shipments[shipment]
                return f"Shipment {shipment} status is {status}."
        return "Please specify the shipment ID you want to check."

    def help_message(self, message):
        return ("You can ask me about:\n"
                "- Inventory status of products (e.g., 'Check inventory for product 1')\n"
                "- Order status by providing order number (e.g., 'What is the status of order 1001?')\n"
                "- Shipment status by shipment ID (e.g., 'Shipment status for shipment1')")

def demand_forecast(scm):
    # Dummy demand forecast: returns a dict of product_id to forecasted demand
    forecast = {}
    for product_id, (product, quantity) in scm.inventory.products.items():
        # Simple forecast: current quantity * random factor (e.g., 1.2)
        forecast[product_id] = int(quantity * 1.2)
    return forecast
