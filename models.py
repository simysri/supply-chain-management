class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

    def __str__(self):
        return f"Product(id={self.product_id}, name={self.name}, price={self.price})"


class Supplier:
    def __init__(self, supplier_id, name, contact_info):
        self.supplier_id = supplier_id
        self.name = name
        self.contact_info = contact_info

    def __str__(self):
        return f"Supplier(id={self.supplier_id}, name={self.name}, contact={self.contact_info})"


class Inventory:
    def __init__(self):
        self.products = {}  # product_id -> (Product, quantity)

    def add_product(self, product, quantity):
        if product.product_id in self.products:
            self.products[product.product_id] = (product, self.products[product.product_id][1] + quantity)
        else:
            self.products[product.product_id] = (product, quantity)

    def remove_product(self, product_id, quantity):
        if product_id in self.products:
            product, current_quantity = self.products[product_id]
            if quantity > current_quantity:
                raise ValueError("Not enough quantity in inventory")
            self.products[product_id] = (product, current_quantity - quantity)
        else:
            raise ValueError("Product not found in inventory")

    def get_quantity(self, product_id):
        if product_id in self.products:
            return self.products[product_id][1]
        return 0

    def update_quantity(self, product_id, quantity):
        if product_id in self.products:
            product, _ = self.products[product_id]
            self.products[product_id] = (product, quantity)
        else:
            raise ValueError("Product not found in inventory")

    def __str__(self):
        inventory_list = []
        for product_id, (product, quantity) in self.products.items():
            inventory_list.append(f"{product} - Quantity: {quantity}")
        return "\n".join(inventory_list)


class Order:
    def __init__(self, order_id, product, quantity, supplier):
        self.order_id = order_id
        self.product = product
        self.quantity = quantity
        self.supplier = supplier
        self.status = "Pending"

    def process_order(self, inventory):
        if inventory.get_quantity(self.product.product_id) >= self.quantity:
            inventory.remove_product(self.product.product_id, self.quantity)
            self.status = "Completed"
        else:
            self.status = "Failed - Insufficient inventory"

    def __str__(self):
        return f"Order(id={self.order_id}, product={self.product.name}, quantity={self.quantity}, supplier={self.supplier.name}, status={self.status})"


class SupplyChainManagement:
    def __init__(self):
        self.inventory = Inventory()
        self.suppliers = {}
        self.orders = {}

    def add_supplier(self, supplier):
        self.suppliers[supplier.supplier_id] = supplier

    def add_product_to_inventory(self, product, quantity):
        self.inventory.add_product(product, quantity)

    def update_product_quantity(self, product_id, quantity):
        self.inventory.update_quantity(product_id, quantity)

    def place_order(self, order_id, product_id, quantity, supplier_id):
        if product_id not in self.inventory.products:
            raise ValueError("Product not found in inventory")
        if supplier_id not in self.suppliers:
            raise ValueError("Supplier not found")
        product = self.inventory.products[product_id][0]
        supplier = self.suppliers[supplier_id]
        order = Order(order_id, product, quantity, supplier)
        order.process_order(self.inventory)
        self.orders[order_id] = order
        return order

    def __str__(self):
        return f"Inventory:\n{self.inventory}\n\nSuppliers:\n" + \
               "\n".join(str(s) for s in self.suppliers.values()) + \
               "\n\nOrders:\n" + "\n".join(str(o) for o in self.orders.values())
