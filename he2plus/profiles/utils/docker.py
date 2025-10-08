"""
Utils-Docker Profile

Complete containerization and orchestration environment with Docker Desktop, Kubernetes,
containerization tools, and comprehensive DevOps tooling for modern development workflows.
"""

from ..base import BaseProfile, Component, ProfileRequirements, VerificationStep, SampleProject


class DockerProfile(BaseProfile):
    """Complete containerization and orchestration environment."""
    
    def __init__(self):
        super().__init__()
        
        self.id = "utils-docker"
        self.name = "Containerization Environment"
        self.description = "Complete containerization and orchestration environment with Docker Desktop, Kubernetes, containerization tools, and comprehensive DevOps tooling"
        self.category = "utils"
        self.version = "1.0.0"
    
    def _initialize_profile(self) -> None:
        """Initialize the containerization profile."""
        
        # Containerization tools have moderate requirements
        self.requirements = ProfileRequirements(
            ram_gb=8.0,  # Containers and orchestration need memory
            disk_gb=25.0,  # Docker images and Kubernetes data
            cpu_cores=4,  # Container orchestration benefits from multiple cores
            gpu_required=False,
            gpu_vendor=None,
            cuda_required=False,
            metal_required=False,
            min_os_version=None,
            supported_archs=['x86_64', 'arm64', 'arm'],
            internet_required=True,
            download_size_mb=3000.0  # Docker Desktop and Kubernetes tools are large
        )
        
        self.components = [
            # Core Container Runtime
            Component(
                id="runtime.docker",
                name="Docker Desktop",
                description="Complete containerization platform with GUI",
                category="runtime",
                version="4.26.1",
                download_size_mb=800.0,
                install_time_minutes=15,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64'],
                install_methods=['brew', 'official'],
                verify_command="docker --version",
                verify_expected_output="Docker version"
            ),
            
            Component(
                id="runtime.docker-engine",
                name="Docker Engine",
                description="Lightweight container runtime",
                category="runtime",
                version="24.0.7",
                download_size_mb=200.0,
                install_time_minutes=8,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="docker --version",
                verify_expected_output="Docker version"
            ),
            
            Component(
                id="tool.docker-compose",
                name="Docker Compose",
                description="Multi-container Docker application tool",
                category="tool",
                version="2.21.0",
                download_size_mb=50.0,
                install_time_minutes=3,
                depends_on=['runtime.docker'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="docker-compose --version",
                verify_expected_output="Docker Compose version"
            ),
            
            Component(
                id="tool.docker-buildx",
                name="Docker Buildx",
                description="Extended build capabilities for Docker",
                category="tool",
                version="0.11.2",
                download_size_mb=20.0,
                install_time_minutes=2,
                depends_on=['runtime.docker'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['included'],
                verify_command="docker buildx version",
                verify_expected_output="buildx"
            ),
            
            # Container Orchestration
            Component(
                id="orchestration.kubernetes",
                name="Kubernetes",
                description="Container orchestration platform",
                category="orchestration",
                version="1.28.2",
                download_size_mb=300.0,
                install_time_minutes=10,
                depends_on=['runtime.docker'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="kubectl version --client",
                verify_expected_output="Client Version"
            ),
            
            Component(
                id="orchestration.minikube",
                name="Minikube",
                description="Local Kubernetes development environment",
                category="orchestration",
                version="1.32.0",
                download_size_mb=200.0,
                install_time_minutes=8,
                depends_on=['orchestration.kubernetes'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="minikube version",
                verify_expected_output="minikube version"
            ),
            
            Component(
                id="orchestration.kind",
                name="Kind",
                description="Kubernetes in Docker for testing",
                category="orchestration",
                version="0.20.0",
                download_size_mb=100.0,
                install_time_minutes=5,
                depends_on=['orchestration.kubernetes'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="kind version",
                verify_expected_output="kind version"
            ),
            
            Component(
                id="orchestration.k3s",
                name="K3s",
                description="Lightweight Kubernetes distribution",
                category="orchestration",
                version="1.28.2",
                download_size_mb=150.0,
                install_time_minutes=6,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="k3s --version",
                verify_expected_output="k3s version"
            ),
            
            Component(
                id="tool.helm",
                name="Helm",
                description="Kubernetes package manager",
                category="tool",
                version="3.13.0",
                download_size_mb=50.0,
                install_time_minutes=3,
                depends_on=['orchestration.kubernetes'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="helm version",
                verify_expected_output="version.BuildInfo"
            ),
            
            # Container Development Tools
            Component(
                id="tool.containerd",
                name="containerd",
                description="Industry-standard container runtime",
                category="tool",
                version="1.7.6",
                download_size_mb=100.0,
                install_time_minutes=5,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="containerd --version",
                verify_expected_output="containerd"
            ),
            
            Component(
                id="tool.runc",
                name="runc",
                description="CLI tool for spawning and running containers",
                category="tool",
                version="1.1.8",
                download_size_mb=20.0,
                install_time_minutes=2,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="runc --version",
                verify_expected_output="runc version"
            ),
            
            Component(
                id="tool.buildah",
                name="Buildah",
                description="Tool for building Open Container Initiative containers",
                category="tool",
                version="1.31.0",
                download_size_mb=50.0,
                install_time_minutes=4,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="buildah --version",
                verify_expected_output="buildah version"
            ),
            
            Component(
                id="tool.podman",
                name="Podman",
                description="Daemonless container engine",
                category="tool",
                version="4.7.0",
                download_size_mb=80.0,
                install_time_minutes=5,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="podman --version",
                verify_expected_output="podman version"
            ),
            
            # Container Registry Tools
            Component(
                id="tool.harbor",
                name="Harbor",
                description="Enterprise container registry",
                category="tool",
                version="2.9.0",
                download_size_mb=200.0,
                install_time_minutes=10,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="harbor --version",
                verify_expected_output="Harbor"
            ),
            
            Component(
                id="tool.registry",
                name="Docker Registry",
                description="Simple Docker registry server",
                category="tool",
                version="2.8.2",
                download_size_mb=50.0,
                install_time_minutes=3,
                depends_on=['runtime.docker'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="registry --version",
                verify_expected_output="registry"
            ),
            
            # Container Security Tools
            Component(
                id="tool.trivy",
                name="Trivy",
                description="Vulnerability scanner for containers",
                category="tool",
                version="0.46.0",
                download_size_mb=30.0,
                install_time_minutes=3,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="trivy --version",
                verify_expected_output="trivy version"
            ),
            
            Component(
                id="tool.falco",
                name="Falco",
                description="Runtime security monitoring",
                category="tool",
                version="0.36.2",
                download_size_mb=100.0,
                install_time_minutes=5,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="falco --version",
                verify_expected_output="falco version"
            ),
            
            Component(
                id="tool.opa",
                name="Open Policy Agent",
                description="Policy-based control for cloud native environments",
                category="tool",
                version="0.58.0",
                download_size_mb=40.0,
                install_time_minutes=3,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="opa version",
                verify_expected_output="Version"
            ),
            
            # Container Monitoring & Observability
            Component(
                id="tool.prometheus",
                name="Prometheus",
                description="Monitoring and alerting toolkit",
                category="tool",
                version="2.47.0",
                download_size_mb=80.0,
                install_time_minutes=5,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="prometheus --version",
                verify_expected_output="prometheus"
            ),
            
            Component(
                id="tool.grafana",
                name="Grafana",
                description="Analytics and monitoring platform",
                category="tool",
                version="10.2.0",
                download_size_mb=150.0,
                install_time_minutes=8,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="grafana-server --version",
                verify_expected_output="Version"
            ),
            
            Component(
                id="tool.jaeger",
                name="Jaeger",
                description="Distributed tracing system",
                category="tool",
                version="1.49.0",
                download_size_mb=100.0,
                install_time_minutes=6,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="jaeger-all-in-one --version",
                verify_expected_output="jaeger"
            ),
            
            # Container Development Libraries
            Component(
                id="library.docker-py",
                name="docker-py",
                description="Python library for Docker API",
                category="library",
                version="6.1.3",
                download_size_mb=5.0,
                install_time_minutes=2,
                depends_on=['runtime.docker'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['pip'],
                verify_command="python -c 'import docker; print(docker.__version__)'",
                verify_expected_output="6.1."
            ),
            
            Component(
                id="library.kubernetes-py",
                name="kubernetes",
                description="Python client for Kubernetes API",
                category="library",
                version="28.1.0",
                download_size_mb=3.0,
                install_time_minutes=2,
                depends_on=['orchestration.kubernetes'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['pip'],
                verify_command="python -c 'import kubernetes; print(kubernetes.__version__)'",
                verify_expected_output="28.1."
            ),
            
            # Container Management Tools
            Component(
                id="tool.lazydocker",
                name="LazyDocker",
                description="Simple Docker management interface",
                category="tool",
                version="0.22.0",
                download_size_mb=10.0,
                install_time_minutes=2,
                depends_on=['runtime.docker'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="lazydocker --version",
                verify_expected_output="lazydocker"
            ),
            
            Component(
                id="tool.dive",
                name="Dive",
                description="Docker image analysis tool",
                category="tool",
                version="0.12.0",
                download_size_mb=15.0,
                install_time_minutes=2,
                depends_on=['runtime.docker'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="dive --version",
                verify_expected_output="dive version"
            ),
            
            Component(
                id="tool.hadolint",
                name="Hadolint",
                description="Dockerfile linter",
                category="tool",
                version="2.12.0",
                download_size_mb=20.0,
                install_time_minutes=2,
                depends_on=[],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="hadolint --version",
                verify_expected_output="hadolint version"
            ),
            
            Component(
                id="tool.portainer",
                name="Portainer",
                description="Container management UI",
                category="tool",
                version="2.19.0",
                download_size_mb=100.0,
                install_time_minutes=5,
                depends_on=['runtime.docker'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="portainer --version",
                verify_expected_output="portainer"
            ),
            
            # CI/CD Integration
            Component(
                id="tool.tekton",
                name="Tekton",
                description="Cloud-native CI/CD framework",
                category="tool",
                version="0.50.0",
                download_size_mb=150.0,
                install_time_minutes=8,
                depends_on=['orchestration.kubernetes'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="tkn version",
                verify_expected_output="Client version"
            ),
            
            Component(
                id="tool.argocd",
                name="ArgoCD",
                description="GitOps continuous delivery tool",
                category="tool",
                version="2.8.0",
                download_size_mb=200.0,
                install_time_minutes=10,
                depends_on=['orchestration.kubernetes'],
                conflicts_with=[],
                supported_platforms=['macos', 'linux', 'windows'],
                supported_archs=['x86_64', 'arm64', 'arm'],
                install_methods=['brew', 'apt', 'choco', 'official'],
                verify_command="argocd version",
                verify_expected_output="argocd"
            )
        ]
        
        # Verification steps for all installed components
        self.verification_steps = [
            VerificationStep(
                name="Docker Desktop",
                command="docker --version",
                expected_output=None,
                contains_text="Docker version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Docker Compose",
                command="docker-compose --version",
                expected_output=None,
                contains_text="Docker Compose version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Kubernetes",
                command="kubectl version --client",
                expected_output=None,
                contains_text="Client Version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Minikube",
                command="minikube version",
                expected_output=None,
                contains_text="minikube version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Kind",
                command="kind version",
                expected_output=None,
                contains_text="kind version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Helm",
                command="helm version",
                expected_output=None,
                contains_text="version.BuildInfo",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="containerd",
                command="containerd --version",
                expected_output=None,
                contains_text="containerd",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="runc",
                command="runc --version",
                expected_output=None,
                contains_text="runc version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Buildah",
                command="buildah --version",
                expected_output=None,
                contains_text="buildah version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Podman",
                command="podman --version",
                expected_output=None,
                contains_text="podman version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Trivy",
                command="trivy --version",
                expected_output=None,
                contains_text="trivy version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Falco",
                command="falco --version",
                expected_output=None,
                contains_text="falco version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Open Policy Agent",
                command="opa version",
                expected_output=None,
                contains_text="Version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Prometheus",
                command="prometheus --version",
                expected_output=None,
                contains_text="prometheus",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Grafana",
                command="grafana-server --version",
                expected_output=None,
                contains_text="Version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Jaeger",
                command="jaeger-all-in-one --version",
                expected_output=None,
                contains_text="jaeger",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="docker-py",
                command="python -c 'import docker; print(docker.__version__)'",
                expected_output=None,
                contains_text="6.1.",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="kubernetes-py",
                command="python -c 'import kubernetes; print(kubernetes.__version__)'",
                expected_output=None,
                contains_text="28.1.",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="LazyDocker",
                command="lazydocker --version",
                expected_output=None,
                contains_text="lazydocker",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Dive",
                command="dive --version",
                expected_output=None,
                contains_text="dive version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Hadolint",
                command="hadolint --version",
                expected_output=None,
                contains_text="hadolint version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Portainer",
                command="portainer --version",
                expected_output=None,
                contains_text="portainer",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="Tekton",
                command="tkn version",
                expected_output=None,
                contains_text="Client version",
                timeout_seconds=10
            ),
            
            VerificationStep(
                name="ArgoCD",
                command="argocd version",
                expected_output=None,
                contains_text="argocd",
                timeout_seconds=10
            )
        ]
        
        # Sample project for containerization
        self.sample_project = SampleProject(
            name="Container Development Starter Kit",
            description="Complete containerization environment with sample applications, Kubernetes manifests, and CI/CD pipelines",
            type="git_clone",
            source="https://github.com/he2plus/container-starter-kit.git",
            directory="~/container-project",
            setup_commands=[
                "cd ~/container-project",
                "docker-compose up -d",
                "kubectl apply -f k8s/",
                "minikube start",
                "helm install my-app helm/chart"
            ],
            next_steps=[
                "Start Docker Desktop",
                "Initialize Minikube: minikube start",
                "Create Kind cluster: kind create cluster",
                "Install Helm chart: helm install my-app ./chart",
                "Open Portainer: docker run -d -p 9000:9000 portainer/portainer",
                "Start monitoring: docker-compose -f monitoring/docker-compose.yml up -d",
                "Run security scan: trivy image my-app:latest"
            ]
        )
        
        # Comprehensive next steps for containerization
        self.next_steps = [
            "🎉 Complete containerization and orchestration environment ready!",
            "",
            "🐳 Container Runtime Installed:",
            "   ✅ Docker Desktop 4.26.1 (Complete containerization platform)",
            "   ✅ Docker Engine 24.0.7 (Lightweight container runtime)",
            "   ✅ Docker Compose 2.21.0 (Multi-container applications)",
            "   ✅ Docker Buildx 0.11.2 (Extended build capabilities)",
            "",
            "☸️ Container Orchestration:",
            "   ✅ Kubernetes 1.28.2 (Container orchestration platform)",
            "   ✅ Minikube 1.32.0 (Local Kubernetes development)",
            "   ✅ Kind 0.20.0 (Kubernetes in Docker for testing)",
            "   ✅ K3s 1.28.2 (Lightweight Kubernetes distribution)",
            "   ✅ Helm 3.13.0 (Kubernetes package manager)",
            "",
            "🔧 Container Development Tools:",
            "   ✅ containerd 1.7.6 (Industry-standard container runtime)",
            "   ✅ runc 1.1.8 (CLI tool for spawning containers)",
            "   ✅ Buildah 1.31.0 (OCI container building)",
            "   ✅ Podman 4.7.0 (Daemonless container engine)",
            "",
            "📦 Container Registry Tools:",
            "   ✅ Harbor 2.9.0 (Enterprise container registry)",
            "   ✅ Docker Registry 2.8.2 (Simple registry server)",
            "",
            "🔒 Container Security Tools:",
            "   ✅ Trivy 0.46.0 (Vulnerability scanner)",
            "   ✅ Falco 0.36.2 (Runtime security monitoring)",
            "   ✅ Open Policy Agent 0.58.0 (Policy-based control)",
            "",
            "📊 Container Monitoring & Observability:",
            "   ✅ Prometheus 2.47.0 (Monitoring and alerting)",
            "   ✅ Grafana 10.2.0 (Analytics and monitoring)",
            "   ✅ Jaeger 1.49.0 (Distributed tracing)",
            "",
            "📚 Container Development Libraries:",
            "   ✅ docker-py 6.1.3 (Python Docker API client)",
            "   ✅ kubernetes 28.1.0 (Python Kubernetes API client)",
            "",
            "🖥️ Container Management Tools:",
            "   ✅ LazyDocker 0.22.0 (Simple Docker management)",
            "   ✅ Dive 0.12.0 (Docker image analysis)",
            "   ✅ Hadolint 2.12.0 (Dockerfile linter)",
            "   ✅ Portainer 2.19.0 (Container management UI)",
            "",
            "🚀 CI/CD Integration:",
            "   ✅ Tekton 0.50.0 (Cloud-native CI/CD framework)",
            "   ✅ ArgoCD 2.8.0 (GitOps continuous delivery)",
            "",
            "🚀 Quick Start Options:",
            "  1. Docker Development:",
            "     docker run hello-world",
            "     docker-compose up -d",
            "     lazydocker",
            "",
            "  2. Kubernetes Development:",
            "     minikube start",
            "     kubectl get nodes",
            "     helm create my-chart",
            "",
            "  3. Container Security:",
            "     trivy image nginx:latest",
            "     falco --version",
            "     opa eval --data policy.rego 'data.example.allow'",
            "",
            "  4. Monitoring Setup:",
            "     docker run -d -p 9090:9090 prom/prometheus",
            "     docker run -d -p 3000:3000 grafana/grafana",
            "     docker run -d -p 16686:16686 jaegertracing/all-in-one",
            "",
            "  5. Python Container Development:",
            "     python -c 'import docker; print(docker.from_env().version())'",
            "     python -c 'import kubernetes; print(kubernetes.client.VersionApi().get_code())'",
            "",
            "📋 Common Docker Commands:",
            "  • Build: docker build -t my-app .",
            "  • Run: docker run -p 3000:3000 my-app",
            "  • Compose: docker-compose up -d",
            "  • Images: docker images",
            "  • Containers: docker ps -a",
            "  • Logs: docker logs container-name",
            "  • Shell: docker exec -it container-name /bin/bash",
            "",
            "☸️ Common Kubernetes Commands:",
            "  • Context: kubectl config current-context",
            "  • Nodes: kubectl get nodes",
            "  • Pods: kubectl get pods",
            "  • Services: kubectl get services",
            "  • Deploy: kubectl apply -f deployment.yaml",
            "  • Logs: kubectl logs pod-name",
            "  • Shell: kubectl exec -it pod-name -- /bin/bash",
            "",
            "🔧 Advanced Features:",
            "  • Multi-architecture builds: docker buildx build --platform linux/amd64,linux/arm64",
            "  • Kubernetes development: kind create cluster --config kind-config.yaml",
            "  • Helm charts: helm install my-app ./chart --values values.yaml",
            "  • GitOps: argocd app create my-app --repo https://github.com/user/repo",
            "  • Security scanning: trivy k8s cluster",
            "  • Policy enforcement: opa test policies/",
            "",
            "📖 Resources:",
            "  • Docker Docs: https://docs.docker.com/",
            "  • Kubernetes Docs: https://kubernetes.io/docs/",
            "  • Helm Docs: https://helm.sh/docs/",
            "  • Prometheus Docs: https://prometheus.io/docs/",
            "  • Grafana Docs: https://grafana.com/docs/",
            "  • Tekton Docs: https://tekton.dev/docs/",
            "",
            "💡 Pro Tips:",
            "  • Use Docker Compose for local development",
            "  • Use Minikube or Kind for local Kubernetes testing",
            "  • Use Helm for package management in Kubernetes",
            "  • Use Trivy for container security scanning",
            "  • Use Prometheus + Grafana for monitoring",
            "  • Use ArgoCD for GitOps workflows",
            "  • Use Tekton for cloud-native CI/CD",
            "  • Use Portainer for container management UI",
            "",
            "🔗 Community:",
            "  • Docker Community: https://www.docker.com/community/",
            "  • Kubernetes Community: https://kubernetes.io/community/",
            "  • CNCF Community: https://www.cncf.io/community/",
            "  • Container Security: https://container-security.dev/",
            "",
            "📞 Support:",
            "  • Container-specific documentation and tutorials",
            "  • Kubernetes troubleshooting guides",
            "  • he2plus Community: https://discord.gg/he2plus"
        ]
