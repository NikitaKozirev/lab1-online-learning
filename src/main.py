from src.models import LearningPlatform, Student, Course, ValidationError
from src.storage import save_to_json, load_from_json, save_to_xml, load_from_xml

def main() -> None:
    p = LearningPlatform()
    p.add_student(Student(1, "Иван", "ivan@mail.ru"))
    p.courses.append(Course(1, "Python", 1, 1500.0))

    try:
        print("Сохранение в JSON и XML...")
        save_to_json(p, "data.json")
        save_to_xml(p, "data.xml")

        print("Загрузка из JSON...")
        p2 = LearningPlatform()
        load_from_json(p2, "data.json")
        print(f"Успешно загружен курс: {p2.courses[0].title}")

        print("Тест обработки ошибок...")
        load_from_json(p2, "no_file.json")
    except Exception as e:
        print(f"Перехвачено исключение: {type(e).__name__} - {e}")

if __name__ == "__main__":
    main()
