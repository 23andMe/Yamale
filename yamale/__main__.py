#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
    Validate yaml files and check them against their schemas. Designed to be used outside of Vagrant.

    Just install Yamale:
        pip install yamale
    And run with:
        yamale
          OR
        python -m yamale
"""
from .command_line import main

main()
