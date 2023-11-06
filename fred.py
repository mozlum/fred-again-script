import requests, random, threading, time
from discord_webhook import DiscordWebhook, DiscordEmbed

def run(proxy):
    while True:
        try:
            headers = {
                'authority': 'events.humanitix.com',
                'accept': 'application/json, text/plain, */*',
                'accept-language': 'en-US,en-GB;q=0.9,en;q=0.8',
                'cache-control': 'no-cache',
                'content-type': 'application/json;charset=UTF-8',
                'newrelic': 'eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMyMDI0ODUiLCJhcCI6IjEwOTkxMzM1NzAiLCJpZCI6IjcxZDA4MjQ5NjFmOTQwYzciLCJ0ciI6IjNiZDRkZjRiYTJjODI3OGI1MWRkODM3NWI4MjJlMjEwIiwidGkiOjE2NzUzODAxMzg2MTF9fQ==',
                'origin': 'https://events.humanitix.com',
                'pragma': 'no-cache',
                'referer': 'https://events.humanitix.com/fred-again-friday/tickets',
                'sec-ch-ua': '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"macOS"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'traceparent': '00-3bd4df4ba2c8278b51dd8375b822e210-71d0824961f940c7-01',
                'tracestate': '3202485@nr=0-1-3202485-1099133570-71d0824961f940c7----1675380138611',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
                'x-event-level-location': 'AU',
                'x-user-level-location': 'AU',
            }

            tickets = random.choice([
                [
                    {
                        'type': 'fixed',
                        'ticketTypeId': '63d86789c94c453f99f84802',
                    },
                ],
                [
                    {
                        'type': 'fixed',
                        'ticketTypeId': '63d86789c94c453f99f84802',
                    },
                    {
                        'type': 'fixed',
                        'ticketTypeId': '63d86789c94c453f99f84802',
                    },
                ]
            ])

            json_data = {
                'eventId': '63d86789c94c453f99f847f0',
                'eventDateId': '63d86789c94c453f99f847f8',
                'requestedTickets': tickets,
                'requestedPackageTickets': [],
                'clientDonation': 0,
                'lastOrderId': None,
            }
            print("\u001b[44m:: CREATING CHECKOUT\033[0;0m")
            response = requests.put('https://events.humanitix.com/api/order/request', headers=headers, json=json_data, proxies=proxy)
            if response.json()['success']:
                print("\u001b[42m:: CHECKOUT SUCCESS\033[0;0m")
                checkoutID = response.json()['order']['_id']
                link = f"https://events.humanitix.com/fred-again-friday/details/{checkoutID}"
                #SEND WEBHOOK WITH CHECKOUT LINK
                webhook = DiscordWebhook(url='DISCORD WEBHOOK URL')
                embed = DiscordEmbed(title='Fred Again Friday', description='Checkout Link', color=242424)
                embed.set_thumbnail(url='https://cdn.filestackcontent.com/compress/output=format:webp/cache=expiry:max/resize=width:780/5VAJ0vZvQeK1gGzmsMez')
                embed.add_embed_field(name='Link', value=link)
                embed.add_embed_field(name="Quantity", value=len(tickets))
                webhook.add_embed(embed)
                webhook.execute()
                with open("LINKS.txt", "a") as s:
                    s.write(link + "\n")
                    s.close()
            else:
                print("\u001b[41m:: CHECKOUT FAILED\033[0;0m")
            time.sleep(1)
        except Exception:
            print("\u001b[41m:: CHECKOUT FAILED\033[0;0m")
            time.sleep(1)
            continue

proxies = []
with open("test_proxies.txt", "r") as f:
    ps = f.read().splitlines()
    for proxy in ps:
        proxy = proxy.split(":")
        proxies.append(
            {
                "http":
                f"http://{proxy[2]}:{proxy[3]}@{proxy[0]}:{proxy[1]}"
                }
            )
for i in range(25):
    proxy = random.choice(proxies)
    threading.Thread(target=run, args=(proxy,)).start()