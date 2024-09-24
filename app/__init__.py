from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask_migrate import Migrate

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SECRET_KEY'] = 'secret_key'

db = SQLAlchemy(app)

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Base = declarative_base()
Session = sessionmaker(bind=engine)

#flask db init
#flask db migrate
#flask db upgrade

class Post(Base):
    __tablename__ = 'post'
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String(80), nullable=False)
    content = Column(db.Text, nullable=False)
    image = Column(db.String)
class Comment(Base):
    __tablename__ = 'comment'
    id = Column(db.Integer, primary_key=True)
    text = Column(db.Text, nullable=False)
    post = Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

Base.metadata.create_all(engine)
session_db = Session()



@app.route('/', methods=['GET'])
def index():
    posts = session_db.query(Post).all()
    return render_template('index.html', posts=posts)


@app.route('/', methods=['POST'])
def post_create():
    title = request.form['title']
    text = request.form['text']
    image = request.files['image']
    image.save(f'static/images/{image.filename}')
    post = Post(title=title, content=text, image=f'static/images/{image.filename}')
    session_db.add(post)
    session_db.commit()
    return {'img_path':f'static/images/{image.filename}'}


@app.route('/post/<int:id>', methods=['GET'])
def show_post(id):
    post = session_db.query(Post).get(id)
    comment = session_db.query(Comment).filter_by(post=post.id)
    return render_template('post_details.html', post=post, comment=comment,) #comment_id=com_id)


@app.route('/post/<int:id>/add-comment/', methods=['POST'])
def post_add_comment(id):
    text = request.form['comment']
    comment = Comment(text=text, post=id)
    session_db.add(comment)
    session_db.commit()
    return {}

@app.route('/post/<int:id>/del-comment/', methods=['POST'])
def post_delete_comment(id):
    comment = session_db.query(Comment).get(id)
    session_db.delete(comment)
    session_db.commit()
    return {'id':id}

@app.route('/post/<int:id>/update-comment/', methods=['POST'])
def post_update_comment(id):
    guagua = request.form[id]
    print('sdfase')
    #session_db.delete(comment)
    #session_db.commit()
    return {'id':id}


if __name__ =='__main__':
    app.run(debug=True)