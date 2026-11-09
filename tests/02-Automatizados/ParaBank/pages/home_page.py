


import constants

class HomePage:
    def __init__(self, page):
        self.page = page

    def ir_a_home(self):
        self.page.goto(constants.HOME_URL)

    def ir_a_register(self):
        self.page.get_by_role("link", name="Register").click()

    def ir_a_account_overview(self):
        self.page.get_by_role("link", name="Accounts Overview").click()

    def ir_a_transfer_funds(self):
        self.page.get_by_role("link", name="Transfer Funds").click()
        