"""
Python Machine Learning development profile for he2plus.

This profile sets up a complete Python ML development environment
with popular frameworks, tools, and libraries.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

from ..base import BaseProfile, Component, VerificationStep, SampleProject


class PythonMLProfile(BaseProfile):
    """Python Machine Learning development environment."""

    def _initialize_profile(self) -> None:
        self.id = "ml-python"
        self.name = "Python Machine Learning"
        self.description = "Complete Python ML environment with TensorFlow, PyTorch, scikit-learn, and modern tooling"
        self.category = "ml"
        self.version = "1.0.0"

        # Requirements
        self.requirements.ram_gb = 8.0
        self.requirements.disk_gb = 20.0
        self.requirements.cpu_cores = 4
        self.requirements.gpu_required = True
        self.requirements.gpu_vendor = "NVIDIA"
        self.requirements.cuda_required = True
        self.requirements.internet_required = True
        self.requirements.download_size_mb = 3000.0
        self.requirements.supported_archs = ["x86_64", "arm64"]

        # Components
        self.components = [
            # Core Python environment
            Component(
                id="language.python.3.11",
                name="Python 3.11",
                description="Python interpreter for ML development",
                category="language",
                version="3.11",
                download_size_mb=50.0,
                install_time_minutes=5,
                install_methods=["package_manager", "pyenv", "conda", "official"]
            ),
            
            # Package managers
            Component(
                id="tool.pip",
                name="pip",
                description="Python package installer (comes with Python)",
                category="tool",
                download_size_mb=0.0,
                install_time_minutes=0,
                install_methods=["package_manager"]
            ),
            
            Component(
                id="tool.conda",
                name="Conda",
                description="Package and environment management system",
                category="tool",
                download_size_mb=200.0,
                install_time_minutes=10,
                install_methods=["official"]
            ),
            
            Component(
                id="tool.mamba",
                name="Mamba",
                description="Fast conda-compatible package manager",
                category="tool",
                download_size_mb=50.0,
                install_time_minutes=5,
                install_methods=["conda"]
            ),
            
            Component(
                id="tool.poetry",
                name="Poetry",
                description="Dependency management and packaging tool",
                category="tool",
                download_size_mb=10.0,
                install_time_minutes=3,
                install_methods=["pip", "official"]
            ),
            
            # Version control
            Component(
                id="tool.git",
                name="Git",
                description="Version control system",
                category="tool",
                download_size_mb=30.0,
                install_time_minutes=3,
                install_methods=["package_manager", "official"]
            ),
            
            # Development tools
            Component(
                id="tool.vscode",
                name="Visual Studio Code",
                description="Code editor with excellent Python and ML support",
                category="tool",
                download_size_mb=100.0,
                install_time_minutes=5,
                install_methods=["package_manager", "official"]
            ),
            
            Component(
                id="tool.jupyter",
                name="Jupyter Lab",
                description="Interactive development environment for data science",
                category="tool",
                download_size_mb=50.0,
                install_time_minutes=5,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="tool.jupyter-notebook",
                name="Jupyter Notebook",
                description="Web-based interactive computing platform",
                category="tool",
                download_size_mb=30.0,
                install_time_minutes=3,
                install_methods=["pip", "conda"]
            ),
            
            # Core ML frameworks
            Component(
                id="library.tensorflow",
                name="TensorFlow",
                description="End-to-end open source machine learning platform",
                category="library",
                download_size_mb=500.0,
                install_time_minutes=15,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.pytorch",
                name="PyTorch",
                description="Deep learning framework with dynamic computation graphs",
                category="library",
                download_size_mb=400.0,
                install_time_minutes=12,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.scikit-learn",
                name="scikit-learn",
                description="Machine learning library for Python",
                category="library",
                download_size_mb=50.0,
                install_time_minutes=5,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.keras",
                name="Keras",
                description="High-level neural networks API",
                category="library",
                download_size_mb=20.0,
                install_time_minutes=3,
                install_methods=["pip", "conda"]
            ),
            
            # Data manipulation and analysis
            Component(
                id="library.pandas",
                name="Pandas",
                description="Data manipulation and analysis library",
                category="library",
                download_size_mb=30.0,
                install_time_minutes=3,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.numpy",
                name="NumPy",
                description="Fundamental package for scientific computing",
                category="library",
                download_size_mb=20.0,
                install_time_minutes=2,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.scipy",
                name="SciPy",
                description="Scientific computing library",
                category="library",
                download_size_mb=40.0,
                install_time_minutes=4,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.polars",
                name="Polars",
                description="Fast multi-threaded DataFrame library",
                category="library",
                download_size_mb=10.0,
                install_time_minutes=2,
                install_methods=["pip", "conda"]
            ),
            
            # Visualization
            Component(
                id="library.matplotlib",
                name="Matplotlib",
                description="Plotting library for Python",
                category="library",
                download_size_mb=25.0,
                install_time_minutes=3,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.seaborn",
                name="Seaborn",
                description="Statistical data visualization library",
                category="library",
                download_size_mb=15.0,
                install_time_minutes=2,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.plotly",
                name="Plotly",
                description="Interactive plotting library",
                category="library",
                download_size_mb=20.0,
                install_time_minutes=3,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.bokeh",
                name="Bokeh",
                description="Interactive visualization library",
                category="library",
                download_size_mb=15.0,
                install_time_minutes=2,
                install_methods=["pip", "conda"]
            ),
            
            # Deep learning utilities
            Component(
                id="library.transformers",
                name="Transformers",
                description="State-of-the-art Natural Language Processing library",
                category="library",
                download_size_mb=100.0,
                install_time_minutes=8,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.datasets",
                name="Datasets",
                description="Library for easily accessing and sharing datasets",
                category="library",
                download_size_mb=30.0,
                install_time_minutes=3,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.accelerate",
                name="Accelerate",
                description="Library for accelerating PyTorch training",
                category="library",
                download_size_mb=10.0,
                install_time_minutes=2,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.optuna",
                name="Optuna",
                description="Hyperparameter optimization framework",
                category="library",
                download_size_mb=20.0,
                install_time_minutes=3,
                install_methods=["pip", "conda"]
            ),
            
            # Computer vision
            Component(
                id="library.opencv",
                name="OpenCV",
                description="Computer vision and image processing library",
                category="library",
                download_size_mb=100.0,
                install_time_minutes=8,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.pillow",
                name="Pillow",
                description="Python Imaging Library",
                category="library",
                download_size_mb=15.0,
                install_time_minutes=2,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.albumentations",
                name="Albumentations",
                description="Fast image augmentation library",
                category="library",
                download_size_mb=10.0,
                install_time_minutes=2,
                install_methods=["pip", "conda"]
            ),
            
            # Natural language processing
            Component(
                id="library.nltk",
                name="NLTK",
                description="Natural Language Toolkit",
                category="library",
                download_size_mb=50.0,
                install_time_minutes=5,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.spacy",
                name="spaCy",
                description="Industrial-strength Natural Language Processing",
                category="library",
                download_size_mb=100.0,
                install_time_minutes=8,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.gensim",
                name="Gensim",
                description="Topic modeling and document similarity",
                category="library",
                download_size_mb=30.0,
                install_time_minutes=3,
                install_methods=["pip", "conda"]
            ),
            
            # Time series
            Component(
                id="library.prophet",
                name="Prophet",
                description="Forecasting tool for time series data",
                category="library",
                download_size_mb=40.0,
                install_time_minutes=5,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.statsmodels",
                name="Statsmodels",
                description="Statistical modeling and econometrics",
                category="library",
                download_size_mb=50.0,
                install_time_minutes=5,
                install_methods=["pip", "conda"]
            ),
            
            # Model deployment and serving
            Component(
                id="library.fastapi",
                name="FastAPI",
                description="Modern web framework for building APIs",
                category="library",
                download_size_mb=20.0,
                install_time_minutes=3,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.streamlit",
                name="Streamlit",
                description="Framework for building data applications",
                category="library",
                download_size_mb=30.0,
                install_time_minutes=3,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.gradio",
                name="Gradio",
                description="Build and share machine learning demos",
                category="library",
                download_size_mb=25.0,
                install_time_minutes=3,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.mlflow",
                name="MLflow",
                description="Open source platform for ML lifecycle",
                category="library",
                download_size_mb=40.0,
                install_time_minutes=5,
                install_methods=["pip", "conda"]
            ),
            
            # Data storage and databases
            Component(
                id="library.sqlalchemy",
                name="SQLAlchemy",
                description="SQL toolkit and ORM",
                category="library",
                download_size_mb=15.0,
                install_time_minutes=2,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.redis",
                name="Redis",
                description="In-memory data structure store",
                category="library",
                download_size_mb=10.0,
                install_time_minutes=2,
                install_methods=["pip", "conda"]
            ),
            
            # Testing and quality
            Component(
                id="tool.pytest",
                name="pytest",
                description="Testing framework for Python",
                category="tool",
                download_size_mb=10.0,
                install_time_minutes=2,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="tool.black",
                name="Black",
                description="Python code formatter",
                category="tool",
                download_size_mb=5.0,
                install_time_minutes=1,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="tool.flake8",
                name="Flake8",
                description="Python style guide enforcement",
                category="tool",
                download_size_mb=5.0,
                install_time_minutes=1,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="tool.mypy",
                name="MyPy",
                description="Static type checker for Python",
                category="tool",
                download_size_mb=10.0,
                install_time_minutes=2,
                install_methods=["pip", "conda"]
            ),
            
            # GPU and CUDA support
            Component(
                id="library.cupy",
                name="CuPy",
                description="NumPy-compatible array library for GPU",
                category="library",
                download_size_mb=200.0,
                install_time_minutes=10,
                install_methods=["pip", "conda"]
            ),
            
            Component(
                id="library.rapids",
                name="RAPIDS",
                description="GPU-accelerated data science libraries",
                category="library",
                download_size_mb=500.0,
                install_time_minutes=20,
                install_methods=["conda"]
            ),
        ]

        # Verification steps
        self.verification_steps = [
            VerificationStep(
                name="Python Version",
                command="python --version",
                contains_text="Python 3.11"
            ),
            VerificationStep(
                name="pip Version",
                command="pip --version"
            ),
            VerificationStep(
                name="Git Version",
                command="git --version",
                contains_text="git version"
            ),
            VerificationStep(
                name="Jupyter Lab",
                command="jupyter lab --version",
                contains_text="."
            ),
            VerificationStep(
                name="TensorFlow",
                command="python -c 'import tensorflow as tf; print(tf.__version__)'",
                contains_text="."
            ),
            VerificationStep(
                name="PyTorch",
                command="python -c 'import torch; print(torch.__version__)'",
                contains_text="."
            ),
            VerificationStep(
                name="scikit-learn",
                command="python -c 'import sklearn; print(sklearn.__version__)'",
                contains_text="."
            ),
            VerificationStep(
                name="Pandas",
                command="python -c 'import pandas; print(pandas.__version__)'",
                contains_text="."
            ),
            VerificationStep(
                name="NumPy",
                command="python -c 'import numpy; print(numpy.__version__)'",
                contains_text="."
            ),
            VerificationStep(
                name="Matplotlib",
                command="python -c 'import matplotlib; print(matplotlib.__version__)'",
                contains_text="."
            ),
            VerificationStep(
                name="CUDA Support",
                command="python -c 'import torch; print(torch.cuda.is_available())'",
                contains_text="True"
            ),
        ]

        # Sample project
        self.sample_project = SampleProject(
            name="ML Starter Project",
            description="A complete machine learning project with data preprocessing, model training, and evaluation",
            type="create_app",
            source="git clone https://github.com/he2plus/ml-starter-kit.git",
            directory="~/ml-starter-kit",
            setup_commands=[
                "cd ~/ml-starter-kit",
                "pip install -r requirements.txt",
                "jupyter lab"
            ],
            next_steps=[
                "Open Jupyter Lab in your browser",
                "Explore the sample notebooks in the notebooks/ directory",
                "Run the data preprocessing notebook",
                "Train your first model",
                "Evaluate model performance",
                "Deploy your model with FastAPI"
            ]
        )

        # Next steps
        self.next_steps = [
            "🎉 Python Machine Learning environment ready!",
            "",
            "📚 Quick Start:",
            "  • Start Jupyter Lab: jupyter lab",
            "  • Create new notebook: File > New > Notebook",
            "  • Import libraries: import pandas as pd, import numpy as np",
            "  • Load data: df = pd.read_csv('data.csv')",
            "  • Train model: from sklearn.ensemble import RandomForestClassifier",
            "",
            "🛠️  Development Tools:",
            "  • Jupyter Lab for interactive development",
            "  • VS Code with Python and ML extensions",
            "  • TensorBoard for model visualization",
            "  • MLflow for experiment tracking",
            "  • FastAPI for model serving",
            "",
            "📊 Key Libraries:",
            "  • TensorFlow 2.x for deep learning",
            "  • PyTorch for research and development",
            "  • scikit-learn for traditional ML",
            "  • Pandas for data manipulation",
            "  • NumPy for numerical computing",
            "  • Matplotlib/Seaborn for visualization",
            "",
            "🚀 Model Deployment:",
            "  • FastAPI for REST APIs",
            "  • Streamlit for web apps",
            "  • Gradio for ML demos",
            "  • Docker for containerization",
            "  • Kubernetes for orchestration",
            "  • AWS SageMaker for cloud deployment",
            "",
            "📖 Resources:",
            "  • TensorFlow Documentation: https://tensorflow.org/docs",
            "  • PyTorch Documentation: https://pytorch.org/docs",
            "  • scikit-learn Documentation: https://scikit-learn.org/stable/",
            "  • Pandas Documentation: https://pandas.pydata.org/docs",
            "  • Jupyter Documentation: https://jupyter.org/documentation",
            "",
            "💡 Pro Tips:",
            "  • Use virtual environments for project isolation",
            "  • Leverage GPU acceleration for deep learning",
            "  • Implement proper data validation and preprocessing",
            "  • Use MLflow for experiment tracking and model versioning",
            "  • Set up automated testing for your ML pipeline",
            "  • Monitor model performance in production",
            "",
            "🔗 Community:",
            "  • TensorFlow Community: https://discuss.tensorflow.org",
            "  • PyTorch Community: https://discuss.pytorch.org",
            "  • scikit-learn Community: https://scikit-learn.org/community.html",
            "  • Stack Overflow: https://stackoverflow.com/questions/tagged/machine-learning",
            "",
            "📞 Support:",
            "  • GitHub Issues: https://github.com/tensorflow/tensorflow/issues",
            "  • PyTorch Forums: https://discuss.pytorch.org",
            "  • Stack Overflow: https://stackoverflow.com/questions/tagged/python+machine-learning"
        ]

    def get_installation_plan(self) -> Dict[str, any]:
        """Get detailed installation plan for this profile."""
        return {
            "profile": {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "category": self.category,
                "version": self.version
            },
            "requirements": {
                "ram_gb": self.requirements.ram_gb,
                "disk_gb": self.requirements.disk_gb,
                "cpu_cores": self.requirements.cpu_cores,
                "gpu_required": self.requirements.gpu_required,
                "gpu_vendor": self.requirements.gpu_vendor,
                "cuda_required": self.requirements.cuda_required,
                "internet_required": self.requirements.internet_required,
                "download_size_mb": self.requirements.download_size_mb,
                "supported_archs": self.requirements.supported_archs
            },
            "components": [
                {
                    "id": comp.id,
                    "name": comp.name,
                    "description": comp.description,
                    "category": comp.category,
                    "version": comp.version,
                    "download_size_mb": comp.download_size_mb,
                    "install_time_minutes": comp.install_time_minutes,
                    "install_methods": comp.install_methods
                }
                for comp in self.components
            ],
            "verification": [
                {
                    "name": step.name,
                    "command": step.command,
                    "expected_output": step.expected_output,
                    "contains_text": step.contains_text,
                    "timeout_seconds": step.timeout_seconds
                }
                for step in self.verification_steps
            ],
            "sample_project": {
                "name": self.sample_project.name,
                "description": self.sample_project.description,
                "type": self.sample_project.type,
                "source": self.sample_project.source,
                "directory": self.sample_project.directory,
                "setup_commands": self.sample_project.setup_commands,
                "next_steps": self.sample_project.next_steps
            },
            "next_steps": self.next_steps,
            "estimated_total_time_minutes": sum(comp.install_time_minutes for comp in self.components),
            "estimated_download_size_mb": sum(comp.download_size_mb for comp in self.components),
            "ml_specific": {
                "frameworks": ["TensorFlow", "PyTorch", "scikit-learn", "Keras"],
                "languages": ["Python", "R", "Julia", "Scala"],
                "data_manipulation": ["Pandas", "NumPy", "Polars", "Dask"],
                "visualization": ["Matplotlib", "Seaborn", "Plotly", "Bokeh"],
                "deep_learning": ["TensorFlow", "PyTorch", "Keras", "Transformers"],
                "computer_vision": ["OpenCV", "Pillow", "Albumentations", "torchvision"],
                "nlp": ["Transformers", "spaCy", "NLTK", "Gensim"],
                "deployment": ["FastAPI", "Streamlit", "Gradio", "MLflow"],
                "gpu_acceleration": ["CUDA", "CuPy", "RAPIDS", "TensorRT"],
                "popular_libraries": [
                    "Pandas", "NumPy", "Matplotlib", "Seaborn", "scikit-learn",
                    "TensorFlow", "PyTorch", "OpenCV", "NLTK", "spaCy"
                ]
            }
        }

    def get_development_workflow(self) -> List[str]:
        """Get typical development workflow for ML projects."""
        return [
            "1. Create virtual environment: python -m venv ml-env",
            "2. Activate environment: source ml-env/bin/activate (Linux/macOS) or ml-env\\Scripts\\activate (Windows)",
            "3. Install dependencies: pip install -r requirements.txt",
            "4. Start Jupyter Lab: jupyter lab",
            "5. Create new notebook for data exploration",
            "6. Load and explore data with Pandas",
            "7. Perform data preprocessing and cleaning",
            "8. Split data into train/validation/test sets",
            "9. Train initial model with scikit-learn",
            "10. Evaluate model performance",
            "11. Experiment with different algorithms",
            "12. Use TensorFlow/PyTorch for deep learning",
            "13. Tune hyperparameters with Optuna",
            "14. Track experiments with MLflow",
            "15. Deploy model with FastAPI or Streamlit"
        ]

    def get_troubleshooting_guide(self) -> Dict[str, List[str]]:
        """Get troubleshooting guide for common ML issues."""
        return {
            "Installation Issues": [
                "Python version compatibility - ensure Python 3.8+ is installed",
                "CUDA version mismatch - check CUDA compatibility with TensorFlow/PyTorch",
                "Memory issues - increase virtual memory or use smaller batch sizes",
                "Permission errors - use virtual environments or conda environments",
                "Network issues - check proxy settings and firewall configuration",
                "Disk space - ensure at least 20GB free space for ML libraries"
            ],
            "Development Issues": [
                "Jupyter not starting - check port availability and firewall settings",
                "Import errors - verify package installation and Python path",
                "Memory errors - reduce batch size or use data generators",
                "GPU not detected - check CUDA installation and driver compatibility",
                "Slow performance - enable GPU acceleration and optimize data loading",
                "Version conflicts - use virtual environments for project isolation"
            ],
            "Model Training Issues": [
                "Overfitting - use regularization, dropout, or early stopping",
                "Underfitting - increase model complexity or feature engineering",
                "Training instability - adjust learning rate and batch size",
                "Memory overflow - reduce batch size or use gradient checkpointing",
                "Slow training - enable mixed precision and optimize data pipeline",
                "Convergence issues - check data preprocessing and model architecture"
            ],
            "Deployment Issues": [
                "Model size too large - use model compression or quantization",
                "Inference speed - optimize model architecture and use TensorRT",
                "API errors - check input validation and error handling",
                "Scaling issues - use load balancing and container orchestration",
                "Monitoring gaps - implement proper logging and metrics collection",
                "Version management - use MLflow for model versioning and tracking"
            ]
        }

    def get_recommended_extensions(self) -> List[str]:
        """Get recommended VS Code extensions for ML development."""
        return [
            "ms-python.python",
            "ms-python.vscode-pylance",
            "ms-python.flake8",
            "ms-python.black-formatter",
            "ms-python.isort",
            "ms-toolsai.jupyter",
            "ms-toolsai.jupyter-keymap",
            "ms-toolsai.jupyter-renderers",
            "ms-toolsai.vscode-jupyter-cell-tags",
            "ms-toolsai.vscode-jupyter-slideshow",
            "ms-vscode.vscode-json",
            "ms-vscode.vscode-yaml",
            "ms-vscode.vscode-markdown",
            "ms-vscode.vscode-git",
            "ms-vscode.vscode-git-graph",
            "ms-vscode.vscode-gitlens",
            "ms-vscode.vscode-thunder-client",
            "ms-vscode.vscode-restclient",
            "ms-vscode.vscode-docker",
            "ms-vscode.vscode-kubernetes-tools"
        ]

    def get_useful_commands(self) -> Dict[str, List[str]]:
        """Get useful commands for ML development."""
        return {
            "Environment Management": [
                "python -m venv ml-env - Create virtual environment",
                "source ml-env/bin/activate - Activate environment (Linux/macOS)",
                "ml-env\\Scripts\\activate - Activate environment (Windows)",
                "pip install -r requirements.txt - Install dependencies",
                "pip freeze > requirements.txt - Save dependencies",
                "conda create -n ml-env python=3.11 - Create conda environment",
                "conda activate ml-env - Activate conda environment"
            ],
            "Jupyter Commands": [
                "jupyter lab - Start Jupyter Lab",
                "jupyter notebook - Start Jupyter Notebook",
                "jupyter lab --port 8888 - Start on specific port",
                "jupyter lab --no-browser - Start without opening browser",
                "jupyter lab --ip=0.0.0.0 - Allow external access",
                "jupyter lab --generate-config - Generate config file",
                "jupyter lab --version - Check Jupyter version"
            ],
            "Data Science": [
                "python -c 'import pandas as pd; print(pd.__version__)' - Check Pandas version",
                "python -c 'import numpy as np; print(np.__version__)' - Check NumPy version",
                "python -c 'import matplotlib; print(matplotlib.__version__)' - Check Matplotlib version",
                "python -c 'import sklearn; print(sklearn.__version__)' - Check scikit-learn version",
                "python -c 'import tensorflow as tf; print(tf.__version__)' - Check TensorFlow version",
                "python -c 'import torch; print(torch.__version__)' - Check PyTorch version"
            ],
            "Model Training": [
                "python train.py --epochs 100 --batch-size 32 - Train model with parameters",
                "python train.py --gpu 0 --workers 4 - Train with GPU and multiple workers",
                "python train.py --resume checkpoint.pth - Resume training from checkpoint",
                "python train.py --validate - Train with validation",
                "python train.py --test - Test trained model",
                "python train.py --export - Export model for deployment"
            ],
            "Testing and Quality": [
                "pytest tests/ - Run all tests",
                "pytest tests/ -v - Run tests with verbose output",
                "pytest tests/ -k test_model - Run specific test",
                "black . - Format code with Black",
                "flake8 . - Check code style with Flake8",
                "mypy . - Check types with MyPy",
                "pytest --cov=src tests/ - Run tests with coverage"
            ],
            "Deployment": [
                "python -m uvicorn main:app --reload - Start FastAPI server",
                "streamlit run app.py - Start Streamlit app",
                "gradio app.py - Start Gradio app",
                "docker build -t ml-app . - Build Docker image",
                "docker run -p 8000:8000 ml-app - Run Docker container",
                "kubectl apply -f deployment.yaml - Deploy to Kubernetes"
            ]
        }
