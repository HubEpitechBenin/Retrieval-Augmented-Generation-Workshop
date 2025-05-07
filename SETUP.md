# Setup for RAG Workshop

- [Setup for RAG Workshop](#setup-for-rag-workshop)
  - [Install](#install)
    - [Python](#python)
      - [Windows](#windows)
      - [macOS](#macos)
      - [Linux](#linux)
    - [VS Code](#vs-code)
      - [Windows](#windows-1)
      - [macOS](#macos-1)
      - [Linux](#linux-1)
    - [Python Extensions for VS Code](#python-extensions-for-vs-code)
    - [UV Package Manager](#uv-package-manager)
  - [Environment Setup](#environment-setup)
    - [Setting Up API Keys](#setting-up-api-keys)
  - [Troubleshooting](#troubleshooting)

## Install

You will need the following tools to participate in this workshop:
1. Python 3.8 or higher
2. VS Code (or another IDE of your choice)
3. UV package manager (for dependency management)

### Python

#### Windows

1. Download the Python installer from [python.org](https://www.python.org/downloads/)
2. Run the installer, checking "Add Python to PATH"
3. Verify installation by opening Command Prompt and typing:
   ```shell
   python --version
   ```

#### macOS

1. Using Homebrew (recommended):
   ```shell
   brew install python
   ```
2. Or download from [python.org](https://www.python.org/downloads/)
3. Verify installation:
   ```shell
   python3 --version
   ```

#### Linux

Most Linux distributions come with Python pre-installed. If not:

```shell
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch Linux
sudo pacman -S python python-pip
```

Verify installation:
```shell
python3 --version
```

### VS Code

#### Windows

1. Download the VS Code installer from [code.visualstudio.com](https://code.visualstudio.com/)
2. Run the installer, following the installation wizard
3. Launch VS Code after installation

#### macOS

1. Download VS Code from [code.visualstudio.com](https://code.visualstudio.com/)
2. Open the downloaded `.zip` file
3. Drag VS Code.app to the Applications folder
4. Launch from Applications folder or Spotlight search (Cmd+Space)

#### Linux

```shell
# Ubuntu/Debian
sudo apt update
sudo apt install software-properties-common apt-transport-https wget
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"
sudo apt update
sudo apt install code

# Fedora
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
sudo dnf update
sudo dnf install code

# Arch Linux
sudo pacman -S visual-studio-code-bin
```

### Python Extensions for VS Code

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X or Cmd+Shift+X on macOS)
3. Search for and install the "Python" extension by Microsoft
4. Also install "Jupyter" extension for notebook support

### UV Package Manager

UV is a fast, reliable Python package installer and resolver. Install it using:

```shell
# Windows (PowerShell)
curl -sSf https://astral.sh/uv/install.sh | powershell

# macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify installation:
```shell
uv --version
```

## Environment Setup

Clone the repository and install dependencies:

```shell
# Clone the repository
git clone https://github.com/HubEpitechBenin/Retrieval-Augmented-Generation-Workshop.git
cd Retrieval-Augmented-Generation-Workshop

# Create and activate a virtual environment
uv venv

# On Windows
.venv\Scripts\activate

# On macOS/Linux
source .venv/bin/activate

# Install dependencies with UV
uv pip install -r requirements.txt
```

### Setting Up API Keys

1. Create a `.env` file in the root directory of the project
2. Add your API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_API_BASE=https://api.openai.com/v1  # Default OpenAI endpoint
   MODEL_NAME=gpt-3.5-turbo  # or gpt-4
   ```

## Troubleshooting

If you encounter issues:

1. **Python not found in PATH**: Restart your terminal after installation or manually add Python to your PATH
2. **Permission errors on Linux/macOS**: Use `sudo` for installation commands or check file permissions
3. **Package installation failures**: Try using traditional pip if UV encounters issues:
   ```
   pip install -r requirements.txt
   ```
4. **API connection issues**: Verify your API keys and network connection
