# Building a Complete Web3 DApp

Learn how to build a full-featured decentralized application (DApp) using the Web3 Solidity profile.

## Prerequisites

```bash
# Install the Web3 Solidity development environment
he2plus install web3-solidity

# Verify installation
node --version    # Should show v18.x
npm --version     # Should show 10.x
npx hardhat --version
forge --version
```

## Project Overview

We'll build a **Decentralized Task Management DApp** with the following features:
- Create tasks with descriptions and deadlines
- Assign tasks to wallet addresses
- Mark tasks as complete
- View all tasks and filter by status
- Full Web3 integration with MetaMask

## Step 1: Initialize the Project

### Create Smart Contract Project

```bash
# Create project directory
mkdir task-manager-dapp
cd task-manager-dapp

# Initialize Hardhat project
npx hardhat init

# Select: Create a TypeScript project
# Install dependencies as prompted
```

### Project Structure

```
task-manager-dapp/
├── contracts/           # Smart contracts
├── scripts/            # Deployment scripts
├── test/               # Contract tests
├── frontend/           # React frontend (we'll create this)
├── hardhat.config.ts   # Hardhat configuration
└── package.json
```

## Step 2: Write the Smart Contract

Create `contracts/TaskManager.sol`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.22;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

/**
 * @title TaskManager
 * @dev Manage tasks on the blockchain
 */
contract TaskManager is Ownable, ReentrancyGuard {
    struct Task {
        uint256 id;
        string title;
        string description;
        address assignee;
        uint256 deadline;
        bool completed;
        uint256 createdAt;
    }
    
    uint256 private taskIdCounter;
    mapping(uint256 => Task) public tasks;
    mapping(address => uint256[]) public userTasks;
    
    event TaskCreated(
        uint256 indexed taskId,
        string title,
        address indexed assignee,
        uint256 deadline
    );
    
    event TaskCompleted(uint256 indexed taskId, address indexed completedBy);
    event TaskAssigned(uint256 indexed taskId, address indexed assignee);
    
    constructor() Ownable(msg.sender) {
        taskIdCounter = 0;
    }
    
    /**
     * @dev Create a new task
     * @param title Task title
     * @param description Task description
     * @param assignee Address to assign the task to
     * @param deadline Unix timestamp for deadline
     */
    function createTask(
        string memory title,
        string memory description,
        address assignee,
        uint256 deadline
    ) external returns (uint256) {
        require(bytes(title).length > 0, "Title cannot be empty");
        require(assignee != address(0), "Invalid assignee address");
        require(deadline > block.timestamp, "Deadline must be in the future");
        
        uint256 taskId = taskIdCounter++;
        
        tasks[taskId] = Task({
            id: taskId,
            title: title,
            description: description,
            assignee: assignee,
            deadline: deadline,
            completed: false,
            createdAt: block.timestamp
        });
        
        userTasks[assignee].push(taskId);
        
        emit TaskCreated(taskId, title, assignee, deadline);
        
        return taskId;
    }
    
    /**
     * @dev Complete a task
     * @param taskId ID of the task to complete
     */
    function completeTask(uint256 taskId) external nonReentrant {
        Task storage task = tasks[taskId];
        require(task.id == taskId, "Task does not exist");
        require(!task.completed, "Task already completed");
        require(
            msg.sender == task.assignee || msg.sender == owner(),
            "Only assignee or owner can complete task"
        );
        
        task.completed = true;
        
        emit TaskCompleted(taskId, msg.sender);
    }
    
    /**
     * @dev Reassign a task to a different address
     * @param taskId ID of the task
     * @param newAssignee New assignee address
     */
    function reassignTask(uint256 taskId, address newAssignee) external {
        Task storage task = tasks[taskId];
        require(task.id == taskId, "Task does not exist");
        require(!task.completed, "Cannot reassign completed task");
        require(
            msg.sender == owner() || msg.sender == task.assignee,
            "Not authorized"
        );
        require(newAssignee != address(0), "Invalid assignee");
        
        // Remove from old assignee's list
        _removeTaskFromUser(task.assignee, taskId);
        
        // Add to new assignee's list
        task.assignee = newAssignee;
        userTasks[newAssignee].push(taskId);
        
        emit TaskAssigned(taskId, newAssignee);
    }
    
    /**
     * @dev Get all tasks for a specific user
     * @param user Address of the user
     */
    function getUserTasks(address user) external view returns (Task[] memory) {
        uint256[] memory taskIds = userTasks[user];
        Task[] memory result = new Task[](taskIds.length);
        
        for (uint256 i = 0; i < taskIds.length; i++) {
            result[i] = tasks[taskIds[i]];
        }
        
        return result;
    }
    
    /**
     * @dev Get task by ID
     * @param taskId ID of the task
     */
    function getTask(uint256 taskId) external view returns (Task memory) {
        require(tasks[taskId].id == taskId, "Task does not exist");
        return tasks[taskId];
    }
    
    /**
     * @dev Get total number of tasks created
     */
    function getTotalTasks() external view returns (uint256) {
        return taskIdCounter;
    }
    
    /**
     * @dev Remove task from user's task list
     * @param user User address
     * @param taskId Task ID to remove
     */
    function _removeTaskFromUser(address user, uint256 taskId) private {
        uint256[] storage tasks = userTasks[user];
        for (uint256 i = 0; i < tasks.length; i++) {
            if (tasks[i] == taskId) {
                tasks[i] = tasks[tasks.length - 1];
                tasks.pop();
                break;
            }
        }
    }
}
```

### Install OpenZeppelin Contracts

```bash
npm install @openzeppelin/contracts
```

## Step 3: Write Tests

Create `test/TaskManager.test.ts`:

```typescript
import { expect } from "chai";
import { ethers } from "hardhat";
import { TaskManager } from "../typechain-types";
import { SignerWithAddress } from "@nomicfoundation/hardhat-ethers/signers";

