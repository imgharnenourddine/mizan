# CSV parsing helpers — parse schedule, exam, project, and student trombinoscope CSV files
# app/utils/csv_parser.py
import csv
import io
from fastapi import UploadFile


async def parse_trombi_csv(file: UploadFile) -> list[dict]:
    content = await file.read()
    decoded = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))
    
    results = []
    for row in reader:
        if not any(row.values()):
            continue
        cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k}
        results.append(cleaned_row)
    return results


async def parse_schedule_csv(file: UploadFile) -> list[dict]:
    content = await file.read()
    decoded = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))
    
    results = []
    for row in reader:
        if not any(row.values()):
            continue
        cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k}
        results.append(cleaned_row)
    return results


async def parse_exam_csv(file: UploadFile) -> list[dict]:
    content = await file.read()
    decoded = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))
    
    results = []
    for row in reader:
        if not any(row.values()):
            continue
        cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k}
        results.append(cleaned_row)
    return results


async def parse_project_csv(file: UploadFile) -> list[dict]:
    content = await file.read()
    decoded = content.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))
    
    results = []
    for row in reader:
        if not any(row.values()):
            continue
        cleaned_row = {k.strip(): v.strip() for k, v in row.items() if k}
        if "members" in cleaned_row:
            members_list = [m.strip() for m in cleaned_row["members"].split(",") if m.strip()]
            cleaned_row["members"] = members_list
        results.append(cleaned_row)
    return results