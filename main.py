from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.middleware.cors import CORSMiddleware
from . import crud, models, schemas, auth, database

app = FastAPI()

# Разрешаем фронтенду общаться с бэкендом
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: AsyncSession = Depends(database.get_db)):
    db_user = await crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return await crud.create_user(db=db, user=user)

@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(database.get_db)):
    user = await crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = auth.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/tasks", response_model=list[schemas.Task])
async def get_tasks(db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return await crud.get_tasks(db, owner_id=current_user.id)

@app.post("/tasks", response_model=schemas.Task)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return await crud.create_task(db, task=task, owner_id=current_user.id)

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    success = await crud.delete_task(db, task_id=task_id, owner_id=current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"status": "success"}
