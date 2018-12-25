import sqlite3

class tables_init:
    def __init__(self):
        self.path = "./register.db"
        self.cursor = None
        self.connection = None

    def data_init(self,recover):
        self.recover = recover
        self.connect()
        self.drop_tables()
        self.create_tables()
        self.data_insert()
        
    def connect(self):
        self.connection = sqlite3.connect(self.path)
        print("tables_init: open database successfully")
        self.cursor = self.connection.cursor()
        if self.recover:
            self.cursor.execute(' PRAGMA foreign_keys=OFF; ')
        else:
            self.cursor.execute(' PRAGMA foreign_keys=ON; ')
        self.connection.commit()
        return

    def drop_tables(self):
        drop_members = 'drop table if exists members;'
        drop_cars = 'drop table if exists cars;'
        drop_locations = 'drop table if exists locations;'
        drop_rides = 'drop table if exists rides;'
        drop_bookings = 'drop table if exists bookings;'
        drop_enroute = 'drop table if exists enroute;'
        drop_request = 'drop table if exists requests;'
        drop_inbox = 'drop table if exists inbox;'

        self.cursor.execute(drop_members)
        self.cursor.execute(drop_locations)
        self.cursor.execute(drop_cars) 
        self.cursor.execute(drop_rides)
        self.cursor.execute(drop_request)
        self.cursor.execute(drop_enroute)
        self.cursor.execute(drop_bookings)
        self.cursor.execute(drop_inbox)
        

    def create_tables(self):
        members = '''create table members (
                    email		char(15),
                    name		char(20),
                    phone		char(12),
                    pwd		    char(6),
                    primary key (email)
                    );'''

        cars = '''create table cars (
                    cno		    int,
                    make		char(12),
                    model		char(12),
                    year		int,
                    seats		int,
                    owner		char(15),
                    primary key (cno),
                    foreign key (owner) references members
                    );'''

        locations = '''create table locations (
                        lcode		char(5),
                        city		char(16),
                        prov		char(16),
                        address	char(16),
                        primary key (lcode)
                        );'''

        rides = '''create table rides (
                    rno		int,
                    price		int,
                    rdate		date,
                    seats		int,
                    lugDesc	char(10),
                    src		char(5),
                    dst		char(5),
                    driver	char(15),
                    cno		int,
                    primary key (rno),
                    foreign key (src) references locations,
                    foreign key (dst) references locations,
                    foreign key (driver) references members,
                    foreign key (cno) references cars
                    );'''

        bookings = '''create table bookings (
                        bno		int,
                        email		char(15),
                        rno		int,
                        cost		int,
                        seats		int,
                        pickup	char(5),
                        dropoff	char(5),
                        primary key (bno),
                        foreign key (email) references members,
                        foreign key (rno) references rides,
                        foreign key (pickup) references locations,
                        foreign key (dropoff) references locations
                        );'''
        enroutes = '''create table enroute (
                        rno		int,
                        lcode		char(5),
                        primary key (rno,lcode),
                        foreign key (rno) references rides,  
                        foreign key (lcode) references locations
                        );'''

        requests = '''create table requests (
                        rid		int,
                        email		char(15),
                        rdate		date,
                        pickup	char(5),
                        dropoff	char(5),
                        amount	int,
                        primary key (rid),
                        foreign key (email) references members,
                        foreign key (pickup) references locations,
                        foreign key (dropoff) references locations
                        );'''
        
        inbox = '''create table inbox (
                    email		char(15),
                    msgTimestamp	date,
                    sender	char(15),
                    content	text,
                    rno		int,
                    seen		char(1),
                    primary key (email, msgTimestamp),
                    foreign key (email) references members,
                    foreign key (sender) references members,
                    foreign key (rno) references rides
                    );'''

        self.cursor.execute(members)
        self.cursor.execute(cars)
        self.cursor.execute(locations)
        self.cursor.execute(rides)
        self.cursor.execute(bookings)
        self.cursor.execute(enroutes)
        self.cursor.execute(requests)
        self.cursor.execute(inbox)
        self.connection.commit()

    def data_insert(self):
        self.cursor.execute("INSERT INTO members VALUES \
                            ('davood@abc.com','Davood Rafiei','780-111-3333','123456'),\
                            ('joe@gmail.com','Joe Anderson','780-111-2222','123456'),\
                            ('mary@abc.com','Mary Smith','780-222-3333','123456'),\
                            ('ajohn@gmail.com','ajohn aduo','780-333-4441','123456'),\
                            ('bjohn@gmail.com','bjohn aduo','780-333-4442','123456'),\
                            ('cjohn@gmail.com','cjohn aduo','780-333-4443','123456'),\
                            ('djohn@gmail.com','djohn aduo','780-333-4444','123456'),\
                            ('ejohn@gmail.com','ejohn aduo','780-333-4445','123456'),\
                            ('fjohn@gmail.com','fjohn aduo','780-333-4446','123456'),\
                            ('gjohn@gmail.com','gjohn aduo','780-333-4447','123456'),\
                            ('hjohn@gmail.com','hjohn aduo','780-333-4448','123456'),\
                            ('ijohn@gmail.com','ijohn aduo','780-333-4449','123456'),\
                            ('paul@a.com','John Paul','780-333-4444','123456'),\
                            ('ljohn@gmail.com','l john','777','123456'),\
                            ('mjohn@gmail.com','m john','123','123456'),\
                            ('njohn@gmail.com','n john','12334','123456'),\
                            ('ojohn@gmail.com','o john','12334','123456'),\
                            ('pjohn@gmail.com','p john','34242','123456'),\
                            ('q8@gmail.com','user question8','19376','123456'), \
                            ('q81@gmail.com','user2 question8','19377','123456');")

        self.cursor.execute("INSERT INTO cars VALUES \
                            (1,'Aston Martin','DB5',1964,1,'davood@abc.com'),\
                            (2,'Honda','Civic',2017,4,'joe@gmail.com'),\
                            (3,'Nissan','Rogue',2018,4,'mary@abc.com'),\
                            (4,'Honda','DB5',2016,1,'ajohn@gmail.com'),\
                            (5,'Honda','Civic',2017,4,'ajohn@gmail.com'),\
                            (6,'Nissan','Rogue',2018,3,'ajohn@gmail.com'),\
                            (7,'Nissan','Rogue',2019,5,'davood@abc.com'),\
                            (8,'Nissan','Rogue',2000,5,'cjohn@gmail.com'),\
                            (9,'Honda','Rogue',2001,4,'cjohn@gmail.com'),\
                            (10,'Honda','Rogue',2001,4,'djohn@gmail.com'),\
                            (11,'Honda','Rogue',2002,4,'djohn@gmail.com'),\
                            (12,'Honda','Rogue',2003,4,'djohn@gmail.com'),\
                            (20,'','','',4,'ljohn@gmail.com'),\
                            (21,'','','',4,'mjohn@gmail.com'),\
                            (13,'','','',5,'mjohn@gmail.com'),\
                            (22,'','','','','pjohn@gmail.com');")
        
        self.cursor.execute("INSERT into locations VALUES \
                            ('ab1','Edmonton','Alberta','UofA LRT st'),\
                            ('ab2','Edmonton','Alberta','Century LRT st'),\
                            ('ab3','Edmonton','Alberta','Rogers Place'),\
                            ('ab4','Calgary','Alberta','111 Edmonton Tr'),\
                            ('ab5','Calgary','Alberta','Airport'),\
                            ('ab6','Red Deer','Alberta','City Hall'),\
                            ('ab7','Red Deer','Alberta','Airport'),\
                            ('bc1','Vancouver','British Columbia','Stanley Park'),\
                            ('bc2','Vancouver','British Columbia','Airport'),\
                            ('bc888','Vancouver','British Columbia','BC Place'),\
                            ('bc999','Vancouver','British Columbia','Burrard Street'),\
                            ('on300','Toronto','Ontario','Bay Street'),\
                            ('on301','Ottawa','Ontario','Ahearn Avenue');")

        self.cursor.execute("INSERT into rides VALUES \
                            (100,30,'2018-11-12',7,'small bag','ab1','ab4','joe@gmail.com',2),\
                            (101,30,'2018-11-13',3,'small bag','ab1','ab4','joe@gmail.com',2),\
                            (102,40,'2018-11-12',3,'small bag','ab1','ab4','cjohn@gmail.com',8),\
                            (103,50,'2018-11-12',3,'small bag','ab1','ab4','djohn@gmail.com',12),\
                            (104,50,'2017-11-12',3,'','ab1','ab4','joe@gmail.com',NULL),\
                            (105,50,'2018-12-12',3,'','ab1','ab4','joe@gmail.com',2),\
                            (106,50,'2018-11-12',3,'','ab1','bc1','joe@gmail.com',2),\
                            (107,50,'2018-11-12',3,'','bc1','ab4','joe@gmail.com',2),\
                            (108,50,'2018-11-20',3,'','ab4','ab1','joe@gmail.com',2),\
                            (109,200,'2018-10-1',4,'','ab4','ab1','hjohn@gmail.com',13),\
                            (110,300,'2018-10-1',4,'','ab4','ab1','hjohn@gmail.com',13),\
                            (111,310,'2018-10-1',4,'','ab4','ab1','hjohn@gmail.com',13),\
                            (112,150,'2018-11-1',4,'','ab4','ab1','hjohn@gmail.com',13),\
                            (113,140,'2017-11-1',4,'','ab4','ab1','hjohn@gmail.com',13),\
                            (114,130,'2016-9-1',4,'','ab4','ab1','hjohn@gmail.com',13),\
                            (115,120,'2018-10-1',4,'','ab4','bc1','hjohn@gmail.com',13),\
                            (116,110,'2018-10-1',4,'','bc1','ab1','hjohn@gmail.com',13),\
                            (117,100,'2018-10-1',4,'','bc1','bc2','hjohn@gmail.com',13),\
                            (118,10,'2015-11-11',2,'','ab1','ab2','ljohn@gmail.com',20),\
                            (119,10,'2015-10-11',2,'','ab1','ab2','ljohn@gmail.com',20),\
                            (120,10,'2015-09-11',2,'','ab1','ab2','ljohn@gmail.com',20),\
                            (121,10,'2015-08-11',2,'','ab1','ab2','ljohn@gmail.com',20),\
                            (122,30,'2018-12-10',3,'','ab1','ab4','mjohn@gmail.com',21),\
                            (123,30,'2017-12-10',3,'','ab1','ab4','mjohn@gmail.com',21),\
                            (124,30,'2018-10-10',3,'','ab1','ab4','mjohn@gmail.com',21),\
                            (131,20,'2018-10-14',3,'','ab1','ab4','mjohn@gmail.com',21),\
                            (132,10,'2018-10-15',4,'','ab1','ab4','mjohn@gmail.com',21),\
                            (125,30,'2018-12-10',3,'','ab1','bc1','mjohn@gmail.com',21),\
                            (126,30,'2018-12-10',3,'','bc1','ab4','mjohn@gmail.com',21),\
                            (127,10,'2018-12-12','','','bc1','ab1','pjohn@gmail.com',22),\
                            (128,10,'2018-12-12','','','bc1','ab3','pjohn@gmail.com',22),\
                            (129,10,'2018-12-12','','','bc1','ab4','pjohn@gmail.com',22),\
                            (130,10,'2018-12-12','','','bc1','ab5','pjohn@gmail.com',22),\
                            (914,10,'2018-08-08','','','bc888','bc1','q8@gmail.com',22),\
                            (915,10,'2018-08-09','','','bc888','bc2','q8@gmail.com',22),\
                            (916,10,'2018-08-10','','','bc999','bc888','q8@gmail.com',22),\
                            (917,10,'2018-08-11','','','bc888','bc999','q8@gmail.com',22),\
                            (918,10,'2012-01-20','','','ab2','ab1','q81@gmail.com',22),\
                            (919,10,'2014-01-20','','','ab1','ab2','q81@gmail.com',22),\
                            (920,10,'2015-01-20','','','ab1','ab3','q81@gmail.com',22),\
                            (921,10,'2017-03-23','','','ab2','ab4','q81@gmail.com',22),\
                            (777,20,'2018-11-07',NULL,'','ab3','ab5','pjohn@gmail.com',22),\
                            (778,20,'2018-11-07','','','ab3','ab5','pjohn@gmail.com',22),\
                            (308,20,'2014-12-16','','','on300','on301','ljohn@gmail.com',20),\
                            (309,20,'2014-12-17','','','on300','on301','ljohn@gmail.com',20),\
                            (310,20,'2014-12-18','','','on300','on301','ljohn@gmail.com',20),\
                            (1002,55,'2018-12-01',1,'no luggage','ab2','ab5','joe@gmail.com',2),\
                            (1003,60,'2018-12-13',3,'light','ab1','ab5','mjohn@gmail.com',21),\
                            (1005,10,'2018-12-29',2,'no luggage','ab2','ab5','pjohn@gmail.com',2);")

        self.cursor.execute("INSERT INTO bookings VALUES \
                            (10,'davood@abc.com',100,NULL,1,'ab2',NULL),\
                            (12,'davood@abc.com',101,28,1,'ab2','ab5'),\
                            (14,'paul@a.com',100,NULL,1,NULL,NULL),\
                            (15,'joe@gmail.com',100,10,2,'ab1','ab4'),\
                            (16,'fjohn@gmail.com',100,10,2,'ab1','ab4'),\
                            (17,'ejohn@gmail.com',104,10,1,'ab1','ab4'),\
                            (18,'ejohn@gmail.com',105,10,1,'ab1','ab4'),\
                            (19,'ejohn@gmail.com',106,10,1,'ab1','bc1'),\
                            (20,'ejohn@gmail.com',107,10,1,'bc1','ab4'),\
                            (21,'ejohn@gmail.com',108,10,1,'ab4','ab1'),\
                            (22,'ejohn@gmail.com',122,10,3,'ab1','ab4'),\
                            (23,'ejohn@gmail.com',124,10,2,'ab1','ab4'),\
                            (24,'ejohn@gmail.com',125,10,1,'ab1','ab4'),\
                            (25,'ejohn@gmail.com',111,10,3,'ab1','ab4'),\
                            (26,'ejohn@gmail.com',112,10,2,'ab1','ab4'),\
                            (27,'ejohn@gmail.com',113,10,1,'ab1','ab4'),\
                            (28,'ejohn@gmail.com',115,10,2,'ab1','ab4'),\
                            (29,'ejohn@gmail.com',132,10,6,'ab1','ab4'),\
                            (30,'pjohn@gmail.com',777,12,4,'ab2','ab4'),\
                            (31,'pjohn@gmail.com',778,12,4,'ab2','ab4'),\
                            (102,'pjohn@gmail.com',1003,60,3,'ab1','ab5'),\
                            (105,'ejohn@gmail.com',1002,55,2,'ab1','ab4'),\
                            (106,'ejohn@gmail.com',1005,55,1,'ab2','ab5');")

        self.cursor.execute("INSERT INTO requests VALUES \
                            (1,'paul@a.com','2018-12-22','ab3','bc1',80),\
                            (2,'davood@abc.com','2018-12-24','ab1','ab7',30),\
                            (3,'fjohn@gmail.com','2018-12-13','ab1','ab4',50),\
                            (4,'fjohn@gmail.com','2018-12-12','ab1','ab4',60),\
                            (5,'fjohn@gmail.com','2018-12-12','ab1','ab4',40),\
                            (6,'fjohn@gmail.com','2018-12-12','ab2','ab4',50),\
                            (7,'fjohn@gmail.com','2018-12-12','bc1','ab4',50),\
                            (8,'fjohn@gmail.com','2018-12-12','ab1','ab5',50),\
                            (9,'fjohn@gmail.com','2018-12-12','ab1','ab6',50);")

        self.cursor.execute("INSERT INTO enroute VALUES\
                            (122, 'ab3'), \
                            (116, 'bc2');")

        self.cursor.execute("INSERT INTO inbox VALUES\
                            ('davood@abc.com', '2018-05-09 21:13:20', 'mary@abc.com', 'i love u', 120, 'n'),\
                            ('davood@abc.com', '2018-05-09 15:13:20', 'njohn@gmail.com', 'i dont love u', 121, 'n');")

        self.connection.commit()
    