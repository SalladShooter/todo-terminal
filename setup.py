from setuptools import setup, find_packages

setup(
    name="todo",
    version="0.1.0",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'todo=todo.main:main',
        ],
    },
    install_requires=[
        'windows-curses; sys_platform == "win32"'
    ],
    author="SalladShooter",
    description="A Todo TUI application",
)
