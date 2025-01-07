<p align="center">
<img src=Figure1.png width=100% height=100%>
</p>

# SM_Framework
CESMII Project: Interface for bi-directional communication between FANUC and desktop PC. This project aims for building an intuitive interfance for users with limited experience of customized robot programming language (e.g., KAREL) to quickly plan, analyze, and verify robotic automation such as machine tending and palletization. 

**This repository only contains Robot - PC Interface of the SM Framework. To fully build the framework, users require to download [IK-MPC](https://github.com/purduelamm/IK-MPC) AND DT-Interface.**

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Repository Structure](#repository-structure)
- [Download Process](#download-process)
- [How to Run](#how-to-run)
- [ToDo Lists](#todo-lists)

## Repository Structure

    ├── faroc        # KAREL - Python Communication
    ├── faroc_main.py              
    ├── importls.py
    ├── opc_server.py     
    └── uploader.py     

## Download Process

> [!NOTE]
This repository has been tested on [Windows 11](https://www.microsoft.com/en-us/software-download/windows11) and [Ubuntu 22.04](https://releases.ubuntu.com/jammy/).

    git https://github.com/purduelamm/SM_Framework.git
    cd SM_Framework/
    pip3 install -r requirements.txt

> [!WARNING]
> SM_Framework also requires [FaRoC](https://codeberg.org/hojak/FaRoC). For more information about how to setup the software and physical robot, please visit [here](https://codeberg.org/hojak/FaRoC).

## How to Run

`importls.py` uploads a .ls file containing series of commands that a robot should execute to controller using FTP protocol. Then, `faroc_main.py` should be run
to actually set values of the waypoints in positions registers, which will be called by each command line in .ls file. 

> [!NOTE]
Waypoints that a robot follows can be created by [IK-MPC](https://github.com/purduelamm/IK-MPC) or other motion planning frameworks.

    python3 importls.py 
    python3 faroc_main.py

## ToDo Lists

| **Documentation** | ![Progress](https://geps.dev/progress/60) |
| --- | --- |
