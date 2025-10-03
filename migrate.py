from database import Base, engine
import models

print("Running migrations...")
Base.metadata.create_all(bind=engine)
print("Done.")