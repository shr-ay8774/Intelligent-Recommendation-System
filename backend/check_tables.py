from app.database.database import Base
from app.models import *

print("Registered tables:")
print(Base.metadata.tables.keys())