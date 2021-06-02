import os
import pickle
import sys
import time
from datetime import datetime

from colorama import Fore, init
from flasher import Login, ShopeeBot, AvailablePaymentChannels, error
from flasher.types import Payment
import colorlog


init()
INFO = colorlog.ColorLog(Fore.LIGHTBLUE_EX + "[*]" + Fore.BLUE)
INPUT = colorlog.ColorLog(Fore.LIGHTGREEN_EX + "[?] " + Fore.GREEN)
ERROR = colorlog.ColorLog(Fore.LIGHTRED_EX + "[!]" + Fore.RED)
WARNING = colorlog.ColorLog(Fore.LIGHTYELLOW_EX + "[!]" + Fore.YELLOW)
SUCCESS = colorlog.ColorLog(Fore.LIGHTGREEN_EX + "[+]" + Fore.GREEN)


def int_input(prompt_: str, max_: int = -1, min_: int = 1) -> int:
    input_: str

    while True:
        input_ = input(f"{INPUT} {prompt_}{Fore.RESET}")

        if input_.isdigit():
            input_int = int(input_)

            if min_ <= input_int <= max_ or (min_ <= input_int and max_ == -1):
                return input_int
            elif input_int > max_ != -1:
                ERROR << "Angka terlalu banyak!"
            elif input_int < min_:
                ERROR << "Angka terlalu sedikit!"
        else:
            ERROR << "Masukkan angka!"


def clear():
    os.system("cls" if os.name == "nt" else "clear")


def line():
    print("-" * 32)


def printerror(e: Exception):
    ERROR << f"{type(e).__name__}: {e}"


def do_login():
    INFO << "Masukkan Username/Email/Telepon"
    user = input(INPUT + "User: " + Fore.RESET)
    INFO << "Masukkan Password"
    password = input(INPUT + "Password: " + Fore.RESET)
    INFO << "Sedang Login..."

    login, success = None, None

    try:
        login, success = Login.init(user, password)
    except error.LoginError as e:
        printerror(e)

    if success:
        with open("cookie", 'wb') as f:
            pickle.dump(login.session.cookies, f)
            SUCCESS << "Login sukses"
        exit(0)

    INFO << "Pilih Metode Verifikasi"
    print(Fore.GREEN + "[1]", Fore.BLUE + "WhatsApp")
    print(Fore.GREEN + "[2]", Fore.BLUE + "SMS")
    print(Fore.GREEN + "[3]", Fore.BLUE + "Telepon")
    print()
    verification_channel = int_input("Input: ", 3, 1)

    cookie = None

    try:
        cookie = login.send_otp({
            1: Login.OTPChannel.WHATSAPP,
            2: Login.OTPChannel.SMS,
            3: Login.OTPChannel.CALL
        }[verification_channel]).verify(input(INPUT + "Masukkan Kode Verifikasi: " + Fore.RESET))
    except error.LoginError as e:
        printerror(e)

    with open("cookie", 'wb') as f:
        pickle.dump(cookie, f)
        SUCCESS << "Login sukses"


def main():
    INFO << "Mengambil Informasi User..."

    with open("cookie", 'rb') as f:
        try:
            bot = ShopeeBot(pickle.load(f))
        except error.LoginError as e:
            printerror(e)
            exit(1)

    INFO << f"Welcome {Fore.GREEN}{bot.user.username}"
    print()

    INFO << "Masukkan Url Barang"
    item = None

    while True:
        try:
            url = input(INPUT + "Url: " + Fore.RESET)
            item = bot.fetch_item_from_url(url)
            break
        except (error.ItemNotFoundError, ValueError) as e:
            printerror(e)

    line()
    print(Fore.LIGHTBLUE_EX, "Nama:", Fore.GREEN, item.name)
    print(Fore.LIGHTBLUE_EX, "Harga:", Fore.GREEN, item.price // 99999)
    print(Fore.LIGHTBLUE_EX, "Brand:", Fore.GREEN, item.brand)
    print(Fore.LIGHTBLUE_EX, "Stok:", Fore.GREEN, item.stock)
    print(Fore.LIGHTBLUE_EX, "Lokasi Toko:", Fore.GREEN, item.shop_location)
    line()
    print()

    selected_model = 0

    if len(item.models) > 1:
        INFO << "Pilih Model/Variasi"
        line()

        for index, model in enumerate(item.models):
            print(Fore.GREEN + '[' + str(index + 1) + ']' + Fore.BLUE, model.name)
            print('\t', Fore.LIGHTBLUE_EX, "Harga:", Fore.GREEN, model.price // 99999)
            print('\t', Fore.LIGHTBLUE_EX, "Stok:", Fore.GREEN, model.stock)
            print('\t', Fore.LIGHTBLUE_EX, "ID Model:", Fore.GREEN, model.model_id)
            line()

        print()
        selected_model = int_input("Pilihan: ", len(item.models))-1
        print()

    INFO << "Pilih Metode Pembayaran"

    for index, channel in enumerate(AvailablePaymentChannels.lists):
        print(f"{Fore.GREEN}[{index+1}] {Fore.BLUE}{channel.name}")

    print()
    selected_payment_channel = AvailablePaymentChannels.lists[int_input("Pilihan: ",
                                                                        len(AvailablePaymentChannels.lists))-1]
    print()
    selected_option_info = None

    if selected_payment_channel.has_option():
        for index, option in enumerate(selected_payment_channel.option_keys()):
            print(f"{Fore.GREEN}[{index+1}] {Fore.BLUE}{option}")

        print()
        selected_option_info = int_input("Pilihan: ", len(selected_payment_channel.options))-1

    if not item.flash_sale:
        if item.upcoming_flash_sale is not None:
            flash_sale_start = datetime.fromtimestamp(item.upcoming_flash_sale.start_time)
            INFO << f"Waktu Flash Sale: {flash_sale_start.strftime('%H:%M:%S')}"
            print(INFO, "Menunggu Flash Sale...\r", end="")
            time.sleep((datetime.fromtimestamp(item.upcoming_flash_sale.start_time) - datetime.now())
                       .total_seconds() - 2)
            INFO << "Bersiap siap...         "

            while not item.flash_sale:
                item = bot.fetch_item(item.item_id, item.shop_id)
        else:
            ERROR << "Flash Sale telah lewat"
            exit(0)

    try:
        INFO << "Flash Sale telah tiba"
        start = datetime.now()
        INFO << "Menambah item ke Cart..."
        cart_item = bot.add_to_cart(item, selected_model)
        INFO << "Checkout..."
        bot.checkout(cart_item, Payment.from_channel(selected_payment_channel, selected_option_info))
        end = datetime.now() - start
        INFO << f"Item berhasil dibeli dalam waktu {Fore.YELLOW}{end.seconds} detik {end.microseconds // 1000}" \
                " milidetik"
        SUCCESS << "Proses selesai"
    except error.CheckoutError as e:
        printerror(e)


if __name__ == "__main__":
    clear()

    if len(sys.argv) > 1 and sys.argv[1] == "login":
        do_login()
        exit(0)

    main()
