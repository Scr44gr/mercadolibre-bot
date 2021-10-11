__author__ = "Scr44gr"
from typing import Any, Dict
import openpyxl
from typing import Union

JSONType = Union[str, Any]

class ExcelFile:

    def __init__(self, filename: str) -> None:

        self._file = openpyxl.load_workbook(filename)
        self.current_sheet = None
    
    def select_sheet(self, name: str) -> Dict:

        sheets = self._file.sheetnames

        if name in sheets:
            self.current_sheet = self._file[name]
            return self.current_sheet
        raise SheetNotFound()
    
    @property
    def worksheet(self):
        return self._file


class SheetNotFound(Exception):
    """
    The sheet is not found in the document.

    """