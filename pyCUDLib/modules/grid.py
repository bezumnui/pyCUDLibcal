from pyCUDLib.modules.generated import Booking, Slot
from pyCUDLib.modules.generated.class_generator_using_json import json_value_normaliser


class GridRequest:
    def __init__(self, lid=None, gid=None, eid=None, seat=None, seatId=None, zone=None, start=None, end=None, pageIndex=None, pageSize=None, **kwargs):
        self._kwargs = kwargs
        self.lid: int = lid
        self.gid: int = gid
        self.eid: int = eid
        self.seat: int = seat
        self.seatId: int = seatId
        self.zone: int = zone
        self.start: str = start
        self.end: str = end
        self.pageIndex: int = pageIndex
        self.pageSize: int = pageSize

    def serialize(self):
        return {
            'lid': self.lid,
            'gid': self.gid,
            'eid': self.eid,
            'seat': self.seat,
            'seatId': self.seatId,
            'zone': self.zone,
            'start': self.start,
            'end': self.end,
            'pageIndex': self.pageIndex,
            'pageSize': self.pageSize,
        }


class GridResponse:
    def __init__(self, data: dict):
        self.data = json_value_normaliser(data)
        self.slots = [Slot(**slot) for slot in self.data.get("slots", [])]
        self.bookings = [Booking(**booking) for booking in self.data.get("bookings", [])]
        self.isPreCreatedBooking = data.get("isPreCreatedBooking", False)
        self.windowEnd = data.get("windowEnd", False)

    def __repr__(self):
        return f'GridResponse[slots: {self.slots}, bookings: {self.bookings}, isPreCreatedBooking: {self.isPreCreatedBooking}, windowEnd: {self.windowEnd}]'