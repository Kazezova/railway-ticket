from connect import conn

cursor = conn.cursor()


def generate(trip_id, date):
    if cursor.execute(
            "SELECT TOP 1 * FROM ticket WHERE trip='%s' AND depature_date='%s'" % (trip_id, date)).rowcount == 0:
        train_id = int(trip_id[2]) * 100000
        for i in range(1, 16):
            for j in range(1, 31):
                seat_id = train_id + i * 100 + j
                query = "INSERT INTO ticket(depature_date, seat_id, trip) VALUES ('%s', '%i', '%s')"
                cursor.execute(query % (date, seat_id, trip_id))
                cursor.commit()
    else:
        print('Tickets on this trip and date were previously generated.')


generate('AL2001', '2021-06-02')
