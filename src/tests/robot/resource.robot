*** Settings ***
Library  SeleniumLibrary
Library  OperatingSystem


*** Variables ***
${BROWSER}  chrome
${DELAY}  0.2 seconds
# Paste the correct URL here:
${URL}  http://localhost:8888/?token=...
${HYPO}  /html/body/div[4]/div/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[3]/div/div[2]/input
${NULL}  /html/body/div[4]/div/div/div[1]/div[1]/div[1]/div[2]/div[2]/div/div[3]/div/div[4]/input


*** Keywords ***
Open Notebook
    Open Browser  browser=${BROWSER}
    Maximize Browser Window
    Set Selenium Speed  ${DELAY}
    Go To  ${URL}
    Click Link  src
    Click Link  tests
    Click Link  test_hypothesis.ipynb
    Switch Window  locator=NEW
    Wait Until Page Does Not Contain  Clusters  timeout=5
    
Run Notebook
    Click Link  Cell
    Click Link  Run All

Input Hypothesis
    Input Text  xpath:${HYPO}  x < 0

Input Null Hypothesis
    Input Text  xpath:${NULL}  x = 0

Save Hypotheses
    Input Hypothesis
    Input Null Hypothesis
    Click Button  Save  