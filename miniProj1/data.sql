-- persons(fname, lname, bdate, bplace, address, phone)

-- births(regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname)

-- marriages(regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname)

-- vehicles(vin, make, model, year, color)

-- registrations(regno, regdate, expiry, plate, vin, fname, lname)

-- tickets(tno, regno, fine, violation, vdate)

-- demeritNotices(ddate, fname, lname, points, desc)

-- payments(tno, pdate, amount)

-- users(uid, pwd, utype, fname, lname, city)

insert or replace into persons values ("Richard", "Wilson", "1983-04-22", "Seattle, Washington", "888 Cedar Street", "123-456-7899");
