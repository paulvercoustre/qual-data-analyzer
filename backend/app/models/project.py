from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

# Use relative import for Base within the same package
from ..database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True) # Optional description
    owner_id = Column(Integer, ForeignKey("users.id"), nullable=False) # Link to the user who owns it

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Define the relationship to the User model
    # 'owner' is the attribute to access the User object from a Project instance
    # 'back_populates' links it to the corresponding relationship in the User model (we'll add this later)
    owner = relationship("User", back_populates="projects")

    # Define relationships to other models if needed later (e.g., data sources, codes)
    # data_sources = relationship("DataSource", back_populates="project", cascade="all, delete-orphan")
    # codes = relationship("Code", back_populates="project", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}', owner_id={self.owner_id})>"

# Now, we need to update the User model to include the reverse relationship
# We'll do that in the next step. 