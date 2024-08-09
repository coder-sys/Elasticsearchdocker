# Define variables
PYTHON = python
PIP = pip
SCRIPT = elasticsearch_example.py
VENV_DIR = .venv
REQUIREMENTS = requirements.txt

# Default target
all: install run

# Create a virtual environment and install dependencies
setup:
	@echo "Setting up the virtual environment..."
	$(PYTHON) -m venv $(VENV_DIR)
	$(VENV_DIR)/bin/$(PIP) install --upgrade pip
	$(VENV_DIR)/bin/$(PIP) install -r $(REQUIREMENTS)

# Install dependencies
install: $(REQUIREMENTS)
	@echo "Installing dependencies..."
	$(VENV_DIR)/bin/$(PIP) install -r $(REQUIREMENTS)

# Run the Python script
run: setup
	@echo "Running the Python script..."
	$(VENV_DIR)/bin/$(PYTHON) $(SCRIPT)

# Clean up temporary files
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_DIR)

# Check if the virtual environment exists, if not, run setup
check:
	@if [ ! -d "$(VENV_DIR)" ]; then $(MAKE) setup; fi
