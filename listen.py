from telethon.sync import TelegramClient, events
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Load Telegram API credentials from environment variables
api_id_telegram = os.getenv('API_ID_TELEGRAM')
api_hash_telegram = os.getenv('API_HASH_TELEGRAM')
phone_number = os.getenv('PHONE_NUMBER')
group_id_telegram = os.getenv('GROUP_ID_TELEGRAM')

# Create a Telegram client
client = TelegramClient(phone_number, api_id_telegram, api_hash_telegram)

# Define the TradeSignal class
class TradeSignal:
    def __init__(self, crypto_sign, position):
        self.crypto_sign = crypto_sign
        self.position = position

# Main asynchronous function
async def main():
    await client.start(phone_number)
    group_entity = await client.get_entity(int(group_id_telegram))

    @client.on(events.NewMessage(chats=group_entity))
    async def handle_new_message(event):
        if "🔰" in event.message.text and "📛" in event.message.text and "🎯" in event.message.text:
            lines = event.message.text.split('\n')
            crypto_sign_line = next((line.strip() for line in lines if line and not line.startswith('🔰')), None)

            start_index = 1
            for i, char in enumerate(crypto_sign_line[start_index:], start=start_index):
                if not char.isalnum():
                    end_index = i
                    break
            else:
                end_index = None

            crypto_sign = crypto_sign_line[start_index:end_index].strip()
            position = "LONG" if "LONG" in lines[0] else "SHORT" if "SHORT" in lines[0] else None

            bitget_symbol = f"{crypto_sign}USDT"

            trade_signal = TradeSignal(crypto_sign, position)

            print("New trade signal detected:")
            print(f"Crypto: {trade_signal.crypto_sign}")
            print(f"Position: {trade_signal.position}")
            print(f"Bitget Symbol: {bitget_symbol}")

        else:
            print("New standard message detected:")
            print(event.message.text)

    await client.run_until_disconnected()

if __name__ == '__main__':
    client.loop.run_until_complete(main())
