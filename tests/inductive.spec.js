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
  await newPage.locator('input[type="text"]').click();
  await newPage.locator('input[type="text"]').fill('Test data');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Importing test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  await newPage.getByPlaceholder('Limitation 1').click();
  await newPage.getByPlaceholder('Limitation 1').fill('Test limitation');
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  await newPage.getByRole('button', { name: 'Explore data' }).click();
  expect(newPage.getByRole('heading', { name: 'Inductive analysis¶' }).isVisible());
  await newPage.getByRole('button', { name: 'Open cells' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Tests');
  await newPage.getByRole('button', { name: 'Submit observation' }).click();
  expect(newPage.getByRole('heading', { name: 'Observation 1: Tests¶' }).isVisible());
  await newPage.getByRole('button', { name: 'Ready to summarize' }).click();
  await newPage.getByPlaceholder('Summary', { exact: true }).click();
  await newPage.getByPlaceholder('Summary', { exact: true }).fill('Test summary');
  expect(newPage.getByRole('heading', { name: 'Summary: Test summary¶' }).isVisible());
});

test('inductive analysis with errors', async ({ page, context }) => {
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
  await newPage.getByRole('button', { name: 'Explore data' }).click();
  await newPage.getByRole('button', { name: 'Open cells' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  await newPage.getByRole('button', { name: 'Submit observation' }).click();
  expect(newPage.getByText('You must write some kind of summary').isVisible());
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test observation');
  await newPage.getByRole('button', { name: 'Submit observation' }).click();
  await newPage.getByRole('button', { name: 'Ready to summarize' }).click();
  expect(newPage.getByText('You must write some kind of summary').isVisible());
});

test('inductive analysis all done shows export buttons', async ({ page, context }) => {
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
  await newPage.getByRole('button', { name: 'Explore data' }).click();
  await newPage.getByRole('button', { name: 'Open cells' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Tests');
  await newPage.getByRole('button', { name: 'Submit observation' }).click();
  await newPage.getByRole('button', { name: 'Ready to summarize' }).click();
  await newPage.getByPlaceholder('Summary', { exact: true }).click();
  await newPage.getByPlaceholder('Summary', { exact: true }).fill('Test summary');
  await newPage.getByRole('button', { name: 'Submit summary' }).click();
  await newPage.getByRole('button', { name: 'All done' }).click();
  expect(newPage.getByRole('button', { name: 'Export to pdf' }).isVisible());
  expect(newPage.getByRole('button', { name: 'Close BringOrder' }).isVisible());
  await newPage.getByRole('button', { name: 'Close BringOrder' }).click();
  expect(newPage.getByRole('heading', { name: 'Summary: Test summary¶' }).isVisible());
});
