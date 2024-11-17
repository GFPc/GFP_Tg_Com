import datetime
import json
import logging
import asyncio
from typing import Dict, Optional

from colorama import Fore, init
from telethon import TelegramClient, events
from pydantic import BaseModel, ValidationError
import config
import aiohttp
init(autoreset=True)

logging.basicConfig(level=logging.INFO)

API_ID = config.API_ID
API_HASH = config.API_HASH
SESSION_NAME = config.SESSION_NAME
PHONE_NUMBER = config.PHONE_NUMBER
SOURCES = config.SOURCES

DRIVER_USER_ID = 574

client = TelegramClient(SESSION_NAME, API_ID, API_HASH,device_model="Telegram Desktop", lang_code="ru",system_version="4.16.30-vxCUSTOM3",app_version="4.16.30")

url_prefix = "https://ibronevik.ru/taxi/c/gruzvill/api/v1/"
car_classes = {
        "1": {
          "ru": "Эконом",
          "en": "Economy",
          "ar": None,
          "fr": None,
          "about_ru": "",
          "about_en": "",
          "about_ar": "",
          "about_fr": "",
          "seats": "4",
          "luggage": "3",
          "photo": "",
          "courier_call_rate": "10.0000",
          "courier_fare_per_1_km": "2.5000",
          "booking_location_classes": None
        },
        "2": {
          "ru": "Комфорт",
          "en": "Comfort",
          "ar": None,
          "fr": None,
          "about_ru": "",
          "about_en": "",
          "about_ar": "",
          "about_fr": "",
          "seats": "4",
          "luggage": "3",
          "photo": "",
          "courier_call_rate": "20.0000",
          "courier_fare_per_1_km": "3.0000",
          "booking_location_classes": [
            "3"
          ]
        },
        "3": {
          "ru": "Бизнес",
          "en": "Business",
          "ar": None,
          "fr": None,
          "about_ru": "",
          "about_en": "",
          "about_ar": "",
          "about_fr": "",
          "seats": "10",
          "luggage": "3",
          "photo": "",
          "courier_call_rate": "40.0000",
          "courier_fare_per_1_km": "3.5000",
          "booking_location_classes": None
        },
        "9": {
          "ru": "Стандарт",
          "en": "Standart",
          "ar": None,
          "fr": None,
          "about_ru": "",
          "about_en": "",
          "about_ar": "",
          "about_fr": "",
          "seats": "0",
          "luggage": "0",
          "photo": "",
          "courier_call_rate": "0.0000",
          "courier_fare_per_1_km": "0.0000",
          "booking_location_classes": None
        },
        "10": {
          "ru": "Микровэн",
          "en": "Microvan",
          "ar": None,
          "fr": None,
          "about_ru": "",
          "about_en": "",
          "about_ar": "",
          "about_fr": "",
          "seats": "0",
          "luggage": "0",
          "photo": "",
          "courier_call_rate": "0.0000",
          "courier_fare_per_1_km": "0.0000",
          "booking_location_classes": None
        },
        "11": {
          "ru": "Минивэн",
          "en": "Minivan",
          "ar": None,
          "fr": None,
          "about_ru": "",
          "about_en": "",
          "about_ar": "",
          "about_fr": "",
          "seats": "0",
          "luggage": "0",
          "photo": "",
          "courier_call_rate": "0.0000",
          "courier_fare_per_1_km": "0.0000",
          "booking_location_classes": None
        },
        "12": {
          "ru": "Комфорт+ / D класс",
          "en": "Comfort+ / D class",
          "ar": None,
          "fr": None,
          "about_ru": "",
          "about_en": "",
          "about_ar": "",
          "about_fr": "",
          "seats": "0",
          "luggage": "0",
          "photo": "",
          "courier_call_rate": "0.0000",
          "courier_fare_per_1_km": "0.0000",
          "booking_location_classes": None
        },
        "13": {
          "ru": "Бизнес / E класс",
          "en": "Business / E class",
          "ar": None,
          "fr": None,
          "about_ru": "",
          "about_en": "",
          "about_ar": "",
          "about_fr": "",
          "seats": "0",
          "luggage": "0",
          "photo": "",
          "courier_call_rate": "0.0000",
          "courier_fare_per_1_km": "0.0000",
          "booking_location_classes": None
        },
        "14": {
          "ru": "Бизнес минивэн / V класс",
          "en": "Business minivan / V class",
          "ar": None,
          "fr": None,
          "about_ru": "",
          "about_en": "",
          "about_ar": "",
          "about_fr": "",
          "seats": "0",
          "luggage": "0",
          "photo": "",
          "courier_call_rate": "0.0000",
          "courier_fare_per_1_km": "0.0000",
          "booking_location_classes": None
        },
        "15": {
          "ru": "Бизнес+ / S класс",
          "en": "Business+ / S class",
          "ar": None,
          "fr": None,
          "about_ru": "",
          "about_en": "",
          "about_ar": "",
          "about_fr": "",
          "seats": "0",
          "luggage": "0",
          "photo": "",
          "courier_call_rate": "0.0000",
          "courier_fare_per_1_km": "0.0000",
          "booking_location_classes": None
        },
        "16": {
          "ru": "Микроавтобус",
          "en": "Microbus",
          "ar": None,
          "fr": None,
          "about_ru": "",
          "about_en": "",
          "about_ar": "",
          "about_fr": "",
          "seats": "0",
          "luggage": "0",
          "photo": "",
          "courier_call_rate": "0.0000",
          "courier_fare_per_1_km": "0.0000",
          "booking_location_classes": None
        },
        "17": {
          "ru": "Автобус",
          "en": "Bus",
          "ar": None,
          "fr": None,
          "about_ru": "",
          "about_en": "",
          "about_ar": "",
          "about_fr": "",
          "seats": "0",
          "luggage": "0",
          "photo": "",
          "courier_call_rate": "0.0000",
          "courier_fare_per_1_km": "0.0000",
          "booking_location_classes": None
        },
        "18": {
          "ru": "Эвакуатор / Манипулятор",
          "en": "Evacuator / Manipulator",
          "ar": None,
          "fr": None,
          "about_ru": "",
          "about_en": "",
          "about_ar": "",
          "about_fr": "",
          "seats": "0",
          "luggage": "0",
          "photo": "",
          "courier_call_rate": "0.0000",
          "courier_fare_per_1_km": "0.0000",
          "booking_location_classes": None
        }
      
}

