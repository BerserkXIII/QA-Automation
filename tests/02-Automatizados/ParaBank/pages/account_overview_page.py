

import constants

class AccountOverviewPage:
    def __init__(self, page):
        self.page = page

    def ir_a_account_overview(self):
        self.page.goto(constants.ACCOUNT_OVERVIEW_URL)

    def localizar_cuenta(self, bank_id):
        return self.page.locator("#accountTable").get_by_role("link", name=str(bank_id), exact=True)

    def obtener_id_cuentas(self):
        self.page.locator("#accountTable").wait_for(state="visible")
        bankID = []
        rows = self.page.locator("#accountTable tbody tr")
        for i in range(rows.count()):
            row = rows.nth(i)
            id_text = row.locator("td").first.inner_text()
            bankID.append(int(id_text))
        return bankID

    def obtener_saldos(self):
        filas = self.page.locator("#accountTable tbody tr").filter(has=self.page.get_by_role("link"))
        filas.first.wait_for(state="visible")
        saldos = {}
        for i in range(filas.count()):
            celdas = filas.nth(i).locator("td")
            id_cuenta = int(celdas.first.inner_text())
            texto_saldo = celdas.nth(1).inner_text()
            saldos[id_cuenta] = float(texto_saldo.replace("$", "").replace(",", ""))
        return saldos