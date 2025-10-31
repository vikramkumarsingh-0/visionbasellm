from setuptools import setup, find_packages

setup(
    name="vision-web-automation",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "playwright>=1.40.0",
        "ultralytics>=8.1.0",
        "torch>=2.1.0",
        "ollama>=0.1.6",
        "groq>=0.4.1",
        "celery>=5.3.4",
        "fastapi>=0.108.0",
        "loguru>=0.7.2",
    ],
    author="Vision Automation Team",
    description="Self-learning vision-based web automation system",
    python_requires=">=3.10",
)
