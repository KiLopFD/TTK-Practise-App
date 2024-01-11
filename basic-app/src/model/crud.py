from src.model.setup import engine, session, Base, User

# Create
# Create a new user
def create_user(name, address, cmnd, date):
    new_user = User(name=name, address=address, cmnd=cmnd, date=date)
    session.add(new_user)
    session.commit()
    return new_user

def get_all_users():
    return session.query(User).all()

def delete_user(id):
    user = session.query(User).filter(User.id == id).first()
    session.delete(user)
    session.commit()

def delete_all():
    session.query(User).delete()
    session.commit()

def up_user(id, name, address, cmnd, date):
    user = session.query(User).filter(User.id == id).first()
    user.name = name
    user.address = address
    user.cmnd = cmnd
    user.date = date
    session.commit()