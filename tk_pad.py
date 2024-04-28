from functions import *


# Main function
def tk_pad_definition():
    # Database connection parameters
    host = "localhost"
    user = "root"
    password = "password"
    database = "ging"

    # Establish connection to the database
    connection = connect_to_database(host, user, password, database)

    # Create the main window
    window = tk.Tk()
    window.title("Gin Management System")

    # Create labels and entry fields for adding a new gin
    tk.Label(window, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(window)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(window, text="Origin:").grid(row=1, column=0, padx=5, pady=5)
    origin_entry = tk.Entry(window)
    origin_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(window, text="Flavor Profile:").grid(row=2, column=0, padx=5, pady=5)
    flavor_entry = tk.Entry(window)
    flavor_entry.grid(row=2, column=1, padx=5, pady=5)

    # Listbox to display gins
    gin_listbox = tk.Listbox(window, width=50, height=10)
    gin_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    # Listbox to display countries and their IDs
    country_listbox = tk.Listbox(window, width=25, height=5)
    country_listbox.grid(row=6, column=2, padx=5, pady=5)

    gins = get_all_from_table(connection, 'gins', 'gin_id')

    # Button to add a new gin
    add_button = tk.Button(window, text="Add Gin", command=lambda: handle_add_gin(connection, name_entry, flavor_entry, origin_entry, gin_listbox, country_listbox))
    add_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)

    

    # Button to delete selected gin
    delete_button = tk.Button(window, text="Delete Selected Gin", command=lambda: handle_delete_gin(connection, gins, gin_listbox))
    delete_button.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    # Refresh the list of gins displayed in the listbox
    refresh_table_list(connection, gin_listbox, 'gins')
    refresh_country_list(connection, country_listbox)

    # # Create labels and entry fields for filtering gins by country and flavor
    # tk.Label(window, text="Filter by Country:").grid(row=0, column=2, padx=5, pady=5)
    # country_listbox_filter = tk.Entry(window)
    # country_listbox_filter.grid(row=0, column=3, padx=5, pady=5)


    tk.Label(window, text="Filter by Flavor:").grid(row=1, column=2, padx=5, pady=5)
    flavor_entry_filter = tk.Entry(window)
    flavor_entry_filter.grid(row=1, column=3, padx=5, pady=5)

    # Button to filter gins
    filter_button = tk.Button(window, text="Filter Gins", command=lambda: handle_filter_gins(connection, country_listbox, flavor_entry_filter, filtered_gin_listbox))
    filter_button.grid(row=2, column=2, columnspan=2, padx=5, pady=5)

    # Listbox to display filtered gins
    filtered_gin_listbox = tk.Listbox(window, width=50, height=10)
    filtered_gin_listbox.grid(row=4, column=2, columnspan=2, padx=5, pady=5)

    # Run the main event loop
    window.mainloop()

    # Close the database connection
    connection.close


if __name__ == "__main__":
    tk_pad_definition()