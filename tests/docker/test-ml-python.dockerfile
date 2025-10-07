# Test Docker image for ML Python Profile
FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3.11-venv \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy he2plus library
WORKDIR /app
COPY . /app

# Install he2plus
RUN pip3 install -e .

# Test script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
echo "================================="\n\
echo "Testing ML Python Profile"\n\
echo "================================="\n\
\n\
echo "\n1. Checking he2plus installation..."\n\
he2plus --version || exit 1\n\
\n\
echo "\n2. Getting profile info..."\n\
he2plus info ml-python || exit 1\n\
\n\
echo "\n3. Checking Python version..."\n\
python3 --version || exit 1\n\
\n\
echo "\n4. Creating virtual environment..."\n\
cd /tmp\n\
python3 -m venv ml-env || exit 1\n\
source ml-env/bin/activate || exit 1\n\
\n\
echo "\n5. Installing core ML libraries (this may take a while)..."\n\
pip install --no-cache-dir numpy pandas matplotlib seaborn scikit-learn || exit 1\n\
\n\
echo "\n6. Installing TensorFlow (CPU version for testing)..."\n\
pip install --no-cache-dir tensorflow-cpu || exit 1\n\
\n\
echo "\n7. Installing PyTorch (CPU version for testing)..."\n\
pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu || exit 1\n\
\n\
echo "\n8. Testing imports..."\n\
python3 -c "import numpy; print(f\"NumPy version: {numpy.__version__}\")" || exit 1\n\
python3 -c "import pandas; print(f\"Pandas version: {pandas.__version__}\")" || exit 1\n\
python3 -c "import sklearn; print(f\"scikit-learn version: {sklearn.__version__}\")" || exit 1\n\
python3 -c "import tensorflow as tf; print(f\"TensorFlow version: {tf.__version__}\")" || exit 1\n\
python3 -c "import torch; print(f\"PyTorch version: {torch.__version__}\")" || exit 1\n\
\n\
echo "\n9. Creating simple ML test..."\n\
python3 << EOF\n\
import numpy as np\n\
from sklearn.datasets import make_classification\n\
from sklearn.model_selection import train_test_split\n\
from sklearn.ensemble import RandomForestClassifier\n\
from sklearn.metrics import accuracy_score\n\
\n\
# Generate sample data\n\
X, y = make_classification(n_samples=1000, n_features=20, random_state=42)\n\
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)\n\
\n\
# Train model\n\
model = RandomForestClassifier(n_estimators=100, random_state=42)\n\
model.fit(X_train, y_train)\n\
\n\
# Evaluate\n\
y_pred = model.predict(X_test)\n\
accuracy = accuracy_score(y_test, y_pred)\n\
print(f\"Model accuracy: {accuracy:.2f}\")\n\
assert accuracy > 0.7, \"Model accuracy too low\"\n\
print(\"✓ ML test passed\")\n\
EOF\n\
\n\
echo "\n10. Testing PyTorch..."\n\
python3 << EOF\n\
import torch\n\
import torch.nn as nn\n\
\n\
# Simple neural network\n\
model = nn.Sequential(\n\
    nn.Linear(10, 20),\n\
    nn.ReLU(),\n\
    nn.Linear(20, 1)\n\
)\n\
\n\
# Test forward pass\n\
x = torch.randn(32, 10)\n\
y = model(x)\n\
assert y.shape == (32, 1), \"Output shape mismatch\"\n\
print(\"✓ PyTorch test passed\")\n\
EOF\n\
\n\
echo "\n✅ All ML Python profile tests passed!"\n\
' > /test.sh

RUN chmod +x /test.sh

CMD ["/test.sh"]

