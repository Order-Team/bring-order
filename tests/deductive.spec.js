// @ts-check
require('dotenv').config();
const testURL = process.env.URL;
const { test, expect } = require('@playwright/test');

test('deductive analysis without errors', async ({ page, context }) => {
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
  await newPage.getByPlaceholder('​').click();
  await newPage.getByPlaceholder('​').fill('Test limitation');
  await newPage.getByRole('button', { name: 'Start analysis' }).click();
  await newPage.getByRole('button', { name: 'Deductive' }).click();
  expect(newPage.getByRole('heading', { name: 'Deductive analysis¶' }).isVisible());
  await newPage.getByPlaceholder('Theory').click();
  await newPage.getByPlaceholder('Theory').fill('Test theory');
  await newPage.getByPlaceholder('​').first().click();
  await newPage.getByPlaceholder('​').first().fill('Test hypothesis');
  await newPage.getByPlaceholder('​').nth(1).click();
  await newPage.getByPlaceholder('​').nth(1).fill('Test null hypothesis');
  await newPage.getByRole('button', { name: 'Save' }).click();
  expect(newPage.getByText('Do the hypotheses fit within the limitations of the data set?').isVisible());
  expect(newPage.getByText('You have set hypothesis (H1): Test hypothesis').isVisible());
  expect(newPage.getByText('You have set hypothesis (H0): Test null hypothesis').isVisible());
});

test('deductive analysis theory and hypothesis errors', async ({ page, context }) => {
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
    await newPage.getByPlaceholder('​').click();
    await newPage.getByPlaceholder('​').fill('Test limitation');
    await newPage.getByRole('button', { name: 'Start analysis' }).click();
    await newPage.getByRole('button', { name: 'Deductive' }).click();
    await newPage.getByRole('button', { name: 'Save' }).click();
    expect(newPage.getByText('You must describe your theory and insights').isVisible());
    expect(newPage.getByText('Hypothesis missing').isVisible());
    expect(newPage.getByText('Null hypothesis missing').isVisible());
  });