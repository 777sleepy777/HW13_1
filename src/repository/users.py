from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.schemas import UserModel
from src.database.models import User

async def get_user_by_email(email: str, db: Session) -> User:
    """
       Retrieves a single user with the unique email for a specific user.
       :param email: The email of the user to retrieve.
       :type email: str
       :param db: The database session.
       :type db: Session
       :return: The user with the unique email, or None if it does not exist.
       :rtype: User | None
       """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
        Creates a new user for a specific email.

        :param body: The data for the note to create.
        :type body: UserModel
        :param db: The database session.
        :type db: Session
        :return: The newly created user.
        :rtype: User
        """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    user.refresh_token = token
    db.commit()
    
async def confirmed_email(email: str, db: Session) -> None:
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
