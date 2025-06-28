from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import HTTPException
import logging

# 导入数据库和模型
from .database import engine
from . import models

# 导入路由
from .routers import user, home, device, analytics

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建数据库表
try:
    models.Base.metadata.create_all(bind=engine)
    logger.info("Database tables created successfully")
except Exception as e:
    logger.error(f"Error creating database tables: {e}")

# 创建FastAPI应用实例
app = FastAPI(
    title="Smart Home API",
    description="""
    智能家居管理系统API
    
    ## 功能特性
    
    * **用户管理**: 创建、查询、更新、删除用户
    * **房屋管理**: 管理房屋信息和用户关联关系
    * **设备管理**: 管理智能家居设备
    * **使用分析**: 设备使用统计和分析
    * **数据可视化**: 提供图表数据接口
    * **安全监控**: 安全事件记录和分析
    * **用户反馈**: 设备反馈管理系统
    
    ## 主要分析功能
    
    1. 查看用户关联的所有房屋
    2. 设备使用时长统计（日/周/月/年）
    3. 设备使用时间段分布分析
    4. 设备使用关联性分析
    5. 房屋面积对设备使用的影响分析
    6. 系统警报类型分布分析
    7. 用户反馈统计和解决率分析
    """,
    version="1.0.0",
    contact={
        "name": "Smart Home API Support",
        "email": "support@smarthome.com",
    },
    license_info={
        "name": "MIT",
    },
)

# 添加CORS中间件，允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该指定具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理器
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error", "status_code": 500}
    )

# 包含所有路由
app.include_router(
    user.router,
    prefix="/api/v1"
)

app.include_router(
    home.router,
    prefix="/api/v1"
)

app.include_router(
    device.router,
    prefix="/api/v1"
)

app.include_router(
    analytics.router,
    prefix="/api/v1"
)

# 根路径
@app.get("/")
async def read_root():
    """
    根路径，返回API欢迎信息
    """
    return {
        "message": "Welcome to Smart Home API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc"
    }

# 健康检查端点
@app.get("/health")
async def health_check():
    """
    健康检查端点，用于监控API状态
    """
    return {
        "status": "healthy",
        "message": "Smart Home API is running"
    }

# API信息端点
@app.get("/api/v1/info")
async def api_info():
    """
    返回API的详细信息
    """
    return {
        "title": "Smart Home API",
        "version": "1.0.0",
        "description": "智能家居管理系统API",
        "endpoints": {
            "users": "/api/v1/users",
            "homes": "/api/v1/homes", 
            "devices": "/api/v1/devices",
            "analytics": "/api/v1/analytics"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )