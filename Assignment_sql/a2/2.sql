.print Question2 - zijun4
SELECT name, email
FROM members
EXCEPT
SELECT name, email
FROM members m, rides rd
WHERE m.email = rd.driver
INTERSECT
SELECT m.name, m.email
FROM members m, cars c, bookings b 
WHERE m.email = c.owner and m.email = b.email;