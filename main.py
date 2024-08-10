from fastapi import FastAPI, Depends, HTTPException, status
from models import Student, SessionLocal
from schemas import StudentCreate, StudentUpdate, StudentInDB
from utils import get_db

app = FastAPI()


# Create a new student
@app.post("/students/", response_model=StudentInDB, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: SessionLocal = Depends(get_db)):
    new_student = Student(name=student.name, email=student.email)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)  # Refresh student object with generated ID
    return new_student

# Update an existing student
@app.put("/students/{student_id}", response_model=StudentInDB)
def update_student(student_id: int, student: StudentUpdate, db: SessionLocal = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    db_student.name = student.name
    db_student.email = student.email
    db.commit()
    db.refresh(db_student)
    return db_student

# Delete a student
@app.delete("/students/{student_id}")
def delete_student(student_id: int, db: SessionLocal = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    

    db.delete(db_student)
    db.commit()
    return {"message": "Student deleted successfully"}  

# Get all students  
@app.get("/students/", response_model=list[StudentInDB])
def read_students(db: SessionLocal = Depends(get_db)):
    students = db.query(Student).all()
    return students

# Get a single student
@app.get("/students/{student_id}", response_model=StudentInDB)
def read_student(student_id: int, db: SessionLocal = Depends(get_db)):
    db_student = db.query(Student).filter(Student.id == student_id).first()
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found")
    return db_student