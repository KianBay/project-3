import paho.mqtt.client as mqtt
import mariadb, sys

class db:
    def __init__(self, user, psw, db, table):
        self._user = user
        self._psw = psw
        self._db = db
        self._table = table
            
        #We are passing the class variables as credentials to the db
        try:
            #We try to connect to our database using the db parameter as name
            self._conn = mariadb.connect(
            user="%s" % self._user,
            password="%s" % self._psw,
            host="127.0.0.1",
            port=3306,
            database="%s" % self._db,
            autocommit=True
            )
            
                #print('Sucess!')
        except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                sys.exit(1)
            
        #Nicer looking cursor object for our use
        self._cur = self._conn.cursor()

    #Returns the whole database, limited by default to latest 10000 entries
    def return_all(self, limit=100000):
        self._cur.execute(f'SELECT * FROM {self._table} LIMIT {limit}')
        all_rows = []
        for (time, loc, temp, position, created) in self._cur:
            all_rows.append(f'{loc}, {temp}, {position}, {created}')
        return all_rows
        print("\n".join(all_rows))

    def return_all_by_loc(self, loc, limit=10000):
        self._cur.execute(f'SELECT * FROM {self._table} WHERE location = {loc} LIMIT {limit}')

    def write_to_db(self, table, payload, topicLoc):
        #Cleaning the string then splitting it on space character
        data = payload[2:-1].split(' ')

        #Each data point is now a member of the list, we assign each of these to a variables
        #While stripping the leading character like T for temperature
        temp = float(data[0][1:])
        humi = float(data[1][1:])
        light = int(data[2][1:])
        loc = topicLoc
        self._cur.execute(f'INSERT INTO project3.{table}(location,temperature,humidity,lightIntensity)'
                            'VALUES (?,?,?,?)',(loc, temp, humi, light))
        


def main():
    myDb = db('root', 'newpass', 'project3', 'measures')
    #myDb = db('root', 'newpass', '127.0.0.1', 3306, 'measurements')
    print(myDb.return_all())

if __name__ == '__main__':
    main()