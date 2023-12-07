from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class ZhviNeighborhoodRecord(db.Model):
    region_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    size_rank: Mapped[int] = mapped_column(Integer, nullable=True)
    region_name: Mapped[str] = mapped_column(String, nullable=True)
    region_type: Mapped[str] = mapped_column(String, nullable=True)
    state_name: Mapped[str] = mapped_column(String, nullable=True)
    state: Mapped[str] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=True)
    metro: Mapped[str] = mapped_column(String, nullable=True)
    county_name: Mapped[str] = mapped_column(String, nullable=True)
