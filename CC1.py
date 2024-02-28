import os
from prettytable import PrettyTable 
#saya menggunakan plugin prettytable untuk tabel outputnya

# File path untuk database nya (Untuk path-nya saat ini saya sesuaikan dengan path yang ada di PC saya)
database_file_path = "E:\DATA SCIENCE PURWADHIKA\DATA-SCIENCE-PURWADHIKA\CAPSTONE PURWADHIKA 1\student_database.txt"

# Init database 
database = []

def load_database():
    global database
    if os.path.exists(database_file_path):
        with open(database_file_path, 'r') as file: #r = read (buka file)
            lines = file.readlines()
            database = [line.strip().split(',') for line in lines] 
            for record in database:
                record[0] = int(record[0])  # Untuk mengconvert ID siswa menjadi form Integer
                record[2:5] = map(float, record[2:5]) # untuk mengconvert nilai siswa menjadi form Float

#fungsi agar menyimpan revisi, penghapusan, penambahan, dll pada database
def save_database():
    with open(database_file_path, 'w') as file: #w = write (overwrite/save file)
        for record in database:
            file.write(','.join(map(str, record)) + '\n')


#Fungsi display menu tampilan utama
def display_menu():
    print("\n========Perwadhoka High School Score Database========")
    print("1. Read Database")
    print("2. Add Record")
    print("3. Update Record")
    print("4. Delete Record")
    print("5. Exit")
    print("=====================================================")
#Fungsi utama untuk function READ
def read_database():
    print("\n>>>>>>>>>> Read Database <<<<<<<<<<")
    print("1. Display All Records")
    print("2. Search for Specific Data")
    print("3. Back to Main Menu")
    print('>>>>>>>>>>>>>>>>>.<<<<<<<<<<<<<<<<<\n')
    choice = input("Enter your choice (1-3): ")

    if choice == '1':
        display_records(database)
    elif choice == '2':
        #Ini adalah fungsi sub-menu jika user hanya ingin mencari 1 data tertentu.
        #Fungsi validation_nisn ini agar ID tidak bisa dimasukkan dengan selain dengan kombinasi 10 angka
        search_id = validation_nisn("Enter the Student's ID: ", is_integer=True) 
        matching_records = [record for record in database if record[0] == int(search_id)]
        display_records(matching_records)
        return read_database()
    elif choice == '3':
        return
    else:
        print("Error! Please choose a number between 1-3")
        return read_database()

#Jika tidak ada data sama sekali, maka fungsi akan print string dibawah ini dan kembali ke menu utama
def display_records(records):
    if not records:
        print("No records found.")
        return read_database()
        
#kita masukkan plugin prettytable pada output nya
    table = PrettyTable()
    table.field_names = ["Student ID", "Name", "Math Score", "Science Score", "English Score", "Pass Status"]

    for record in records:
        formatted_record = []
        for item in record:
            # Fungsi ini saya buat agar show table tidak memberi hasil desimal kosong demi kerapian. contoh : (100.0 atau 59.0)
            formatted_item = int(item) if isinstance(item, float) and item.is_integer() else item
            formatted_record.append(formatted_item)

        table.add_row(formatted_record)

    print(table)

#Submenu menuju fungsi ADD
def add_submenu() :
    print("\n++++++++++ Add Record ++++++++++")
    print("1. Input New Student Record")
    print("2. Back to main menu")
    print('++++++++++++++++++++++++++++++++\n')
    choice = input("Enter your choice (1-2): ")

    if choice == '1' :
        return add_record()
    elif choice == '2' :
        return
    else :
        print("Error! Please choose a number between 1-2")
        return add_submenu()
    
#Fungsi utama untuk function ADD
def add_record():
    print("\n========Add Record========")
    student_id = validation_nisn("Enter Student's ID: ", is_integer=True)


    # Kita cek apakah ID sudah terdaftar atau belum. Jika sudah, user akan ditolak dan diminta memasukkan input baru
    if any(record[0] == student_id for record in database):
        print("Student ID already exists. Cannot add duplicate records.")
        return add_submenu()

    name = validation_name("Enter Student's Name: ")
    math_score = validation_score("Enter Math Score: ")
    science_score = validation_score("Enter Science Score: ")
    english_score = validation_score("Enter English Score: ")
    pass_status = calculate_pass_status(math_score, science_score, english_score)

    record = [student_id, name, math_score, science_score, english_score, pass_status]
    database.append(record)
    #konfirmasi display akan menunjukkan yang user baru saja add. Jika sudah cocok, maka user dapat konfirmasikan
    print("\nRecent Changes:")
    display_records([record])
    confirmation = input("Do you want to add this record? (type yes to confirm): ").lower()

    if confirmation == 'yes':
        save_database()
        print("Record added successfully.")
        return add_submenu()
    else:
        print("Add operation canceled.")
        return add_submenu()
    
#submenu menuju fungsi UPDATE
def update_submenu() :
    print("\n^^^^^^^^^^ Update Record ^^^^^^^^^^")
    print("1. Update Existing Student Record")
    print("2. Back to main menu")
    print('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n')
    choice = input("Enter your choice (1-2): ")

    if choice == '1' :
        return update_record()
    elif choice == '2' :
        return
    else :
        print("Error! Please choose a number between 1-2")
        return update_submenu()
    

