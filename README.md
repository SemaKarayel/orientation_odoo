# orientation_odoo

# Odoo 15 Installation Guide (macOS 15.6.1) --PyCharm

1. Directory Setup

    ```bash
   mkdir -p ~/odoo/odoo15/custom
    ```

2. Clone Odoo Source Code 

   Inside the Odoo15 directory run these commands
    ```bash
   git clone https://www.github.com/odoo/odoo --depth 1 --branch 15.0 --single-branch
    ```

3. Install HomeBrew

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
   Add HomeBrew to your PATH (for zsh users)

    ```bash
    echo >> ~/.zprofile
    echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/usr/local/bin/brew shellenv)"
    ```

4. Update & Upgrade HomeBrew and packages

   ```bash
   brew update
   brew upgrade
    ```

5. Install Pyenv and set Python 3.8.10

    ```bash
    brew install pyenv
    ```
   
    Set up pyenv in Zsh
    ```bash
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc
    ```
   
   Apply changes to current terminal session
   ```bash
   source ~/.zshrc
   ```

   Install required libraries for building Python
   ```bash
    brew install openssl readline sqlite3 xz tcl-tk@8 libb2 zstd zlib
   ```
   
   Install Python 3.8.10 via pyenv
   ```bash
   pyenv install 3.8.10
   ```

   Set Python 3.8.10 as the local version for the Odoo project
   ```bash
   cd ~/odoo/odoo15
   pyenv local 3.8.10
   ```

6.  OPTIONAL – Orientation Odoo Repo on GitHub 

   If you want, you can clone your project repository to track your Odoo.

   ```bash
   cd ~/odoo/odoo15/custom
   git clone git@github.com:<your-username>/orientation_odoo.git
   cd orientation_odoo    
   ```

7. Install PostgreSQL

   ```bash
   brew install postgresql
   ```
   
   Start PostgreSQL service
   ```bash
   brew services start postgresql
   ```
   
   Create a database user for Odoo
   ```bash
   createuser -s <your-username>
    ```
   
   Create a database for Odoo
   ```bash
   createdb odoodb
    ```
   
   Optional: Set a password for the Odoo database user
   ```bash
   psql -U <your-username> -d odoodb
   ALTER USER <your-username> WITH PASSWORD 'odoo';
   \q
   ```
   
8. Install Python requirements for Odoo

   ```bash
   pip3 install -r ~/odoo/odoo15/odoo/requirements.txt
   ```

9. Install wkhtmltopdf (for PDF reporting)

   Download and install the Cocoa Package

   ```bash
   curl -LO https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox-0.12.5-1.macos-cocoa.pkg
   ```
   
   Open the installer
   ```bash
   open wkhtmltox-0.12.5-1.macos-cocoa.pkg
   ```
   
10. Run Odoo for the first time (using your config)

   ```bash
   python3 odoo-bin -c ~/odoo/odoo15/custom/configs/odoo.conf -d odoodb --init=base
    ```
