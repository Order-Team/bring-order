// @ts-check
require('dotenv').config();
const testURL = process.env.URL;
const { test, expect } = require('@playwright/test');

test('import data without errors', async ({ page, context }) => {
  // @ts-ignore
  await page.goto(testURL);
  await expect(page).toHaveTitle(/Home Page - Select or create a notebook/);
  
  const pagePromise = context.waitForEvent('page');
  await page.click('#new-dropdown-button');
  await page.click('#kernel-python3');
  const newPage = await pagePromise;
  await newPage.waitForLoadState();
  await expect(newPage.getByRole('link', { name: 'Jupyter Notebook' })).toBeEnabled();
  await newPage.getByLabel('Edit code here').type('from bring_order import BringOrder\nBringOrder()');
  await page.waitForTimeout(1200);
  await newPage.getByLabel('Run').click();
  await newPage.getByRole('button', { name: 'Skip' }).click();
  await newPage.getByLabel('', { exact: true }).first().click({delay: 200});
  await newPage.getByLabel('', { exact: true }).first().fill('Test study');
  await newPage.getByLabel('', { exact: true }).nth(1).click({delay: 200});
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test data');
  await newPage.getByLabel('', { exact: true }).nth(2).click({delay: 200});
  await newPage.getByLabel('', { exact: true }).nth(2).fill('Importing test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await expect(newPage.getByRole('heading', { name: 'Test study' })).toBeVisible();
  await expect(newPage.getByRole('heading', { name: 'Data: Test data' })).toBeVisible();
  await expect(newPage.getByRole('heading', { name: 'Description' })).toBeVisible();
  await expect(newPage.getByRole('paragraph').filter({ hasText: 'Importing test data' })).toBeVisible();
  await newPage.getByRole('button', { name: 'Select' }).click();
  await newPage.getByRole('listbox').selectOption('📁 tests');
  await newPage.getByRole('listbox').selectOption('loansData.csv');
  await newPage.getByRole('button', { name: 'Select' }).click({delay: 100});
  await newPage.getByRole('button', { name: 'Analyze this data' }).click();
  await expect(newPage.getByRole('heading', { name: 'There are some data limitations you should consider:' })).toBeVisible();
  await newPage.getByRole('button', { name: 'Check limitations' }).click();
  await expect(newPage.getByRole('button', { name: 'Start analysis' })).toBeEnabled();
  await expect(newPage.getByRole('button', { name: 'Add limitation' })).toBeEnabled();
  await expect(newPage.getByRole('button', { name: 'Remove limitations' })).toBeEnabled();
  await newPage.locator('.widget-label-basic > input').first().check();
  await newPage.locator('div:nth-child(2) > .widget-label-basic > input').check();
  await expect(newPage.locator('.widget-label-basic > input').first()).toBeChecked();
  await expect(newPage.locator('.widget-label-basic > input').first()).toBeChecked();
  await newPage.getByRole('button', { name: 'Remove limitations' }).click();
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  await expect(newPage.getByText('Monthly.Income is not normally distributed', { exact: true })).toBeVisible();
  await expect(newPage.getByText('Open.CREDIT.Lines is not normally distributed', { exact: true })).toBeVisible();
  await expect(newPage.getByRole('button', { name: 'Explore data' })).toBeEnabled();
  await expect(newPage.getByRole('button', { name: 'Test hypothesis' })).toBeEnabled();
 });

 test('import data and limitations errors', async ({ page, context }) => {
  // @ts-ignore
  await page.goto(testURL);
  const pagePromise = context.waitForEvent('page');
  await page.click('#new-dropdown-button');
  await page.click('#kernel-python3');
  const newPage = await pagePromise;
  await newPage.waitForLoadState();
  await newPage.getByLabel('Edit code here').type('from bring_order import BringOrder\nBringOrder()');
  await page.waitForTimeout(1200);
  await newPage.getByLabel('Run').click();
  await newPage.getByRole('button', { name: 'Skip' }).click();
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await expect(newPage.getByText('The title cannot be empty or contain special symbols')).toBeVisible();
  await newPage.getByLabel('', { exact: true }).first().click();
  await newPage.getByLabel('', { exact: true }).first().fill('Test study');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await expect(newPage.getByText('The data set name cannot be empty or contain special symbols')).toBeVisible();
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await expect(newPage.getByText('The data description cannot be empty or contain special characters')).toBeVisible();
  await newPage.getByLabel('', { exact: true }).nth(2).click();
  await newPage.getByLabel('', { exact: true }).nth(2).fill('Importing test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await newPage.getByRole('button', { name: 'Import manually' }).click();
  await newPage.getByRole('button', { name: 'Check limitations' }).click();
  await newPage.getByPlaceholder('Limitation 1').click();
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  await expect(newPage.getByText('Data limitations cannot be empty or contain special symbols')).toBeVisible();
  await newPage.getByRole('button', { name: 'Add limitation', exact: true }).click();
  await expect(newPage.getByPlaceholder('Limitation 2')).toBeVisible();
});

test('import csv data with variable independence testing', async ({ page, context }) => {
  // @ts-ignore
  await page.goto(testURL);
  const pagePromise = context.waitForEvent('page');
  await page.click('#new-dropdown-button');
  await page.click('#kernel-python3');
  const newPage = await pagePromise;
  await newPage.waitForLoadState();
  await newPage.getByLabel('Edit code here').type('from bring_order import BringOrder\nBringOrder()');
  await page.waitForTimeout(1200);
  await newPage.getByLabel('Run').click();
  await newPage.getByRole('button', { name: 'Skip' }).click();
  await newPage.getByLabel('', { exact: true }).first().click({delay: 200});
  await newPage.getByLabel('', { exact: true }).first().fill('Test loan study');
  await newPage.getByLabel('', { exact: true }).nth(1).click({delay: 200});
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test loan data');
  await newPage.getByLabel('', { exact: true }).nth(2).click({delay: 200});
  await newPage.getByLabel('', { exact: true }).nth(2).fill('Importing test loan data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await newPage.getByRole('button', { name: 'Select' }).click({delay: 100});
  await newPage.getByRole('listbox').selectOption('📁 tests');
  await newPage.getByRole('listbox').selectOption('loansData.csv');
  await newPage.getByRole('button', { name: 'Select' }).click();
  await newPage.getByRole('button', { name: 'Analyze this data' }).click();
  await expect(newPage.getByRole('heading', { name: 'There are some data limitations you should consider:' })).toBeVisible();
  await expect(newPage.getByText('Variables that are not normally distributed: Amount.Requested, Amount.Funded.By.')).toBeVisible();
  await newPage.getByRole('button', { name: 'Test independence' }).click();
  await expect(newPage.getByText('Choose variables to test their independence:')).toBeVisible();
  await expect(newPage.getByRole('combobox', { name: 'Explanatory variable' })).toBeEnabled();
  await expect(newPage.getByRole('combobox', { name: 'Dependent variable' })).toBeEnabled();
  await newPage.getByRole('combobox', { name: 'Explanatory variable' }).selectOption('Loan.Purpose');
  await newPage.getByRole('combobox', { name: 'Dependent variable' }).selectOption('Loan.Length');
  await newPage.getByRole('button', { name: 'Test' , exact: true }).click();
  await expect(newPage.getByText('Loan.Purpose and Loan.Length are not independent')).toBeVisible();
});

test('import csv data without variable independence testing', async ({ page, context }) => {
  // @ts-ignore
  await page.goto(testURL);
  const pagePromise = context.waitForEvent('page');
  await page.click('#new-dropdown-button');
  await page.click('#kernel-python3');
  const newPage = await pagePromise;
  await newPage.waitForLoadState();
  await newPage.getByLabel('Edit code here').type('from bring_order import BringOrder\nBringOrder()');
  await page.waitForTimeout(1200);
  await newPage.getByLabel('Run').click();
  await newPage.getByRole('button', { name: 'Skip' }).click();
  await newPage.getByLabel('', { exact: true }).first().click({delay: 200});
  await newPage.getByLabel('', { exact: true }).first().fill('Test iris study');
  await newPage.getByLabel('', { exact: true }).nth(1).click({delay: 200});
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test iris data');
  await newPage.getByLabel('', { exact: true }).nth(2).click({delay: 200});
  await newPage.getByLabel('', { exact: true }).nth(2).fill('Importing test iris data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await newPage.getByRole('button', { name: 'Select' }).click();
  await newPage.getByRole('listbox').selectOption('📁 tests');
  await newPage.getByRole('listbox').selectOption('test_iris.csv');
  await newPage.getByRole('button', { name: 'Select' }).click({delay: 100});  
  await newPage.getByRole('button', { name: 'Analyze this data' }).click({delay: 100});
  await newPage.getByRole('button', { name: 'Test independence' }).click();
  await expect(newPage.getByText('There are not enough categorical variables to perform a chi-square test.')).toBeVisible();
});

test('manual import data with ai assistant', async ({ page, context }) => {
  // @ts-ignore
  await page.goto(testURL);
  const pagePromise = context.waitForEvent('page');
  await page.click('#new-dropdown-button');
  await page.click('#kernel-python3');
  const newPage = await pagePromise;
  await newPage.waitForLoadState();
  await newPage.getByLabel('Edit code here').type('from bring_order import BringOrder\nBringOrder()');
  await page.waitForTimeout(1200);
  await newPage.getByLabel('Run').click();
  await newPage.locator('input[type="password"]').click();
  await newPage.locator('input[type="password"]').fill('testpassword');
  await newPage.getByRole('button', { name: 'Submit key' }).click();
  await expect(newPage.getByText('Incorrect Open AI api key. You can generate API keys in the OpenAI web interface.')).toBeVisible();
});
