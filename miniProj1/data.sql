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
insert or replace into persons values ("Richard", "Wilson", "1983-04-22", "Seattle, Washington", "888 Cedar Street", "123-456-7899");

insert or replace into persons values ("Stewart", "Smith", "1989-07-14", "Brampton, Ontario", "321 Fairway Drive", "587-979-3434");

-- births
insert or replace into births values (1234567, "Richard", "Wilson", "1983-04-22", "Seattle Washington", "m", "Dwight", "Wilson", "Andrea", "Wilson");

insert or replace into births values (7654321, "Stewart", "Smith", "1989-07-14", "Brampton Ontario", "m", "Fred", "Smith", "Carla", "Smith");

-- users
insert or replace into users values ("rwilson", "qwerty", "a", "Richard", "Wilson", "Seattle");

insert or replace into users values ("ssmith1", "asdfgh", "o", "Stewart", "Smith", "Brampton");