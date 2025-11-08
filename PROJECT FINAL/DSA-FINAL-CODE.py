import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from datetime import datetime

class Product:
    """Product class to represent items in the store"""
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def __str__(self):
        return f"{self.name} - ₱{self.price:.2f} (Qty: {self.quantity})"

class ProductNode:
    """Node for product linked list"""
    def __init__(self, product):
        self.product = product
        self.next = None

class SalesNode:
    """Node for sales history linked list"""
    def __init__(self, sale_data):
        self.sale_data = sale_data
        self.next = None

class CartNode:
    """Node for cart linked list"""
    def __init__(self, product, quantity):
        self.product = product
        self.quantity = quantity
        self.subtotal = product.price * quantity
        self.next = None

class CashierSystem:
    def __init__(self):
        self.products_head = None
        self.sales_head = None
        self.cart_head = None
        self.current_user = "123"
        self.initialize_sample_data()
    
    def initialize_sample_data(self):
        """Initialize the system with sample products using linked list"""
        sample_products = [
            Product("Pancit Canton", 25.50, 5),  
            Product("Sardines", 12.25, 150),
            Product("Softdrinks", 65.99, 30),
            Product("C2", 45.00, 3), 
            Product("Eggs", 220.00, 60),
            Product("Coffee", 189.50, 25),
            Product("Sugar", 55.75, 50),
            Product("Rice", 62.50, 35)
        ]
        
        for product in sample_products:
            self.add_product_to_list(product)
    
    def add_product_to_list(self, product):
        """Add product to the linked list"""
        new_node = ProductNode(product)
        if not self.products_head:
            self.products_head = new_node
        else:
            current = self.products_head
            while current.next:
                current = current.next
            current.next = new_node
    
    def find_product(self, product_name):
        """Find a product by name using linked list traversal"""
        current = self.products_head
        while current:
            if current.product.name.lower() == product_name.lower():
                return current.product
            current = current.next
        return None
    
    def find_product_by_name(self, search_term):
        """Find products by name (partial match) using linked list"""
        results = []
        current = self.products_head
        while current:
            if search_term.lower() in current.product.name.lower():
                results.append(current.product)
            current = current.next
        return results
    
    def get_all_products(self):
        """Get all products from linked list"""
        products = []
        current = self.products_head
        while current:
            products.append(current.product)
            current = current.next
        return products
    
    def add_to_cart(self, product_name, quantity):
        """Add product to current transaction using linked list"""
        product = self.find_product(product_name)
        if product:
            if product.quantity >= quantity:
                # Check if product already in cart
                current = self.cart_head
                while current:
                    if current.product.name == product.name:
                        current.quantity += quantity
                        current.subtotal = current.product.price * current.quantity
                        return True, f"Updated {product.name} quantity to {current.quantity}"
                    current = current.next
                
                # Add new item to cart
                new_node = CartNode(product, quantity)
                new_node.next = self.cart_head
                self.cart_head = new_node
                return True, f"Added {quantity} x {product.name} to cart"
            else:
                return False, f"Only {product.quantity} available in stock"
        return False, "Product not found"
    
    def get_cart_items(self):
        """Get all items from cart linked list"""
        items = []
        current = self.cart_head
        while current:
            items.append({
                'product': current.product,
                'quantity': current.quantity,
                'subtotal': current.subtotal
            })
            current = current.next
        return items
    
    def clear_cart(self):
        """Clear current transaction by resetting linked list"""
        self.cart_head = None
    
    def get_cart_total(self):
        """Calculate total from cart linked list"""
        total = 0
        current = self.cart_head
        while current:
            total += current.subtotal
            current = current.next
        return total
    
    def add_sale_to_history(self, sale_data):
        """Add sale to sales history linked list"""
        new_node = SalesNode(sale_data)
        if not self.sales_head:
            self.sales_head = new_node
        else:
            new_node.next = self.sales_head
            self.sales_head = new_node
    
    def get_sales_history(self):
        """Get all sales from linked list"""
        sales = []
        current = self.sales_head
        while current:
            sales.append(current.sale_data)
            current = current.next
        return sales
    
    def process_sale(self):
        """Process the current transaction"""
        if not self.cart_head:
            return False, "Cart is empty"
        
        total = self.get_cart_total()
        
        # Update inventory and create sale record
        current = self.cart_head
        items_list = []
        while current:
            current.product.quantity -= current.quantity
            items_list.append(f"{current.quantity}x {current.product.name}")
            current = current.next
        
        items_str = ", ".join(items_list)
        sale_record = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {items_str} - Total: ₱{total:.2f}"

        self.add_sale_to_history(sale_record)
        self.clear_cart()
        
        return True, total
    
    def get_low_stock_items(self, threshold=10):
        """Get products with low stock using linked list traversal"""
        low_stock = []
        current = self.products_head
        while current:
            if current.product.quantity <= threshold:
                low_stock.append(current.product)
            current = current.next
        return low_stock
    
    def add_product(self, name, price, quantity):
        """Add new product to inventory linked list"""
        if self.find_product(name):
            return False, f"Product '{name}' already exists!"
        
        new_product = Product(name, price, quantity)
        self.add_product_to_list(new_product)
        return True, f"Successfully added {name} to inventory"
    
    def change_price(self, product_name, new_price):
        """Change product price using linked list"""
        product = self.find_product(product_name)
        if product:
            old_price = product.price
            product.price = new_price
            return True, f"Changed {product.name} price from ₱{old_price:.2f} to ₱{new_price:.2f}"
        return False, "Product not found"
    
    def restock_product(self, product_name, quantity):
        """Restock a product using linked list"""
        product = self.find_product(product_name)
        if product:
            product.quantity += quantity
            return True, f"Restocked {product.name}. New quantity: {product.quantity}"
        return False, "Product not found"

