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
  await page.waitForTimeout(1500);
  await newPage.getByLabel('Run').click();
  await newPage.getByLabel('', { exact: true }).first().click();
  await newPage.getByLabel('', { exact: true }).first().fill('Test study');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test data');
  await newPage.getByLabel('', { exact: true }).nth(2).click();
  await newPage.getByLabel('', { exact: true }).nth(2).fill('Importing test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await newPage.getByRole('button', { name: 'Import manually' }).click();
  await newPage.getByRole('button', { name: 'Check limitations' }).click();
  await newPage.getByPlaceholder('Limitation 1').click();
  await newPage.getByPlaceholder('Limitation 1').fill('Test limitation');
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  await newPage.getByRole('button', { name: 'Explore data' }).click();
  expect(newPage.getByRole('heading', { name: 'Data exploration¶' }).isVisible());
  await newPage.getByPlaceholder('Preconception 1', { exact: true }).click();
  await newPage.getByPlaceholder('Preconception 1', { exact: true }).fill('Test preconception');
  await newPage.getByRole('button', { name: 'Save preconceptions' }).click();
  expect(newPage.getByRole('heading', { name: 'Preconceptions¶' }).isVisible());
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
  await page.waitForTimeout(1500);
  await newPage.getByLabel('Run').click();
  await newPage.getByLabel('', { exact: true }).first().click();
  await newPage.getByLabel('', { exact: true }).first().fill('Test study');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test data');
  await newPage.getByLabel('', { exact: true }).nth(2).click();
  await newPage.getByLabel('', { exact: true }).nth(2).fill('Importing test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await newPage.getByRole('button', { name: 'Import manually' }).click();
  await newPage.getByRole('button', { name: 'Check limitations' }).click();
  await newPage.getByPlaceholder('Limitation 1').click();
  await newPage.getByPlaceholder('Limitation 1').fill('Test limitation');
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  await newPage.getByRole('button', { name: 'Explore data' }).click();
  await newPage.getByRole('button', { name: 'Save preconceptions' }).click();
  expect(newPage.getByText('You must name at least one preconception').isVisible());
  await newPage.getByPlaceholder('Preconception 1', { exact: true }).click();
  await newPage.getByPlaceholder('Preconception 1', { exact: true }).fill('Test preconception');
  await newPage.getByRole('button', { name: 'Save preconceptions' }).click();
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
  await page.waitForTimeout(1500);
  await newPage.getByLabel('Run').click();
  await newPage.getByLabel('', { exact: true }).first().click();
  await newPage.getByLabel('', { exact: true }).first().fill('Test study');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test data');
  await newPage.getByLabel('', { exact: true }).nth(2).click();
  await newPage.getByLabel('', { exact: true }).nth(2).fill('Importing test data');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await newPage.getByRole('button', { name: 'Import manually' }).click();
  await newPage.getByRole('button', { name: 'Check limitations' }).click();
  await newPage.getByPlaceholder('Limitation 1').click();
  await newPage.getByPlaceholder('Limitation 1').fill('Test limitation');
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  await newPage.getByRole('button', { name: 'Explore data' }).click();
  await newPage.getByPlaceholder('Preconception 1', { exact: true }).click();
  await newPage.getByPlaceholder('Preconception 1', { exact: true }).fill('Test preconception');
  await newPage.getByRole('button', { name: 'Save preconceptions' }).click();
  await newPage.getByRole('button', { name: 'Open cells' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Tests');
  await newPage.getByRole('button', { name: 'Submit observation' }).click();
  await newPage.getByRole('button', { name: 'Ready to summarize' }).click();
  await newPage.getByPlaceholder('Summary', { exact: true }).click();
  await newPage.getByPlaceholder('Summary', { exact: true }).fill('Test summary');
  await newPage.getByRole('button', { name: 'Submit summary' }).click();
  await newPage.locator('div').filter({ hasText: /^50$/ }).first().click();
  await newPage.getByRole('button', { name: 'Lock evaluation' }).click();
  await newPage.getByLabel('Test preconception').check();
  await newPage.locator('div').filter({ hasText: /^50$/ }).first().click();
  await newPage.getByRole('button', { name: 'Save' }).click();
  await newPage.getByRole('button', { name: 'All done' }).click();
  expect(newPage.getByRole('button', { name: 'Export to pdf' }).isVisible());
  expect(newPage.getByRole('button', { name: 'Close BringOrder' }).isVisible());
  await newPage.getByRole('button', { name: 'Close BringOrder' }).click();
  expect(newPage.getByRole('heading', { name: 'Summary: Test summary¶' }).isVisible());
});

test('Data limitations are printed in evaluation', async ({ page, context }) => {
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
  await newPage.getByLabel('', { exact: true }).first().fill('Dogs');
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('iris');
  await newPage.getByLabel('', { exact: true }).nth(2).click();
  await newPage.getByLabel('', { exact: true }).nth(2).fill('Data including nothing about dogs.');
  await newPage.getByRole('button', { name: 'Save description' }).click();
  await newPage.getByRole('button', { name: 'Select' }).click();
  await newPage.getByRole('listbox').selectOption('📁 tests');
  await newPage.getByRole('listbox').selectOption('test_iris.csv');
  await newPage.getByRole('button', { name: 'Select' }).click();
  await newPage.getByRole('button', { name: 'Analyze this data' }).click();
  await newPage.getByRole('button', { name: 'Check limitations' }).click();
  await newPage.getByRole('button', { name: 'Add limitation', exact: true }).click();
  await newPage.getByPlaceholder('Limitation 4').click();
  await newPage.getByPlaceholder('Limitation 4').fill('Nothing about the dogs.');
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  await newPage.getByRole('button', { name: 'Explore data' }).click();
  await newPage.getByPlaceholder('Preconception 1').click();
  await newPage.getByPlaceholder('Preconception 1').fill('Dogs are as smart as cats');
  await newPage.getByRole('button', { name: 'Save preconceptions' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  await newPage.getByRole('button', { name: 'Open cells' }).click();
  await newPage.getByRole('button', { name: 'Run cells' }).click();
  await newPage.getByLabel('', { exact: true }).nth(1).click();
  await newPage.getByLabel('', { exact: true }).nth(1).fill('dogs are smarter than cats.');
  await newPage.getByRole('button', { name: 'Submit observation' }).click();
  await newPage.getByRole('button', { name: 'Ready to summarize' }).click();
  await newPage.getByPlaceholder('Summary').click();
  await newPage.getByPlaceholder('Summary').fill('Dogs are smarter than cats!');
  await newPage.getByRole('button', { name: 'Submit summary' }).click();
  await newPage.getByRole('button', { name: 'Lock evaluation' }).click();
  await newPage.getByText('50').click();
  await newPage.getByRole('button', { name: 'Save' }).click();
  expect(newPage.getByText('Nothing about the dogs.').nth(3).isVisible());
  expect(newPage.getByRole('heading', { name: 'Limitations that were noticed in the data:¶' }).isVisible());
  await newPage.getByRole('button', { name: 'All done' }).click();
  await newPage.getByRole('button', { name: 'Close BringOrder' }).click();
});
