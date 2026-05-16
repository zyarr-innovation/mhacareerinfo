import fitz  # PyMuPDF
import pandas as pd
import re
import json

def MCA_Int_extract_college_info(df: pd.DataFrame, page_no: int) -> dict:
    result = {}
    start_row = None

    # Find row starting with 5 digit code like: 01002 -
    for idx in range(len(df)):
        cell_value = str(df.iloc[idx, 0]).strip()
        if re.match(r'^\d{5}\s*-', cell_value):
            start_row = idx
            break

    if start_row is None:
        return {}
    
    result["name"] = str(df.iloc[start_row, 0]).strip()
    result["status"] = str(df.iloc[start_row + 1, 0]).strip()
    result["cap_seats"] = None
    for col in range(df.shape[1]):
        cell_text = str(df.iloc[start_row + 1, col]).strip()
        match = re.search(r'CAP Seats\s*:?\s*(\d+)', cell_text)
        if match:
            result["cap_seats"] = int(match.group(1))
            break

    result["choice_code"] = str(df.iloc[start_row + 3, 0]).strip()
    result["course_name"] = str(df.iloc[start_row + 3, 1]).strip()
    result["page_no"] = str(page_no)
    return result

def MBA_MMS_extract_college_info(df: pd.DataFrame, page_no: int) -> dict:
    result = {}
    result["type"] = str(df.columns[0]).strip()
    result["name"] = None
    result["status"] = None

    # CAP Seats from column headers
    cap_seats = None
    for col_name in df.columns:
        match = re.search(r'CAP Seats\s*:?\s*(\d+)', str(col_name))
        if match:
            cap_seats = int(match.group(1))
            break

    result["cap_seats"] = cap_seats
    # Find row containing choice code
    
    choice_row = None
    for idx in range(len(df)):
        first_col = str(df.iloc[idx, 0]).strip()
        if re.match(r'^\d{9,10}$', first_col):
            choice_row = idx
            break

    if choice_row is not None:
        result["choice_code"] = str(df.iloc[choice_row, 0]).strip()
        result["course_name"] = str(df.iloc[choice_row, 1]).strip()
    else:
        result["choice_code"] = None
        result["course_name"] = None

    result["page_no"] = str(page_no)

    return result

def BPlanning_extract_college_info(df: pd.DataFrame, page_no: int) -> dict:
    result = {}
    start_row = None

    # Find row containing college name like: 03016 -
    for idx in range(len(df)):
        first_col = str(df.iloc[idx, 0]).strip()
        if re.match(r'^\d{5}\s*-', first_col):
            start_row = idx
            break

    if start_row is None:
        return {}

    result["name"] = str(df.iloc[start_row, 0]).strip()
    result["status"] = str(df.iloc[start_row + 1, 0]).strip()

    cap_seats = None
    for col in range(df.shape[1]):
        cell_text = str(df.iloc[start_row + 1, col]).strip()
        match = re.search(r'CAP Seats\s*:?\s*(\d+)', cell_text)
        if match:
            cap_seats = int(match.group(1))
            break
    result["cap_seats"] = cap_seats

    choice_row = None
    for idx in range(start_row, len(df)):
        cell_value = str(df.iloc[idx, 0]).strip()
        if re.match(r'^\d{10}$', cell_value):
            choice_row = idx
            break

    if choice_row is not None:
        result["choice_code"] = str(df.iloc[choice_row, 0]).strip()
        result["course_name"] = str(df.iloc[choice_row, 1]).strip()
    else:
        result["choice_code"] = None
        result["course_name"] = None

    # Page Number
    result["page_no"] = str(page_no)
    return result

def BPharm_extract_college_info(df: pd.DataFrame, page_no: int) -> dict:
    result = {}
    start_row = None

    for idx in range(len(df)):
        cell_value = str(df.iloc[idx, 0]).strip()
        if re.match(r'^\d{5}\s*-', cell_value):
            start_row = idx
            break

    if start_row is None:
        return {}

    result["name"] = str(df.iloc[start_row, 0]).strip()
    result["status"] = str(df.iloc[start_row + 1, 0]).strip()

    cap_seats = None
    for col in range(df.shape[1]):
        cell_value = str(df.iloc[start_row + 1, col])
        match = re.search(r'CAP Seats\s*:?\s*(\d+)', cell_value)
        if match:
            cap_seats = int(match.group(1))
            break

    result["cap_seats"] = cap_seats
    result["choice_code"] = str(df.iloc[start_row + 3, 0]).strip()
    result["course_name"] = str(df.iloc[start_row + 3, 1]).strip()
    result["page_no"] = str(page_no)
    return result
    
def BFA_extract_college_info(df: pd.DataFrame, page_no: int) -> dict:
    result = {}
    college_name = str(df.columns[0]).strip()
    result["name"] = college_name
    result["status"] = str(df.iloc[0, 0]).strip()
    cap_text = str(df.iloc[0, 13])
    cap_match = re.search(r'CAP Seats\s*:?\s*(\d+)', cap_text)
    result["cap_seats"] = int(cap_match.group(1)) if cap_match else None
    result["choice_code"] = str(df.iloc[2, 0]).strip()
    result["course_name"] = str(df.iloc[2, 1]).strip()
    result["page_no"] = str(page_no)

    return result

def MBA_extract_college_info(df: pd.DataFrame, page_no: int) -> dict:
    result = {}
    college_name = str(df.columns[0]).strip()
    result["name"] = college_name
    result["status"] = str(df.iloc[0, 0]).strip()
    cap_text = str(df.iloc[0, 8])
    cap_match = re.search(r'CAP Seats\s*:?\s*(\d+)', cap_text)
    result["cap_seats"] = int(cap_match.group(1)) if cap_match else None
    result["choice_code"] = str(df.iloc[2, 0]).strip()
    result["course_name"] = str(df.iloc[2, 1]).strip()
    result["page_no"] = str(page_no)

    return result

def BE_extract_college_info(df: pd.DataFrame, page_no: int) -> dict:
    result = {}
    start_row = None

    # Find row starting with 5 digit code like: 01002 -
    for idx in range(len(df)):
        cell_value = str(df.iloc[idx, 0]).strip()
        if re.match(r'^\d{5}\s*-', cell_value):
            start_row = idx
            break

    if start_row is None:
        return {}

    result["name"] = str(df.iloc[start_row, 0]).strip()
    result["status"] = str(df.iloc[start_row + 1, 0]).strip()
    cap_text = str(df.iloc[start_row + 1, 8])
    cap_match = re.search(r'CAP Seats:(\d+)', cap_text)
    result["cap_seats"] = int(cap_match.group(1)) if cap_match else None
    result["choice_code"] = str(df.iloc[start_row + 3, 0]).strip()
    result["course_name"] = str(df.iloc[start_row + 3, 1]).strip()
    result["page_no"] = str(page_no)

    return result

if __name__ == '__main__':
    pdf_path = "data/ME-MTech-Integrated.pdf"
    doc = fitz.open(pdf_path)

    capture_info = []
    for page_num, page in enumerate(doc):
        print(f"--- Page {page_num + 1} ---")
        tables = page.find_tables()

        for i, table in enumerate(tables):
            df = table.to_pandas()
            # print(df.to_string())
            table_value = MCA_Int_extract_college_info(df,page_num)
            capture_info.append(table_value)
        # if page_num > 10:
        #     break
    doc.close()
    
    with open("ME-MTech-Integrated", "w", encoding="utf-8") as f:
        json.dump(capture_info, f, indent=4, ensure_ascii=False)