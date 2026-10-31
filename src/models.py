from dataclasses import dataclass, field

class DataException(Exception):
    pass

class ValidationError(DataException):
    pass

@dataclass
class User:
    id: int
    name: str
    email: str

@dataclass
class Student(User):
    enrolled: list[int] = field(default_factory=list)

@dataclass
class Instructor(User):
    specialization: str = "General"

@dataclass
class Course:
    id: int
    title: str
    instructor_id: int
    price: float

    def __post_init__(self):
        if self.price < 0:
            raise ValidationError("Цена не может быть отрицательной")

@dataclass
class Lesson:
    id: int
    course_id: int
    title: str

@dataclass
class Assignment:
    id: int
    course_id: int
    description: str

@dataclass
class Review:
    id: int
    course_id: int
    rating: int

@dataclass
class Category:
    id: int
    name: str

@dataclass
class Certificate:
    id: int
    student_id: int
    course_id: int

class LearningPlatform:
    def __init__(self):
        self.students: list[Student] = []
        self.instructors: list[Instructor] = []
        self.courses: list[Course] = []

    def add_student(self, student: Student) -> None:
        self.students.append(student)

    def remove_student(self, student_id: int) -> None:
        self.students = [s for s in self.students if s.id != student_id]

    def update_course_price(self, course_id: int, new_price: float) -> None:
        course = next((c for c in self.courses if c.id == course_id), None)
        if not course:
            raise DataException("Курс не найден")
        if new_price < 0:
            raise ValidationError("Цена не может быть отрицательной")
        course.price = new_price