#/usr/bin/python3
#coding=utf-8

import sys
import os
import re

from copy import deepcopy as copy

from conll.conll import Token, Conll, Sent

from bs4 import BeautifulSoup

import nltk