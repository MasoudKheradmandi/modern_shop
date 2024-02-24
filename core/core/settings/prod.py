from .base import *
from dotenv import load_dotenv

load_dotenv()
ALLOWED_HOSTS =  os.environ.get('ALLOWED_HOSTS','* ').split(' ')
SECRET_KEY= os.environ.get('SECRET_KEY','test') 
DEBUG =  os.environ.get('DEBUG',False)