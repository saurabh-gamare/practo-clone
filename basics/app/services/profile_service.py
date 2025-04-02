from fastapi import HTTPException
from starlette import status

from models.profile import Profile


class ProfileService:

    def check_if_profile_exists(self, db, user):
        profile = db.query(Profile).filter(Profile.user_id==user.get("id")).first()
        if profile:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Profile already exists for the user.")

    async def create_profile(self, db, request, user):
        self.check_if_profile_exists(db, user)
        profile = Profile(**request.model_dump(), user_id=user.get("id"))
        db.add(profile)
        db.commit()

        return {"profile_id": profile.id}