class SimpleCashierGUI:
    def __init__(self, root):
        self.root = root
        self.cashier = CashierSystem()
        self.setup_gui()
        self.update_displays()
    
    def setup_gui(self):
        self.root.title("Joan's Store")
        self.root.geometry("900x650")
        self.root.configure(bg='white')
        
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text="Joan's Store", 
                               font=("Arial", 20, "bold"))
        title_label.pack(side=tk.LEFT)
        
        user_label = ttk.Label(header_frame, text=f"Welcome, {self.cashier.current_user}", 
                              font=("Arial", 12))
        user_label.pack(side=tk.RIGHT)
        
        self.time_label = ttk.Label(header_frame, text="", font=("Arial", 10))
        self.time_label.pack(side=tk.BOTTOM, anchor='e')
        self.update_time()
        
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=5)
 
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        left_frame = ttk.Frame(content_frame, width=400)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        right_frame = ttk.Frame(content_frame, width=400)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        self.setup_search_section(left_frame)
        self.setup_quick_actions(left_frame)
        
        self.setup_transaction_section(right_frame)
        self.setup_actions_section(right_frame)
    
    def setup_search_section(self, parent):
        """Setup product search section"""
        search_frame = ttk.LabelFrame(parent, text="Search Product", padding="10")
        search_frame.pack(fill=tk.X, pady=(0, 10))

        search_row = ttk.Frame(search_frame)
        search_row.pack(fill=tk.X, pady=5)
        
        ttk.Label(search_row, text="Product Name:").pack(side=tk.LEFT)
        self.search_var = tk.StringVar()
        search_entry = ttk.Entry(search_row, textvariable=self.search_var, width=20)
        search_entry.pack(side=tk.LEFT, padx=5)
        search_entry.bind('<Return>', lambda e: self.search_products())
        
        ttk.Button(search_row, text="Search", command=self.search_products).pack(side=tk.LEFT)
        
        self.search_results = scrolledtext.ScrolledText(search_frame, height=8, width=40)
        self.search_results.pack(fill=tk.BOTH, expand=True, pady=5)
        
        add_cart_frame = ttk.Frame(search_frame)
        add_cart_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(add_cart_frame, text="Product Name:").pack(side=tk.LEFT)
        self.cart_name_var = tk.StringVar()

        self.product_combo = ttk.Combobox(add_cart_frame, textvariable=self.cart_name_var, width=15)
        self.update_product_combo()
        self.product_combo.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(add_cart_frame, text="Quantity:").pack(side=tk.LEFT, padx=(10, 0))
        self.cart_qty_var = tk.StringVar(value="1")
        ttk.Entry(add_cart_frame, textvariable=self.cart_qty_var, width=8).pack(side=tk.LEFT, padx=2)
        
        ttk.Button(add_cart_frame, text="Add to Cart", command=self.add_to_cart).pack(side=tk.LEFT, padx=10)
    
    def setup_quick_actions(self, parent):
        """Setup quick actions section"""
        actions_frame = ttk.LabelFrame(parent, text="Quick Actions", padding="10")
        actions_frame.pack(fill=tk.BOTH, expand=True)

        actions = [
            ("Add Item", self.show_add_item),
            ("Sales History", self.show_sales_history),
            ("Stock Management", self.show_stock_management)
        ]
        
        for text, command in actions:
            ttk.Button(actions_frame, text=text, command=command).pack(fill=tk.X, pady=2)
        
        self.alert_label = ttk.Label(actions_frame, text="", foreground='black', font=("Arial", 9))
        self.alert_label.pack(pady=5)
    
    def setup_transaction_section(self, parent):
        """Setup current transaction section"""
        trans_frame = ttk.LabelFrame(parent, text="Current Transaction", padding="10")
        trans_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.cart_text = scrolledtext.ScrolledText(trans_frame, height=12, width=40)
        self.cart_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_actions_section(self, parent):
        """Setup action buttons section"""
        actions_frame = ttk.Frame(parent)
        actions_frame.pack(fill=tk.X)

        ttk.Button(actions_frame, text="Generate Receipt", 
                  command=self.generate_receipt).pack(fill=tk.X, pady=2)
        
        ttk.Button(actions_frame, text="Clear Cart", 
                  command=self.clear_cart).pack(fill=tk.X, pady=2)
        
        self.alert_button = ttk.Button(actions_frame, text="Low Stock Alert", 
                                      command=self.show_low_stock)
        self.alert_button.pack(fill=tk.X, pady=2)
        
        ttk.Button(actions_frame, text="Logout", 
                  command=self.logout).pack(fill=tk.X, pady=2)
    
    def update_time(self):
        """Update the current date and time"""
        current_time = datetime.now().strftime("%A, %B %d, %Y\n%I:%M:%S %p")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
    
    def update_displays(self):
        """Update all displays"""
        self.update_cart_display()
        self.check_low_stock()
        self.update_product_combo()
    
    def update_product_combo(self):
        """Update product combobox from linked list"""
        products = self.cashier.get_all_products()
        self.product_combo['values'] = [product.name for product in products]
    
    def update_cart_display(self):
        """Update the cart display from linked list"""
        self.cart_text.delete(1.0, tk.END)
        
        cart_items = self.cashier.get_cart_items()
        if not cart_items:
            self.cart_text.insert(tk.END, "Cart is empty\n")
            return
        
        total = 0
        self.cart_text.insert(tk.END, "Current Items:\n")
        self.cart_text.insert(tk.END, "=" * 30 + "\n")
        
        for item in cart_items:
            product = item['product']
            quantity = item['quantity']
            subtotal = item['subtotal']
            total += subtotal
            
            self.cart_text.insert(tk.END, 
                f"{product.name} x{quantity}\n"
                f"  ₱{product.price:.2f} each = ₱{subtotal:.2f}\n\n"
            )
        
        self.cart_text.insert(tk.END, "=" * 30 + "\n")
        self.cart_text.insert(tk.END, f"TOTAL: ₱{total:.2f}\n")
    
    def check_low_stock(self):
        """Check and display low stock alerts using linked list"""
        low_stock = self.cashier.get_low_stock_items()
        if low_stock:
            alert_text = "Low Stock: " + ", ".join([f"{p.name} ({p.quantity})" for p in low_stock])
            self.alert_label.config(text=alert_text)
        else:
            self.alert_label.config(text="All items are well stocked")
    
    def search_products(self):
        """Search for products by name using linked list"""
        search_term = self.search_var.get().strip()
        self.search_results.delete(1.0, tk.END)
        
        if not search_term:
            products = self.cashier.get_all_products()
            self.search_results.insert(tk.END, "All Products:\n")
            self.search_results.insert(tk.END, "=" * 30 + "\n")
        else:
            products = self.cashier.find_product_by_name(search_term)
            self.search_results.insert(tk.END, f"Search Results for '{search_term}':\n")
            self.search_results.insert(tk.END, "=" * 30 + "\n")
        
        if products:
            for product in products:
                stock_status = "LOW STOCK" if product.quantity <= 10 else "In Stock"
                self.search_results.insert(tk.END, 
                    f"Name: {product.name}\n"
                    f"Price: ₱{product.price:.2f}\n"
                    f"Quantity: {product.quantity} ({stock_status})\n"
                    f"{'-'*20}\n"
                )
        else:
            self.search_results.insert(tk.END, "No products found\n")
    
    def add_to_cart(self):
        """Add product to cart using linked list"""
        try:
            product_name = self.cart_name_var.get().strip()
            quantity = int(self.cart_qty_var.get())
            
            if not product_name:
                messagebox.showerror("Error", "Please select a product!")
                return
            
            success, message = self.cashier.add_to_cart(product_name, quantity)
            
            if success:
                messagebox.showinfo("Success", message)
                self.cart_name_var.set("")
                self.cart_qty_var.set("1")
                self.update_displays()
            else:
                messagebox.showerror("Error", message)
                
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid quantity!")
    
    def generate_receipt(self):
        """Generate receipt for current transaction"""
        cart_items = self.cashier.get_cart_items()
        if not cart_items:
            messagebox.showinfo("Info", "Cart is empty!")
            return
        
        success, result = self.cashier.process_sale()
        
        if success:
            receipt_window = tk.Toplevel(self.root)
            receipt_window.title("Receipt")
            receipt_window.geometry("300x400")
            
            receipt_text = scrolledtext.ScrolledText(receipt_window, width=35, height=20)
            receipt_text.pack(padx=10, pady=10)
       
            receipt_text.insert(tk.END, "JOAN'S STORE\n")
            receipt_text.insert(tk.END, "=" * 30 + "\n")
            receipt_text.insert(tk.END, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            receipt_text.insert(tk.END, f"Cashier: {self.cashier.current_user}\n")
            receipt_text.insert(tk.END, "-" * 30 + "\n")
            receipt_text.insert(tk.END, "ITEMS:\n")
            
            for item in cart_items:
                product = item['product']
                receipt_text.insert(tk.END, 
                    f"{product.name} x{item['quantity']}\n"
                    f"  ₱{product.price:.2f} = ₱{item['subtotal']:.2f}\n"
                )
            
            receipt_text.insert(tk.END, "-" * 30 + "\n")
            receipt_text.insert(tk.END, f"TOTAL: ₱{result:.2f}\n")
            receipt_text.insert(tk.END, "=" * 30 + "\n")
            receipt_text.insert(tk.END, "Thank you for shopping!\n")
            
            receipt_text.config(state=tk.DISABLED)
            
            messagebox.showinfo("Success", f"Sale completed! Total: ₱{result:.2f}")
            self.update_displays()
        else:
            messagebox.showerror("Error", result)
    
    def clear_cart(self):
        """Clear the current cart linked list"""
        self.cashier.clear_cart()
        self.update_displays()
        messagebox.showinfo("Success", "Cart cleared!")
    
    def show_low_stock(self):
        """Show low stock items from linked list"""
        low_stock = self.cashier.get_low_stock_items()
        
        alert_window = tk.Toplevel(self.root)
        alert_window.title("Low Stock Alert")
        alert_window.geometry("300x200")
        
        alert_text = scrolledtext.ScrolledText(alert_window, width=35, height=10)
        alert_text.pack(padx=10, pady=10)
        
        if low_stock:
            alert_text.insert(tk.END, "LOW STOCK ITEMS:\n")
            alert_text.insert(tk.END, "=" * 20 + "\n")
            for product in low_stock:
                alert_text.insert(tk.END, f"{product.name}: {product.quantity} left\n")
        else:
            alert_text.insert(tk.END, "All items are well stocked!\n")
        
        alert_text.config(state=tk.DISABLED)
    
    def show_add_item(self):
        """Show add item dialog"""
        self.show_dialog("Add New Item", self.add_item_dialog)
    
    def show_sales_history(self):
        """Show sales history from linked list"""
        self.show_dialog("Sales History", self.sales_history_dialog)
    
    def show_stock_management(self):
        """Show stock management"""
        self.show_dialog("Stock Management", self.stock_management_dialog)
    
    def show_dialog(self, title, dialog_function):
        """Helper to show dialog windows"""
        dialog_window = tk.Toplevel(self.root)
        dialog_window.title(title)
        dialog_window.geometry("400x300")
        dialog_function(dialog_window)
    
    def add_item_dialog(self, window):
        """Dialog for adding new items"""
        ttk.Label(window, text="Add New Product", font=("Arial", 12, "bold")).pack(pady=10)
        
        form_frame = ttk.Frame(window)
        form_frame.pack(pady=10)
        
        ttk.Label(form_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        name_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=name_var, width=20).grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Price (₱):").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        price_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=price_var, width=20).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Quantity:").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        qty_var = tk.StringVar()
        ttk.Entry(form_frame, textvariable=qty_var, width=20).grid(row=2, column=1, padx=5, pady=5)
        
        def add_product():
            try:
                name = name_var.get().strip()
                price = float(price_var.get())
                quantity = int(qty_var.get())
                
                if name:
                    success, result = self.cashier.add_product(name, price, quantity)
                    if success:
                        messagebox.showinfo("Success", result)
                        window.destroy()
                        self.search_products()
                        self.update_displays()
                    else:
                        messagebox.showerror("Error", result)
                else:
                    messagebox.showerror("Error", "Please enter product name!")
            except ValueError:
                messagebox.showerror("Error", "Please enter valid price and quantity!")
        
        ttk.Button(window, text="Add Product", command=add_product).pack(pady=10)
    
    def sales_history_dialog(self, window):
        """Dialog for sales history from linked list"""
        ttk.Label(window, text="Sales History", font=("Arial", 12, "bold")).pack(pady=10)
        
        history_text = scrolledtext.ScrolledText(window, width=45, height=12)
        history_text.pack(padx=10, pady=10)
        
        sales_history = self.cashier.get_sales_history()
        if sales_history:
            for i, sale in enumerate(sales_history, 1):
                history_text.insert(tk.END, f"{i}. {sale}\n")
        else:
            history_text.insert(tk.END, "No sales history yet.")
        
        history_text.config(state=tk.DISABLED)
    
    def stock_management_dialog(self, window):
        """Dialog for stock management"""
        ttk.Label(window, text="Stock Management", font=("Arial", 12, "bold")).pack(pady=10)
        
        price_frame = ttk.Frame(window)
        price_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(price_frame, text="Change Price - Product:").pack(side=tk.LEFT)
        price_name_var = tk.StringVar()
        price_combo = ttk.Combobox(price_frame, textvariable=price_name_var, width=15)
        price_combo['values'] = [product.name for product in self.cashier.get_all_products()]
        price_combo.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(price_frame, text="New Price (₱):").pack(side=tk.LEFT, padx=(10, 0))
        new_price_var = tk.StringVar()
        ttk.Entry(price_frame, textvariable=new_price_var, width=8).pack(side=tk.LEFT, padx=2)
        
        def change_price():
            try:
                product_name = price_name_var.get().strip()
                new_price = float(new_price_var.get())
                success, result = self.cashier.change_price(product_name, new_price)
                if success:
                    messagebox.showinfo("Success", result)
                    self.search_products()
                else:
                    messagebox.showerror("Error", result)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers!")
        
        ttk.Button(price_frame, text="Change", command=change_price).pack(side=tk.LEFT, padx=10)
        
        restock_frame = ttk.Frame(window)
        restock_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(restock_frame, text="Restock - Product:").pack(side=tk.LEFT)
        restock_name_var = tk.StringVar()
        restock_combo = ttk.Combobox(restock_frame, textvariable=restock_name_var, width=15)
        restock_combo['values'] = [product.name for product in self.cashier.get_all_products()]
        restock_combo.pack(side=tk.LEFT, padx=2)
        
        ttk.Label(restock_frame, text="Quantity:").pack(side=tk.LEFT, padx=(10, 0))
        restock_qty_var = tk.StringVar()
        ttk.Entry(restock_frame, textvariable=restock_qty_var, width=8).pack(side=tk.LEFT, padx=2)
        
        def restock():
            try:
                product_name = restock_name_var.get().strip()
                quantity = int(restock_qty_var.get())
                success, result = self.cashier.restock_product(product_name, quantity)
                if success:
                    messagebox.showinfo("Success", result)
                    self.search_products()
                else:
                    messagebox.showerror("Error", result)
            except ValueError:
                messagebox.showerror("Error", "Please enter valid numbers!")
        
        ttk.Button(restock_frame, text="Restock", command=restock).pack(side=tk.LEFT, padx=10)
    
    def logout(self):
        """Logout from the system"""
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            self.root.quit()

def main():
    root = tk.Tk()
    app = SimpleCashierGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()