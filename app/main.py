from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Student(BaseModel):
    id:int
    name:str
    age:int
    
students:list[Student]=[]

@app.get("/")
def home():
    return {"message": "Hello FastAPI"}

@app.get("/students")
def get_students():
    return students

@app.get("/students/{stdent_id}")
def get_student(student_id:int):
    for student in students:
        if student.id==student_id:
            return students
    
    return {"message": "Student didn't found"}


@app.post("/students")
def add_student(student:Student):
    students.append(student)
    return student


@app.update("/students/{student_id}")
def update_student(student_id:int,updated_student:Student):
    for index, student in enumerate(students):
        if student.id==student_id:
             students[index] = updated_student
             return updated_student



    
@app.delete("/students/{stdent_id}")
def delete_student(student_id:int):
     for index, student in enumerate(students):
        if student.id==student_id:
            students.pop(index)
            return student
    
    
