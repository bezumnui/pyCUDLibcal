import json
import re
from re import findall

from pyCUDLib.modules.generated.study_room_resources import StudyRoomResources


class GroupStudyRoomParser:
    def __init__(self, data: str):
        self.data = data

    def parse_rooms(self) -> list[StudyRoomResources]:
        resources = self._get_all_room_resources()
        return [self._parse_resource(resource) for resource in resources]


    def _get_all_room_resources(self):
        resource_re = r"resources\.push\(\{(.+?)\}\);"
        match = re.findall(resource_re, self.data, re.DOTALL)
        return match

    def _parse_resource(self, resource: str):
        re_parse_field = r"([^\s]+?):\s(.+),"
        match = findall(re_parse_field, resource)
        result = {}
        for field, value in match:
            result.update({field: json.loads(value)})
        return StudyRoomResources(**result)

#


if __name__ == '__main__':
    with open("../modules/generated/json_templates/groupstudyroom.html") as f:
        # print(f.read())
        data = GroupStudyRoomParser(f.read()).parse_rooms()
        print(*data, sep="\n")
