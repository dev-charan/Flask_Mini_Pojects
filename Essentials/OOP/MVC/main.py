# main.py

from controller import ProdcutController

def main():
    controller = ProdcutController()

    while True:
        print("\n📦 PRODUCT MANAGER")
        print("1. Add Product")
        print("2. List Products")
        print("3. Update Product")
        print("4. Delete Product")
        print("5. Exit")

        choice = input("Select an option: ")

        if choice == "1":
            pid = int(input("Enter Product ID: "))
            name = input("Enter Product Name: ")
            price = float(input("Enter Product Price: "))
            print(controller.create_product(pid, name, price))

        elif choice == "2":
            products = controller.get_all_product()
            if not products:
                print("⚠️ No products found.")
            for p in products:
                print(p)

        elif choice == "3":
            pid = int(input("Enter Product ID to update: "))
            new_name = input("Enter New Name: ")
            new_price = float(input("Enter New Price: "))
            print(controller.update_product(pid, new_name, new_price))

        elif choice == "4":
            pid = int(input("Enter Product ID to delete: "))
            print(controller.delete_product(pid))

        elif choice == "5":
            print("👋 Exiting...")
            break

        else:
            print("❌ Invalid choice. Try again.")

if __name__ == "__main__":
    main()
