from invoke import task

@task
def tests(c):
    c.run("pytest")

@task
def lint(c):
    c.run("pylint bring_order")

@task
def robottests(c):
    c.run("poetry shell && ./run_robot_tests.sh")

@task
def alltests(c):
    c.run("pytest; pylint bring_order; poetry shell && ./run_robot_tests.sh")

@task
def coverage(c):
    c.run("coverage run --branch -m pytest tests")
    c.run("coverage report -m")
    c.run("coverage html")
