// @ts-check
require('dotenv').config()
const testURL = process.env.URL
const { test, expect } = require('@playwright/test')

test('deductive analysis without errors', async ({ page, context }) => {
  // @ts-ignore
  await page.goto(testURL)
  const pagePromise = context.waitForEvent('page')
  await page.click('#new-dropdown-button')
  await page.click('#kernel-python3')
  const newPage = await pagePromise
  await newPage.waitForLoadState()
  await newPage
    .getByLabel('Edit code here')
    .type('from bring_order import BringOrder\nBringOrder()')
  await page.waitForTimeout(1500)
  await newPage.getByLabel('Run').click()
  await newPage.getByLabel('', { exact: true }).first().click()
  await newPage.getByLabel('', { exact: true }).first().fill('Test study')
  await newPage.getByLabel('', { exact: true }).nth(1).click()
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test data')
  await newPage.getByLabel('', { exact: true }).nth(2).click()
  await newPage
    .getByLabel('', { exact: true })
    .nth(2)
    .fill('Importing test data')
  await newPage.getByRole('button', { name: 'Save description' }).click()
  await newPage.getByRole('button', { name: 'Select' }).click()
  await newPage.getByRole('listbox').selectOption('README.md')
  await newPage.getByRole('button', { name: 'Select' }).click()
  await newPage.getByRole('button', { name: 'Run cells' }).click()
  await newPage.getByPlaceholder('Limitation 1').click()
  await newPage.getByPlaceholder('Limitation 1').fill('Test limitation')
  await newPage.getByRole('button', { name: 'Start analysis' }).click()
  await newPage.getByRole('button', { name: 'Test hypothesis' }).click()
  expect(newPage.getByRole('heading', { name: 'Test limitation¶' }).isVisible())
  await newPage.getByPlaceholder('Theory').click()
  await newPage.getByPlaceholder('Theory').fill('Test theory')
  await newPage.getByLabel('', { exact: true }).nth(1).click()
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test hypothesis')
  await newPage.getByLabel('', { exact: true }).nth(2).click()
  await newPage
    .getByLabel('', { exact: true })
    .nth(2)
    .fill('Test null hypothesis')
  await newPage.getByRole('button', { name: 'Validate input' }).click()
  expect(
    newPage
      .getByText(
        'Do the hypotheses fit within the limitations of the data set?'
      )
      .isVisible()
  )
  expect(
    newPage
      .getByText('You have set hypothesis (H1): Test hypothesis')
      .isVisible()
  )
  expect(
    newPage
      .getByText('You have set hypothesis (H0): Test null hypothesis')
      .isVisible()
  )
})

test('deductive analysis theory and hypothesis errors', async ({
  page,
  context,
}) => {
  // @ts-ignore
  await page.goto(testURL)
  const pagePromise = context.waitForEvent('page')
  await page.click('#new-dropdown-button')
  await page.click('#kernel-python3')
  const newPage = await pagePromise
  await newPage.waitForLoadState()
  await newPage
    .getByLabel('Edit code here')
    .type('from bring_order import BringOrder\nBringOrder()')
  await page.waitForTimeout(1500)
  await newPage.getByLabel('Run').click()
  await newPage.getByLabel('', { exact: true }).first().click()
  await newPage.getByLabel('', { exact: true }).first().fill('Test study')
  await newPage.getByLabel('', { exact: true }).nth(1).click()
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test data')
  await newPage.getByLabel('', { exact: true }).nth(2).click()
  await newPage
    .getByLabel('', { exact: true })
    .nth(2)
    .fill('Importing test data')
  await newPage.getByRole('button', { name: 'Save description' }).click()
  await newPage.getByRole('button', { name: 'Select' }).click()
  await newPage.getByRole('listbox').selectOption('README.md')
  await newPage.getByRole('button', { name: 'Select' }).click()
  await newPage.getByRole('button', { name: 'Run cells' }).click()
  await newPage.getByPlaceholder('Limitation 1').click()
  await newPage.getByPlaceholder('Limitation 1').fill('Test limitation')
  await newPage.getByRole('button', { name: 'Start analysis' }).click()
  await newPage.getByRole('button', { name: 'Test hypothesis' }).click()
  await newPage.getByRole('button', { name: 'Save and continue' }).click()
  expect(
    newPage
      .getByText(
        'The theory must be at least 8 characters and not contain special characters'
      )
      .isVisible()
  )
  expect(
    newPage
      .getByText(
        'The hypothesis must be at least 8 characters and not contain special characters'
      )
      .isVisible()
  )
  expect(
    newPage
      .getByText(
        'The null hypothesis must be at least 8 characters and not contain special characters'
      )
      .isVisible()
  )
  expect(newPage.getByRole('button', { name: 'Save and continue' }).isEnabled())
})

test('deductive analysis all done shows export buttons', async ({
  page,
  context,
}) => {
  // @ts-ignore
  await page.goto(testURL)
  const pagePromise = context.waitForEvent('page')
  await page.click('#new-dropdown-button')
  await page.click('#kernel-python3')
  const newPage = await pagePromise
  await newPage.waitForLoadState()
  await newPage
    .getByLabel('Edit code here')
    .type('from bring_order import BringOrder\nBringOrder()')
  await page.waitForTimeout(1500)
  await newPage.getByLabel('Run').click()
  await newPage.getByLabel('', { exact: true }).first().click()
  await newPage.getByLabel('', { exact: true }).first().fill('Test study')
  await newPage.getByLabel('', { exact: true }).nth(1).click()
  await newPage.getByLabel('', { exact: true }).nth(1).fill('Test data')
  await newPage.getByLabel('', { exact: true }).nth(2).click()
  await newPage
    .getByLabel('', { exact: true })
    .nth(2)
    .fill('Importing test data')
  await newPage.getByRole('button', { name: 'Save description' }).click()
  await newPage.getByRole('button', { name: 'Select' }).click()
  await newPage.getByRole('listbox').selectOption('README.md')
  await newPage.getByRole('button', { name: 'Select' }).click()
  await newPage.getByRole('button', { name: 'Run cells' }).click()
  await newPage.getByPlaceholder('Limitation 1').click()
  await newPage.getByPlaceholder('Limitation 1').fill('Test limitation')
  await newPage.getByRole('button', { name: 'Start analysis' }).click()
  await newPage.getByRole('button', { name: 'Test hypothesis' }).click()
  await newPage.getByPlaceholder('Theory').click()
  await newPage
    .getByPlaceholder('Theory')
    .fill('Everyone wants to move to Turku')
  await newPage.getByLabel('', { exact: true }).nth(1).click()
  await newPage
    .getByLabel('', { exact: true })
    .nth(1)
    .fill('Everyone wants to move to Turku')
  await newPage.getByLabel('', { exact: true }).nth(2).click()
  await newPage
    .getByLabel('', { exact: true })
    .nth(2)
    .fill('Everyone wants to move to Turku')
  await newPage.getByRole('button', { name: 'Validate input' }).click()
  await newPage.getByRole('button', { name: 'Yes' }).click()
  await newPage.getByRole('button', { name: 'Run cells' }).click()
  await newPage.getByPlaceholder('Results').click()
  await newPage.getByPlaceholder('Results').fill('Test results')
  await newPage.getByRole('button', { name: 'Save' }).click()
  await newPage.getByRole('button', { name: 'All done' }).click()
  expect(newPage.getByRole('button', { name: 'Export to pdf' }).isEnabled())
  expect(newPage.getByRole('button', { name: 'Close BringOrder' }).isEnabled())
  await newPage.getByRole('button', { name: 'Close BringOrder' }).click()
})
