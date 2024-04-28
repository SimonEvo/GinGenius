from functions import *
from random import *

def gin_generate(amount):
    #Generater 'amount' number of gin entries with random origins and name
    country_list = ['England', 'Ireland', 'Scotland', 'Wales', 'Italy', 'China']
    type_list = ['Dry', 'Fruity', 'Floral', 'Spiced']
    out_list = []
    for i in range(amount):
        name = 'Gin Name'+str(i)
        type_name = type_list[randint(0, 3)]
        country = country_list[randint(0, 5)]
        arr = [name, type_name, country]

        out_list.append(arr)
    
    return out_list



def main():
    host = "localhost"
    user = "root"
    password = "password"
    database = "ging"
    connection = connect_to_database(host, user, password, database)
    gins_to_add = gin_generate(10)
    

    for i in range(len(gins_to_add)):
        add_gin(connection, gins_to_add[i][0], gins_to_add[i][1], gins_to_add[i][2])

    





if __name__ == "__main__":
    main()