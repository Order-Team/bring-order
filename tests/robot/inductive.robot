*** Settings ***
Resource  resource.robot
Suite Setup  Open Test Notebook
Suite Teardown  Clear Notebook And Close Browser  0    # The number of cells - 1


*** Test Cases ***
Notebook Should Be Open
    Wait Until Page Contains Element  id:kernel_indicator  timeout=5
    Title Should Be  test_file - Jupyter Notebook

Calling BringOrder Should Succeed After Import
    Run Notebook
    Page Should Contain  New Analysis