describe("TaskManager", function () {
  let taskManager: TaskManager;
  let owner: SignerWithAddress;
  let user1: SignerWithAddress;
  let user2: SignerWithAddress;

  beforeEach(async function () {
    [owner, user1, user2] = await ethers.getSigners();
    
    const TaskManager = await ethers.getContractFactory("TaskManager");
    taskManager = await TaskManager.deploy();
    await taskManager.waitForDeployment();
  });

  describe("Task Creation", function () {
    it("Should create a task successfully", async function () {
      const title = "Complete project documentation";
      const description = "Write comprehensive docs";
      const deadline = Math.floor(Date.now() / 1000) + 86400; // 24 hours

      await expect(
        taskManager.createTask(title, description, user1.address, deadline)
      )
        .to.emit(taskManager, "TaskCreated")
        .withArgs(0, title, user1.address, deadline);

      const task = await taskManager.getTask(0);
      expect(task.title).to.equal(title);
      expect(task.assignee).to.equal(user1.address);
      expect(task.completed).to.be.false;
    });

    it("Should fail with empty title", async function () {
      const deadline = Math.floor(Date.now() / 1000) + 86400;

      await expect(
        taskManager.createTask("", "Description", user1.address, deadline)
      ).to.be.revertedWith("Title cannot be empty");
    });

    it("Should fail with past deadline", async function () {
      const pastDeadline = Math.floor(Date.now() / 1000) - 86400;

      await expect(
        taskManager.createTask("Title", "Desc", user1.address, pastDeadline)
      ).to.be.revertedWith("Deadline must be in the future");
    });
  });

  describe("Task Completion", function () {
    beforeEach(async function () {
      const deadline = Math.floor(Date.now() / 1000) + 86400;
      await taskManager.createTask(
        "Test Task",
        "Description",
        user1.address,
        deadline
      );
    });

    it("Should allow assignee to complete task", async function () {
      await expect(taskManager.connect(user1).completeTask(0))
        .to.emit(taskManager, "TaskCompleted")
        .withArgs(0, user1.address);

      const task = await taskManager.getTask(0);
      expect(task.completed).to.be.true;
    });

    it("Should not allow non-assignee to complete task", async function () {
      await expect(
        taskManager.connect(user2).completeTask(0)
      ).to.be.revertedWith("Only assignee or owner can complete task");
    });

    it("Should not allow completing already completed task", async function () {
      await taskManager.connect(user1).completeTask(0);
      
      await expect(
        taskManager.connect(user1).completeTask(0)
      ).to.be.revertedWith("Task already completed");
    });
  });

  describe("Task Reassignment", function () {
    beforeEach(async function () {
      const deadline = Math.floor(Date.now() / 1000) + 86400;
      await taskManager.createTask(
        "Test Task",
        "Description",
        user1.address,
        deadline
      );
    });

    it("Should allow owner to reassign task", async function () {
      await expect(taskManager.reassignTask(0, user2.address))
        .to.emit(taskManager, "TaskAssigned")
        .withArgs(0, user2.address);

      const task = await taskManager.getTask(0);
      expect(task.assignee).to.equal(user2.address);
    });

    it("Should allow assignee to reassign task", async function () {
      await expect(taskManager.connect(user1).reassignTask(0, user2.address))
        .to.emit(taskManager, "TaskAssigned")
        .withArgs(0, user2.address);
    });
  });

  describe("User Tasks", function () {
    it("Should return all tasks for a user", async function () {
      const deadline = Math.floor(Date.now() / 1000) + 86400;
      
      await taskManager.createTask("Task 1", "Desc 1", user1.address, deadline);
      await taskManager.createTask("Task 2", "Desc 2", user1.address, deadline);
      await taskManager.createTask("Task 3", "Desc 3", user2.address, deadline);

      const user1Tasks = await taskManager.getUserTasks(user1.address);
      expect(user1Tasks.length).to.equal(2);
      
      const user2Tasks = await taskManager.getUserTasks(user2.address);
      expect(user2Tasks.length).to.equal(1);
    });
  });
});
```

### Run Tests

```bash
npx hardhat test

