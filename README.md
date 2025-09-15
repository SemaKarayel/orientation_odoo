# orientation_odoo

# Odoo 15 Installation Guide (macOS 15.6.1)

1. Directory Setup

    ```zsh
   mkdir -p ~/odoo/odoo15/custom
    ```

2. Clone Odoo Source Code

    ```zsh
    cd ~/odoo/odoo15/
    git clone https://www.github.com/odoo/odoo --depth 1 --branch 15.0 --single-branch
    ```

3. Install [HomeBrew](https://brew.sh/)

    ```zsh
    /bin/zsh -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```
   
   Add HomeBrew to your PATH (for zsh users)
    ```zsh
    echo 'eval "$(/usr/local/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/usr/local/bin/brew shellenv)"
    brew update
    brew upgrade
    ```

4. (Optional) Install [Pyenv](https://github.com/pyenv/pyenv) and set Python 3.8.10

    Pyenv is a Python version manager that lets you install and switch between multiple Python versions easily.  
    This ensures Odoo runs with the exact required version (3.8.10), regardless of your system default

    ```zsh
    brew install pyenv
   
    # Set up pyenv in Zsh
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
    echo '[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
    echo 'eval "$(pyenv init - zsh)"' >> ~/.zshrc
 
    # Apply changes to current terminal session
    source ~/.zshrc
   
    # Install required libraries and Python versions
    brew install openssl readline sqlite3 xz tcl-tk@8 libb2 zstd zlib

    # Install Python 3.8.10 via pyenv
    pyenv install 3.8.10

    # Set Python 3.8.10 as the local version for the Odoo project
    cd ~/odoo/odoo15
    pyenv local 3.8.10
    ```

5. (Optional) – Your Odoo Addons Repo on GitHub

   > If you want, you can clone your project repository to track your Odoo.  
   > Copy your **addons path**: `~/odoo/odoo15/odoo/addons`  
   > And update your **addons_path** in the `odoo.conf` file.

   ```zsh
   cd ~/odoo/odoo15/custom
   git clone git@github.com:<your-username>/<your-repo>.git
   ```
   
   >    **Note:** Anything inside `< >` (angle brackets) is a placeholder.  
   >    Replace it with your own values.
   
6. Install PostgreSQL

    ```zsh
    brew install postgresql
   
    #Start PostgreSQL service
    brew services start postgresql
   
    # Create a database user for Odoo
    createuser -s <your-db-username>
   
    # Create a database for Odoo (This will be use 'db_user' in odoo.conf)
    createdb <your-db-name>
   
    # Optional: Set a password for the Odoo database user
    psql -U <your-db-username> -d <your-db-name>
    ALTER USER <your-db-username> WITH PASSWORD '<your-db-password>';
    \q
   ```

7. Create a virtual environment and Install Python requirements for Odoo

   ```zsh
   cd ~/odoo
   python3 -m venv <your-venv-name>
   pip3 install -r ~/odoo/odoo15/odoo/requirements.txt
   ```

8. Install wkhtmltopdf (for PDF reporting)

    ```zsh
    # Download and install the Cocoa Package
    curl -LO https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/0.12.5/wkhtmltox-0.12.5-1.macos-cocoa.pkg
   
    # Open the installer
   open wkhtmltox-0.12.5-1.macos-cocoa.pkg
   ```
   
9. Generate Odoo Configuration File

    Run the following command to generate your odoo.conf with default settings:

    ```zsh
    python3 ~/odoo15/odoo/odoo-bin --save --config ~/odoo/odoo15/custom/configs/odoo.conf --limit-memory-hard 0 -s --stop-after-init 
    ```
   
    This will create a configuration file in the path specified.
After the file is created, you can customize the following variables to match your setup:

    ```
    db_name     : <your-db-name>
    db_user     : <your-db-username>
    db_password : <your-db-password>
    db_port     : <your-db-port>
    addons_path : ~/odoo/odoo15/odoo/odoo/addons,~/odoo/odoo15/odoo/addons,~/odoo/odoo15/custom/configs/odoo.conf
    logfile     : ~/odoo/odoo15/odoo.log
    ```
10. Run Odoo for the first time (using your config)

    ```zsh
    python3 odoo-bin -c ~/odoo/odoo15/custom/configs/odoo.conf -d odoodb --init=base
    ```

## Run Odoo
Open your browser and go to:
http://localhost:8069
If the interface loads, your Odoo 15 setup is complete!
---

After you have set up everything, you can start Odoo by running the following command in your terminal:
```zsh
  python3 odoo-bin -c ~/odoo/odoo15/custom/configs/odoo.conf
```
