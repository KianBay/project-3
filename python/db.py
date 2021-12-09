import paho.mqtt.client as mqtt
import mariadb, sys

class db:
    def __init__(self, user, psw, db, table):
        self._user = user
        self._psw = psw
        self._db = db
        self._table = table
            
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

    def return_all(self, limit=100000):
        self._cur.execute(f'SELECT * FROM {self._table} LIMIT {limit}')
        all_rows = []
        for (id, temp, position, created) in self._cur:
            all_rows.append(f'{temp}, {position}, {created}')
        return all_rows
        print("\n".join(all_rows))

    def write_to_db(self, table, payload):
        data = payload.split(' ')
        
        temp = float(data[0][3:])
        #temp = float(temp[3:])
        humi = float(data[1][1:])
        light = int(data[2][1:])
        loc = data[3][0:-1]
        self._cur.execute(f'INSERT INTO project3.{table}(location,temperature,humidity,lightIntensity)'
                            'VALUES (?,?,?,?)',(loc, temp, humi, light))
        print(data)


def main():
    myDb = db('root', 'newpass', 'measurements', 'temperature')
    #myDb = db('root', 'newpass', '127.0.0.1', 3306, 'measurements')
    myDb.return_all()

if __name__ == '__main__':
    main()