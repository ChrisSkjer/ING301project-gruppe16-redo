from smarthouse.domain import SmartHouse

DEMO_HOUSE = SmartHouse()

# Building house structure
ground_floor = DEMO_HOUSE.register_floor(1)
entrance = DEMO_HOUSE.register_room(ground_floor, 13.5, "Entrance")
# TODO: continue registering the remaining floor, rooms and devices

second_floor = DEMO_HOUSE.register_floor(2)

living = DEMO_HOUSE.register_room(ground_floor, 39.75, "LivingRoom/Kitchen")
bath1 = DEMO_HOUSE.register_room(ground_floor, 6.3, "Bathroom 1")
gR1 = DEMO_HOUSE.register_room(ground_floor, 8, "GuestRoom 1")
garage = DEMO_HOUSE.register_room(ground_floor, 19, "Garage")

office = DEMO_HOUSE.register_room(second_floor, 11.75, "Office")
bath2 = DEMO_HOUSE.register_room(second_floor, 9.25, "Bathroom 2")
gR2 = DEMO_HOUSE.register_room(second_floor, 8, "GuestRoom 2")
gR3 = DEMO_HOUSE.register_room(second_floor, 10, "GuestRoom 3")
dR = DEMO_HOUSE.register_room(second_floor, 3, "DressingRoom")
Hall = DEMO_HOUSE.register_room(second_floor, 10, "Hallway")
MasterBed = DEMO_HOUSE.register_room(second_floor, 17, "Master Bedroom")

