*** Settings ***
Resource  resource.robot
Suite Setup  Open Test Notebook
Suite Teardown  Clear Notebook And Close Browser  4    # The number of cells - 1


*** Variables ***
${HYPO}  /html/body/div[4]/div/div/div[1]/div[1]/div[4]/div[2]/div[2]/div[11]/div[3]/input
${DATA}  /html/body/div[4]/div/div/div[1]/div[1]/div[1]/div[2]/div[3]/p
${LIMIT}   /html/body/div[4]/div/div/div[1]/div[1]/div[3]/div[2]/div[2]/div[8]/div[3]/div/div[3]/input
${NULL}  /html/body/div[4]/div/div/div[1]/div[1]/div[4]/div[2]/div[2]/div[11]/div[3]/input
${NEW_CELL}  //*[@id="notebook-container"]/div[2]/div[1]/div[2]/div[2]
${NEW_INPUT}  //*[@id="notebook-container"]/div[2]/div[1]/div[2]
${NEW_OUTPUT}  //*[@id="notebook-container"]/div[2]/div[2]/div[2]/div/div[3]
${NEW_OUTPUT2}  //*[@id="notebook-container"]/div[2]/div[2]/div[2]/div[2]/div[3]
${HYPO2}  /html/body/div[4]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div[3]/div/div[4]/input
${NULL2}  /html/body/div[4]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[3]/div[3]/div/div[6]/input
${CELL_COUNT_INPUT}  /html/body/div[4]/div/div/div[1]/div[1]/div[2]/div[2]/div[2]/div[4]/div[3]/div/div[2]/div[2]/input
${NEW_CELL2}  //*[@id="notebook-container"]/div[3]
${NEW_CELL3}  //*[@id="notebook-container"]/div[4]


*** Test Cases ***
Notebook Should Be Open
    Wait Until Page Contains Element  id:kernel_indicator  timeout=5
    Title Should Be  test_file - Jupyter Notebook

Calling BringOrder Should Succeed After Import
    Run Notebook
    Page Should Contain  Prepare your data

User Is Prompted to Upload Their Data
    Click Button  Prepare your data
    Wait Until Page Contains  Data preparation
    Click Button  Run cells
    Page Should Contain  Data limitations
    
User is Required To Enter Data Limitations
    Input Text  xpath:${LIMIT}  x = 0
    Click Button  Start Analysis
    Page Should Contain  Data limitations cannot be empty
    
User Can Choose Between Inductive And Deductive Analysis
    Input Text  xpath:${LIMIT}  x = "Limitations"	
    Click Button  Start Analysis
    Page Should Contain  Deductive 
    Page Should Contain  Inductive   
 
Saving Empty Hypothesis Shows Error Message
    Click Button  Deductive
    Input Text  xpath:${HYPO}  x < 0
    Click Button  Save
    Page Should Contain  Hypothesis missing
 
Saving Empty Null Hypothesis Shows Error Message
    Click Button  Deductive
    Input Text  xpath:${NULL}  x < 0
    Click Button  Save
    Page Should Contain  Null hypothesis missing
    
Clicking Clear Button Should Clear Input Fields
    Input Text  xpath:${HYPO}  x
    Click Button  Clear
    Textfield Value Should Be  xpath:${HYPO}  ${EMPTY}
    Textfield Value Should Be  xpath:${NULL}  ${EMPTY}

Saving Hypotheses Should Print Them
    Input Text  xpath:${NULL}  x = 0
    Click Button  Save
    Wait Until Element Is Not Visible  class:widget-input  timeout=5
    Page Should Contain  Hypothesis: x < 0
    Page Should Contain  Null hypothesis: x = 0

Clicking Open Cells Should Open One New Cell
    Click Button  Open cells
    Page Should Contain Element  xpath:${NEW_CELL}

Clicking Run Cells Should Run New Cell
    Click Element  xpath:${NEW_INPUT}
    Press Keys  xpath:${NEW_INPUT}  print('testing')  
    Click Button  Run cells
    Scroll Element Into View  xpath:${NEW_OUTPUT}

Clicking Clear Button Should Clear New Cell
    Click Button  Clear cells
    Element Should Not Contain  xpath:${NEW_INPUT}  print('testing')

Clicking Delete Button Should Delete New Cell
    Click Button  Delete last cell
    Page Should Not Contain Element  xpath:${NEW_CELL}

Clicking Start analysis Should Require Checking Data Limitations
    Click Button  New analysis
    Page Should Contain  Data limitations cannot be empty
    Page Should Contain  Accepted: Hypothesis: x < 0
    
Saving New Hypotheses Should Succeed
    Click Button  Deductive
    Input Text  xpath:${HYPO2}  y > 0
    Input Text  xpath:${NULL2}  y = 0
    Click Button  Save
    Page Should Contain  Hypothesis: y > 0
    Page Should Contain  Null hypothesis: y = 0

Opening Two New Cells Should Succeed
    Click Element  xpath:${CELL_COUNT_INPUT}
    Press Keys  xpath:${CELL_COUNT_INPUT}  ARROW_UP
    Click Button  Open cells
    Page Should Contain Element  xpath:${NEW_CELL2}
    Page Should Contain Element  xpath:${NEW_CELL3}

Selecting Null Hypothesis With Radio Button Should Succeed
    Click Button  Run cells
    Click Element  class:widget-radio-box
    Press Keys  class:widget-radio-box  ARROW_DOWN
    Click Button  New analysis
    Page Should Contain  Accepted: Null hypothesis: y = 0
