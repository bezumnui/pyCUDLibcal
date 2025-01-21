import json

import aiohttp

from pyCUDLib.modules.generated.ajax_booking import AjaxBooking
from pyCUDLib.modules.booking_responce import BookingResponse
from pyCUDLib.pycudlib_base import PyCUDLibBase
from pyCUDLib.methods.availability import Availability


class SpaceBooking(PyCUDLibBase):

    async def booking_add(self, id_: int, space_id: int, start_date: str, add_checksum: str):
        self.set_referrer(f"https://cud.libcal.com/space/{space_id}")
        data = {
            "add[eid]": str(space_id),
            "add[gid]": str(Availability.GID),
            "add[lid]": str(Availability.LID),
            "add[start]": start_date,
            "add[checksum]": add_checksum,
            "lid": str(Availability.LID),
            "gid": str(Availability.GID),
            "start": start_date[:-6],
            "end": start_date[:-6],
            "bookings[0][id]": str(id_),
            "bookings[0][eid]": str(space_id),
            "bookings[0][gid]": str(space_id),
            "bookings[0][lid]": str(Availability.LID),
        }
        r = await self.post("spaces/availability/booking/add", data)
        return BookingResponse(await r.json())

    async def book(self, booking: list[AjaxBooking], first_name, last_name, email, people_count, student_id,
                   phone_number, major):
        form_data = aiohttp.FormData()

        data = {
            "session": "00000000",
            "fname": first_name,
            "lname": last_name,
            "email": email,
            "q7451": people_count,
            "q7449": student_id,
            "q7450": phone_number,
            "q21311": major,
            "bookings": json.dumps([self.serialize_ajax_booking(book) for book in booking]),
            "returnUrl": f"/space/{booking[0].eid}",
            "pickupHolds": "",
            "method": "12"
        }

        for key in data:
            value = data[key]
            form_data.add_field(key, value)



        self.set_referrer(f"https://cud.libcal.com/space/{booking[0].eid}")
        # self._session.headers["Content-Type"] = "multipart/form-data"
        r = await self.post("ajax/space/book", form_data)
        return r

    def serialize_ajax_booking(self, booking: AjaxBooking):
        data = {
            "id": booking.id,
            "eid": booking.eid,
            "seat_id": booking.seat_id,
            "gid": Availability.GID,
            "lid": Availability.LID,
            "start": booking.start,
            "end": booking.end,
            "checksum": booking.checksum
        }
        return data
