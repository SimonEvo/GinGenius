import mysql.connector
import tkinter as tk
from tkinter import messagebox

# Function to establish connection to MySQL database
def connect_to_database(host, user, password, database):
    return mysql.connector.connect(
        host=host,
        user=user,
        password=password,
        database=database,
        auth_plugin='mysql_native_password'
    )

# Function to retrieve all gins from the database
def get_all_from_table(connection, table_name, orderBy):
    cursor = connection.cursor()
    cmd = (f"SELECT * FROM {table_name} "
            f"ORDER BY {orderBy};")


    cursor.execute(cmd)
    return cursor.fetchall()

# Function to add a new gin to the database
def add_gin(connection, gin_name, flavor_entry, countries_name):
    cursor = connection.cursor()

    # Check if the countries exists
    cursor.execute("SELECT id FROM countries WHERE name = %s", (countries_name,))
    countries_result = cursor.fetchone()

    if countries_result:
        country_id = countries_result[0]
    else:
        # If the countries doesn't exist, insert a new entry
        cursor.execute("INSERT INTO countries (name) VALUES (%s)", (countries_name,))
        country_id = cursor.lastrowid

    # Insert the gin into the gins table
    cursor.execute("INSERT INTO gins (name, type, country_id) VALUES (%s, %s, %s)", (gin_name, flavor_entry, country_id))
    connection.commit()

    print("Gin inserted successfully!")

# Function to delete a gin from the database
def delete_gin(connection, id):
    cursor = connection.cursor()
    sql = "DELETE FROM gins WHERE gin_id = %s"
    val = (id,)
    cursor.execute(sql, val)
    connection.commit()

# Function to handle adding a new gin
def handle_add_gin(connection, name_entry, flavor_entry, origin_entry, gin_listbox, country_listbox):
    name = name_entry.get()
    origin = origin_entry.get()
    flavor_profile = flavor_entry.get()
    if name and origin and flavor_profile:
        add_gin(connection, name, flavor_profile, origin)
        messagebox.showinfo("Success", "Gin added successfully!")
        refresh_table_list(connection, gin_listbox, 'gins')
        refresh_country_list(connection, country_listbox)
    else:
        messagebox.showerror("Error", "Please enter all fields.")

# Function to handle deleting a gin
def handle_delete_gin(connection, gins, gin_listbox):
    selected_index = gin_listbox.curselection()
    if selected_index:
        id = gins[selected_index[0]][0]
        delete_gin(connection, id)
        messagebox.showinfo("Success", "Gin deleted successfully!")
        refresh_table_list(connection, gin_listbox, 'gins')
    else:
        messagebox.showerror("Error", "Please select a gin to delete.")

# Function to refresh the list of gins displayed in the listbox
def refresh_table_list(connection, gin_listbox, table_name):
    gin_listbox.delete(0, tk.END)
    gins = get_all_from_table(connection, 'gins', 'gin_id')
    for gin in gins:
        gin_listbox.insert(tk.END, f"{gin[0]} - {gin[1]} ({gin[2]}, {gin[3]})")

def refresh_country_list(connection, country_listbox):
    country_listbox.delete(0, tk.END)
    countries = get_all_from_table(connection, 'countries', 'id')
    for country in countries:
        country_listbox.insert(tk.END, f"{country[0]} - {country[1]}")


# Function to handle filtering gins by country and flavor
def handle_filter_gins(connection, country_listbox, flavor_entry, filtered_gin_listbox):
    selected_country_index = country_listbox.curselection()
    selected_country_id = country_listbox.get(selected_country_index[0]).split(' - ')[0] if selected_country_index else None
    selected_flavor = flavor_entry.get()
    if selected_country_id and selected_flavor:
        filtered_gins = filter_gins(connection, selected_country_id, selected_flavor)
        refresh_filtered_gin_list(filtered_gin_listbox, filtered_gins)
    else:
        messagebox.showerror("Error", "Please select a country and enter a flavor.")

# Function to filter gins by country and flavor
def filter_gins(connection, country_id, flavor):
    cursor = connection.cursor()
    sql = "SELECT * FROM gins WHERE country_id = %s AND type = %s"
    val = (country_id, flavor)
    cursor.execute(sql, val)
    return cursor.fetchall()

# Function to refresh the list of filtered gins displayed in the listbox
def refresh_filtered_gin_list(filtered_gin_listbox, filtered_gins):
    filtered_gin_listbox.delete(0, tk.END)
    for gin in filtered_gins:
        filtered_gin_listbox.insert(tk.END, f"{gin[0]} - {gin[1]} ({gin[2]}, {gin[3]})")
