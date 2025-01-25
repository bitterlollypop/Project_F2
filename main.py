import json
import re


class ReportsFileManager:
    def __init__(self, file_name):
        self.file_name = file_name

    def load_reports(self):
        try:
            with open(self.file_name, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_reports(self, reports):
        with open(self.file_name, "w") as file:
            json.dump(reports, file)


class UsersFileManager:
    def __init__(self, file_path="users.json"):
        self.file_path = file_path

    def load_users(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_users(self, users):
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(users, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"خطا در ذخیره‌سازی کاربران: {e}")

    def update_user_info(self, updated_profile):
        users = self.load_users()
        for user in users:
            if user["username"] == updated_profile["username"]:
                user["email"] = updated_profile["email"]
                user["password"] = updated_profile["password"]
                user["cash"] = updated_profile["cash"]
                self.save_users(users)
                break


class ProductsFileManager:
    def __init__(self, file_path="products.json"):
        self.file_path = file_path

    def load_products(self):
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_products(self, products):
        try:
            with open(self.file_path, 'w') as f:
                json.dump(products, f, indent=4)
        except Exception as e:
            print(f"خطا در ذخیره‌سازی اطلاعات: {e}")

    def add_product(self, new_product):
        products = self.load_products()
        if products:
            new_product['id'] = max(product['id'] for product in products) + 1
        else:
            new_product['id'] = 1

        products.append(new_product)
        self.save_products(products)
        print(f"محصول با آیدی {new_product['id']} با موفقیت اضافه شد.")

    def update_product_stock(self, product_id, quantity):
        products = self.load_products()
        for product in products:
            if product['id'] == product_id:
                product['stock'] -= quantity
                self.save_products(products)
                print(f"موجودی محصول {product['brand']} {product['model']} به روز شد.")
                return
        print("محصول مورد نظر یافت نشد.")


class Users:
    def __init__(self, user_manager):
        self.user_manager = user_manager
        self.logged_in_user = None

    def login(self):
        try:
            username = input("نام کاربری خود را وارد کنید: ")
            password = input("رمز عبور خود را وارد کنید: ")
            role = input("نقش خود را انتخاب کنید (1: ادمین، 2: مشتری): ")

            users = self.user_manager.load_users()
            for user in users:
                if user['username'] == username and user['password'] == password:
                    if (role == '1' and user['role'] == 'admin') or (role == '2' and user['role'] == 'customer'):
                        self.logged_in_user = user
                        print(f"ورود موفقیت‌آمیز! خوش آمدید، {username}.")

                        product_manager = ProductsFileManager("products.json")

                        if role == '2':
                            customer = Customer(product_manager, self.user_manager)
                            customer.set_profile(user)
                            customer.customer_menu()
                        elif role == '1':
                            admin = Admin(self.user_manager, product_manager)
                            admin.admin_menu()
                        return
            print("نام کاربری یا رمز عبور اشتباه است یا نقش انتخاب‌شده درست نیست.")
        except Exception as e:
            print(f"خطا در ورود: {e}")
            return False

    def register(self):
        try:
            username = input("نام کاربری: ")
            password = input("رمز عبور: ")
            email = input("ایمیل: ")
            role = input("نقش خود را انتخاب کنید(1: ادمین، 2: مشتری): ")

            new_user = {
                "username": username,
                "password": password,
                "email": email,
                "role": "admin" if role == '1' else "customer",
                "cash": 0
            }

            users = self.user_manager.load_users()

            if any(user['username'] == username for user in users):
                print("نام کاربری قبلاً ثبت شده است.")
                return

            users.append(new_user)
            self.user_manager.save_users(users)
            print("ثبت‌نام با موفقیت انجام شد.")
        except Exception as e:
            print(f"خطا در ثبت‌نام: {e}")

    @staticmethod
    def validate_email(email):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(email_regex, email) is not None

    def update_user_info(self, updated_user):
        users = self.user_manager.load_users()
        for i, user in enumerate(users):
            if user['username'] == updated_user['username']:
                users[i] = updated_user
                self.user_manager.save_users(users)
                print(f"اطلاعات {updated_user['username']} با موفقیت بروزرسانی شد.")
                return
        print("کاربر یافت نشد.")


class Admin(Users):
    def __init__(self, user_manager, product_manager):
        super().__init__(user_manager)
        self.product_manager = product_manager

    def admin_menu(self):
        while True:
            print("\n--- منوی ادمین ---")
            print("1. مشاهده‌ی محصولات")
            print("2. مدیریت کاربران")
            print("3. افزودن محصول جدید")
            print("4. حذف محصول")
            print("5. افزودن ادمین جدید")
            print("6. بروزرسانی قیمت‌ها")
            print("7. بروزرسانی موجودی‌ها")
            print("8. مشاهده گزارش‌ها")
            print("9. بازگشت به منوی اصلی")
            choice = input("لطفاً یک گزینه را انتخاب کنید: ")

            if choice == "1":
                self.view_product()
            elif choice == "2":
                self.manage_users()
            elif choice == "3":
                self.add_product()
            elif choice == "4":
                self.remove_product()
            elif choice == "5":
                self.add_new_admin()
            elif choice == "6":
                self.update_products_price()
            elif choice == "7":
                self.update_products_stock()
            elif choice == "8":
                self.view_reports()
            elif choice == "9":
                break
            else:
                print("عدد وارد شده، نامعتبر است.")

    def view_product(self):
        print("\n--- محصولات موجود ---")
        products = self.product_manager.load_products()
        for product in products:
            print(f"{product['brand']} {product['model']} - قیمت: {product['price']} - موجودی: {product['stock']}")

    def add_product(self):
        new_product = {
            "product_type": input("نوع محصول: "),
            "brand": input("برند: "),
            "model": input("مدل: "),
            "price": float(input("قیمت: ")),
            "year": int(input("سال: ")),
            "specifications": {
                "Engine": input("مشخصات موتور: "),
                "Transmission": input("نوع گیربکس: "),
                "Seats": int(input("تعداد صندلی: "))
            },
            "stock": int(input("موجودی: "))
        }
        self.product_manager.add_product(new_product)

    def manage_users(self):
        users = self.user_manager.load_users()
        if not users:
            print("هیچ کاربری ثبت نشده است.")
            return

        print("\n--- لیست کاربران ---")
        for user in users:
            print(f"نام کاربری: {user['username']}, نقش: {user['role']}")

    def remove_product(self):
        model = input("مدل محصولی که می‌خواهید حذف کنید: ")
        products = self.product_manager.load_products()
        products = [p for p in products if p['model'] != model]
        self.product_manager.save_products(products)
        print("محصول با موفقیت حذف شد.")

    def update_products_price(self):
        products = self.product_manager.load_products()
        model = input("مدل محصولی که می‌خواهید قیمت آن را بروزرسانی کنید: ")
        new_price = float(input("قیمت جدید: "))

        for product in products:
            if product['model'] == model:
                product['price'] = new_price
                print(f"قیمت محصول {model} به {new_price} تغییر یافت.")
                break
        else:
            print(f"محصولی با مدل {model} پیدا نشد.")

        self.product_manager.save_products(products)

    def update_products_stock(self):
        products = self.product_manager.load_products()
        model = input("مدل محصولی که می‌خواهید موجودی آن را بروزرسانی کنید: ")
        new_stock = int(input("موجودی جدید: "))

        for product in products:
            if product['model'] == model:
                product['stock'] = new_stock
                print(f"موجودی محصول {model} به {new_stock} تغییر یافت.")
                break
        else:
            print(f"محصولی با مدل {model} پیدا نشد.")

        self.product_manager.save_products(products)

    def add_new_admin(self):
        username = input("نام کاربری جدید ادمین: ")
        password = input("رمز عبور جدید: ")
        email = input("ایمیل جدید: ")

        new_admin = {
            "username": username,
            "password": password,
            "email": email,
            "role": "admin"
        }

        users = self.user_manager.load_users()
        users.append(new_admin)
        self.user_manager.save_users(users)
        print(f"ادمین جدید با نام کاربری {username} با موفقیت اضافه شد.")

    def view_reports(self):
        reports_manager = ReportsFileManager("reports.json")
        reports = reports_manager.load_reports()

        if not reports:
            print("لیست گزارشات خالی است.")
        else:
            print("\n--- لیست گزارشات ---")
            for report in reports:
                print(
                    f"شناسه سفارش: {report['order_id']}, تاریخ: {report['date']}, مبلغ: {report['amount']} USD, وضعیت: {report['status']}")


class Customer(Users):
    def __init__(self, product_manager, user_manager):
        super().__init__(user_manager)
        self.product_manager = product_manager
        self.cart = Cart(self.logged_in_user)
        self.profile = {}

    def set_profile(self, user_profile):
        self.profile = user_profile

    def view_product(self):
        print("\n--- محصولات موجود ---")
        products = self.product_manager.load_products()
        for index, product in enumerate(products, 1):
            print(
                f"{index}. {product['brand']} {product['model']} - قیمت: {product['price']} - موجودی: {product['stock']}")

    def customer_menu(self):
        while True:
            print("\n--- منوی مشتری ---")
            print("1. مشاهده‌ی محصولات")
            print("2. افزودن محصول به سبد خرید")
            print("3. مشاهده‌ی سبد خرید")
            print("4. بروزرسانی پروفایل")
            print("5. خروج")
            choice = input("لطفاً یک گزینه را انتخاب کنید: ")

            if choice == "1":
                self.view_product()
            elif choice == "2":
                self.add_to_cart()
            elif choice == "3":
                self.show_cart_menu()
            elif choice == "4":
                self.update_profile()
            elif choice == "5":
                break
            else:
                print("عدد وارد شده، نامعتبر است.")

    def add_to_cart(self):
        self.view_product()

        try:
            product_index = int(input("لطفاً شماره محصولی که می‌خواهید به سبد خرید اضافه کنید را وارد کنید: "))
            products = self.product_manager.load_products()
            if product_index < 1 or product_index > len(products):
                print("محصول نامعتبر است.")
                return

            selected_product = products[product_index - 1]
            quantity = int(input(
                f"چند عدد از محصول {selected_product['brand']} {selected_product['model']} می‌خواهید به سبد خرید اضافه کنید؟ "))

            if quantity > 0 and quantity <= selected_product['stock']:
                self.cart.add_item(selected_product, quantity)
                self.product_manager.save_products(products)
                print(f"محصول {selected_product['brand']} {selected_product['model']} به سبد خرید اضافه شد.")
            else:
                print(
                    f"متاسفانه تعداد {quantity} از {selected_product['brand']} {selected_product['model']} در انبار موجود نیست.")
        except ValueError:
            print("لطفاً یک عدد صحیح وارد کنید.")

    def show_cart_menu(self):
        self.cart.view_cart()
        self.cart.show_cart_menu()

    def update_profile(self):
        if not self.profile:
            print("پروفایل شما هنوز تنظیم نشده است.")
            new_username = input("نام کاربری خود را وارد کنید: ")
            new_email = input("ایمیل خود را وارد کنید: ")
            new_password = input("رمز عبور جدید خود را وارد کنید: ")
            new_cash = float(input("موجودی پول نقد خود را وارد کنید: "))
            self.profile = {"username": new_username, "email": new_email, "password": new_password, "cash": new_cash}
            print("پروفایل شما با موفقیت ایجاد شد.")
        else:
            print(
                f"پروفایل فعلی شما: نام کاربری: {self.profile['username']}, ایمیل: {self.profile['email']}, موجودی: {self.profile['cash']} دلار")

            new_username = input("نام کاربری جدید (در صورت تمایل وارد کنید): ")
            new_email = input("ایمیل جدید (در صورت تمایل وارد کنید): ")
            new_password = input("رمز عبور جدید (در صورت تمایل وارد کنید): ")
            new_cash = input("موجودی پول نقد جدید (در صورت تمایل وارد کنید): ")

            if new_username:
                self.profile["username"] = new_username
            if new_email:
                self.profile["email"] = new_email
            if new_password:
                self.profile["password"] = new_password
            if new_cash:
                self.profile["cash"] = float(new_cash)

            self.user_manager.update_user_info(self.profile)

            print("پروفایل شما با موفقیت بروزرسانی شد.")
            print(
                f"نام کاربری جدید: {self.profile['username']}, ایمیل جدید: {self.profile['email']}, موجودی جدید: {self.profile['cash']} دلار")


class Cart:
    def __init__(self, user_profile):
        self.user_profile = user_profile
        self.items = []

    def add_item(self, product, quantity):
        """
        اضافه کردن محصول به سبد خرید
        """
        if quantity <= product['stock']:
            for item in self.items:
                if item['product']['id'] == product['id']:
                    item['quantity'] += quantity
                    print(f"تعداد محصول {product['brand']} {product['model']} در سبد خرید بروزرسانی شد.")
                    return

            self.items.append({"product": product, "quantity": quantity})
            print(f"محصول {product['brand']} {product['model']} به سبد خرید اضافه شد.")
        else:
            print(f"موجودی کافی برای محصول {product['brand']} {product['model']} وجود ندارد.")

    def remove_item(self, product_id):
        """
        حذف محصول از سبد خرید
        """
        for item in self.items:
            if item['product']['id'] == product_id:
                self.items.remove(item)
                print(f"محصول {item['product']['brand']} {item['product']['model']} از سبد خرید حذف شد.")
                return

        print("محصول مورد نظر در سبد خرید یافت نشد.")

    def view_cart(self):
        """
        نمایش محصولات داخل سبد خرید
        """
        if not self.items:
            print("سبد خرید شما خالی است.")
            return

        print("\n--- سبد خرید شما ---")
        total_price = 0
        for index, item in enumerate(self.items, 1):
            product = item['product']
            quantity = item['quantity']
            price = product['price'] * quantity
            total_price += price
            print(f"{index}. {product['brand']} {product['model']} - تعداد: {quantity} - قیمت کل: {price}")

        print(f"مجموع قیمت: {total_price}")

    def checkout(self, product_manager):
        """
        نهایی‌سازی خرید و بروزرسانی موجودی‌ها
        """
        if not self.items:
            print("سبد خرید شما خالی است. امکان خرید وجود ندارد.")
            return

        total_price = 0
        for item in self.items:
            product = item['product']
            quantity = item['quantity']
            total_price += product['price'] * quantity

        if self.user_profile['cash'] < total_price:
            print(f"موجودی نقدی شما کافی نیست. مجموع قیمت: {total_price} - موجودی شما: {self.user_profile['cash']}")
            return

        for item in self.items:
            product = item['product']
            quantity = item['quantity']

            if quantity > product['stock']:
                print(f"محصول {product['brand']} {product['model']} به تعداد کافی در انبار موجود نیست.")
                return

            product['stock'] -= quantity

        self.user_profile['cash'] -= total_price
        product_manager.save_products(product_manager.load_products())

        self.items = []
        print("خرید شما با موفقیت انجام شد. موجودی نقدی شما بروزرسانی شد.")

    def show_cart_menu(self):
        """
        منوی مدیریت سبد خرید
        """
        while True:
            print("\n--- مدیریت سبد خرید ---")
            print("1. حذف محصول از سبد خرید")
            print("2. نهایی‌سازی خرید")
            print("3. بازگشت به منوی قبل")

            choice = input("لطفاً یک گزینه را انتخاب کنید: ")

            if choice == "1":
                self.view_cart()
                try:
                    product_id = int(input("شناسه محصولی که می‌خواهید حذف کنید را وارد کنید: "))
                    self.remove_item(product_id)
                except ValueError:
                    print("لطفاً یک عدد صحیح وارد کنید.")
            elif choice == "2":
                product_manager = ProductsFileManager("products.json")
                self.checkout(product_manager)
            elif choice == "3":
                break
            else:
                print("عدد واردشده، نامعتبر است.")


if __name__ == "__main__":
    users_manager = UsersFileManager("users.json")
    products_manager = ProductsFileManager("products.json")

    users = Users(users_manager)

    while True:
        print("\n--- خوش آمدید ---")
        print("1. ورود به حساب کاربری")
        print("2. ثبت‌نام")
        print("3. خروج")
        choice = input("لطفاً یک گزینه را انتخاب کنید: ")

        if choice == '1':
            role = users.login()
        elif choice == '2':
            users.register()
        elif choice == '3':
            print("خداحافظ!")
            break
        else:
            print("عدد واردشده، نامعتبر است.")