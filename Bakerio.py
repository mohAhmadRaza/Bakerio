import pandas as pd
import streamlit as st

# CSS for initial lookups
st.markdown("""
   <div style="background-color: #000066; text-align: center; padding: 10px;border-radius : 5px"> 
       <h1 style="color:white"; "font-size:70px";"margin-bottom:-49px">Bakerio</h1>
       <h2 style="color: white; font-size: 20px;">Bakery Management System</h2>
   </div> 
""", unsafe_allow_html=True)

# Styling initial message
style_css = """
<style>
.initial_message {
    color: black;
    font-size: 17px;  /* Larger font size */
    text-align: center;
    margin-bottom: 10px;
}
</style>
"""
# Include the CSS in the Streamlit app
st.markdown(style_css, unsafe_allow_html=True)

content = "A customer management tool designed specifically for bakery owners. It allows you to efficiently manage your customer data, all covered here."
st.markdown(f"<div class='initial_message'>{content}</div>", unsafe_allow_html=True)

file = st.file_uploader("Upload your customers data file - CSV Format", type=["csv"])

# Creating Class For Abstraction and Encapsulation

class CustomerManagement:
    def __init__(self, file):
        self.file = file
        self.data = self.load_data()

    def load_data(self):
        if self.file:
            data = pd.read_csv(self.file)
            return data
        return pd.DataFrame()

    def save_data(self, data):
        if self.file:
            data.to_csv(file, index=False)

    def add_customers(self):
        data = self.load_data()
        name = st.text_input("Enter Customer's Name : ")
        order_id = st.text_input("Enter Customer's ID : ")
        order_name = st.text_input("Enter What Customer ordered : ")
        order_data = st.text_input("Date on which customer ordered : ")
        city = st.text_input("Enter the customer's city name : ")

        if st.button("Add"):
            new_data = [name, order_id, order_name, order_data, city]
            data.loc[len(data.index)] = new_data
            self.save_data(data)
            st.success("Customer added successfully, now select again to perform something, Thank You!")


