from smarthouse.domain import SmartHouse, Actuator, Sensor, ActuatorWithSensor

DEMO_HOUSE = SmartHouse()

# Building house structure
ground_floor = DEMO_HOUSE.register_floor(1)
entrance = DEMO_HOUSE.register_room(ground_floor, 13.5, "Entrance")
# TODO: continue registering the remaining floor, rooms and devices

second_floor = DEMO_HOUSE.register_floor(2)

living_room = DEMO_HOUSE.register_room(ground_floor, 39.75, "LivingRoom/Kitchen")
bath1 = DEMO_HOUSE.register_room(ground_floor, 6.3, "Bathroom 1")
gR1 = DEMO_HOUSE.register_room(ground_floor, 8, "GuestRoom 1")
garage = DEMO_HOUSE.register_room(ground_floor, 19, "Garage")

office = DEMO_HOUSE.register_room(second_floor, 11.75, "Office")
bath2 = DEMO_HOUSE.register_room(second_floor, 9.25, "Bathroom 2")
gR2 = DEMO_HOUSE.register_room(second_floor, 8, "GuestRoom 2")
gR3 = DEMO_HOUSE.register_room(second_floor, 10, "GuestRoom 3")
dR = DEMO_HOUSE.register_room(second_floor, 4, "DressingRoom")
Hall = DEMO_HOUSE.register_room(second_floor, 10, "Hallway")
MasterBed = DEMO_HOUSE.register_room(second_floor, 17, "Master Bedroom")

smartLock = Actuator("4d5f1ac6-906a-4fd1-b4bf-3a0671e4c4f1", "MythicalTech", "Smart Lock", "Guardian Lock 7000")
cO2Sensor = Sensor("8a43b2d7-e8d3-4f3d-b832-7dbf37bf629e", "ElysianTech", "CO2 sensor", "Smoke Warden 1000", unit="%")
elMeter = Sensor("a2f8690f-2b3a-43cd-90b8-9deea98b42a7", "MysticEnergy Innovations", "Electricity Meter", "Volt Watch Elite")
heatPump = ActuatorWithSensor("5e13cabc-5c58-4bb3-82a2-3039e4480a6d", "ElysianTech", "Heat Pump", "	Thermo Smart 6000", unit="°C")
motion_senor = Sensor("cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5", "NebulaGuard Innovations", "Motion Sensor", "MoveZ Detect 69")
humSenor = Sensor("3d87e5c0-8716-4b0b-9c67-087eaaed7b45", "AetherCorp", "Humidity Sensor", "Aqua Alert 800")
smartOven1 = Actuator("8d4e4c98-21a9-4d1e-bf18-523285ad90f6", "AetherCorp", "Smart Oven", "Pheonix HEAT 333")
garageDoor = Actuator("9a54c1ec-0cb5-45a7-b20d-2a7349f1b132", "MythicalTech", "Automatic Garage Door", "Guardian Lock 9000")
smartOven2 = Actuator("c1e8fa9c-4b8d-487a-a1a5-2b148ee9d2d1", "IgnisTech Solutions", "Smart Oven", "Ember Heat 3000")
tempSensor = Sensor("4d8b1d62-7921-4917-9b70-bbd31f6e2e8e", "AetherCorp", "Temperature Sensor", "SmartTemp 42")
AQS = Sensor("7c6e35e1-2d8b-4d81-a586-5d01a03bb02c", "CelestialSense Technologies", "Air Quality Sensor", "AeroGuard Pro")
smartPlug = Sensor("1a66c3d6-22b2-446e-bf5c-eb5b9d1a8c79", "MysticEnergy Innovations", "Smart Plug", "FlowState X")
dehumifier = Actuator("9e5b8274-4e77-4e4e-80d2-b40d648ea02a", "ArcaneTech Solutions", "Dehumidifier", "Hydra Dry 8000")
bulp = Actuator("6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28", "Elysian Tech", "Light Bulp", "Lumina Glow 4000")

DEMO_HOUSE.register_device(bath1, humSenor)
DEMO_HOUSE.register_device(living_room, motion_senor)
DEMO_HOUSE.register_device(living_room, heatPump)
DEMO_HOUSE.register_device(living_room, cO2Sensor)
DEMO_HOUSE.register_device(entrance, elMeter)
DEMO_HOUSE.register_device(entrance, smartLock)
DEMO_HOUSE.register_device(garage, garageDoor)
DEMO_HOUSE.register_device(gR1, smartOven1)
DEMO_HOUSE.register_device(office, smartPlug)
DEMO_HOUSE.register_device(bath2,dehumifier)
DEMO_HOUSE.register_device(gR2, bulp)
DEMO_HOUSE.register_device(gR3, AQS)
DEMO_HOUSE.register_device(MasterBed, tempSensor)
DEMO_HOUSE.register_device(MasterBed, smartOven2)
