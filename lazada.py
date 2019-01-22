from bs4 import BeautifulSoup
from sql_connection import ConnectionManager
# from notification import notify
from send_email import send_email
import requests
import datetime
import re
import time

# TODO:
# 1. Integrate current function with sqlite3 functionality
# 2. Front end page for users
# 3. Different website functionality, other than lazada

def obtain_pricing(html):
    """
    This function updates the csv file "monitor_pricing.txt" if the online value of a product
    is cheaper than the recorded value, or if there is a new discount coupon.

    This script runs automatically on the Windows Task Scheduler
    Changes will be shown on the CLI on laptop startup

    :param str html: The lazada html of a specific item
    :return: This function does not return anything
    :rtype: None
    """
    with open("monitor_pricing.txt") as f:
        # the latest values will always be the last line in the file
        current_values = f.readlines()[-1].strip().split(",")
        recorded_price = current_values[1]
        current_coupon = current_values[-1]

    html_page = requests.get(html)
    data = html_page.text
    soup = BeautifulSoup(data, "html.parser")

    price_tag = soup.find("span", class_=" pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl")
    discount_rate_tag = soup.find("span", class_="pdp-product-price__discount")

    if price_tag is None or discount_rate_tag is None:
        raise ValueError("The HTML tags could be broken")

    latest_price = price_tag.text
    latest_disc_rate = discount_rate_tag.text

    coupon = soup.find("span", class_="tag-name")
    latest_coupon = "nil"

    if coupon is not None:
        regex_search = re.search(r"SGD\d+.\d{2}|SGD\d+", coupon.text)
        latest_coupon = regex_search.group(0)

    # remove the SGD from the prices and convert to float for comparison
    if float(latest_price[3:]) < float(recorded_price[3:]) or latest_coupon != current_coupon:
        # date/time from POSIX timestamp
        date = datetime.datetime.now().strftime("%d%m%y %H%M%p")

        with open(r"C:\Users\Lee\Desktop\python_projects\lazada_pricing\monitor_pricing.txt", "a") as f:
            write_string = ",".join([date, latest_price, latest_disc_rate, latest_coupon])
            f.write(write_string + "\n")

        send_email("New Price: {} | Coupon: {}".format(latest_price, latest_coupon))

        # notification is unnecessary since output can be shown on command line
        # code kept for academic purposes
        # notify("New Price: {} | Coupon: {}".format(latest_price, latest_coupon))


jaybird_html = "https://www.lazada.sg/products/jaybird-x3-wireless-in-ear-" \
               "headphones-blackout-i123853561-s137543873.html?spm=a2o42.searchlist.list.19.30745c60CD5bnP&search=1"

if __name__ == "__main__":
    try:
        obtain_pricing(jaybird_html)

    except Exception as e:
        # catch any other errors that might occur for debugging
        print(e)
