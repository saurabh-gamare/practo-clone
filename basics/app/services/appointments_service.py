from fastapi import HTTPException, Depends
from starlette import status
from datetime import datetime, timedelta

from models.appointments import Appointment
from models.auth import User
from models.profile import Profile


class CreateAppmtService:

    def get_blacklisted_slots(self):
        return ["13:00:00-14:00:00", "20:00:00-21:00:00", "22:00:00-09:59:59"] 

    def check_for_blacklisted_slots(self, request):
        appmt_time = request.appmt_date.time()
        for slot in self.get_blacklisted_slots():
            start_time_str, end_time_str = slot.split("-")
            start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()
            end_time = datetime.strptime(end_time_str, "%H:%M:%S").time()
            
            # Day range (e.g., "13:00:00-14:00:00")
            if start_time <= end_time:
                if start_time <= appmt_time <= end_time:
                    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Cannot make appointment in this slot")
            # Case 2: Crosses midnight (e.g., "22:00:00-09:59:00")
            else:
                if appmt_time >= start_time or appmt_time <= end_time:
                    raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Cannot make appointment in this slot")
            
    def check_existing_appmt_in_the_slot(self, db, request):
        buffer_time = request.appmt_date - timedelta(minutes=20)
        appointment = db.query(Appointment).filter(
                        Appointment.appmt_date.between(buffer_time, request.appmt_date), 
                        Appointment.doctor_id==request.doctor_id
                    ).first()
        
        if appointment:
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Cannot make appointment in this slot")
        
    def check_if_doctor_exists(self, db, request):
        doctor_details = db.query(User).filter(User.id==request.doctor_id, User.role=="DOCTOR").first()
        if doctor_details is None:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Doctor does not exists.")

    async def create_appointment(self, db, request, user):
        self.check_if_doctor_exists(db, request)
        self.check_for_blacklisted_slots(request)
        self.check_existing_appmt_in_the_slot(db, request)

        appmt = Appointment(
            patient_id=user.get('id'),
            doctor_id=request.doctor_id, 
            appmt_date=request.appmt_date
        )
        db.add(appmt)
        db.commit()

        return {"appointment_id": appmt.id}
    

class ListAppmtService:
    
    async def list_appointments(self, db, offset, limit, status, user):
        appointments = db.query(Appointment).filter(
            Appointment.doctor_id==user.get("id"),
            )
        if status:
            appointments = appointments.filter(Appointment.status==status)

        return {"details": appointments.limit(limit).offset(offset)}


