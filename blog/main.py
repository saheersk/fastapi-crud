from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, SessionLocal


app = FastAPI()

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)

    return new_blog


@app.delete('/blog/{id}', status_code=status.HTTP_204_NO_CONTENT)
def blog_delete(id:int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    blog.delete(synchronize_session=False)
    db.commit()

    return {"detail": f"Blog {id} is deleted successfully"}


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED)
def blog_update(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {id} not found")
    
    blog.update(request.dict())
    db.commit()

    return {"detail": f"Blog {id} is updated successfully"}


@app.get('/blog')
def all_blog(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()

    return blogs


@app.get('/blog/{id}', status_code=200)
def blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()

    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': }

    return blog