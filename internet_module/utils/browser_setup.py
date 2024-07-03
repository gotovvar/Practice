from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
import os


def get_edge_driver():
    service = EdgeService(executable_path=os.path.join('../edgedriver_win64/msedgedriver.exe'))
    options = Options()
    options.use_chromium = True
    return webdriver.Edge(service=service, options=options)
