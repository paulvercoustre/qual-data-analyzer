from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship

from ..database import Base # Use relative import within the app package

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    # Nullable fields for features added later or dependent on external services
    stripe_customer_id = Column(String, unique=True, nullable=True) 
    subscription_tier = Column(String, default="free", nullable=False)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Define relationships if needed later (e.g., with projects)
    # projects = relationship("Project", back_populates="owner")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}')>" 