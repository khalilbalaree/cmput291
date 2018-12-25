import sqlite3
import sys
##my own data creation
# from init_table import tables_init

class table_exc:
    def __init__(self,path):
        self.path = path
        self.cursor = None
        self.connection = None
        
    def connect(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(' PRAGMA foreign_keys=ON; ')
        self.connection.commit()
        return

    def disconnect(self):
        self.connection.close()
        return
        
    def is_valid_db(self):
        try:
            #check we use the correct database
            self.cursor.execute("select * from members;")
        except:
            print("Check the file name of the database")
            return False
        print("open database successfully")
        return True

    def login(self, username, pwd):  
        if username != '' and pwd != '':
            self.cursor.execute("select * from members where email = '%s' and pwd = '%s';" % (username, pwd))
            result = self.cursor.fetchone()
            return result
        else:
            return False

    def check_username(self, username):
        if username == '':
            return ''
        else:
            self.cursor.execute("select * from members where email = '%s';" % username)
            return self.cursor.fetchone()

    def insert_members(self, username, pwd, name, phone):
        member_insert = "insert into members(email, name, phone, pwd) values ('%s', '%s', '%s', '%s');" %(username, name, phone, pwd)
        self.cursor.execute(member_insert)
        self.connection.commit()
        return "Create new account successful!"

    def check_message(self, email):
        self.cursor.execute("select * from inbox where email = '%s' and seen = 'n';" % email)
        rows = self.cursor.fetchall()
        if rows == []:
            print("No message!")
        else:
            for row in rows:
                print('Content: ',row[3],' |sender: ', row[2], ' |time: ' + row[1] + ' |rno: ' + str(row[4]))
            self.cursor.execute("update inbox set seen = 'y' where email = '%s';" % email)
            self.connection.commit()

    def check_locations_validity(self, location):
        #check if the location is a lcode
        self.cursor.execute("select * from locations where lcode = '%s';" % location)
        #no
        if self.cursor.fetchone() == None:
            self.cursor.execute("select * from locations where city like '%" + location + "%' or prov like '%" + location + "%' or address like '%"+ location +"%';")
            matches = self.cursor.fetchall()
            #cannot find the data
            if matches == []:
                print("Not a proper lcode or no data matching the keyword!")
                return False
            else:
                pages = (len(matches) - 1) // 5 + 1
                code = []
                for i in range(0, pages):
                    for j in matches[(i * 5):(i+1) * 5]:
                        print("lcode: " + j[0] + " |city: " + j[1] + " |prov: " + j[2] + " |address: " + j[3])
                        code.append(j[0])
                    if pages > 1 and i + 1 != pages:
                        while True:
                            choice = input("Press c and go to see more or input the lcode: ")
                            if choice == 'c':
                                break
                            else:
                                if choice not in code:
                                    print("Please retype.")
                                else:
                                    return choice
                    else:
                        while True:
                            choice = input("input the lcode: ")
                            if choice not in code:
                                print("Please retype.")
                            else:
                                return choice
        #yes
        else:
            return location

    def check_car(self, email, cno):
        #check if the cno is belong to email
        self.cursor.execute("select * from cars where cno = %s and owner = '%s';" % (cno, email))
        if self.cursor.fetchone() != None:
            return True
        else:
            return False

    def offer_ride(self, email):
        while True:
            date = input("Date(YYYY-MM-DD): ")
            #check the date
            if len(date.split("-")) == 3 and len(date) == 10:
                break 
        
        while True:
            num_seats = input("Number of seats offered: ")
            if num_seats == "":
                num_seats = "Null"
                break
            if num_seats.isdigit():
                break
        
        while True:
            price = input("Price per seat: ")
            if price == '':
                price = "Null"
                break
            if price.isdigit():
                break

        luggage = input("Luggage description: ")

        while True:
            location_from = input("Source Location: ")
            src = self.check_locations_validity(location_from)
            if src != False:
                break

        while True:   
            location_to = input("Destination Location: ")
            dst = self.check_locations_validity(location_to)
            if dst != False:
                break

        enroute = []
        while True:
            enroute_lo = input("Enroute location:(or type return to the next): ")
            if enroute_lo == '':
                break
            result = self.check_locations_validity(enroute_lo)
            if result != False:
                enroute.append(result)
        
        
        while True:
            car_number = input("Your car number(or type return if you do not want to provide the cno for now): ")
            if car_number == '':
                cno = 'NULL'
                break
            elif self.check_car(email, car_number):
                cno = car_number
                break
            else:
                print("Invalid car number!")
                cno = "NULL"

        #create a unique rno
        self.cursor.execute("select max(rno) from rides;")
        rno = self.cursor.fetchone()[0] + 1

        #insert into the rides tbl
        self.cursor.execute("Insert into rides values\
                             (%s, %s, '%s', %s, '%s', '%s', '%s','%s', %s);" % (rno, price, date, num_seats, luggage, src, dst, email, cno))

        self.connection.commit()

        #insert into the enroutes tbl
        if enroute != []:
            for en in enroute:
                self.cursor.execute("INSERT INTO enroute VALUES\
                                    (%s, '%s');" % (rno, en))
    
        self.connection.commit()
        print("Create ride successful")

    def search_rides(self, email):
        while True:
            promp = input("-Please input at most 3 locations keywords(use space to seperate) or 0 to go back: ")
            keywords = promp.split(" ")
            if keywords[0] == '0':
                break
            elif len(keywords) <= 3 and len(keywords) != 0:
                # print(keywords)
                matches = []
                for keyword in keywords:
                    self.cursor.execute("SELECT distinct(r.rno), r.price, r.rdate, r.seats, r.lugDesc, r.src, r.dst, r.driver, r.cno\
                                        FROM rides r, locations lo1, locations lo2 \
                                        WHERE r.src = lo1.lcode and r.dst = lo2.lcode\
                                            and (r.src = '" + keyword + "' \
                                            or r.dst = '" + keyword + "'\
                                            or r.rno in (SELECT en.rno \
                                                        FROM enroute en, locations lo3, rides r1\
                                                        WHERE en.lcode = lo3.lcode\
                                                            and r1.rno = en.rno\
                                                            and (en.lcode = '" + keyword + "'\
                                                            or lo3.city LIKE '%" + keyword + "%'\
                                                            or lo3.prov LIKE '%" + keyword + "%'\
                                                            or lo3.address LIKE '%" + keyword + "%'))\
                                            or lo1.city LIKE '%" + keyword + "%'\
                                            or lo1.prov LIKE '%" + keyword + "%'\
                                            or lo1.address LIKE '%" + keyword + "%'\
                                            or lo2.city LIKE '%" + keyword + "%'\
                                            or lo2.prov LIKE '%" + keyword + "%'\
                                            or lo2.address LIKE '%" + keyword + "%');")
                    thismatch = self.cursor.fetchall()
                    matches += thismatch

                #let user to select a rno
                rno, em = self.func_select_rides(matches)
                if rno != False:
                    self.cursor.execute("insert into inbox values\
                                        ('%s', datetime('now', 'localtime'), '%s', 'Can I book a seat on your ride?', %s, 'n');" % (em, email, rno))
                    self.connection.commit()
                    print("Message sent!")

            else:
                print("Invalid input!")

                

    def func_select_rides(self, matches):
        # print(matches)
        if matches == []:
            print("No data!")
            return False, False

        pages = (len(matches) - 1) // 5 + 1
        code = {} #dict method
        for i in range(0, pages):
            for j in matches[(i * 5):(i+1) * 5]:
                print("rno: " + str(j[0]) + " |price: " + str(j[1]) + " |date: " + j[2] + " |num_of_seats: " + str(j[3]) + " |luggage description: " + j[4] + " |src: " + j[5] + " |dst: " + j[6] + " |driver: " + j[7])
                code[str(j[0])] = j[7]
                cno = j[8]
                if cno != None:
                    self.cursor.execute("select * from cars where cno = %s" % cno)
                    car_info = self.cursor.fetchone()
                    print("cno: " + str(car_info[0]) + " |make: " + car_info[1] + " |model: " + car_info[2] + " |year: " + str(car_info[3]) + " |seats: " + str(car_info[4]))
                else:
                    print("No car info")
                print("\n")

            if pages > 1 and i + 1 != pages:
                # print(code)
                while True:
                    choice = input("--Press c and go to see more or input the rno: ")
                    if choice == 'c':
                        break
                    else:
                        if choice not in code:
                            print("Please retype.")
                        else: 
                            return choice, code[choice]
            else:
                while True:
                    choice = input("--input the rno: ")
                    if choice not in code:
                        print("Please retype.")
                    else:
                        return choice, code[choice]

                
    def post_request(self,email):
        while True:
            date = input("Date(YYYY-MM-DD): ")
            #check the date
            if len(date.split("-")) == 3 and len(date) == 10:
                break 
        
        while True:
            pickup = input("Pickup: ")
            pickup = self.check_locations_validity(pickup)
            if pickup != False:
                break

        while True:
            dropoff = input("Dropoff: ")
            dropoff = self.check_locations_validity(dropoff)
            if dropoff != False:
                break

        while True:  
            price = input("The amount you want to pay: ")
            if price == '':
                price = 'NULL'
                break
            if price.isdigit():
                break

        #create a unique rid
        self.cursor.execute("select max(rid) from requests;")
        rid = self.cursor.fetchone()[0] + 1

        #insert into requests tbl
        self.cursor.execute("Insert into requests values\
                            (%s, '%s', '%s', '%s', '%s', %s);" % (rid, email, date, pickup, dropoff, price))
        self.connection.commit()
        print("Post request successful!")


    def show_request(self,email):
        self.cursor.execute("select * from requests where email = '%s';" % email)
        requests = self.cursor.fetchall()
        if requests == []:
            print("No requests!")
            result = False
        else:
            result = True
            print("Your ride requests: ")
            for request in requests:
                rid = request[0]
                rdate = request[2]
                pickup = request[3]
                dropoff = request[4]
                amount = request[5]
                print("Rid: "+ str(rid) + "|Date: " + rdate + "|pickup: " + pickup + "|dropoff: " + dropoff + "|amount: " + str(amount))

        return result
        

    def search_delete_requests(self, email):
        while True:
            command0 = input("-Press 1 to see your requests.\n-Press 2 to search requests\n-Press 0 to go back: ")
            if command0 == "1":
                while True:
                    #show all requests this email have
                    if self.show_request(email):
                        command1 = input("--Press A to delete or B to go back: ").upper()
                        if command1 == "A":
                            delt = input("---Select one rid you want to delete: ")
                            if delt != '':
                                self.cursor.execute("select * from requests where rid = %s and email = '%s';" % (delt, email))
                                if self.cursor.fetchone() != None:
                                    self.cursor.execute("delete from requests where rid = %s and email = '%s';" % (delt, email))
                                    self.connection.commit()
                                    print("Delete request successful!")
                                else:
                                    print("Rid not exist!")
                        elif command1 == "B":
                            break
                        else:
                            print("Command not exist! Re-input please!")
                    else:
                        command1 = input("--Press B to go back: ").upper()
                        if command1 == "B":
                            break
                        else:
                            print("Command not exist! Re-input please!")


            if command0 == "0":
                break
            
            if command0 == "2":
                while True:
                    command1 = input("--Search a pickup location by lcode or city or 0 to go back: ")
                    if command1 == '0':
                        break
                    else:
                        rid, em = self.search_requests(email, command1)
                        # print(rid, em)
                        if rid != False:
                            text = input("Input texts to message to the posting member: ")
                            self.cursor.execute("insert into inbox values ('%s', datetime('now', 'localtime'), '%s', '%s', NULL, 'n');" % (em, email, text))
                            self.connection.commit()
                            print("Message Sent!")
                            break


    def search_requests(self, email, location):
        self.cursor.execute("select r.rid, r.email, r.rdate, r.pickup, r.dropoff, r.amount from requests r, locations lo where lo.lcode = r.pickup and lo.city like '%s'\
                            union\
                            select r.rid, r.email, r.rdate, r.pickup, r.dropoff, r.amount from requests r where pickup = '%s';" % (location, location))
        matches = self.cursor.fetchall()
        if matches == []:
            print("No data")
            return False, False
        else:
            pages = (len(matches) - 1) // 5 + 1
            code = {} #dict approach
            for i in range(0, pages):
                for j in matches[(i * 5):(i+1) * 5]:
                    print("rid: " + str(j[0]) + " |email: " + j[1] + " |date: " + j[2] + " |pickup: " + j[3] + " |dropoff: " + j[4] + " |price: " + str(j[5]))
                    code[str(j[0])] = j[1] #dict
                if pages > 1 and i + 1 != pages:
                    while True:
                        choice = input("Press c and go to see more or input the rid: ")
                        if choice == 'c':
                            break
                        else:
                            if choice not in code:
                                print("Please retype.")
                            else:
                                return choice, code[choice]
                else:
                    while True:
                        choice = input("input the rid: ")
                        if choice not in code:
                            print("Please retype.")
                        else:
                            return choice, code[choice]
        
    def bookings(self, email):
        while True:
            command0 = input("-Press 1 to see bookings on your rides.\n-Press 2 to book other members on your rides\n-Press 0 to go back: ")
            #see bookings this email have as a driver
            if command0 == '1':
                while True:
                    self.cursor.execute("SELECT b.bno, b.email, r.rno, b.pickup, b.dropoff, b.seats FROM rides r, bookings b WHERE r.rno = b.rno and r.driver = '%s';" % email)
                    urbs = self.cursor.fetchall()
                    if urbs == []:
                        print("No one book your rides")
                        break
                    else: 
                        code_em = {}
                        code_rno = {}
                        for b in urbs:
                            print("bno: " + str(b[0]) + " |email: " + b[1] + " |rno: " + str(b[2]) + " |pickup: " + str(b[3]) + " |dropoff: " + str(b[4]) + " |seats: " + str(b[5]))
                            code_em[str(b[0])] = str(b[1])
                            code_rno[str(b[0])] = str(b[2])
                        canceled = input("Input the bno you want to cancel or 0 to go back: ")
                        if canceled == '0':
                            break
                        elif canceled in code_em:
                            self.cursor.execute("delete from bookings where bno = %s;" % canceled)
                            self.cursor.execute("insert into inbox values\
                                                ('%s', datetime('now', 'localtime'), '%s', 'Your booking has been canceled', %s, 'n')" % (code_em[canceled], email, code_rno[canceled]))
                            self.connection.commit()
                            print("Deleted!")
                        else:
                            print("Invalid input!")

            #book other members as a driver              
            elif command0 == '2':
                #list all ride the member offer
                print("Your ride offer: ")
                self.cursor.execute("SELECT distinct(r.rno), rdate, src, dst, ifnull(booked, 0), ifnull(r.seats,0) - ifnull(booked, 0)\
                                    FROM rides r, bookings b\
                                    LEFT OUTER JOIN\
                                    (SELECT rno, sum(seats) as booked\
                                    FROM bookings\
                                    GROUP BY rno) USING (rno)\
                                    WHERE r.driver = '%s';" % email)
                matches = self.cursor.fetchall()

                rno = self.func_select_bookings(matches)
                if rno == False:
                    print("You cannot book anyone on your rides")
                else:
                    while True:
                        em = input("Input the email you want to add to your ride: ")
                        self.cursor.execute("select * from members where email = '%s';" % em)
                        if self.cursor.fetchone() != None:
                            break
                        else:
                            print("No such member! Please re-type!")

                    while True:
                        num_seats = input("The number of seats booked: ")
                        if num_seats.isdigit(): 
                            if int(num_seats) >= 1:
                                break
                    
                    while True:  
                        price = input("Cost: ")
                        if price == '':
                            price = 'NULL'
                            break
                        if price.isdigit():
                            break

                    while True:
                        pickup = input("Pickup(lcode): ")
                        if pickup == '':
                            pickup = 'Null'
                            break
                        else:
                            self.cursor.execute("select * from locations where lcode = '%s';" % pickup)
                            if self.cursor.fetchone() != None:
                                pickup = "'" + pickup + "'"
                                break
                    
                    while True:
                        dropoff = input("Dropoff(lcode): ")
                        if dropoff == '':
                            dropoff = 'Null'
                            break
                        else:
                            self.cursor.execute("select * from locations where lcode = '%s';" % dropoff)
                            if self.cursor.fetchone() != None:
                                dropoff = "'" + dropoff + "'"
                                break

                    self.cursor.execute("select max(bno) from bookings;")
                    bno = self.cursor.fetchone()[0] + 1

                    self.cursor.execute("SELECT distinct(r.rno), ifnull(r.seats,0), ifnull(booked, 0)\
                                        FROM rides r, bookings b\
                                        LEFT OUTER JOIN\
                                        (SELECT rno, sum(seats) as booked\
                                        FROM bookings\
                                        GROUP BY rno) USING (rno)\
                                        WHERE r.rno = %s;" % rno)
                    result = self.cursor.fetchone()

                    #overbooked
                    if result[1] == '':
                        seats = 0
                    else:
                        seats = result[1]
                    if int(seats) < int(result[2]) + int(num_seats):
                        while True:
                            choice = input("Warning: overbooked!\nPress 1 to comfirm or 0 to waive: ")
                            if choice == '1':
                                self.cursor.execute("insert into bookings values\
                                                    (%s, '%s', %s, %s, %s, %s, %s);" %(bno, em, rno, price, num_seats, pickup, dropoff))
                                self.cursor.execute("insert into inbox values\
                                                    ('%s', datetime('now', 'localtime'), '%s', 'You are booked on the ride', %s, 'n')" % (em, email, rno))
                                self.connection.commit()
                                print("Member is booked!\nMessage sent!")
                                break
                            elif choice == '0':
                                print("Booking waived!")
                                break
                    #not overbooked
                    else: 
                        self.cursor.execute("insert into bookings values\
                                            (%s, '%s', %s, %s, %s, %s, %s);" %(bno, em, rno, price, num_seats, pickup, dropoff))
                        self.cursor.execute("insert into inbox values\
                                            ('%s', datetime('now', 'localtime'), '%s', 'You are booked on the ride', %s, 'n')" % (em, email, rno))
                        self.connection.commit()
                        print("Member is booked!\nMessage sent!")
                    

            elif command0 == '0':
                break
            else:
                print("Invalid input!")


    def func_select_bookings(self, matches):
        if matches != []:
            pages = (len(matches) - 1) // 5 + 1
            code = []
            for i in range(0, pages):
                for m in matches[(i * 5):(i+1) * 5]:
                    # print(m[5])
                    if m[5] < 0:
                        available = 0
                    else:
                        available = m[5]
                    print("rno: " + str(m[0]) + " |rdate: " + str(m[1]) + " |src: " + str(m[2]) + " |dst: " + str(m[3]) + " |seats booked: " + str(m[4]) + " |seats available: " + str(available))
                    code.append(str(m[0]))
                if pages > 1 and i + 1 != pages:
                    while True:
                        choice = input("Press c and go to see more or input the rno: ")
                        if choice == 'c':
                            break
                        else:
                            if choice not in code:
                                print("Please retype.")
                            else:
                                return choice
                else:
                    while True:
                        choice = input("input the rno: ")
                        if choice not in code:
                            print("Please retype.")
                        else:
                            return choice
        else:
            return False              


def main(path):
    path = "./" + path
    data_exc = table_exc(path)
    data_exc.connect()
    if not data_exc.is_valid_db():
        exit()

    # ##########################################
    # # init data in the table
    # try:
    #     f = open("./cache")
    # except FileNotFoundError:
    #     #No data in db file, create one
    #     f = open("./cache","w+")
    #     start = tables_init()
    #     start.data_init(False)
    # f.close()
    # #########################################
    
    while True:
        choice = input("---------MAIN MENU---------\nPress 1 to login\nPress 2 to create account\nPress 0 to exit: ")
        #login
        if choice == '1':
            username = input('Username(email): ')
            pwd = input('Password: ')

            # ##############################################################
            # # recover the database
            # if username == 'admin' and pwd == 'admin':
            #     recovery = input('Press 1 to recover the database: ')
            #     if recovery == '1':
            #         start = tables_init()
            #         start.data_init(True)
            #         continue
            # ##############################################################

            result = data_exc.login(username, pwd)
            if result == None or result == False:
                print("invalid Username or Password!")
                continue
            else:
                print("Login successful!")

            login = True

            while login:
                print("****************************INBOX****************************")
                data_exc.check_message(username)
                print("*************************************************************\nPlease choose operations:\nA: Offer a ride\nB: Search for rides\nC: Book members or cancel bookings\nD: Post ride requests\nE: Search and delete ride requests\n0: logout from (" + username + ")")
                
                function = input("-> ").upper()
                #Q1
                if function == "A":
                    data_exc.offer_ride(username) 
                #Q2         
                elif function == 'B':
                    data_exc.search_rides(username)
                #Q3
                elif function == 'C':
                    data_exc.bookings(username)
                #Q4
                elif function == 'D':
                    data_exc.post_request(username)
                #Q5
                elif function == 'E':
                    data_exc.search_delete_requests(username)
                #logout
                elif function == '0':
                    login = False
                #exception
                else:
                    print('Invalid input!\n')

                
        #create new account
        elif choice == '2':
            while True:
                username = input('Create your username using email: ')
                user_valid = data_exc.check_username(username)
                if user_valid == '':
                    print("Username cannot be nothing!")
                    break
                elif user_valid != None:
                    print("Username already existed!")
                    break
                else:
                    # break
                    while True:
                        pwd = input('Create your password(maximum 6 characters): ')
                        if len(pwd) <= 6 and len(pwd) > 0:
                            break
                    name = input('Input your name: ')
                    while True:
                        phone = input('Input your phone: ')
                        if len(phone) <= 11:
                            break

                    result = data_exc.insert_members(username, pwd, name, phone)
                    print(result)
                    break

        #exit the program
        elif choice == '0':
            data_exc.disconnect()
            exit()

        else:
            print('Invalid input!\n')
            continue

#pass the db filename using command
main(sys.argv[1])  
        

