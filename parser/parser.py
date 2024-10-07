import os.path

from xls2xlsx import XLS2XLSX
from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet
from typing import List, Dict, Any
import re
from utils import json_utils


class SheduleParser:
    def __init__(self, document_path: str) -> None:
        self._document_path = document_path

    def _open_worksheet(self) -> None:
        if self._document_path.endswith(".xls"):
            xls2xlsx = XLS2XLSX(self._document_path)
            self._document_path = f"{os.path.splitext(self._document_path)[0]}.xlsx"
            xls2xlsx.to_xlsx(self._document_path)

        self._workbook = load_workbook(self._document_path)
        self._worksheet = self._workbook["2022-2023"]

    def get_groups(self, group_row_index: int = 6) -> List:
        groups: List = []
        for row in self._worksheet.iter_rows(min_row=group_row_index, max_row=group_row_index):
            for cell in row:
                cell_value: str = str(cell.value)
                if cell_value.count('-') >= 1:
                    if cell_value.count('-') > 1:
                        if cell_value.count(',') == 0:
                            cell_value = re.sub('  +', ',', cell_value)
                        cell_value = cell_value.replace(' ', '')
                        cell_value = cell_value.replace(',', ", ")
                    else:
                        cell_value = cell_value.replace(' ', '')
                    groups.append(cell_value)
        print(groups)
        return groups

    def get_group_coordinates(self, group_row_index: int = 6) -> List:
        study_group_coordinates: List = []
        for row in self._worksheet.iter_rows(min_row=group_row_index, max_row=group_row_index):
            for cell in row:
                if cell.value is None or cell.value.count('-') == 0:
                    continue
                else:
                    study_group_coordinates.append(cell.column)
        return study_group_coordinates

    def read_sheet(self) -> Dict:
        lesson_time: str | None = None
        day: str | None = None
        lessons: Dict = {}
        group_column_coordinates: List = self.get_group_coordinates()

        study_days: List = ["понедельник", "вторник", "среда", "четверг", "пятница"]
        lesson_numbers: List = ['1', '3', '5', '7']

        for row in self._worksheet.iter_rows(min_row=7):
            for cell in row:
                cell_value: Any = cell.value
                if cell_value is None:
                    if cell.column in group_column_coordinates:
                        cell_value = "Нет пары"
                    else:
                        continue
                else:
                    cell_value = str(cell.value)
                if cell_value in lesson_numbers:
                    lesson_time = cell_value + f'-{int(cell_value) + 1} урок'
                    if lesson_time not in lessons[day]:
                        lessons[day][lesson_time] = []
                elif cell_value.strip().lower() in study_days:
                    day = cell_value.strip()
                    if day not in lessons:
                        lessons[day] = {}
                else:
                    if len(cell_value) > 1:
                        subject: str = re.sub(" +", " ", cell_value.strip())
                        lessons[day][lesson_time].append(subject)
        print(lessons)
        return lessons

    def get_schedule_for_each_group(self) -> Dict:
        groups: List = self.get_groups()
        raw_schedule: Dict = self.read_sheet()
        schedule: Dict = {}
        for group_index in range(len(groups)):
            lesson_index: int = group_index
            schedule[groups[group_index]] = {}
            for day in raw_schedule:
                schedule[groups[group_index]][day] = {}
                for time in raw_schedule[day]:
                    schedule[groups[group_index]][day][time] = raw_schedule[day][time][lesson_index]
        print(schedule)
        return schedule

    def get_json_schedule(self, schedule: Dict) -> None:
        json_schedule = json_utils.json_converter(schedule)
        print(json_schedule)
        json_utils.save_json(json_schedule)

    def get_json_groups(self, groups: List) -> None:
        json_groups = json_utils.json_converter(groups)
        print(json_groups)
        json_utils.save_json(json_groups, file_name="groups.json")
