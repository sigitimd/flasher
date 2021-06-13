from flasher import ShopeeBot, Logistic, AvailableLogisticChannels


def configure(bot: ShopeeBot):
    config = bot.checkoutconfig

    # taruh konfigurasi lanjutan disni / put advanced configuration here

    # 0 = Pengiriman setiap saat
    # 1 = Pengiriman pada jam kantor
    config.logistic(Logistic(AvailableLogisticChannels.Reguler, 0))
