from enum import unique, Enum

@unique
class UserRole(Enum):
    CUSTOMER = 1
    SALE = 2
    INVENTORY = 3

class ShippingStatus(Enum):
    DANG_XU_LY = 1
    DA_TIEP_NHAN = 2
    DANG_LAY_HANG = 3
    DANG_GIAO_HANG = 4
    DA_GIAO = 5
    HUY = 6