from setuptools import find_packages, setup

# find_packages will find all the packages with __init__.py
print(find_packages())

setup(
    name="travel_planner",
    version="0.0.1",
    description="""
    This package is used for travel planning in public transport.
    It has backend code, frontend code and utils.
    """,
    author="YOUR_NAME",
    author_email="YOUR_EMAIL@mail.com",
    install_requires=["streamlit", "pandas", "folium", "requests"],
    packages=find_packages(
        exclude=("test*", "explorations"), include=["backend", "frontend", "utils"]
    ),
    entry_points={"console_scripts": ["dashboard = utils.run_dashboard:run_dashboard"]},
)
