from datetime import datetime
from random import random
from pydantic import BaseModel

class Measurement(BaseModel):
    """
    This class represents a measurement taken from a sensor.
    """
    timestamp: str 
    value: float 
    unit: str | None

class Device:
    def __init__(self, id, supplier, device_type, model_name, room = None, name = None) -> None:
        self.id = id
        self.supplier = supplier
        self.device_type = device_type
        self.model_name = model_name
        self.room = room
        self.name = name

    def is_sensor(self):
        return False
    
    def is_actuator(self):
        return False

class Sensor(Device):
    def __init__(self, id, supplier, device_type, model_name, room = None, name=None, unit = None) -> None:
        super().__init__(id, supplier, device_type, model_name, room, name)
        self.unit = unit
        self.measurments = []
        
    def is_sensor(self):
        return True
    
    def last_measurement(self):
        if len(self.measurments) > 0:
            return self.measurments[-1]
        else:
            return Measurement(datetime.now().isoformat(), random() * 10, self.unit)
    
    
class Actuator(Device):
    def __init__(self, id, supplier, device_type, model_name, actuator_state: bool = False, room = None, name=None) -> None:
        super().__init__(id, supplier, device_type, model_name, room, name)
        self.actuator_state = actuator_state
        self.state = actuator_state  #må legges inn for å få godkjent tester
        
    def is_actuator(self):
        return True
    
    def turn_on(self, target_value = None):
        if target_value is None:
            self.actuator_state = True
            self.state = True
        elif target_value:
            self.actuator_state = True
            self.state = True

    def turn_off(self):
        self.actuator_state = False
        self.state = False

    def is_active(self):
        return self.actuator_state

class ActuatorWithSensor(Device):
    def __init__(self, id, supplier, device_type, model_name, actuator_state: bool = False, room = None, name=None, unit = None) -> None:
        super().__init__(id, supplier, device_type, model_name, room, name)
        self.unit = unit
        self.actuator_state = actuator_state
        
    def is_sensor(self):
        return True
    
    def is_actuator(self):
        return True
    
    def turn_on(self, target_value = None):
        if target_value is None:
            self.actuator_state = True
        elif target_value:
            self.actuator_state = True

    def turn_off(self):
        self.actuator_state = False
    
    def is_active(self):
        return self.actuator_state


class Floor:
    '''
    This class represents a floor in the smarthouse
    '''
    def __init__(self, level:int) -> None:
        self.level = level
        self.rooms = []

class Room:
    '''
    This class represents a room in the smarthouse
    '''
    def __init__(self, area: float, floor: Floor, room_name: str = None, rid = None) -> None:
        self.area = area
        self.floor = floor
        self.room_name = room_name
        self.rid = rid
        self.db_id = rid #lagt inn for å passe testen
        self.devices = []


    def register_device(self, device: Device):
        self.devices.append(device)
        
        

class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """
    def __init__(self) -> None:
        self.floors = []

    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        floor = Floor(level)
        self.floors.append(floor)
        return floor

    def register_room(self, floor: Floor, room_size, room_name = None, rid = None):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        room = Room(room_size, floor, room_name, rid)
        floor.rooms.append(room)
        
        return room


    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        return self.floors
        


    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        floors = self.get_floors()

        rooms = []
        for floor in floors:
            rooms.extend(floor.rooms)
        
        return rooms


    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        rooms = self.get_rooms()
        areas = []
        for room in rooms:
            areas.append(room.area)
        
        return sum(areas)

    def register_device(self, room: Room, device: Device):
        """
        This methods registers a given device in a given room.
        """
        old_room = device.room
        if old_room:
            old_room.devices.remove(device)
        device.room = room
        room.register_device(device)


    
    def get_devices(self):
        """
        This method retrives all devices in the smarthouse
        """
        rooms = self.get_rooms()
        devices = []
        for room in rooms:
            devices.extend(room.devices)
        
        return devices
        

    def get_device_by_id(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        devices = self.get_devices()
        the_device = None

        for device in devices:
            if device.id == device_id:
                the_device = device

        
        return the_device


