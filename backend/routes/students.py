from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models.student import Student
from backend.schemas.student_schema import StudentAcademicPayload, StudentResponse, StudentUpdate
from backend.services.student_service import (
    create_or_update_student_with_record,
    delete_student_and_related,
    get_student,
    student_to_response,
    update_student,
)


router = APIRouter(prefix="/students", tags=["Students"])


@router.get("", response_model=list[StudentResponse])
def list_students(db: Session = Depends(get_db)):
    students = db.query(Student).order_by(Student.student_id).all()
    return [student_to_response(db, student) for student in students]


@router.get("/{student_id}", response_model=StudentResponse)
def retrieve_student(student_id: str, db: Session = Depends(get_db)):
    student = get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_to_response(db, student)


@router.post("", response_model=StudentResponse, status_code=201)
def create_student(payload: StudentAcademicPayload, db: Session = Depends(get_db)):
    student = create_or_update_student_with_record(db, payload)
    return student_to_response(db, student)


@router.put("/{student_id}", response_model=StudentResponse)
def update_student_route(student_id: str, payload: StudentUpdate, db: Session = Depends(get_db)):
    student = get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    try:
        updated = update_student(db, student, payload)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return student_to_response(db, updated)


@router.delete("/{student_id}")
def delete_student_route(student_id: str, db: Session = Depends(get_db)):
    student = get_student(db, student_id)
    if student is None:
        raise HTTPException(status_code=404, detail="Student not found")
    delete_student_and_related(db, student)
    return {"status": "deleted", "student_id": student_id}
