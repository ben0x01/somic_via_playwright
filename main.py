import asyncio
import random
from playwright.async_api import async_playwright, expect

from helper import get_random_balance

EXTENSIONS_PATH = r"C:\Users\user\AppData\Local\Google\Chrome\User Data\Default\Extensions\nkbihfbeogaeaoehlefnkodbefgpgknn\12.4.1_0"
MM_PASSWORD = "B7601As5T78"


async def fill_balance_input(page, contract_list, wallet_address):
    non_zero_balances = await get_random_balance(contract_list, wallet_address)

    if non_zero_balances:
        selected_token = random.choice(non_zero_balances)
        symbol = selected_token["symbol"]
        balance = selected_token["balance"]

        random_amount = round(balance * random.uniform(0.1, 1), 6)
        print(f"Selected token: {symbol}, Balance: {balance}, Random Amount: {random_amount}")

        try:
            input_field = page.locator('input[name="fromTokenAmount"]')
            await expect(input_field).to_be_visible()
            await input_field.fill(str(random_amount))
            print(f"Input field filled with random amount: {random_amount}")
        except Exception as e:
            print(f"Error filling input field: {e}")
    else:
        print(f"No non-zero balances found for wallet {wallet_address}")


async def main(seed_phrase):
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            '',
            headless=False,
            args=[
                '--disable-blink-features=AutomationControlled',
                f"--disable-extensions-except={EXTENSIONS_PATH}",
                f"--load-extension={EXTENSIONS_PATH}"
            ],
        )

        titles = [await page.title() for page in context.pages]
        while "MetaMask" not in titles:
            titles = [await page.title() for page in context.pages]

        mm_page = context.pages[1]
        await mm_page.wait_for_load_state()

        await asyncio.sleep(1)
        checkbox = mm_page.locator('//*[@id="onboarding__terms-checkbox"]')
        await mm_page.wait_for_load_state(state='domcontentloaded')
        await checkbox.click()

        import_wallet = mm_page.get_by_test_id(test_id="onboarding-import-wallet")
        await expect(import_wallet).to_be_enabled()
        await import_wallet.click()

        i_dont_agree = mm_page.get_by_test_id(test_id="metametrics-no-thanks")
        await expect(i_dont_agree).to_be_enabled()
        await i_dont_agree.click()

        for i in range(12):
            await mm_page.get_by_test_id(test_id=f'import-srp__srp-word-{i}').fill(seed_phrase[i])

        confirm_seed = mm_page.get_by_test_id(test_id="import-srp-confirm")
        await expect(confirm_seed).to_be_enabled()
        await confirm_seed.click()

        await mm_page.get_by_test_id(test_id='create-password-new').fill(MM_PASSWORD)
        await mm_page.get_by_test_id(test_id='create-password-confirm').fill(MM_PASSWORD)
        terms_button = mm_page.get_by_test_id(test_id="create-password-terms")
        await expect(terms_button).to_be_enabled()
        await terms_button.click()

        terms_button_2 = mm_page.get_by_test_id(test_id="create-password-import")
        await expect(terms_button_2).to_be_enabled()
        await terms_button_2.click()

        terms_button_3 = mm_page.get_by_test_id(test_id="onboarding-complete-done")
        await expect(terms_button_3).to_be_enabled()
        await terms_button_3.click()

        terms_button_5 = mm_page.get_by_test_id(test_id="pin-extension-next")
        await expect(terms_button_5).to_be_enabled()
        await terms_button_5.click()

        terms_button_6 = mm_page.get_by_test_id(test_id="pin-extension-done")
        await expect(terms_button_6).to_be_enabled()
        await terms_button_6.click()

        await asyncio.sleep(5)
        await mm_page.goto("https://testnet.soniclabs.com/account")
        await asyncio.sleep(10)

        await mm_page.get_by_test_id(test_id="tradeform_connect_wallet_button").click()
        await asyncio.sleep(10)

        await mm_page.evaluate('''() => {
            const span = Array.from(document.querySelectorAll("span")).find(el => el.textContent.includes("Metamask"));
            if (span) {
                const clickableElement = span.closest("li");
                if (clickableElement) {
                    clickableElement.scrollIntoView();
                    clickableElement.click();
                } else {
                    console.log("Clickable ancestor of Metamask span not found.");
                }
            } else {
                console.log("Span with text 'Metamask' not found.");
            }
        }''')

        await asyncio.sleep(5)

        pages = context.pages
        mm_page = context.pages[-1]
        await mm_page.bring_to_front()
        await asyncio.sleep(10)

        terms_button_7 = mm_page.get_by_test_id(test_id="page-container-footer-next")
        await expect(terms_button_7).to_be_enabled()
        await terms_button_7.click()
        await asyncio.sleep(5)

        terms_button_8 = mm_page.get_by_test_id(test_id="page-container-footer-next")
        await expect(terms_button_8).to_be_enabled()
        await terms_button_8.click()
        await asyncio.sleep(3)

        await asyncio.sleep(10)
        mm_page = context.pages[1]
        await mm_page.wait_for_load_state()
        print("Wallet connected and ready")
        input_field = mm_page.locator('input[name="fromTokenAmount"]')
        await expect(input_field).to_be_visible()
        await input_field.fill("1")

        await asyncio.sleep(5)
        print("Жмем на свап")

        await mm_page.click('button.fbutton.btn.btn-lg.input-w100[data-testid="tradeform_submit_button"]')

        await asyncio.sleep(5)

        await mm_page.click('//span[text()="Switch to Sonic Testnet chain"]/ancestor::button')

        await asyncio.sleep(5)

        pages = context.pages
        mm_page = context.pages[-1]
        await mm_page.bring_to_front()
        await asyncio.sleep(10)

        terms_button_7 = mm_page.get_by_test_id(test_id="confirmation-submit-button")
        await expect(terms_button_7).to_be_enabled()
        await terms_button_7.click()
        await asyncio.sleep(5)

        terms_button_8 = mm_page.get_by_test_id(test_id="confirmation-submit-button")
        await expect(terms_button_8).to_be_enabled()
        await terms_button_8.click()
        await asyncio.sleep(3)

        await asyncio.sleep(10)
        mm_page = context.pages[1]
        await mm_page.wait_for_load_state()

        await mm_page.click('button.fbutton.btn.btn-lg.input-w100[data-testid="tradeform_submit_button"]')

        await asyncio.sleep(5)

        pages = context.pages
        mm_page = context.pages[-1]
        await mm_page.bring_to_front()
        await asyncio.sleep(3)

        terms_button_8 = mm_page.get_by_test_id(test_id="confirm-footer-button")
        await expect(terms_button_8).to_be_enabled()
        await terms_button_8.click()
        await asyncio.sleep(3)

        await asyncio.sleep(30)



if __name__ == '__main__':
    with open('seed.txt', 'r') as seed_file, open('wallets.txt', 'r') as wallet_file:
        seeds = [line.split() for line in seed_file.readlines()]
        addresses = [line.strip() for line in wallet_file.readlines()]

    if len(seeds) != len(addresses):
        print("Количество сид фраз и адресов кошельков не совпадает.")
    else:
        for seed, address in zip(seeds, addresses):
            asyncio.run(main(seed))
