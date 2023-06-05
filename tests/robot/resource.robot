*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem


*** Variables ***
${BROWSER}  chrome
${DELAY}  0.2 seconds
# Paste the correct URL here:
${URL}  http://localhost:8888/?token=...
${CLEAR_OUTPUT}  //*[@id="clear_all_output"]/a


*** Keywords ***
Open Test Notebook
    Open Browser  browser=${BROWSER}
    Maximize Browser Window
    Set Selenium Speed  ${DELAY}
    Go To  ${URL}
    Click Link  test_file.ipynb
    Switch Window  locator=NEW
    Wait Until Page Does Not Contain  Clusters  timeout=5
    
Run Notebook
    Click Link  Cell
    Click Link  Run All

Clear Notebook And Close Browser
    [Arguments]  ${cell_count}    # The number of cells to be cut (all cells - 1)
    Click Link  Cell
    Click Link  All Output
    Click Link  xpath:${CLEAR_OUTPUT}
    FOR  ${index}  IN RANGE  1  ${cell_count}
        Click Button  title:cut selected cells
    END
    Close Browser

Import And Call BringOrder
    Wait Until Element Is Enabled  class:CodeMirror-line
    Input Text  class:CodeMirror-line  from src.bringorder import BringOrder; BringOrder(0)
    Run Notebook
