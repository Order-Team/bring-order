// @ts-check
require('dotenv').config();
const testURL = process.env.URL;
const { test, expect } = require('@playwright/test');

test('inductive analysis without errors', async ({ page, context }) => {
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
  await newPage.locator('#notebook-container div').filter({ hasText: 'In [ ]: . . .' }).locator('pre').click();
  await newPage.getByRole('button', { name: '' }).click();
  await newPage.getByPlaceholder('​').click();
  await newPage.getByPlaceholder('​').fill('Test data');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Importing test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  await newPage.getByPlaceholder('Limitation 1').click();
  await newPage.getByPlaceholder('Limitation 1').fill('Limitation');
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  await newPage.getByRole('button', { name: 'Inductive' }).click();
  expect(newPage.getByRole('heading', { name: 'Inductive analysis¶' }).isVisible());
  await newPage.getByRole('button', { name: 'Open cells' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Tests');
  await newPage.getByRole('button', { name: 'Submit observation' }).click();
  expect(newPage.getByRole('heading', { name: 'Observation 1: Tests¶' }).isVisible());
});

test('inductive analysis summary error', async ({ page, context }) => {
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
  await newPage.locator('#notebook-container div').filter({ hasText: 'In [ ]: . . .' }).locator('pre').click();
  await newPage.getByRole('button', { name: '' }).click();
  await newPage.getByPlaceholder('​').click();
  await newPage.getByPlaceholder('​').fill('Test data');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Importing test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  await newPage.getByPlaceholder('Limitation 1').click();
  await newPage.getByPlaceholder('Limitation 1').fill('Limitation');
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  await newPage.getByRole('button', { name: 'Inductive' }).click();
  await newPage.getByRole('button', { name: 'Open cells' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  await newPage.getByRole('button', { name: 'Submit observation' }).click();
  expect(newPage.getByText('You must write some kind of summary').isVisible());
});
