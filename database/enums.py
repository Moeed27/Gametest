import enum

#Enum for the Roles a user may have (User.role)
class Roles(enum.Enum):
    user = 0
    admin = 1

#Enum for the Types a log may have (CarbonLog.log_type)
class LogTypes(enum.Enum):
    trip = 0
    appliance = 1

#Enum for fuel types
class FuelTypes(enum.Enum):
    petrol = 0
    diesel = 1