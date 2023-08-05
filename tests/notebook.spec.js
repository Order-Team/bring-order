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
  expect(newPage.getByRole('link', { name: 'Jupyter Notebook' }).isEnabled());
  await newPage.getByLabel('Edit code here').type('from bring_order import BringOrder\nBringOrder()');
  await page.waitForTimeout(1500);
  await newPage.getByLabel('Run').click();
  await newPage.getByLabel('', { exact: true }).first().click();
  await newPage.getByLabel('', { exact: true }).first().fill('Test study');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test data');
  await newPage.getByLabel('', { exact: true }).nth(2).click();
  await newPage.getByLabel('', { exact: true }).nth(2).fill('Importing test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  expect(newPage.getByRole('heading', { name: 'Test study¶' }).isVisible());
  expect(newPage.getByRole('heading', { name: 'Data: Test data¶' }).isVisible());
  expect(newPage.getByRole('heading', { name: 'Description¶' }).isVisible());
  await page.waitForTimeout(500);
  await newPage.getByRole('button', { name: 'Select' }).click();
  await newPage.getByRole('listbox').selectOption('📁 tests');
  await newPage.getByRole('listbox').selectOption('loansData.csv');
  await newPage.getByRole('button', { name: 'Select' }).click();
  await newPage.getByRole('button', { name: 'Analyze this data' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  expect(newPage.getByRole('button', { name: 'Start analysis' }).isVisible());
  expect(newPage.getByRole('button', { name: 'Add limitation' }).isVisible());
  expect(newPage.getByRole('button', { name: 'Remove limitation' }).isVisible());
 });

 test('import data errors', async ({ page, context }) => {
  // @ts-ignore
  await page.goto(testURL);
  const pagePromise = context.waitForEvent('page');
  await page.click('#new-dropdown-button');
  await page.click('#kernel-python3');
  const newPage = await pagePromise;
  await newPage.waitForLoadState();
  await newPage.getByLabel('Edit code here').type('from bring_order import BringOrder\nBringOrder()');
  await page.waitForTimeout(1500);
  await newPage.getByLabel('Run').click();
  await newPage.getByRole('button', { name: 'Save description' }).click();
  expect(newPage.locator('Please give your study a title').isVisible());
  await newPage.getByLabel('', { exact: true }).first().click();
  await newPage.getByLabel('', { exact: true }).first().fill('Test study');
  expect(newPage.locator('You must name the data set').isVisible());
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  expect(newPage.locator('You must give some description of the data').isVisible());
});

test('data limitations errors', async ({ page, context }) => {
  // @ts-ignore
  await page.goto(testURL);
  const pagePromise = context.waitForEvent('page');
  await page.click('#new-dropdown-button');
  await page.click('#kernel-python3');
  const newPage = await pagePromise;
  await newPage.waitForLoadState();
  await newPage.getByLabel('Edit code here').type('from bring_order import BringOrder\nBringOrder()');
  await page.waitForTimeout(1500);
  await newPage.getByLabel('Run').click();
  await newPage.getByLabel('', { exact: true }).first().click();
  await newPage.getByLabel('', { exact: true }).first().fill('Test study');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test data');
  await newPage.getByLabel('', { exact: true }).nth(2).click();
  await newPage.getByLabel('', { exact: true }).nth(2).fill('Importing test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await page.waitForTimeout(500);
  await newPage.getByRole('button', { name: 'Import manually' }).click();
  await newPage.getByRole('button', { name: 'Add limitations' }).click();
  await newPage.getByPlaceholder('Limitation 1').click();
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  expect(newPage.getByText('Data limitations cannot be empty').isVisible());
  await newPage.getByRole('button', { name: 'Add limitation', exact: true }).click();
  expect(newPage.getByPlaceholder('Limitation 2').isVisible);
});

test('start of inductive and deductide', async ({ page, context }) => {
  // @ts-ignore
  await page.goto(testURL);
  const pagePromise = context.waitForEvent('page');
  await page.click('#new-dropdown-button');
  await page.click('#kernel-python3');
  const newPage = await pagePromise;
  await newPage.waitForLoadState();
  await newPage.getByLabel('Edit code here').type('from bring_order import BringOrder\nBringOrder()');
  await page.waitForTimeout(1500);
  await newPage.getByLabel('Run').click();
  await newPage.getByLabel('', { exact: true }).first().click();
  await newPage.getByLabel('', { exact: true }).first().fill('Test study');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test data');
  await newPage.getByLabel('', { exact: true }).nth(2).click();
  await newPage.getByLabel('', { exact: true }).nth(2).fill('Importing test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await page.waitForTimeout(500);
  await newPage.getByRole('button', { name: 'Import manually' }).click();
  await newPage.getByRole('button', { name: 'Add limitations' }).click();
  await newPage.getByPlaceholder('Limitation 1').click();
  await newPage.getByPlaceholder('Limitation 1').fill('Test limitation');
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  expect(newPage.getByRole('button', { name: 'Explore data' }).isVisible());
  expect(newPage.getByRole('button', { name: 'Test hyporthesis' }).isVisible());
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
  await page.waitForTimeout(1500);
  await newPage.getByLabel('Run').click();
  await newPage.getByLabel('', { exact: true }).first().click();
  await newPage.getByLabel('', { exact: true }).first().fill('Test loan study');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test loan data');
  await newPage.getByLabel('', { exact: true }).nth(2).click();
  await newPage.getByLabel('', { exact: true }).nth(2).fill('Importing test loan data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await page.waitForTimeout(500);
  await newPage.getByRole('button', { name: 'Select' }).click();
  await newPage.getByRole('listbox').selectOption('📁 tests');
  await newPage.getByRole('listbox').selectOption('loansData.csv');
  await newPage.getByRole('button', { name: 'Select' }).click();
  await newPage.getByRole('button', { name: 'Analyze this data' }).click();
  expect(newPage.getByText('Amount.Requested is not normally distributed').isVisible());
  await newPage.getByRole('button', { name: 'Test independence' }).click();
  expect(newPage.getByText('Choose variables to test their independence:').isVisible());
  expect(newPage.getByRole('combobox', { name: 'Explanatory variable' }).isVisible());
  expect(newPage.getByRole('combobox', { name: 'Dependent variable' }).isVisible());
  await newPage.getByRole('combobox', { name: 'Explanatory variable' }).selectOption('Loan.Purpose');
  await newPage.getByRole('combobox', { name: 'Dependent variable' }).selectOption('Loan.Length');
  await newPage.getByRole('button', { name: 'Test' , exact: true }).click();
  expect(newPage.getByText('Loan.Purpose and Loan.Length are not independent').isVisible());
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
  await page.waitForTimeout(1500);
  await newPage.getByLabel('Run').click();
  await newPage.getByLabel('', { exact: true }).first().click();
  await newPage.getByLabel('', { exact: true }).first().fill('Test iris study');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test iris data');
  await newPage.getByLabel('', { exact: true }).nth(2).click();
  await newPage.getByLabel('', { exact: true }).nth(2).fill('Importing test iris data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await page.waitForTimeout(500);
  await newPage.getByRole('button', { name: 'Select' }).click();
  await newPage.getByRole('listbox').selectOption('📁 tests');
  await newPage.getByRole('listbox').selectOption('test_iris.csv');
  await newPage.getByRole('button', { name: 'Select' }).click();  
  await newPage.getByRole('button', { name: 'Analyze this data' }).click();
  await newPage.getByRole('button', { name: 'Test independence' }).click();
  expect(newPage.getByText('There are not enough categorical variables to perform a chi-square test.').isVisible());
});
