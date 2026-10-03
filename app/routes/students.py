from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Student, User
from app.schemas import StudentCreate, StudentResponse
from app.auth import get_current_user, require_admin

router = APIRouter(prefix="/students", tags=["Students"])


@router.get("/", response_model=list[StudentResponse])
def get_students(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Student).all()


@router.get("/{student_id}", response_model=StudentResponse)
def get_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@router.post("/", response_model=StudentResponse)
def create_student(
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    existing_student = (
        db.query(Student)
        .filter(Student.email == student_data.email)
        .first()
    )

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Student email already exists"
        )

    student = Student(
        name=student_data.name,
        email=student_data.email,
        course=student_data.course,
        year=student_data.year
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return student
@router.put("/{student_id}", response_model=StudentResponse)
def update_student(
    student_id: int,
    student_data: StudentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = student_data.name
    student.email = student_data.email
    student.course = student_data.course
    student.year = student_data.year

    db.commit()
    db.refresh(student)

    return student


@router.delete("/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    student = (
        db.query(Student)
        .filter(Student.id == student_id)
        .first()
    )

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {
        "message": "Student deleted successfully"
    }