# Run with gas reporting
REPORT_GAS=true npx hardhat test

# Run with coverage
npx hardhat coverage
```

## Step 4: Deploy Smart Contract

Create `scripts/deploy.ts`:

```typescript
import { ethers } from "hardhat";

async function main() {
  console.log("Deploying TaskManager contract...");

  const TaskManager = await ethers.getContractFactory("TaskManager");
  const taskManager = await TaskManager.deploy();

  await taskManager.waitForDeployment();

  const address = await taskManager.getAddress();
  console.log(`TaskManager deployed to: ${address}`);

  // Verify on Etherscan (optional)
  if (process.env.ETHERSCAN_API_KEY) {
    console.log("Waiting for block confirmations...");
    await taskManager.deploymentTransaction()?.wait(5);
    
    console.log("Verifying contract on Etherscan...");
    try {
      await run("verify:verify", {
        address: address,
        constructorArguments: [],
      });
      console.log("Contract verified!");
    } catch (error) {
      console.log("Verification failed:", error);
    }
  }
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });
```

### Deploy to Local Network

```bash
# Terminal 1: Start local blockchain
npx hardhat node

# Terminal 2: Deploy
npx hardhat run scripts/deploy.ts --network localhost
```

### Deploy to Testnet (Sepolia)

Update `hardhat.config.ts`:

```typescript
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import "dotenv/config";

const config: HardhatUserConfig = {
  solidity: "0.8.22",
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL || "",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY,
  },
};

export default config;
```

Create `.env`:

```bash
SEPOLIA_RPC_URL=https://eth-sepolia.g.alchemy.com/v2/YOUR_API_KEY
PRIVATE_KEY=your_private_key_here
ETHERSCAN_API_KEY=your_etherscan_api_key
```

Deploy:

```bash
npx hardhat run scripts/deploy.ts --network sepolia
```

## Step 5: Build the Frontend

### Create React App

```bash
npx create-next-app@latest frontend --typescript --tailwind --app
cd frontend
npm install ethers wagmi viem @rainbow-me/rainbowkit
```

### Configure RainbowKit

Create `frontend/src/app/providers.tsx`:

```typescript
'use client';

import '@rainbow-me/rainbowkit/styles.css';
import { getDefaultWallets, RainbowKitProvider } from '@rainbow-me/rainbowkit';
import { configureChains, createConfig, WagmiConfig } from 'wagmi';
import { sepolia, hardhat } from 'wagmi/chains';
import { publicProvider } from 'wagmi/providers/public';

const { chains, publicClient } = configureChains(
  [sepolia, hardhat],
  [publicProvider()]
);

const { connectors } = getDefaultWallets({
  appName: 'Task Manager DApp',
  projectId: 'YOUR_PROJECT_ID', // Get from WalletConnect
  chains,
});

const wagmiConfig = createConfig({
  autoConnect: true,
  connectors,
  publicClient,
});

export function Providers({ children }: { children: React.ReactNode }) {
  return (
    <WagmiConfig config={wagmiConfig}>
      <RainbowKitProvider chains={chains}>
        {children}
      </RainbowKitProvider>
    </WagmiConfig>
  );
}
```

### Create Contract Hook

Create `frontend/src/hooks/useTaskManager.ts`:

```typescript
import { useContractRead, useContractWrite, useWaitForTransaction } from 'wagmi';
import { parseEther } from 'viem';
import TaskManagerABI from '../abi/TaskManager.json';

const CONTRACT_ADDRESS = '0x...'; // Your deployed contract address

