import asyncio
import random
from pyppeteer.launcher import launch

webdriver_js = '''() =>{
           Object.defineProperties(navigator,{
             webdriver:{
               get: () => false
             }
           })
        }
'''


def input_random():
    return random.randint(100, 150)


async def dayu_login(username, password):
    browser = await launch(headless=True)
    pages = await browser.pages()
    page = pages[0]
    await page.setUserAgent(
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36")
    await page.evaluate(webdriver_js)
    await page.goto("https://mp.dayu.com/")
    await page.evaluate(webdriver_js)  # webdriver特征值修改
    iframe = page.frames[1]
    await iframe.evaluate(webdriver_js)  # 可能原因是iframe外执行的修改浏览器特征无法应用到iframe内
    await iframe.type("#login_name", username, {"delay": input_random()})
    await iframe.type("#password", password, {"delay": input_random()})
    await iframe.hover("#nc_1_n1z")
    await page.mouse.down()
    await page.mouse.move(2000, 0, {'delay': input_random(), "steps": 20})
    await page.mouse.up()
    await iframe.click("#submit_btn")
    await page.waitForXPath("/html/body/header/div[3]/div[2]/img")  # 页面加载成功的xpath
    cookies = await page.cookies()
    return cookies


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(dayu_login("3335674227@qq.com", "zhonghuilv2016"))
    print(result)
