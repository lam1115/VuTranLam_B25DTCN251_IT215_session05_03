from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

students = [
    {"id": 1, "name": "Nguyen Van A"},
    {"id": 2, "name": "Tran Thi B"},
    {"id": 3, "name": "Le Van C"},
]
courses = [
    {"id": 1, "name": "FastAPI Basic", "capacity": 2},
    {"id": 2, "name": "Python OOP", "capacity": 2},
]
registrations = [
    {"id": 1, "student_id": 1, "course_id": 1},
    {"id": 2, "student_id": 2, "course_id": 1},
]


class RegistrationsCreate(BaseModel):
    student_id: int
    course_id: int


@app.post("/registrations")
def create_registrations(registration: RegistrationsCreate):
    for item in registrations:
        if (
            item["student_id"] == registration.student_id
            and item["course_id"] == registration.course_id
        ):
            raise HTTPException(
                status_code=409, detail="Student already registered this course"
            )

    course = []
    for item in courses:
        if item["id"] == registration.course_id:
            course = item
            break

    result = [
        item for item in registrations if item["course_id"] == registration.course_id
    ]

    if len(result) == course["capacity"]:
        raise HTTPException(status_code=507, detail="Course is full")

    new_registration = {
        "id": len(registrations) + 1,
        "student_id": registration.student_id,
        "course_id": registration.course_id,
    }
    registrations.append(new_registration)
    return {"message": "Regist successfully", "data": new_registration}


# 1.Input:
# API: POST /registrations
# Body gửi lên:
# {
#     "student_id": 1,
#     "course_id": 2
# }
# Trong FastAPI:
# class RegistrationsCreate(BaseModel):
#     student_id: int
#     course_id: int

# 2. Output khi thành công
# Tạo một bản ghi đăng ký mới.
# Thêm vào danh sách registrations.
# Trả về HTTP 201 Created.

# 3. Output thất bại:
# Đăng ký trùng: 409 Conflict
# {
#     "detail": "Student already registered this course"
# }

# Khóa học đã đầy: 507 Insufficient Storage
# {
#     "detail": "Course is full"
# }


# Đề xuất giải pháp
# Nhận dữ liệu student_id và course_id.
# Kiểm tra học viên đã đăng ký khóa học này chưa.
# Đếm số lượng đăng ký của khóa học.
# So sánh với capacity.
# Nếu chưa đầy thì tạo đăng ký mới.
# Trả về HTTP 201 Created.
