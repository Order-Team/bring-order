// @ts-check
require('dotenv').config();
const testURL = process.env.URL;
const { test, expect, selectors } = require('@playwright/test');

test('has title', async ({ page, context }) => {
   // @ts-ignore
   await page.goto(testURL);
   await expect(page).toHaveTitle(/Home Page - Select or create a notebook/);
  
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
   await newPage.getByRole('button', { name: 'Open cells' }).click();
   await newPage.locator('#notebook-container div').filter({ hasText: 'In [ ]:xxxxxxxxxx . . .' }).locator('pre').nth(1).click();
   await newPage.getByRole('textbox').fill('a=5');
   await newPage.getByRole('button', { name: 'Run cells' }).click();
 });
   
