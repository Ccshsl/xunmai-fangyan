"""
后端唯一启动入口
在 backend/ 目录下运行：python run.py
"""

from app import create_app

app = create_app()


if __name__ == '__main__':
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG'],
    )