# Repeat similar structure for other buttons...
    def categorized_by_city(self):
        data = self.load_data()
        data['Total Customers'] = data.groupby('City Name')['City Name'].transform('count')
        data = data[['City Name', 'Total Customers']]
        data.drop_duplicates(inplace=True)
        if st.button("Categorize By City"):
           st.write(data)
           st.success("Now select again to perform something, Thank You!")


    def frequent_ordered_dish(self):
        data = self.load_data()
        data['Total Orders'] = data.groupby('Order Name')['Order Name'].transform('count')
        data = data[['Order Name', 'Total Orders']]
        data.sort_values(by="Total Orders", inplace=True)
        data.drop_duplicates(inplace=True)
        if st.button("Frequently Order"):
            st.write(data)
            st.success("Now select again to perform something, Thank You!")

    def same_city_customers(self):
        data = self.load_data()
        c = st.text_input("Enter City Name : ")
        if st.button("Find Customers"):
            data = data.loc[data['City Name'] == c]
            st.write(data)
            st.success("Now select again to perform something, Thank You!")

    def customers_with_same_orders(self):
        c = st.text_input("Enter Order Name : ")
        data = self.load_data()
        if st.button("Find Orders"):
            data = data.loc[data['Order Name'] == c]
            st.write(data)
            st.success("Now select again to perform something, Thank You!")

    def delete_customers(self):
        data = self.load_data()
        order_id = st.text_input("Enter OrderID of customer : ")
        if st.button("Delete Customer"):
            if order_id in data['Order ID']:
                ind = data.index[data['Order ID'] == order_id].tolist()
                data.drop(ind, inplace=True)
                st.title("Remaining Customers")
                st.write(data)
                self.save_data(data)
                st.success("Now select again to perform something, Thank You!")

    def search_customers(self):
        data = self.load_data()
        order_id = st.text_input("Enter Order ID of the customer : ")
        if st.button("Customer Details"):
            ind = data.loc[data['Order ID'] == order_id]
            st.write(ind)

    def update_details(self):
        data = self.load_data()
        order_id = st.text_input("Enter Order ID : ")
        if st.button("Update Details"):
            try:
                order_id = int(order_id)
                ind = data.index[data['Order ID'] == order_id].tolist()
                if not ind:
                    st.write("Order ID Not Found")
                ind = ind[0]
                men = ["Update Name", "Update OrderID", "Update OrderName", "Update OrderDate", "Update CityName"]
                field = st.selectbox("Select Field For Action ", men)
                new_value = st.text_input(f"Enter New {field.split()[-1]} : ")
                if new_value:
                    if new_value and st.button(f"Confirm Update {field.split()[-1]}"):
                        if field == "Update Name":
                            data.loc[ind, 'Name'] = new_value
                        elif field == "Update OrderID":
                            data.loc[ind, 'Order ID'] = new_value
                        elif field == "Update OrderName":
                            data.loc[ind, 'Order Name'] = new_value
                        elif field == "Update OrderDate":
                            data.loc[ind, 'Order Date'] = new_value
                        elif field == "Update CityName":
                            data.loc[ind, 'City Name'] = new_value
                        self.save_data(data)
                        st.info("Successfully Updated")
            except ValueError:
                st.write("Invalid Order ID. Please enter a numeric Order ID.")

    def view_customers(self):
        data = self.load_data()
        if st.button("View All"):
            st.write(data)

    def add_new_field(self):
        data = self.load_data()
        field = input("Add New Field : ")
        cases = ['Yes', 'No']
        char = st.selectbox("You Want To Add Values In This Field For Previous Customers", cases)
        if char == 'Yes':
            array = [st.text_input(f'Enter {field} for customer: {name}') for name in data['Name']]
        else:
            array = [None]*len(data)
        data[field] = array
        self.save_data(data)

    def import_customers_data(self):
        data = self.load_data()
        second_file = st.file_uploader("Upload Your Second Customer's Data File -CSV Formate.", type=["csv"])
        others = pd.read_csv(second_file)
        data = pd.concat([data, others], ignore_index=True)
        self.save_data(data)
        st.success("Data imported successfully, now select again to perform something, Thank You!")


# Sidebar for navigation
with st.sidebar:
    st.title("Customer Management")
    menu = [
        "Select an Option", "Add Customer", "Delete Customer", "Find Customer on Order ID",
        "View All Customers", "Update Details", "Same City Customers", "Most Demanding Dish",
        "Customers With Same Order", "Cities With Number Of Customers", "Import More Data",
        "Add New Field In File"
    ]
    choice = st.selectbox("Select Action To Perform", menu)

# Creating a customer having its customer data file
customer = CustomerManagement(file)

# Main content based on the choice
if choice == "Add Customer":
    st.header("Add a New Customer")
    customer.add_customers()

elif choice == "Delete Customer":
    st.header("Delete a Customer")
    customer.delete_customers()

elif choice == "Find Customer on Order ID":
    st.header("Find Customer by Order ID")
    customer.search_customers()

elif choice == "View All Customers":
    st.header("All Customers")
    customer.view_customers()

elif choice == "Update Details":
    st.header("Update Customer Details")
    customer.update_details()

elif choice == "Same City Customers":
    st.header("Customers in the Same City")
    customer.same_city_customers()

elif choice == "Most Demanding Dish":
    st.header("Most Demanding Dish")
    customer.frequent_ordered_dish()

elif choice == "Customers With Same Order":
    st.header("Customers with the Same Order")
    customer.customers_with_same_orders()

elif choice == "Cities With Number Of Customers":
    st.header("Customers by City")
    customer.categorized_by_city()

elif choice == "Import More Data":
    st.header("Import More Customer Data")
    customer.import_customers_data()

elif choice == "Add New Field In File":
    st.header("Add a New Field to the File")
    customer.add_new_field()
