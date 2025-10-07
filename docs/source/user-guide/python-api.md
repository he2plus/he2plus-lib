# Python API

Use he2plus programmatically in your Python code.

## Basic Usage

```python
import he2plus
from he2plus.core import SystemProfiler
from he2plus.profiles import ProfileRegistry

# Get system information
profiler = SystemProfiler()
system_info = profiler.profile()

# Load profiles
registry = ProfileRegistry()
profile = registry.get("web3-solidity")

# Get installation plan
plan = registry.get_installation_plan(["web3-solidity"])
```

See source code for complete API reference.
