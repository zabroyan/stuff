Installation guide
========================

Requirements
-----------------------

**Python**

Python 3.7.* is required because of some features and better performance


**External packages requirement**


* ``PyQt5`` - Graphical interface
* ``click`` - Console interface
* ``antlr4-python3-runtime`` - Knowledge base language parser
* ``multi_key_dict`` - Package for multi key dictionary support


Framework installation
-------------------------


School computers
~~~~~~~~~~~~~~~~~~~~

On the school computers you should already have Python 3.7 installed. Use system Python 3.7 with virtual
environment.

 #. Clone framework to you directory

    .. code-block:: bash

        cd <your_directory>
        # From GitLab for FIT CTU Prague
        git clone git@gitlab.fit.cvut.cz:hajkokla/orodaelturrim.git
        # or from GitHub for others
        git clone git@github.com:Wilson194/OrodaelTurrim.git

 #. Create virtual environment for framework and install all dependencies

    .. code-block:: bash

        cd zna_framework_python             # Change directory to framework
        python3.7 -m venv __venv__          # Create virtual environment
        . __venv__/bin/activate             # Activate virtual environment
        pip install -r requirements.txt     # Install all requirements

 #. Run framework (you need tu run framework from console where you activate virtual environment)

    .. code-block:: bash

        python OrodaelTurrim

Windows
~~~~~~~~~

For the windows user I recommend to use Anaconda_ distribution. You will get whole Python installation with integration
to the system and also virtual environments support with few steps in GUI installation. Also if you are using
PyCharm, in the new version (2019) PyCharm support Anaconda distribution, so some features are implemented directly
to IDE.

.. warning::

   If you have some older Anaconda installation on your system, it is recommended to uninstall whole distribution
   and install new one with Python 3.7. If you only update the distribution, there could be some problems
   with PyQt dependencies.


.. _Anaconda: https://www.anaconda.com/distribution/


Ubuntu 18
~~~~~~~~~~~~~~~~

On Ubuntu you have 2 possibilities to run Python 3.7. You can use system Python interpreter or Anaconda.

**System Python**

 #. Install Python 3.7

    .. code-block:: bash

        sudo apt update                                 # Update apt repositories
        sudo apt install software-properties-common     # Install program for apt adding
        sudo add-apt-repository ppa:deadsnakes/ppa      # Add Python apt repository
        sudo apt install python3.7                      # Install Python 3.7
        sudo apt install python-virtualenv              # Install virtual environments support
        sudo apt install python3.7-venv                 # Install require packages for Python 3.7

 #. At this point, Python 3.7 is installed on your Ubuntu system and ready to be used.
    You can verify it by typing

    .. code-block:: bash

        python3.7 --version

 #. Clone framework from the GitLab or GitHub

    .. code-block:: bash

        cd <your_directory>
        # From GitLab
        git clone https://gitlab.fit.cvut.cz/bi-zns_pracovni/zna_framework_python
        # or from GitHub
        git clone git@github.com:Wilson194/OrodaelTurrim.git

 #. Create virtual environment for framework and activate

    .. code-block:: bash

        cd zna_framework_python             # Change directory to framework
        python3.7 -m venv __venv__          # Create virtual environment
        . __venv__/bin/activate             # Activate virtual environment
        pip install -r requirements.txt     # Install all requirements

 #. Run framework

    .. code-block:: bash

        python OrodaelTurrim                # Run Framework


**Anaconda**

 #. Download Anaconda from the source page https://www.anaconda.com/distribution/

 #. Add executable permissions and run installer from you console. You can left all options default, but it's
    better to disable auto activate conda. It is better to add conda bin folder to PATH.

    .. code-block:: bash

        cd <Downloaded_directory>
        chmod +x <Downloaded_file>
        ./<Downloaded_file>

 #. Edit ``.bashrc`` file

    .. code-block:: bash

        export PATH="</path_to_installation>/bin:$PATH"

 #. Now you have conda bin folder in path. You should have Python 3.7. You can verify that with

    .. code-block:: bash

        python --version

 #. Clone framework from the GitLab or GitHub

    .. code-block:: bash

        cd <your_directory>
        # From GitLab
        git clone https://gitlab.fit.cvut.cz/bi-zns_pracovni/zna_framework_python
        # or from GitHub
        git clone git@github.com:Wilson194/OrodaelTurrim.git

 #. Install dependencies

    .. code-block:: bash

        cd <cloned_repository>
        pip install -r requirements.txt

 #. Run framework

    .. code-block:: bash

        python OrodaelTurrim

Linux Mint
~~~~~~~~~~~~~~~

Python 3.7 is not added to apt yet. You need to install Python 3.7 from other original source. Don't worry,
it is so hard.

 #. Install Python 3.7

    .. code-block:: bash

        sudo apt install build-essential checkinstall
        sudo apt install libreadline-gplv2-dev libncursesw5-dev libssl-dev libffi-dev
        sudo apt install libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev

        cd /usr/src
        sudo wget https://www.python.org/ftp/python/3.7.3/Python-3.7.3.tgz   # Download Python

        sudo tar xzf Python-3.7.3.tgz                                        # Extract python source

        cd Python-3.7.3
        sudo ./configure --enable-optimizations
        sudo make altinstall  # Install python under python3.7 (don't replace old python version)

        sudo apt install python-virtualenv                                  # Install virtual environment support

 #. Clone framework from the GitLab or GitHub

    .. code-block:: bash

        cd <your_directory>
        # From GitLab
        git clone https://gitlab.fit.cvut.cz/bi-zns_pracovni/zna_framework_python
        # or from GitHub
        git clone git@github.com:Wilson194/OrodaelTurrim.git

 #. Create virtual environment for framework and activate

    .. code-block:: bash

        cd zna_framework_python             # Change directory to framework
        python3.7 -m venv __venv__          # Create virtual environment
        . __venv__/bin/activate             # Activate virtual environment
        pip install -r requirements.txt     # Install all requirements

 #. Run framework

    .. code-block:: bash

        python OrodaelTurrim                # Run Framework

Fedora
~~~~~~~~~~~~~~~~~~~

 #. Install Python 3.7

    .. code-block:: bash

        sudo dnf install python37

  #. Clone framework from the GitLab or GitHub

    .. code-block:: bash

        cd <your_directory>
        # From GitLab
        git clone https://gitlab.fit.cvut.cz/bi-zns_pracovni/zna_framework_python
        # or from GitHub
        git clone git@github.com:Wilson194/OrodaelTurrim.git

 #. Create virtual environment for framework and activate

    .. code-block:: bash

        cd zna_framework_python             # Change directory to framework
        python3.7 -m venv __venv__          # Create virtual environment
        . __venv__/bin/activate             # Activate virtual environment
        pip install -r requirements.txt     # Install all requirements

 #. Run framework

    .. code-block:: bash

        python OrodaelTurrim                # Run Framework


Documentation build
-----------------------

You can build local documentation from source files.

.. code-block:: bash

   cd docs
   python3.7 -m pip install -r requirements.txt

   make html   # For windows make.bat html

Those commands will create ``Index.html`` file in ``docs/_build`` folder. This file is index page of the documentation.

