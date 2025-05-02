from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./db.sqlite3"
engine = create_engine(DATABASE_URL, echo=True)

def get_session():
    with Session(engine) as session:
        yield session

def init_db():
    # Importar todos los modelos ORM para que SQLModel pueda crear las tablas
    from infrastructure.orm.models import User, Role, UserRole
    
    # Crear todas las tablas
    SQLModel.metadata.create_all(engine)
    
    # Inicializar algunos roles básicos si es necesario
    with Session(engine) as session:
        from infrastructure.orm.models import Role
        from sqlmodel import select
        
        # Verificar si ya existe el rol ADMIN
        admin_statement = select(Role).where(Role.name == "ADMIN")
        admin_role = session.exec(admin_statement).first()
        
        # Crear rol ADMIN si no existe
        if not admin_role:
            admin_role = Role(name="ADMIN", description="Administrador con acceso total")
            session.add(admin_role)
        
        # Verificar si ya existe el rol USER
        user_statement = select(Role).where(Role.name == "USER")
        user_role = session.exec(user_statement).first()
        
        # Crear rol USER si no existe
        if not user_role:
            user_role = Role(name="USER", description="Usuario regular")
            session.add(user_role)
        
        session.commit()
