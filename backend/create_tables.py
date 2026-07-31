from app.database.database import Base, engine
from app.models import *

print("Creating tables...")
Base.metadata.create_all(bind=engine)
print("Done!")