async def register_user():
    data = {
        "u_name": "admin_tg_com",
        "u_role": "2",
        "u_email": "admin_tg_com@ibronevik.ru",
        "data":{
            "password": "p@ssw0rd",
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url_prefix + "register", data=data) as response:
            if response.status != 200:
                logging.error(f"Failed to register user: {response.status} {await response.text()}")
                return None
            response_data = await response.json()
            print(json.dumps(response_data, indent=4, ensure_ascii=False))
            token = response_data["token"]
            u_hash = response_data["u_hash"]
            return token, u_hash

async def get_admin_credentials():
    login = "admin@ibronevik.ru"
    password = "p@ssw0rd"
    auth_type = "e-mail"

    # check auth file exists
    try:
        with open("api_auth.txt", "r") as f:
            auth_hash = f.readline().strip()
    except FileNotFoundError:
        f = open("api_auth.txt", "w")
        f.close()

    f = open("api_auth.txt", "r")
    data = f.read().split("\n")
    if len(data)==2:
        return [data[0], data[1]]
    f.close()

    auth_hash = ""
    token = ""
    u_hash = ""
    async with aiohttp.ClientSession() as session:
        async with session.post(url_prefix + "auth", data={"login": login, "password": password, "type": auth_type}) as response:
            if response.status != 200:
                logging.error(f"Failed to get admin credentials: {response.status} {await response.text()}")
                return None
            response_data = await response.json()
            auth_hash = response_data["auth_hash"]
        async with session.post(url_prefix + "token", data={"auth_hash": auth_hash}) as response:
            if response.status != 200:
                logging.error(f"Failed to get admin token: {response.status} {await response.text()}")
                return None
            response_data = await response.json()
            token = response_data["data"]["token"]
            u_hash = response_data["data"]["u_hash"]

    f = open("api_auth.txt", "w")
    f.write(f"{token}\n{u_hash}")
    f.close()
    return [token, u_hash]

class Order(BaseModel):
    date: str
    time: str
    start_location: str = "Точка А"
    end_location: str = "Точка Б"
    vehicle_type: str = "Неизвестно"
    price: int = 0
    passengers: int = 0
    order_number: int = 0


original_message_cache: Dict[int, int] = {}


async def send_api_request(endpoint: str, method: str = "GET", params: dict = None) -> dict:
    admin_credentials = await get_admin_credentials()
    params["token"] = admin_credentials[0]
    params["u_hash"] = admin_credentials[1]
    #print(json.dumps(params, indent=4, ensure_ascii=False))
    async with aiohttp.ClientSession() as session:
        if method == "POST":
            async with session.post(url_prefix + endpoint, data=params) as response:
                if response.status != 200:
                    logging.error(f"Failed to post data: {response.status} {await response.text()}")
                    return {}
                response_data = await response.json()
                return response_data
        else:
            async with session.get(url_prefix + endpoint, params=params) as response:
                if response.status != 200:
                    logging.error(f"Failed to fetch data: {response.status} {await response.text()}")
                    return {}
                response_data = await response.json()
                return response_data


async def process_message(message: str, event) -> Optional[Order]:
    try:
        lines = message.split('\n')
        date_time = lines[0].split()
        for i in date_time:
            if i.lower() in "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя":
                return None
        locations = lines[1].split(' - ') if len(lines) > 1 else ["Точка А", "Точка Б"]
        vehicle_info = lines[2].split() if len(lines) > 2 else ["Неизвестно", "0₽", "", "0", "", "№: 0"]

        order = Order(
            date=date_time[0].replace("🔥", ""),
            time=date_time[1],
            start_location=locations[0],
            end_location=locations[1],
            vehicle_type=vehicle_info[0],
            price=int(vehicle_info[1].replace('₽', '')),
            passengers=int(vehicle_info[3]),
            order_number=int(vehicle_info[5].replace('№: ', ''))
        )

        original_message_cache[event.message.id] = event.message.id

        return order
    except (IndexError, ValueError, ValidationError) as e:
        logging.error(f"Error processing message: {e}")
        return None


async def send_order_request(order: Order):
    order_date = datetime.datetime.strptime(order.date.replace("🔥", ""), "%d.%m.%Y").strftime("%Y-%m-%d")
    order_time = datetime.datetime.strptime(order.time, "%H:%M").strftime("%H:%M:%S")
    order_timezone = "+03:00"

    car_class_id = "-1"
    for i in car_classes:
        if car_classes[i]["ru"] == order.vehicle_type:
            car_class_id = i
            break

    data = {
        "b_start_address": order.start_location,
        "b_destination_address": order.end_location,
        "b_start_datetime": f"{order_date} {order_time}{order_timezone}",
        "b_passengers_count": order.passengers,
        "b_car_class": car_class_id,
        "b_options": {
            "customer_price": order.price
        },
        "b_payment_way": "1",
        "b_max_waiting": 7200,
    }
    data = {
        "data": json.dumps(data, ensure_ascii=False),
    }

    response_data = await send_api_request("drive", method="POST", params=data)
    b_id = response_data["data"]["b_id"]
    if b_id:
        logging.info(f"Created order with b_id: {b_id}")
    else:
        logging.error("Failed to create order.")


async def accept_order(event):
    for original_message_id in original_message_cache:
        original_message = await client.get_messages(event.chat_id, ids=original_message_id)
        print(original_message)
        try:
            #await original_message.click(0)
            logging.info("Clicked 'Взять заказ'.")
        except Exception as e:
            logging.error(f"Error clicking 'Взять заказ': {e}")
        break


@client.on(events.NewMessage(from_users=SOURCES))
async def new_message_from_sources(event):
    print(event,event.reply_markup)
    if event.reply_markup:
        try:
            #await event.message.click(0)
            logging.info("Clicked '✅Да, взять заказ'.")
        except Exception as e:
            logging.error(f"Error clicking '✅Да, взять заказ': {e}")
    return


async def compare_offers_with_active_orders(response_data: dict, incoming_offer: Order) -> Optional[str]:
    print("POINT-0: Scanning order state || booking_positions_len=", len(response_data.get("data", {}).get("booking", {})))
    for booking_id, booking_data in response_data.get("data", {}).get("booking", {}).items():
        active_offer = Order(
            date=booking_data.get("b_start_datetime", "").split()[0] if "b_start_datetime" in booking_data else "",
            time=booking_data.get("b_start_datetime", "").split()[1] if "b_start_datetime" in booking_data else "",
            start_location=booking_data.get("b_start_address", "Точка А"),
            end_location=booking_data.get("b_destination_address", "Точка Б"),
            vehicle_type="Неизвестно" if not booking_data.get("b_car_class", "Неизвестно") else booking_data.get("b_car_class", "Неизвестно"),
            price=int(0 if not booking_data["b_options"] else booking_data["b_options"]["customer_price"]),
            passengers=int(booking_data.get("b_passengers_count", 0)),
            order_number=int(booking_id)
        )
        #print(Fore.LIGHTYELLOW_EX + f"POINT-2: Active offer Example: {active_offer}" + Fore.RESET,end="\n")
        #print(incoming_offer.date, ".".join([str(active_offer.date.split("-")[len(active_offer.date.split("-"))-1-i]) for i in range(len(active_offer.date.split("-")))]))
        #print(incoming_offer.time, active_offer.time[0:5])
        #print(incoming_offer.start_location, active_offer.start_location)
        #print(incoming_offer.end_location, active_offer.end_location)
        #print(incoming_offer.vehicle_type, active_offer.vehicle_type)
        #print(incoming_offer.price, active_offer.price)
        #print(incoming_offer.passengers, active_offer.passengers)
        #print(incoming_offer.order_number, active_offer.order_number)
        car_class_id = "-1"
        for i in car_classes:
            if car_classes[i]["ru"] == incoming_offer.vehicle_type:
                car_class_id = i
                break

        cond = (
            incoming_offer.date == ".".join([str(active_offer.date.split("-")[len(active_offer.date.split("-"))-1-i]) for i in range(len(active_offer.date.split("-")))])
            and incoming_offer.time == active_offer.time[0:5]
            and incoming_offer.start_location == active_offer.start_location
            and incoming_offer.end_location == active_offer.end_location
            and car_class_id == active_offer.vehicle_type
            and incoming_offer.price == active_offer.price
            and incoming_offer.passengers == active_offer.passengers
            #and incoming_offer.order_number == active_offer.order_number
        )
        if cond:
            return booking_id
    return None


async def handle_order(order: Order, event):
    endpoint = "drive"
    admin_credentials = await get_admin_credentials()
    params = {
        "token": admin_credentials[0],
        "u_hash": admin_credentials[1],
        "u_a_role": "1",
        "fields": "000000002"
    }

    response_data = await send_api_request(endpoint=endpoint, method="POST", params=params)

    order_id = await compare_offers_with_active_orders(response_data, order)

    if order_id is None:
        print(Fore.RED + "POINT-1: Order ID not found in active trips." + Fore.RESET)
        #logging.error("Order ID not found in active trips.")
        return
    print(Fore.GREEN + f"POINT-1: Found order ID: {order_id}" + Fore.RESET)

    booking_data = response_data["data"]["booking"].get(order_id)

    if booking_data and booking_data.get("b_offers"):
        print(Fore.LIGHTGREEN_EX + f"POINT-2: Found offers: {booking_data['b_offers']}" + Fore.RESET)
        logging.info(f"Driver accepted the order. Offers: {booking_data['b_offers']}")
        print("ACCEPTING IN TG",event)
        await accept_order(event=event)
        return True
    else:
        logging.info("No driver has accepted the order yet. Continuing to monitor...")


async def check_order_acceptance(order: Order,event):
    start_time = asyncio.get_event_loop().time()
    while (asyncio.get_event_loop().time() - start_time) < 300:  # 300 секунд = 5 минут
        flag = await handle_order(order,event)
        if flag:
            break
        await asyncio.sleep(5)  # ждать 5 секунд между проверками


@client.on(events.NewMessage(chats=SOURCES))
async def new_message_handler(event):
    message_text = event.raw_text
    print(f"New message: {message_text}")

    order = await process_message(message_text, event)
    if order:
        await send_order_request(order)
        asyncio.create_task(check_order_acceptance(order,event))


async def main():
    await client.connect()
    if not await client.is_user_authorized():
        await client.send_code_request(PHONE_NUMBER)
        try:
            phone_hash = await client.send_code_request(PHONE_NUMBER)
        except:
            phone_hash = await client.send_code_request(PHONE_NUMBER)
        phone_hash = phone_hash.phone_code_hash
        print(phone_hash)
        await client.sign_in(PHONE_NUMBER, input('GFP | Enter code: '), phone_code_hash=phone_hash)
    print('GFP | Signed in')
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())