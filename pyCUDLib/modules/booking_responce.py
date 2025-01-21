from pyCUDLib.modules import Booking, GridUpdateData
from pyCUDLib.modules import json_value_normaliser


class BookingResponse:

    def __init__(self, data: dict):
        self.data = json_value_normaliser(data)
        self.bookings = [Booking(**booking) for booking in self.data.get("bookings", [])]
        self.gridUpdateData = GridUpdateData(**self.data.get("gridUpdateData", {}))
        self.limitIssues = self.data.get("limitIssues", None);

    def __repr__(self):
        return f'BookingResponse[bookings: {self.bookings}, gridUpdateData: {self.gridUpdateData}, limitIssues: {self.limitIssues}]'