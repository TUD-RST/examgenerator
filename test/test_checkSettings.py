import pytest
import os
import json
from addict import Dict

from exam_generator import funcs
from exam_generator import customExceptions


def test_check_settings_working():
    """
    Expects no Errors from valid json.
    """
    file_name = "test_working.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    

    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)

    assert funcs.check_settings(settings, file_name) == None

def test_check_settings_groupPairs_1():
    """
    Expects a SettingsError: group_pair not int
    """
    file_name = "test_group_pairs_1.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)

def test_check_settings_groupPairs_2():
    """
    Expects a SettingsError: group_pair below one
    """
    file_name = "test_group_pairs_2.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)

def test_check_settings_title():
    """
    Expects a SettingsError: title not str
    """
    file_name = "test_title.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)

def test_check_settings_variantName():
    """
    Expects a SettingsError: variant name not str
    """
    file_name = "test_variant_name.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)

def test_check_settings_pagesPerSheetTest_1():
    """
    Expects a SettingsError: pages_per_sheet_test not int
    """
    file_name = "test_pages_per_sheet_test_1.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)

def test_check_settings_pagesPerSheetTest_2():
    """
    Expects a SettingsError: pages_per_sheet_test not 2 or 4
    """
    file_name = "test_pages_per_sheet_test_2.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)


def test_check_settings_pagesPerSheetSolution_1():
    """
    Expects a SettingsError: pages_per_sheet_solution not int
    """
    file_name = "test_pages_per_sheet_solution_1.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)

def test_check_settings_pagesPerSheetSolution_2():
    """
    Expects a SettingsError: pages_per_sheet_solution not 2 or 4
    """
    file_name = "test_pages_per_sheet_solution_2.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)

def test_sumoProblemCopies():
    """
    Expects a SettingsError: sumo_problem_copies is not int
    """
    file_name = "test_sumo_problem_copies.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)

def test_sumoSolutionCopies():
    """
    Expects a SettingsError: sumo_solution_copies is not int
    """
    file_name = "test_sumo_solution_copies.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)


def test_amountOfCopies():
    """
    Expects a SettingsError: number of copies below one
    """
    file_name = "test_copies_amount.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)

def test_generateSinglePDFs():
    """
    Expects a SettingsError: generate_single_pdfs not bool
    """
    file_name = "test_generate_single_pdfs.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)

def test_generateSumoPDF():
    """
    Expects a SettingsError: generate_sumo_pdf not bool
    """
    file_name = "test_generate_sumo_pdf.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)

def test_deleteTempData():
    """
    Expects a SettingsError: delete_temp_data not bool
    """
    file_name = "test_delete_temp_data.json"
    path_settings = os.path.join(os.getcwd(), "test_directories", "checkSettings", file_name)
    
    with open(path_settings, "r") as json_datei:
        settings = json.load(json_datei)
    
    settings = Dict(settings)
    with pytest.raises(customExceptions.SettingsError):
        funcs.check_settings(settings, file_name)


