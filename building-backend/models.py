from sqlalchemy import Column, Integer, String, Text, Float, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()


class Item(Base):
    __tablename__ = "items"
    id = Column(Text, primary_key=True)
    title = Column(Text)
    input_video = Column(Text)
    output_video = Column(Text, default=None)
    events = Column(Text, default=r"{}")
    downtime_events = Column(Text, default=r"{}")
    seed = Column(Text, default=r"")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    preview_img = Column(Text, default="")
    duration = Column(Integer, default=0)
    is_complete = Column(Boolean, default=False)
