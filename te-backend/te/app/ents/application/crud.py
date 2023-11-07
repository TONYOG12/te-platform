from datetime import date

from sqlalchemy.orm import Session
import tempfile, os  # Import the tempfile module
import app.ents.application.models as application_models
import app.ents.application.schema as application_schema
import app.ents.company.crud as company_crud
import app.ents.company.schema as company_schema
import app.ents.user.crud as user_crud
import app.core.service as service
from app.core.config import settings
from googleapiclient.http import MediaFileUpload


def read_application_multi(
    db: Session, *, skip: int = 0, limit: int = 100
) -> list[application_models.Application]:
    return (
        db.query(application_models.Application).offset(skip).limit(limit).all()
    )


def create_application(
    db: Session, *, user_id: int, data: application_schema.ApplicationCreate
):
    location = None
    company = company_crud.read_company_by_name(db, name=data.company)
    if not company:
        company = company_crud.create_company(
            db,
            data=company_schema.CompanyCreate(
                **{
                    "name": data.company,
                    "location": {
                        "country": data.location.country,
                        "city": data.location.city,
                    },
                    "domain": "",
                }
            ),
        )
        location = company.locations[0]

    if not location:
        for loc in company.locations:
            if (
                loc.country == data.location.country
                and loc.city == data.location.city
            ):
                location = loc
                break
            if loc.country == data.location.country:
                location = loc

        if not location:
            location = company_crud.add_location(
                db, company=company, data=data.location
            ).locations[-1]

    application = application_models.Application(
        **(data.dict(exclude={"company", "location"}))
    )

    application.company = company
    application.location = location
    application.date = date.today().strftime("%Y-%m-%d")

    application.user_id = user_id

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


def read_user_applications(
    db: Session, *, user_id
) -> list[application_models.Application]:
    user = user_crud.read_user_by_id(db, id=user_id)
    if not user:
        ...
    return user.applications


def read_user_application_files(
    db: Session, *, user_id
) -> tuple[application_models.Resume, application_models.OtherFiles]:
    user = user_crud.read_user_by_id(db, id=user_id)
    if not user:
        ...

    return user.resumes, user.other_files


def upload_file(file) -> application_schema.FileUpload:
    drive_service = service.get_drive_service()
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(file.file.read())

    file_metadata = {
        "name": file.filename,
        "parents": [settings.GDRIVE_RESUMES],
    }

    media = MediaFileUpload(temp_file.name, resumable=True)
    uploaded_file = (
        drive_service.files()
        .create(
            body=file_metadata,
            media_body=media,
            fields="id,name,webContentLink",
        )
        .execute()
    )

    os.remove(temp_file.name)
    return application_schema.FileUpload(
        file_id=uploaded_file.get("id"),
        name=uploaded_file.get("name"),
        link=uploaded_file.get("webContentLink"),
    )


def upload_resume(db, file, user_id):
    data = upload_file(file=file)
    resume = application_models.Resume(
        file_id=data.file_id,
        name=data.name,
        link=data.link[: data.link.find("&export=download")],
        date=date.today().strftime("%Y-%m-%d"),
        user_id=user_id,
    )

    db.add(resume)
    db.commit()
    db.refresh(resume)

    return resume


def get_user_resumes(db: Session, user_id) -> list[application_models.Resume]:
    resumes = (
        db.query(application_models.Resume)
        .filter(application_models.Resume.user_id == user_id)
        .all()
    )
    return [resume for resume in resumes if resume.active]


def update_essay(db: Session, user_id, *, data) -> str:
    user = user_crud.read_user_by_id(db, id=user_id)
    if not user:
        ...

    user.essay = data.get("essay")

    db.add(user)
    db.commit()
    db.refresh(user)
    return user.essay


# def update(
#     db: Session,
#     *,
#     db_obj: company_models.Company,
#     data: company_schema.CompanyUpdate | dict[str, Any],
# ) -> company_models.Company:
#     if isinstance(data, dict):
#         update_data = data
#     else:
#         update_data = data.dict(exclude_unset=True)
#     if update_data["password"]:
#         hashed_password = security.get_password_hash(update_data["password"])
#         del update_data["password"]
#         update_data["hashed_password"] = hashed_password
#     return super().update(db, db_obj=db_obj, data=update_data)
