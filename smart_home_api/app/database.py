from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 从环境变量获取数据库URL，如果没有则使用PostgreSQL默认值
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:cyqsxxna30813282@localhost:5432/smart_home"
)

logger.info(f"Connecting to database: {DATABASE_URL.split('@')[0]}@***")

try:
    # 创建数据库引擎
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,  # 验证连接是否有效
        pool_recycle=300,    # 5分钟后回收连接
        echo=False           # 设置为True可以看到SQL查询日志
    )
    
    # 测试数据库连接
    with engine.connect() as connection:
        logger.info("Database connection successful!")
        
except Exception as e:
    logger.error(f"Database connection failed: {e}")
    logger.info("Please check your PostgreSQL configuration:")
    logger.info("1. PostgreSQL服务是否正在运行")
    logger.info("2. 数据库用户名和密码是否正确")
    logger.info("3. 数据库名称是否存在")
    logger.info("4. 连接参数是否正确")
    raise

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
Base = declarative_base()

# 数据库依赖项
def get_db():
    """
    创建数据库会话的依赖项函数
    用于FastAPI的依赖注入系统
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()