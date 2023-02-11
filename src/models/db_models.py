import uuid

from sqlalchemy import Column, DateTime, Text, Boolean, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime

from db.db import Base


class UrlModel(Base):
    __tablename__ = "url"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    original_url = Column(Text, unique=True, nullable=False)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)
    is_deleted = Column(Boolean, default=False)
    history = relationship("HistoryModel")

    __mapper_args__ = {"eager_defaults": True}

    def __repr__(self):
        return "Url(origin_url='%s', id='%s)" % (self.original_url, self.id)


class HistoryModel(Base):
    __tablename__ = 'history'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    url_id = Column(ForeignKey('url.id'), nullable=False)
    counter = Column(Integer, default=0)
    url = relationship('UrlModel', back_populates='history')

    def __repr__(self):
        return "History(url_id='%s', counter='%d')" % (self.url_id, self.counter)
