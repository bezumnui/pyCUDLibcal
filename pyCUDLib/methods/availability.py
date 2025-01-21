from datetime import datetime, timedelta

from pyCUDLib.pycudlib_base import PyCUDLibBase
from pyCUDLib.modules import GridRequest, GridResponse
from pyCUDLib.utils.parse import GroupStudyRoomParser


class Availability(PyCUDLibBase):
    LID = 7109
    GID = 12579

    async def get_availability_grid(self, day: datetime):
        current_day = self.get_formatted_day(day)
        next_day = self.get_formatted_day(day + timedelta(1))
        raw = GridRequest(self.LID, self.GID, -1, 0, 0, 0, current_day, next_day, 1, 100)
        self.set_referrer("https://cud.libcal.com/reserve/groupstudyroom")
        r = await self.post('/spaces/availability/grid', raw.serialize())
        return GridResponse(await r.json())

    async def get_rooms(self):

        r = await self.get('reserve/groupstudyroom')
        return GroupStudyRoomParser(await r.text()).parse_rooms()


# https://cud.libcal.com/reserve/groupstudyroom