export function useTaskManager() {
  // Read functions
  const { data: totalTasks } = useContractRead({
    address: CONTRACT_ADDRESS,
    abi: TaskManagerABI,
    functionName: 'getTotalTasks',
  });

  const { data: createTaskData, write: createTask } = useContractWrite({
    address: CONTRACT_ADDRESS,
    abi: TaskManagerABI,
    functionName: 'createTask',
  });

  const { isLoading: isCreatingTask, isSuccess: taskCreated } =
    useWaitForTransaction({
      hash: createTaskData?.hash,
    });

  const { data: completeTaskData, write: completeTask } = useContractWrite({
    address: CONTRACT_ADDRESS,
    abi: TaskManagerABI,
    functionName: 'completeTask',
  });

  return {
    totalTasks,
    createTask,
    isCreatingTask,
    taskCreated,
    completeTask,
  };
}
```

### Create Task Components

Create `frontend/src/components/CreateTaskForm.tsx`:

```typescript
'use client';

import { useState } from 'react';
import { useTaskManager } from '../hooks/useTaskManager';

export default function CreateTaskForm() {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [assignee, setAssignee] = useState('');
  const [deadline, setDeadline] = useState('');

  const { createTask, isCreatingTask } = useTaskManager();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    const deadlineTimestamp = Math.floor(new Date(deadline).getTime() / 1000);
    
    createTask({
      args: [title, description, assignee, deadlineTimestamp],
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4 max-w-md mx-auto p-6 bg-white rounded-lg shadow">
      <h2 className="text-2xl font-bold">Create New Task</h2>
      
      <div>
        <label className="block text-sm font-medium mb-2">Title</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full px-4 py-2 border rounded"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full px-4 py-2 border rounded"
          rows={3}
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Assignee Address</label>
        <input
          type="text"
          value={assignee}
          onChange={(e) => setAssignee(e.target.value)}
          className="w-full px-4 py-2 border rounded font-mono text-sm"
          placeholder="0x..."
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">Deadline</label>
        <input
          type="datetime-local"
          value={deadline}
          onChange={(e) => setDeadline(e.target.value)}
          className="w-full px-4 py-2 border rounded"
          required
        />
      </div>

      <button
        type="submit"
        disabled={isCreatingTask}
        className="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700 disabled:opacity-50"
      >
        {isCreatingTask ? 'Creating...' : 'Create Task'}
      </button>
    </form>
  );
}
```

### Main Page

Update `frontend/src/app/page.tsx`:

```typescript
import { ConnectButton } from '@rainbow-me/rainbowkit';
import CreateTaskForm from '../components/CreateTaskForm';
import TaskList from '../components/TaskList';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold">Task Manager DApp</h1>
          <ConnectButton />
        </div>
      </nav>

      <div className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid md:grid-cols-2 gap-8">
          <div>
            <CreateTaskForm />
          </div>
          <div>
            <TaskList />
          </div>
        </div>
      </div>
    </main>
  );
}
```

## Step 6: Run the DApp

```bash
# Start frontend
cd frontend
npm run dev
```

Visit `http://localhost:3000`

## Key Features Implemented

✅ **Smart Contract**:
- Create tasks with title, description, assignee, and deadline
- Complete tasks with access control
- Reassign tasks
- Query tasks by user
- Event emission for all actions

✅ **Frontend**:
- MetaMask wallet connection
- Create new tasks
- View task list
- Complete tasks
- Real-time updates

✅ **Testing**:
- Comprehensive unit tests
- Gas reporting
- Code coverage

✅ **Deployment**:
- Local network deployment
- Testnet deployment
- Contract verification

## Next Steps

1. **Add More Features**:
   - Task comments
   - Task rewards
   - Task categories
   - Search and filter

2. **Enhance Security**:
   - Add role-based access control
   - Implement pausable pattern
   - Add time locks

3. **Improve UI/UX**:
   - Add loading states
   - Better error handling
   - Task notifications
   - Mobile responsive design

4. **Deploy to Production**:
   - Deploy to Ethereum mainnet
   - Set up subgraph for indexing
   - Implement IPFS for file storage
   - Add monitoring and analytics

## Resources

- **Smart Contract**: [OpenZeppelin Documentation](https://docs.openzeppelin.com)
- **Frontend**: [RainbowKit Docs](https://www.rainbowkit.com/docs)
- **Testing**: [Hardhat Testing Guide](https://hardhat.org/tutorial/testing-contracts)
- **Deployment**: [Hardhat Deploy Guide](https://hardhat.org/tutorial/deploying-to-a-live-network)

---

**Congratulations! You've built a complete Web3 DApp! 🎉**
