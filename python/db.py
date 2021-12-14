import paho.mqtt.client as mqtt
import mariadb, sys
import pandas as pd

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
        for (id, time, loc, temp, position, created) in self._cur:
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

    #Converting to a dataframe since it is much easier to graph from
    def db_to_df(self):

        self._df = pd.read_sql("SELECT * FROM measurements", self._conn)
        return self._df

    def get_unique_classrooms(self, table, column):
        self._cur.execute(f'SELECT DISTINCT {column} FROM {table}')
        unique_classrooms = []
        for classroom in self._cur:
            #Since these are tuples with a single member we iterate once again to get plain strings
            for i in classroom:
                unique_classrooms.append(i)
        return unique_classrooms
    """
    def get_match_on_room(self, table, classroom):
        mac_adds = []
        #Needs quotes around the string for sql to interpret correctly; else it expects a column name
        self._cur.execute(f'SELECT mac FROM {table} WHERE classroom = "{classroom}"')
        for mac in self._cur:
            for i in mac:
                mac_adds.append(i)
        return mac_adds
"""

    #This function is used to get the mac address from a classroom id
    def get_match_on_room(self, table, classroom):
        mac_adds = []
        #Needs quotes around the string for sql to interpret correctly; else it expects a column name
        mac = self._cur.execute(f'SELECT MacAddress FROM {table} WHERE Classroom = "{classroom}"')
        for mac in self._cur:
            for i in mac:
                mac_adds.append(i)
        #Gives an IndexError saying list index is out of range, yet the list has 1 member and the first element is
        #the one to be returned... Curious. It works though, but needs looking at!
        return mac_adds[0]
    #This function is used for graphing the data based on the given mac address
    def db_mac_to_df(self, table, mac):
        self._df = pd.read_sql(f'SELECT * FROM {table} WHERE location = "{mac}"', self._conn)
        return self._df

def main():
    myDb = db('root', 'newpass', 'project3', 'measurements')
    #myDb = db('root', 'newpass', '127.0.0.1', 3306, 'measurements')
    #print(myDb.return_all())
    #myDb.db_to_df()
    #print(myDb.db_to_df())
    df = myDb.db_mac_to_df('measurements', '04:8C:9A:2E:46:77')
    print(df)
    #classrooms = myDb.get_unique_classrooms('locations', 'classroom')
    #print(type(classrooms))
    #locs = myDb.get_match_on_room('locations', 'a12.16')
    #print(locs)
    #mac = '04:8C:9A:2E:46:77'
    #df = myDb.db_mac_to_df('measurements', mac)
    #classroom = 'a12.16'
    #mac = myDb.get_match_on_room('locations', classroom)
    #print(mac)
    #print(type(mac))
    
#04:8C:9A:2E:46:77 one of our mac addys
if __name__ == '__main__':
    main()