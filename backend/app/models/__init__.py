from .user import User
from .project import Project

# Import Base from database to ensure it's available if needed,
# though models already import it. Redundant but safe.
from ..database import Base 