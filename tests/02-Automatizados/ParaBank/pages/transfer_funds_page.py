
import constants



class TransferFundsPage:

    def __init__(self, page):
        self.page = page

    def ir_a_transfer_funds(self):
        self.page.goto(constants.TRANSFER_FUNDS_URL)

    def transferir_fondos(self, from_account_id=0, to_account_id=1, amount=0):
        self.page.locator("#amount").fill(amount)
        self.page.locator("#fromAccountId option").first.wait_for(state="attached")
        self.page.locator("#toAccountId option").first.wait_for(state="attached")
        self.page.locator("#fromAccountId").select_option(str(from_account_id))
        self.page.locator("#toAccountId").select_option(str(to_account_id))
        self.page.get_by_role("button", name="Transfer").click()
        bank_id_origen = self.page.locator("#fromAccountId").input_value()
        bank_id_destino = self.page.locator("#toAccountId").input_value()
        return bank_id_origen, bank_id_destino