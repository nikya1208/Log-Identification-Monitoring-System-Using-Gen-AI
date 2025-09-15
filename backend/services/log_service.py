# # app/services/log_service.py
# from sqlalchemy.orm import Session
# from app import models, schemas, crud

# def process_log_entry(db: Session, log: schemas.LogCreate):
#     """
#     Process and store a log entry in the database.
#     Additional business logic such as filtering, transformations, etc., can be added.
#     """
#     return crud.create_log(db=db, log=log)

# def fetch_logs(db: Session):
#     """
#     Retrieve all logs from the database.
#     Business logic like filtering by severity, time range, etc., can be implemented here.
#     """
#     return crud.get_logs(db=db)




# app/services/log_service.py
from sqlalchemy.orm import Session
from app import models, schemas, crud

def process_log_entry(db: Session, log: schemas.LogCreate):
    """
    Process and store a log entry in the database.
    Additional business logic such as filtering, transformations, etc., can be added.
    """
    return crud.create_log(db=db, log=log)

def fetch_logs(db: Session):
    """
    Retrieve all logs from the database.
    Business logic like filtering by severity, time range, etc., can be implemented here.
    """
    logs = crud.get_logs(db=db)
    
    # Modify log messages before sending to frontend
    for log in logs:
        if "Database connection failed" in log.message:
            log.message = "⚠️ Database Issue Detected!"
        elif "High memory usage detected" in log.message:
            log.message = "🚨 High Memory Alert!"
    
    return logs