#Fungsi utama untuk function UPDATE
def update_record():
    print("\n========Update Record========")
    search_id = validation_nisn("Enter the Student's ID to update: ", is_integer=True)
    matching_records = [record for record in database if record[0] == int(search_id)]

    if not matching_records:
        print("No record found with the given ID. Please input existing ID")
        return update_submenu()
    
    #Program akan menampilkan terlebih dahulu data yang user ingin update sebelum user memutuskan untuk update apa tidak
    display_records(matching_records)
    #konfirmasi apakah user benar ingin meng-update data tersebut
    confirmation = input("Do you want to update this record? (type yes to confirm): ").lower()

    if confirmation != 'yes':
        print('Update operation canceled.')
        return update_submenu()

    elif confirmation == 'yes':
        student_id = [record[0] for record in database]
        new_id = input("Enter new Student's ID: ")
        if int(new_id) in student_id :
            print('Cannot update to an already existing ID in the database.')
            return update_record()
        new_name = validation_name("Enter new Student's Name: ")
        #validation_score adalah fungsi yang saya gunakan agar user hanya bisa menginput nilai mulai dari 0 - 100
        new_math_score = validation_score("Enter new Math Score: ")
        new_science_score = validation_score("Enter new Science Score: ")
        new_english_score = validation_score("Enter new English Score: ")
        new_pass_status = calculate_pass_status(new_math_score, new_science_score, new_english_score)

        updated_record = [new_id, new_name, new_math_score, new_science_score, new_english_score, new_pass_status]
       

    #konfirmasi display akan menunjukkan yang user baru saja add.3
    #  Jika sudah cocok, maka user dapat konfirmasikan
        print("\nRecent Changes:")
        display_records([updated_record])
    confirmation = input("Do you want to update this record? (type yes to confirm): ").lower()

    if confirmation == 'yes':
        database.remove(matching_records[0])
        database.append(updated_record)
        save_database()
        print("Record updated successfully.")
        return update_submenu()
    else:
        print("Update operation canceled.")
        return update_submenu()

#submenu menuju fungsi DELETE      
def delete_submenu() :
    print("\n-------------Delete Record-------------")
    print("1. Delete Existing Student Record")
    print("2. Back to main menu")
    print('---------------------------------------\n')
    choice = input("Enter your choice (1-2): ")

    if choice == '1' :
        return delete_record()
    elif choice == '2' :
        return
    else :
        print("Error! Please choose a number between 1-2")
        return delete_submenu()

#Fungsi utama function DELETE
def delete_record():
    print("\n========Delete Record========")
    search_id = validation_nisn("Enter the Student's ID to delete: ", is_integer=True)
    matching_records = [record for record in database if record[0] == int(search_id)]

    if not matching_records:
        print("No record found with the given ID.")
        return delete_submenu()
    
    #ditampilkan data nya terlebih dahulu (sama seperti update tadi)
    display_records(matching_records)
    #lalu konfirmasi
    confirmation = input("Do you want to delete this record? (type yes to confirm): ").lower()

    if confirmation == 'yes':
        database.remove(matching_records[0])
        print("Record deleted successfully.")
        return delete_submenu()
    else:
        print("Delete operation canceled.")
        return delete_submenu()
    

#Ini adalah penjabaran dari fungsi validasi ID NISN siswa agar user hanya bisa memasukkan kombinasi 10 angka
def validation_nisn(prompt, is_integer=True):
    while True:
        try:
            value = input(prompt)
            if value.isdigit and len(value) == 10 and int(value) >= 0 :
                    return int(value)
            else:
                raise ValueError("Error! Value must be a positive 10-digit number")
        except ValueError:
            print("Error! Invalid input. Please enter a positive 10-digit number")

#Ini adalah penjabaran dari fungsi validasi angka 0-100 yang digunakan untuk input nilai siswa
def validation_score(prompt):
    while True:
        try:
            score = float(input(prompt))
            if not (0 <= score <= 100):
                raise ValueError("Error! Score range must be between 0 and 100.")
            return score
        except ValueError:
            print("Error! Invalid input. Please enter a score between 0 and 100.")

#Ini adalah fungsi untuk menentukan apakah siswa dinyatakan lulus atau tidak
def calculate_pass_status(math_score, science_score, english_score):
    average_score = (math_score + science_score + english_score) / 3
    return "Pass" if average_score >= 70 else "Fail"

#Ini adalah fungsi validasi agar nama tidak bisa dikosongkan dan harus diisi setidaknya dengan 1 karakter
def validation_name(prompt):
    while True:
        try:
            name = input(prompt).strip()
            if len(name) > 0:
                return name
            else:
                raise ValueError("Error! Must input at least 1 character.")
        except ValueError as i:
            print(i)


# Fungsi program MAIN
load_database()

while True:
    display_menu()
    choice = input("Enter your choice (1-5): ")

    if choice == '1':
        read_database()
    elif choice == '2':
        add_submenu()
        save_database()
    elif choice == '3':
        update_submenu()
        save_database()
    elif choice == '4':
        delete_submenu()
        save_database()
    elif choice == '5':
        print('''Thank you for using this program!     
Programmed by : Muhammad Hunafa Rizal Aqli ^_^''')
        break
    else:
        print("Error! Please choose a number between 1-5")
