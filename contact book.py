Contacts={}
def add_contact():
    Name= input("Enter Name:")
    if Name in Contacts:
        print(f"Contact {Name} already exist")
    else:
        try:
            Phone= int(input("Enter the contact number:"))
            Email= input("Enter email:")
            Address= input("Enter Address:")
            Contacts[Name]= {"Phone":Phone , "Email": Email, "Address": Address}
            print("Contact successfully added")
        except ValueError as e:
            print(f"Error adding contact: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def view_contact():
    if not Contacts:
        print("No contacts to display.")
    else:
        print("\n--- All Contacts ---")
        for name, details in Contacts.items():
            print(f"Name: {name}")
            print(f"  Phone: {details['Phone']}")
            print(f"  Email: {details['Email']}")
            print(f"  Address: {details['Address']}")

def search_contact():
    search_name= input("Enter name to search:")
    if search_name in Contacts:
        print(f"\n--- Contact Found: {search_name} ---")
        details = Contacts[search_name]
        print(f"  Phone: {details['Phone']}")
        print(f"  Email: {details['Email']}")
        print(f"  Address: {details['Address']}")
    else:
        print(f"Contact '{search_name}' not found.")
    
def update_contact():
    name_to_update = input("Enter contact to update:")
    if name_to_update in Contacts:
        try:
            Phone= int(input("Enter the contact number:"))
            Email= input("Enter email:")
            Address= input("Enter Address:")
            Contacts[name_to_update]= {"Phone":Phone , "Email": Email, "Address": Address}
            print("Contact successfully updated")
        except Exception as e:
            print(f"An error occurred while updating contact: {e}")
    else:
        print("Contact not found")
         
def delete_contact():
    name_to_delete= input("Enter contact to delete:")
    if name_to_delete in Contacts:
        del Contacts[name_to_delete]
        print(f"Contact named {name_to_delete} removed successfully")
    else:
        print("Invalid contact name")
              
while True:
    print("Enter 1 for adding the contact")
    print("Enter 2 for viewing the contact")
    print("Enter 3 for searching the contact")
    print("Enter 4 for updating the contact")
    print("Enter 5 for deleting the contact")
    print("Enter 6 for exit ")
    
    choice= int(input("Enter you choice:"))
    if choice == 1:
        add_contact()
    elif choice == 2:
        view_contact()
    elif choice == 3:
        search_contact()
    elif choice == 4:
        update_contact()
    elif choice == 5:
        delete_contact()
    elif choice == 6:
        print("Exiting Contact Management System. Goodbye!")
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 6.")
    
