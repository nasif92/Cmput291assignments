-- persons(fname, lname, bdate, bplace, address, phone)

-- births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname)

-- marriages(regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname)

-- vehicles(vin, make, model, year, color)

-- registrations(regno, regdate, expiry, plate, vin, fname, lname)

-- tickets(tno, regno, fine, violation, vdate)

-- demeritNotices(ddate, fname, lname, points, desc)

-- payments(tno, pdate, amount)

-- users(uid, pwd, utype, fname, lname, city)


-- persons
insert or replace into persons values ("Dwight", "Wilson", "1954-08-24", "Edison, New Jersey", "111 Boyle Street", "897-888-4343");
insert or replace into persons values ("Andrea", "Wilson", "1956-01-12", "Manhattan, New York", "222 Aspen Avenue", "987-432-7654");

insert or replace into persons values ("Richard", "Wilson", "1983-04-22", "Seattle, Washington", "888 Cedar Street", "123-456-7899");
                                         

insert or replace into persons values ("Fred", "Smith", "1960-08-04", "Calgary, Alberta", "321 Fairway Drive", "474-131-2233");
insert or replace into persons values ("Carla", "Smith", "1962-03-21", "Edmonton, Alberta", "321 Fairway Drive", "834-454-9999");

insert or replace into persons values ("Stewart", "Smith", "1989-07-14", "Brampton, Ontario", "321 Fairway Drive", "587-979-3434");


insert or replace into persons values ("Johnny", "Cage", "1966-05-11", "Phoenix, Arizona", "4312 Broadview Road", "231-451-6734");
insert or replace into persons values ("Sonya", "Blade", "1969-04-09", "San Fransisco, California", "873 Allard Drive", "999-888-7777");

insert or replace into persons values ("Cassandra", "Cage", "1993-01-01", "Los Angeles, California", "747 Meadowlark Road", "111-222-3333");


insert or replace into persons values ("Jackson", "Briggs", "1959-05-29", "Denver, Colorado", "344 Fredrickson Avenue", "239-445-7355");
insert or replace into persons values ("Vera", "Briggs", "1964-01-10", "Miami, Florida", "344 Fredrickson Avenue", "849-148-8383");

insert or replace into persons values ("Jacqui", "Briggs", "1991-09-30", "Denver, Colorado", "819 Pleasant Park", "619-619-6191");

-- births
insert or replace into births values (88888888, "Richard", "Wilson", "1983-04-22", "Seattle Washington", "m", "Dwight", "Wilson", "Andrea", "Wilson");

insert or replace into births values (76543219, "Stewart", "Smith", "1989-07-14", "Brampton Ontario", "m", "Fred", "Smith", "Carla", "Smith");

insert or replace into births values (79685715, "Cassandra", "Cage", "1993-01-01", "Los Angeles, California", "f", "Johnny", "Cage", "Sonya", "Blade");

insert or replace into births values (12345678, "Jacqui", "Briggs", "1991-09-30", "Miami, Florida", "f", "Jackson", "Briggs", "Vera", "Briggs");

-- vehicles
insert or replace into vehicles values (7777777, "Porsche", "Boxter", 2017, "pink");
insert or replace into vehicles values (1717171, "Audi", "R8", 2019, "purple");
insert or replace into vehicles values (7700077, "Lamborghini", "Aventador", 2018, "pink");

insert or replace into vehicles values (1234567, "Toyota", "Prius", 2018, "white");
insert or replace into vehicles values (7654321, "Honda", "Accord", 2018, "black");

insert or replace into vehicles values (5489721, "Dodge", "Dart", 2018, "Orange");

-- registrations
insert or replace into registrations values (999999999, "2017-06-19", "2020-06-19", "CASSIE", 7777777, "Cassandra", "Cage");
insert or replace into registrations values (191919191, "2019-03-07", "2023-03-07", "LUVU2", 1717171, "Cassandra", "Cage");
insert or replace into registrations values (990000099, "2018-07-05", "2021-07-05", "CATCHME", 7700077, "Cassandra", "Cage");
insert or replace into registrations values (123231099, "2019-05-05", "2021-07-05", "VOTEME", 7123127, "Sonya", "Blade");

insert or replace into registrations values (333666999, "2018-03-12", "2021-03-12", "EATTHIS", 1234567, "Jacqui", "Briggs");
insert or replace into registrations values (999666333, "2018-10-29", "2021-10-29", "IAMCOOL", 7654321, "Jacqui", "Briggs");

insert or replace into registrations values (473682223, "2018-01-10", "2021-01-10", "AMERICA", 5489721, "Jackson", "Briggs");

-- tickets
insert or replace into tickets values (395121, 999999999, 150, "Speeding", "2019-08-22");
insert or replace into tickets values (164186, 191919191, 250, "Red light violation", "2019-09-09");
insert or replace into tickets values (853983, 191919191, 300, "Impaired driving", "2019-01-30");
insert or replace into tickets values (365540, 999999999, 300, "Street racing", "2019-10-26");
insert or replace into tickets values (258800, 999999999, 200, "Drifting", "2019-10-29");

insert or replace into tickets values (261095, 999666333, 250, "Hit and Run", "2019-10-30");

-- demeritNotices(ddate, fname, lname, points, desc)
insert or replace into demeritNotices values ("2018-05-30","Cassandra", "Cage", 2, "Speeding");
insert or replace into demeritNotices values ("2019-05-30","Cassandra", "Cage", 5, "Speeding");
insert or replace into demeritNotices values ("2018-01-30","Cassandra", "Cage", 5, "Speeding");
insert or replace into demeritNotices values ("2017-11-30","Cassandra", "Cage", 5, "Speeding");
insert or replace into demeritNotices values ("2019-10-30","Cassandra", "Cage", 5, "Repair");

insert or replace into demeritNotices values ("2018-05-30","Cassandra", "Cage", 10, "Dead");
insert or replace into demeritNotices values ("2018-05-15","Sonya", "Blade", 2, "Speeding");

insert or replace into demeritNotices values ("2013-07-12","Richard", "Wilson", 5, "Hit and Run");
insert or replace into demeritNotices values ("2018-05-30","Jacqui", "Briggs", 2, "Speeding");

insert or replace into demeritNotices values ("2019-07-12","Richard", "Wilson", 5, "Hit and Run");
insert or replace into demeritNotices values ("2019-07-12","Jacqui", "Briggs", 5, "Hit and Run");


-- payments(tno, pdate, amount)
insert or replace into payments values (365540, "2019-10-31", 300);


-- users
insert or replace into users values ("rwilson", "qwerty", "a", "Richard", "Wilson", "Seattle");

insert or replace into users values ("ssmith1", "asdfgh", "o", "Stewart", "Smith", "Brampton");




