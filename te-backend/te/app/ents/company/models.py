from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.types import Enum

import app.ents.company.schema as company_schema
import app.ents.application.schema as application_schema
from app.database.base_class import Base


class Posting(Base):
    __tablename__ = "postings"
    id = Column(Integer, primary_key=True)
    date = Column(String, nullable=False)
    deadline = Column(String, nullable=False)
    notes = Column(String, nullable=False)
    sponsor = Column(Boolean, nullable=False)
    recruiter_name = Column(String, nullable=False)
    recruiter_email = Column(String, nullable=False)
    active = Column(Boolean, nullable=False)
    role = Column(Enum(company_schema.JobRoles), nullable=False)
    status = Column(Enum(application_schema.ApplicationStatuses), nullable=False)

    # Relationships
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="postings")


class Location(Base):
    __tablename__ = "locations"
    id = Column(Integer, primary_key=True)
    country = Column(String, nullable=False, index=True)
    city = Column(String, nullable=False)
    companies = relationship(
        "Company",
        secondary="companies_locations_rel",
        back_populates="locations",
    )
    application = relationship("Application", back_populates="location")


class Referral(Base):
    __tablename__ = "referrals"
    id = Column(Integer, primary_key=True)
    status = Column(Enum(company_schema.ReferralStatuses))
    year = Column(Integer, nullable=False)
    role = Column(String, nullable=True)
    notes = Column(String, nullable=True)

    # Relationships
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="referrals")
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="referrals")


class ReferralMaterials(Base):
    __tablename__ = "referral_materials"
    id = Column(Integer, primary_key=True)
    resume = Column(Boolean, nullable=False, default=True)
    essay = Column(Boolean, nullable=False, default=True)
    contact = Column(Boolean, nullable=False, default=True)

    # Relationships
    company_id = Column(Integer, ForeignKey("companies.id"))
    company = relationship("Company", back_populates="referral_materials")


class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    image = Column(String, nullable=True)
    name = Column(String, nullable=False)
    domain = Column(String, nullable=True)
    can_refer = Column(Boolean, nullable=True)

    # Relationships
    users = relationship("User", back_populates="company")
    referral_materials = relationship(
        "ReferralMaterials", back_populates="company", uselist=False
    )
    referrals = relationship("Referral", back_populates="company")
    postings = relationship("Posting", back_populates="company")
    applications = relationship("Application", back_populates="company")
    locations = relationship(
        "Location",
        secondary="companies_locations_rel",
        back_populates="companies",
    )


class CompanyLocationRel(Base):
    __tablename__ = "companies_locations_rel"
    __table_args__ = {"extend_existing": True}
    company_id = Column(Integer, ForeignKey("companies.id"), primary_key=True)
    location_id = Column(Integer, ForeignKey("locations.id"), primary_key=True)
