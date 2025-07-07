from fastapi import APIRouter,Depends,status,HTTPException
from .. import schemas,database,models
from passlib.context import CryptContext
from sqlalchemy.orm import Session
 
from ..schemas import TokenData
from datetime import datetime,timedelta
from ..database import get_db
from jose import jwt,JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "1234567"
ALOGORITHM = "HS256"
ACCESS_TOKEN_EXPIRES_MINUTES = 20
def generate_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRES_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt
@router.post('/login')
def login(request:schemas.Login,db: Session = Depends(get_db)):
    seller = db.query(models.Seller).filter(models.Seller.username==request.username).first()
    if not seller:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = 'Username not found/ invalid user')
    if not pwd_context.verify(request.password,seller.password):
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = 'Invalid Password')
    access_token = generate_token(
        data = {"sub":seller.username}
    )
    return {"access_token":access_token,"token_type":"bearer"}

def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED,
                                          detail = "Invalid auth credentials",
                                          headers = {'WWW-Authenticate':"Bearer"})
    try:
        jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        credentials_exception
    return token_data