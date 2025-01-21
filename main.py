# PyCUDLib
import os
from datetime import datetime, timedelta

from pyCUDLib.modules.generated.ajax_booking import AjaxBooking
from pyCUDLib.modules import Slot
from pyCUDLib.modules.generated.study_room_resources import StudyRoomResources
from pyCUDLib.client import PyCUDLib
import aiohttp
import asyncio


class InteractiveBooking:
    def __init__(self, day_offset = 0):
        self.client: PyCUDLib | None = None
        self.free_rooms = []
        self.room_chosen: StudyRoomResources | None = None
        self.slot_chosen: Slot | None = None

        self.room_list: list[StudyRoomResources] = []
        self.slot_list: list[Slot] = []
        self.day_offset = day_offset

        self.first_name = "John"
        self.last_name = "Doe"
        self.email = "mail@students.cud.ac.ae"
        self.people_count = 4
        self.student_id = "2023000000"
        self.phone_number = "+971000000"
        self.major = "Bachelor of Architecture"



    def start(self):
        asyncio.run(self.__start())

    @staticmethod
    def clear_console():
        os.system('clear')

    async def __start(self):
        self.client = PyCUDLib()
        self.room_list = await self.client.get_rooms()
        grid = await self.client.get_availability_grid(datetime.now()  + timedelta(self.day_offset))
        self.slot_list = grid.slots
        self.clear_console()
        self.ask_user_chose_room()
        self.ask_user_chose_slot()
        await self.reserve()

        await self.client.close()

    @staticmethod
    def wait_int_input(prompt: str) -> int:
        while True:
            value = input(prompt)
            if value.isdigit():
                return int(value)
            print("Error to read integer. Try again.\n")

    def ask_user_chose_room(self):
        for i, room in zip(range(len(self.room_list)), self.room_list):
            print(f'{i}: {room.title}')
        room_index = self.wait_int_input("Please enter index of the room:\n")
        assert room_index < len(self.room_list)
        self.room_chosen = self.room_list[room_index]

    def ask_user_chose_slot(self):
        local_slots = []

        for slot in self.slot_list:
            if slot.itemId == self.room_chosen.eid:
                local_slots.append(slot)

        for i, slot in zip(range(len(local_slots)), local_slots):
            print(f'{i}: {slot.start} - {slot.end}')
        slot_index = self.wait_int_input("Please enter index of the slot:\n")
        self.slot_chosen = local_slots[slot_index]

    async def reserve(self):
        booking = await self.client.booking_add(0, self.room_chosen.eid, self.slot_chosen.start[:-3], self.slot_chosen.checksum)
        if len(booking.bookings) == 0:
            print("Error to book. The room is busy")
            return
        ajaxBooking = AjaxBooking(**booking.bookings[0].__dict__)
        try:
            await self.client.book([ajaxBooking], self.first_name, self.last_name, self.email, self.people_count, self.student_id, self.phone_number, self.major)
        except Exception as e:
            print(f"Error to book: {e}")
            return
        print("Successfully booked")





if __name__ == '__main__':
    print("Please wait...")
    InteractiveBooking(1).start()
