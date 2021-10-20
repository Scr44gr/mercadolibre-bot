from typing import Dict, List, Union
from src.commons import get_maximum_rows
from src.mercadolibre import MercadoLibre
from src.utils import params_format
from src.xlsx import ExcelFile
from src.utils import DATE_TO
from re import search
import json
from logging import getLogger, basicConfig
from logging import INFO
from datetime import datetime


def get_uuid(target: str) -> str:
    if not isinstance(target, str):
        target = target.hyperlink.target
    return search(r'MLC(.[\d]*)', target).group().replace('-', '')



def extract_ids_from_excel(filename: str, sheet_name: str, column, hyperlink=False) -> List[str]:

    excel = ExcelFile(filename)
    sheet = excel.select_sheet(sheet_name)
    row_count = get_maximum_rows(sheet)
    ids = []

    for row_index in range(row_count):
        data = sheet.cell(row=row_index+1, column=column+1)

        if hyperlink:
            url = data.hyperlink            
        else:
            url = data.value
        if url is not None and url.target is not None:
            if len(url.target) >= 1:
                id = get_uuid(url.target)
                ids.append(id)
    return ids

def parse_data(data: List[Dict], fetching_params: Dict, list_reference) -> List[Dict]:
    

    for item in data:
        item = item['body']
        uuid = item.get('id')
        payload = {uuid: {}}
        for param in fetching_params:
            try:
                if param == 'free_shipping':
                    free_shipping = params_format[uuid][param](item)
                    payload[uuid][param] = 'Si' if free_shipping else 'No' # quick fix
                else:
                    payload[uuid][param] = item[params_format[param]]
            except KeyError:
                continue
        list_reference(payload)


def update_excel(filename: str, sheet_name: str, data: List[Dict], get_column, column_date_value: Union[str, bool]) -> None:

    excel = ExcelFile(filename)
    sheet = excel.select_sheet(sheet_name)
    
    for i in range(len(data)):
        try:
            column_uuid = get_uuid(sheet.cell(row=i+1, column=get_column('title')+1))
            item = data[column_uuid]
            for key in item:
                p_key = key
                if key == 'sales' and column_date_value:
                    key = 'date'
                sheet.cell(row=i+1, column=get_column(key)+1).value = item[p_key]
        except AttributeError:
            continue
    if column_date_value is not None and len(column_date_value) >=1:
        date = datetime.now()
        sheet.cell(row=1, column=get_column('date')+1).value = f'{date.day}-{DATE_TO[str(date.month)][0:3]}'
    
    return excel.worksheet

def main() -> None:
    logger = getLogger('main')
    try:
        file = open(r'./settings.json').read()
        document_format = json.loads(file)
        excel_sheets: List[Dict] = document_format['sheets']
        
        logger.info('[*] starting..')
        for sheet in excel_sheets:
            if sheet.get('active'):
                sheet_name: str = sheet.get('name', '')
                document_path: str = sheet.get('path')
                document_output_path: str = sheet.get('output_path')
                columns_names: List[str] = sheet.get('columns')
                fetching_params: List[str] = sheet.get('fetching_params')
                hyperlink_in : Union[str, bool] = sheet.get('hyperlink_in')
                column_date_value: bool = sheet.get('column_date_value')
                
                logger.info(f'[*] getting ids from {sheet_name} sheet')
                # we need to obtain the urls from the excel to extract the ids..
                # ..to get the items info from the mcapi
                
                # get the column url index
                column = lambda key:[i for (i, cn) in enumerate(columns_names) if cn == key][0]
                
                # extract all urls from the excel sheet
                if hyperlink_in:
                    ids = extract_ids_from_excel(document_path, sheet_name, column(hyperlink_in), hyperlink=True)
                else:
                    ids = extract_ids_from_excel(document_path, sheet_name, column('url'))
                
                if len(ids) >= MercadoLibre.MAX_IDS_SIZE:
                    logger.info('[*] fetching data..')

                    idx = list(range(0, len(ids)))[::MercadoLibre.MAX_IDS_SIZE]
                    idx_size = len(idx)
                    
                    in_memory_data = {}
                    add_to_memory = lambda d: in_memory_data.update(d)
                    for sub_idx in range(0, idx_size):
                        try:
                            if sub_idx+1 >= idx_size:
                                queue = ids[idx[sub_idx]::]
                            else:
                                queue = ids[idx[sub_idx]:idx[sub_idx+1]]
                            mcapi = MercadoLibre(queue)
                            response = mcapi.get_items_info()
                            parse_data(response, fetching_params, add_to_memory)
                        except IndexError:
                            break
                    logger.info('[*] done!')
                    logger.info('[*] updating excel..')
                    logger.info(f'[*] output path {document_output_path}')

                    update_excel(document_path, sheet_name, in_memory_data, column, column_date_value=column_date_value).save(document_output_path)
                    logger.info(f'[+] document updated!')
        _ = input('/> press enter to exit')
    except TypeError:
        raise Exception('Bad format on settings.json')

if __name__ == '__main__':
    FORMAT = '%(asctime)-15s %(message)s'
    basicConfig(format=FORMAT, level=INFO)
    main()
