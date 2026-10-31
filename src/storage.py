import json
import xml.etree.ElementTree as ET
from dataclasses import asdict
from src.models import LearningPlatform, Student, Course, DataException

class FileFormatError(DataException):
    pass

def save_to_json(platform: LearningPlatform, filename: str) -> None:
    data = {
        "students": [asdict(s) for s in platform.students],
        "courses": [asdict(c) for c in platform.courses],
    }
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_from_json(platform: LearningPlatform, filename: str) -> None:
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        platform.students = [Student(**s) for s in data.get("students", [])]
        platform.courses = [Course(**c) for c in data.get("courses", [])]
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except json.JSONDecodeError:
        raise FileFormatError("Некорректный JSON")

def save_to_xml(platform: LearningPlatform, filename: str) -> None:
    root = ET.Element("platform")
    for c in platform.courses:
        c_el = ET.SubElement(root, "course", id=str(c.id), price=str(c.price))
        ET.SubElement(c_el, "title").text = c.title

    for s in platform.students:
        s_el = ET.SubElement(root, "student", id=str(s.id))
        ET.SubElement(s_el, "name").text = s.name

    ET.ElementTree(root).write(filename, encoding="utf-8", xml_declaration=True)

def load_from_xml(platform: LearningPlatform, filename: str) -> None:
    try:
        root = ET.parse(filename).getroot()
        platform.courses = [
            Course(id=int(el.get("id")), title=el.find("title").text,
                   price=float(el.get("price")), instructor_id=0)
            for el in root.findall("course")
        ]
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден")
    except ET.ParseError:
        raise FileFormatError("Некорректный XML")
