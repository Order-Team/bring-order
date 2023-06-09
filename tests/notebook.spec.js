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
   await page.waitForTimeout(800);
   await newPage.getByLabel('Run').click();
   await newPage.locator('input[type="text"]').click();
   await newPage.locator('input[type="text"]').fill('Test data');
   await newPage.getByLabel('', { exact: true }).nth(1).click();
   await newPage.getByLabel('', { exact: true }).nth(1).fill('Importing test data');
   await newPage.getByRole('button', { name: 'Save description' }).click();
   await newPage.getByRole('button', { name: 'Open cells' }).click();
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
  await page.waitForTimeout(800);
  await newPage.getByLabel('Run').click();
  await newPage.getByRole('button', { name: 'Save description' }).click();
  expect(newPage.locator('You must name the data set').isVisible());
  await newPage.locator('input[type="text"]').click();
  await newPage.locator('input[type="text"]').fill('Test data');
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
  await page.waitForTimeout(800);
  await newPage.getByLabel('Run').click();
  await newPage.locator('input[type="text"]').click();
  await newPage.locator('input[type="text"]').fill('Test data');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Importing test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await newPage.getByRole('button', { name: 'Open cells' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  await newPage.getByPlaceholder('Limitation 1').click();
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  expect(newPage.getByText('Data limitations cannot be empty').isVisible());
  await newPage.getByRole('button', { name: 'Add limitation' }).click();
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
  await page.waitForTimeout(800);
  await newPage.getByLabel('Run').click();
  await newPage.locator('input[type="text"]').click();
  await newPage.locator('input[type="text"]').fill('Test data');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Importing test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  await newPage.getByPlaceholder('Limitation 1').click();
  await newPage.getByPlaceholder('Limitation 1').fill('Test limitation');
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  expect(newPage.getByRole('button', { name: 'Explore data' }).isVisible());
  expect(newPage.getByRole('button', { name: 'Test hyporthesis' }).isVisible());
});
