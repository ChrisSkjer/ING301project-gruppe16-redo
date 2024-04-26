import sqlite3
from typing import Optional
from smarthouse.domain import Measurement, SmartHouse, Room, Floor, Sensor, Actuator,ActuatorWithSensor, Device

class SmartHouseRepository:
    """
    Provides the functionality to persist and load a _SmartHouse_ object 
    in a SQLite database.
    """

    def __init__(self, file: str) -> None:
        self.file = file
        self.conn = sqlite3.connect(file, check_same_thread=False)

    def __del__(self):
        self.conn.close()

    def cursor(self) -> sqlite3.Cursor:
        """
        Provides a _raw_ SQLite cursor to interact with the database.
        When calling this method to obtain a cursors, you have to 
        rememeber calling `commit/rollback` and `close` yourself when
        you are done with issuing SQL commands.
        """
        return self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)

    
    def load_smarthouse_deep(self):
        """
        This method retrives the complete single instance of the _SmartHouse_ 
        object stored in this database. The retrieval yields a _deep_ copy, i.e.
        all referenced objects within the object structure (e.g. floors, rooms, devices) 
        are retrieved as well. 
        """
        # TODO: START here! remove the following stub implementation and implement this function 
        #       by retrieving the data from the database via SQL `SELECT` statements.

        house = SmartHouse()
        c = self.cursor()
        
        

        #Creating floors
        c.execute("SELECT MAX(floor) from rooms;")
        no_floors = c.fetchone()[0]
        floors = []
        for i in range(0, no_floors):
            floors.append(house.register_floor(i + 1))

        #Creating rooms
        room_dict = {}
        c.execute("SELECT floor, area, name, id from rooms;")
        rooms = c.fetchall()
        for room_tuple in rooms:
            floor = floors[int(room_tuple[0])-1]
            area = float(room_tuple[1])
            room_name = room_tuple[2]
            rid = room_tuple[3]
            room = house.register_room(floor, area, room_name, rid)
            room_dict[rid] = room

        #Creating devices
        c.execute("SELECT id, room, kind, category, supplier , product FROM devices;")
        device_tuples = c.fetchall()
        
        device_dict = {}
        for device_tuple in device_tuples:
            room = room_dict[device_tuple[1]]
            category = device_tuple[3]
            did = device_tuple[0]
            supplier = device_tuple[4]
            device_type = device_tuple[2]
            model_name = device_tuple[5]

            if category == "sensor":
                device = Sensor(did, supplier, device_type, model_name)
                
            elif category == "actuator":
                device = Actuator(did, supplier, device_type, model_name)
               
            else: 
                device = ActuatorWithSensor(did, supplier, device_type, model_name)
               
            house.register_device(room, device)
            device_dict[device.id] = device
        
        c.execute("SELECT * FROM states s; ")
        states = c.fetchall()

        for state in states:
            device = device_dict[state[0]]
            device.actuator_state = state[1]

        c.close()

        return house
    
    def get_readings(self, sensor: str, limit_n: int | None) -> list[Measurement]:
        cursor = self.cursor()
        if limit_n:
            cursor.execute("""\
SELECT ts, value, unit 
FROM measurements
WHERE device = ?
ORDER BY datetime(ts) DESC 
LIMIT ?
            """, (sensor, limit_n))
        else:
            cursor.execute("""\
SELECT ts, value, unit 
FROM measurements
WHERE device = ?
ORDER BY datetime(ts) DESC 
            """, (sensor,))
        tuples = cursor.fetchall()
        result = [Measurement(timestamp=t[0], value=t[1], unit=t[2]) for t in tuples]
        cursor.close()
        return result


    def delete_oldest_reading(self, sensor: str) -> Measurement | None:
        c = self.cursor()
        query = """\
SELECT ts, value, unit FROM measurements WHERE device = ? ORDER BY datetime(ts) ASC LIMIT 1
        """
        c.execute(query, (sensor,))
        tup = c.fetchone()
        if tup:
            query = f"""
    DELETE FROM measurements
    WHERE device = ?
    AND ts = ?
            """
            c.execute(query, (sensor, tup[0]))
            self.conn.commit()
        c.close()
        if tup:
            return Measurement(timestamp=tup[0], value=tup[1], unit=tup[2])
        else:
            return None

            

    def insert_measurement(self, sensor: str, measurement: Measurement) -> None:
        query = f"""
INSERT INTO measurements (device, ts, value, unit) VALUES (?, ?, ?, ?)
        """
        c = self.cursor()
        c.execute(query, (sensor, measurement.timestamp, measurement.value, measurement.unit))
        self.conn.commit()
        c.close()


    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        c = self.cursor()
        
        c.execute("""SELECT device, MAX(ts), value, unit FROM measurements m
                    WHERE m.device = ?;""", (sensor.id, ))
        measurment_tuple = c.fetchall()[0]
        c.close()
        if  measurment_tuple[0] is None:
            return None

        else:
            ts = measurment_tuple[1]
            value = measurment_tuple[2]
            unit = measurment_tuple[3]
            return Measurement(ts, value, unit)


    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
        cur = self.cursor()
       
        cur.execute("""UPDATE states SET state = ? WHERE device = ? """, (actuator.is_active(), actuator.id))
        
        self.conn.commit()
        cur.close()
    


    # statistics

    
    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> dict:
        """Calculates the average temperatures in the given room for the given time range by
        fetching all available temperature sensor data (either from a dedicated temperature sensor 
        or from an actuator, which includes a temperature sensor like a heat pump) from the devices 
        located in that room, filtering the measurement by given time range.
        The latter is provided by two strings, each containing a date in the ISO 8601 format.
        If one argument is empty, it means that the upper and/or lower bound of the time range are unbounded.
        The result should be a dictionary where the keys are strings representing dates (iso format) and 
        the values are floating point numbers containing the average temperature that day.
        """
        result = {}
        if isinstance(room, Room) and room.db_id is not None:
            lower_bound_pred = ""
            upper_bound_pred = ""
            if from_date is not None:
                lower_bound_pred = f"AND ts >= '{from_date} 00:00:00'"
            if until_date is not None:
                upper_bound_pred = f"AND ts <= '{until_date} 23:59:59'"
            query = f"""
    SELECT STRFTIME('%Y-%m-%d', DATETIME(ts)), avg(value) 
    FROM devices d 
    INNER join measurements m ON m.device = d.id 
    WHERE d.room = {room.db_id} AND m.unit = '°C' {lower_bound_pred} {upper_bound_pred}
    GROUP BY STRFTIME('%Y-%m-%d', DATETIME(ts)) ;
            """
            cursor = self.cursor()
            cursor.execute(query)
            query_result = cursor.fetchall()
            for row in query_result:
                result[row[0]] = float(row[1])
        return result

    
    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        result = []
        if isinstance(room, Room) and room.db_id is not None:
            query = f"""
SELECT  STRFTIME('%H', DATETIME(m.ts)) AS hours 
FROM measurements m 
INNER JOIN devices d ON m.device = d.id 
INNER JOIN rooms r ON r.id = d.room 
WHERE 
r.id = {room.db_id}
AND m.unit = '%' 
AND DATE(m.ts) = DATE('{date}')
AND m.value > (
	SELECT AVG(value) 
	FROM measurements m 
	INNER JOIN devices d on d.id = m.device
	WHERE d.room = 4 AND DATE(ts) = DATE('{date}'))
GROUP BY hours
HAVING COUNT(m.value) > 3;
            """
            cursor = self.cursor()
            cursor.execute(query)
            for h in cursor.fetchall():
                result.append(int(h[0]))
        return result

