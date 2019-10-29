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

-- births
insert or replace into births values (888888888, "Richard", "Wilson", "1983-04-22", "Seattle Washington", "m", "Dwight", "Wilson", "Andrea", "Wilson");

insert or replace into births values (76543219, "Stewart", "Smith", "1989-07-14", "Brampton Ontario", "m", "Fred", "Smith", "Carla", "Smith");

insert or replace into births values (79685715, "Cassandra", "Cage", "1993-01-01", "Los Angeles, California", "f", "Johnny", "Cage", "Sonya", "Blade");

-- vehicles
insert or replace into vehicles values (7777777, "Porsche", "Boxter", 2017, "pink");
insert or replace into vehicles values (1717171, "Audi", "R8", 2019, "purple");

-- registrations
insert or replace into registrations values (999999999, "2017-06-19", "2020-06-19", "CASSIE", 7777777, "Cassandra", "Cage");
insert or replace into registrations values (191919191, "2019-03-07", "2023-03-07", "LUVU2", 1717171, "Cassandra", "Cage");

-- tickets
insert or replace into tickets values (395121, 999999999, 150, "Speeding", "2019-08-22");
insert or replace into tickets values (164186, 191919191, 250, "Red light violation", "2019-09-09");
insert or replace into tickets values (853983, 191919191, 300, "Impaired driving", "2019-01-30");
insert or replace into tickets values (365540, 999999999, 300, "Street racing", "2019-10-26");

-- users
insert or replace into users values ("rwilson", "qwerty", "a", "Richard", "Wilson", "Seattle");

insert or replace into users values ("ssmith1", "asdfgh", "o", "Stewart", "Smith", "Brampton");