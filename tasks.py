from invoke import task

@task
def tests(c):
    c.run("pytest src")

@task
def lint(c):
    c.run("pylint src")

@task
def robottests(c):
    c.run("poetry shell \ ./run_robot_tests.sh")

@task
def alltests(c):
    c.run("pytest src; pylint src; poetry shell && ./run_robot_tests.sh")
