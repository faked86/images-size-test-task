import asyncio

import aiohttp


keywords = [
    "mediumrectangle",
    "squarepopup",
    "verticalrectangle",
    "largerectangle",
    "rectangle",
    "popunder",
    "fullbanner",
    "halfbanner",
    "microbar",
    "button1",
    "button2",
    "verticalbanner",
    "squarebutton",
    "leaderboard",
    "wideskyscraper",
    "skyscraper",
    "halfpage",
]


async def main():
    async with aiohttp.ClientSession() as session:
        for keyword in keywords:
            async with session.get(f"https://dummyimage.com/{keyword}") as response:
                print("Status:", response.status)
                print("Content-type:", response.headers["content-type"])
                with open(f"images/{keyword}.png", "wb") as f:
                    f.write(await response.read())


if __name__ == "__main__":
    asyncio.run(main())
