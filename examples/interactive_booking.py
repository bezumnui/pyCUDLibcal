import os
import sys
import random
from datetime import datetime, timedelta

# We want to do so because we are in the examples folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pyCUDLib.modules.generated.ajax_booking import AjaxBooking
from pyCUDLib.modules import Slot
from pyCUDLib.modules.generated.study_room_resources import StudyRoomResources
from pyCUDLib.client import PyCUDLib
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
        #
        # self.first_name = "Heohii"
        # self.last_name = "Vizniuk"
        # self.email = "2023.0002867@students.cud.ac.ae"
        # self.people_count = 3
        # self.student_id = "20230002867"
        # self.phone_number = "+971526082212"
        # self.major = "Bachelor of Architecture"


    def start(self):
        asyncio.run(self._start())

    @staticmethod
    def clear_console():
        os.system('clear')

    async def set_random_email(self):
        asset = "abcdefghijklmnopqrstuvwxyz1234567890"
        tokenized_name = "".join(random.choices(asset, k=10))
        # self.student_id = "".join(random.choices(asset, k=10)) # student id can be common. could not be unique

        self.email = tokenized_name + "@students.cud.ac.ae"

    async def _start(self):
        self.client = PyCUDLib()
        self.room_list = await self.client.get_rooms()
        grid = await self.client.get_availability_grid(datetime.now()  + timedelta(self.day_offset))
        self.slot_list = grid.slots
        self.clear_console()
        await self.ask_user_chose_mode()
        await self.client.close()

    @staticmethod
    def wait_int_input(prompt: str) -> int:
        while True:
            value = input(prompt)
            if value.isdigit():
                return int(value)
            print("Error to read integer. Try again.\n")

    async def ask_user_chose_mode(self):
        mode = self.wait_int_input("Please enter mode:\n0: Reserve every slot\n1: Reserve a single slot\n")
        assert mode <= 1
        self.ask_user_chose_room()

        if mode == 0:
            await self.reserve_every_timing()

        elif mode == 0:
            self.ask_user_chose_slot()
            r = await self.reserve()
            print("Success!\nCancellation link:", r.get_cancellation_link())

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

    async def reserve_every_timing(self):
        input("Press enter to book every single slot at the room\n")
        for slot in self.slot_list:
            await self.set_random_email()
            if slot.itemId == self.room_chosen.eid:
                self.slot_chosen = slot
                if r := await self.reserve():
                    print(f"{slot.start} - {slot.end} booked on email {self.email}")
                    print("Cancel link:", r.get_cancellation_link())


    async def reserve(self):
        booking = await self.client.booking_add(0, self.room_chosen.eid, self.slot_chosen.start[:-3], self.slot_chosen.checksum)
        if len(booking.bookings) == 0:
            print("Error to book. The room is busy")
            return
        ajax_booking = AjaxBooking(**booking.bookings[0].__dict__)
        try:
            r = await self.client.book([ajax_booking], self.first_name, self.last_name, self.email, self.people_count, self.student_id, self.phone_number, self.major)
        except Exception as e:
            print("Error while booking", str(e))
            return None
        return r





if __name__ == '__main__':
    day_offset = InteractiveBooking.wait_int_input("Please enter day offset for booking (0 - today, 1 - tomorrow, etc):\n")
    print("Please wait...")
    InteractiveBooking(day_offset).start()
