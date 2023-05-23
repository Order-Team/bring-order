*** Settings ***
Resource  resource.robot
Suite Setup  Open Notebook
Suite Teardown  Close Browser


*** Variables ***
${OUTPUT}  /html/body/div[4]/div/div/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[3]/pre


*** Test Cases ***
Notebook Should Be Open
    Title Should Be  test_hypothesis - Jupyter Notebook

Running Notebook Should Show Text Boxes
    Run Notebook
    Wait Until Page Contains Element  class:widget-input
    Page Should Contain Element  class:widget-input

Saving Hypotheses Should Print Them
    Save Hypotheses
    Wait Until Page Does Not Contain Element  class:widget-input
    Page Should Contain  Hypothesis: x < 0
    Page Should Contain  Null hypothesis: x = 0

Saving Empty Hypotheses Prints Error Message
    Run Notebook
    Wait Until Page Contains Element  class:widget-input
    Click Button  Save
    Wait Until Page Contains Element  xpath:${OUTPUT}  timeout=5
    Element Should Contain  xpath:${OUTPUT}  Hypothesis and Null hypothesis missing

Saving Empty Hypothesis Prints Correct Error Message
    Run Notebook
    Wait Until Page Contains Element  class:widget-input
    Input Null Hypothesis
    Click Button  Save
    Wait Until Page Contains Element  xpath:${OUTPUT}  timeout=5
    Element Should Contain  xpath:${OUTPUT}  Hypothesis missing

Saving Empty Null Hypothesis Prints Correct Error Message
    Run Notebook
    Wait Until Page Contains Element  class:widget-input
    Input Hypothesis
    Click Button  Save
    Wait Until Page Contains Element  xpath:${OUTPUT}  timeout=5
    Element Should Contain  xpath:${OUTPUT}  Null hypothesis missing


