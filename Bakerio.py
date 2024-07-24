import pandas as pd
import streamlit as st

# Custom CSS for styling the sidebar buttons
st.markdown("""
<style>
div.stButton > button:first-child{
    background-color: #000066 !important;
    color: white !important;
    width: 100% !important;
    padding: 10px 0px !important;
    border: none !important;
    border-radius: 5px !important;
    font-size: 16px !important;
}
div.stButton > button:hover {
    background-color: gray !important;
}
</style>
""", unsafe_allow_html=True)

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


def load_data(f=file):
    d = pd.read_csv(f)
    print(d)
    return d


def save_data(data):
    data.to_csv(r'C:\Users\LENOVO\Desktop\Book1.csv', index=False)


def add_customers():
    data = load_data()
    name = st.text_input("Enter Customer's Name : ")
    order_id = st.text_input("Enter Customer's ID : ")
    order_name = st.text_input("Enter What Customer ordered : ")
    order_data = st.text_input("Date on which customer ordered : ")
    city = st.text_input("Enter the customer's city name : ")

    if st.button("Add"):
        new_data = [name, order_id, order_name, order_data, city]
        data.loc[len(data.index)] = new_data
        save_data(data)
        st.success("Customer added successfully, now select again to perform something, Thank You!")


# Repeat similar structure for other buttons...
def categorized_by_city():
    data = load_data()
    data['Total Customers'] = data.groupby('City Name')['City Name'].transform('count')
    data = data[['City Name', 'Total Customers']]
    data.drop_duplicates(inplace=True)
    if st.button("Categorize By City"):
        st.write(data)
        st.success("Now select again to perform something, Thank You!")


def frequent_ordered_dish():
    data = load_data()
    data['Total Orders'] = data.groupby('Order Name')['Order Name'].transform('count')
    data = data[['Order Name', 'Total Orders']]
    data.sort_values(by="Total Orders", inplace=True)
    data.drop_duplicates(inplace=True)
    if st.button("Frequently Order"):
        st.write(data)
        st.success("Now select again to perform something, Thank You!")


def same_city_customers():
    data = load_data()
    c = st.text_input("Enter City Name : ")
    if st.button("Find Customers"):
        data = data.loc[data['City Name'] == c]
        st.write(data)
        st.success("Now select again to perform something, Thank You!")


def customers_with_same_orders():
    c = st.text_input("Enter Order Name : ")
    data = load_data()
    if st.button("Find Orders"):
        data = data.loc[data['Order Name'] == c]
        st.write(data)
        st.success("Now select again to perform something, Thank You!")


def delete_customers():
    data = load_data()
    order_id = st.text_input("Enter OrderID of customer : ")
    if st.button("Delete Customer"):
        if order_id in data['Order ID']:
            ind = data.index[data['Order ID'] == order_id].tolist()
            data.drop(ind, inplace=True)
            st.title("Remaining Customers")
            st.write(data)
            save_data(data)
            st.success("Now select again to perform something, Thank You!")


def search_customers():
    data = load_data()
    order_id = st.text_input("Enter Order ID of the customer : ")
    if st.button("Customer Details"):
        ind = data.loc[data['Order ID'] == order_id]
        st.write(ind)


def update_details():
    data = load_data()
    order_id = st.text_input("Enter Order ID : ")
    if st.button("Update Details"):
        try:
            order_id = int(order_id)
            ind = data.index[data['Order ID'] == order_id].tolist()
            if not ind:
                st.write("Order ID Not Found")
            ind = ind[0]
            menu = ["Update Name", "Update OrderID", "Update OrderName", "Update OrderDate", "Update CityName"]
            field = st.selectbox("Select Field For Action ", menu)
            new_value = st.text_input(f"Enter New {field.split()[-1]} : ")
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
        except ValueError:
            st.write("Invalid Order ID. Please enter a numeric Order ID.")


def view_customers():
    data = load_data()
    if st.button("View All"):
        st.write(data)


def add_new_field():
    data = load_data()
    field = input("Add New Field : ")
    cases = ['Yes', 'No']
    char = st.selectbox("You Want To Add Values In This Field For Previous Customers", cases)
    array = []
    if char == 'Yes':
        for i in data['Name']:
            val = st.text_input(r'Enter {field} for customer : {i}')
            array.append(val)
    else:
        array = [None]*len(data)
    data[field] = array
    save_data(data)


def import_customers_data():
    data = load_data()
    second_file = st.file_uploader("Upload Your Second Customer's Data File -CSV Formate.", type=["csv"])
    others = load_data(second_file)
    data.append(others, ignore_index=True)
    save_data(data)


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


# Custom CSS for styling
st.markdown("""
    <style>
    /* Sidebar background color */
    .css-1aumxhk {
        background-color: #f0f0f5;
    }
    /* Button styles */
    .stButton>button {
        background-color: #007bff;
        color: white;
        border-radius: 5px;
        width: 100%;
    }
    div stButton > button:hover {
        background-color: #0056b3;
        color: white;
    }
    /* Header styles */
    .css-10trblm {
        color: #007bff;
    }
    </style>
    """, unsafe_allow_html=True)


# Main content based on the choice
if choice == "Add Customer":
    st.header("Add a New Customer")
    add_customers()

elif choice == "Delete Customer":
    st.header("Delete a Customer")
    delete_customers()

elif choice == "Find Customer on Order ID":
    st.header("Find Customer by Order ID")
    search_customers()

elif choice == "View All Customers":
    st.header("All Customers")
    view_customers()

elif choice == "Update Details":
    st.header("Update Customer Details")
    update_details()

elif choice == "Same City Customers":
    st.header("Customers in the Same City")
    same_city_customers()

elif choice == "Most Demanding Dish":
    st.header("Most Demanding Dish")
    frequent_ordered_dish()

elif choice == "Customers With Same Order":
    st.header("Customers with the Same Order")
    customers_with_same_orders()

elif choice == "Cities With Number Of Customers":
    st.header("Customers by City")
    categorized_by_city()

elif choice == "Import More Data":
    st.header("Import More Customer Data")
    import_customers_data()

elif choice == "Add New Field In File":
    st.header("Add a New Field to the File")
    add_new_field()

