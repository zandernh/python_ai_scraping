from langchain_openai import ChatOpenAI
from browser_use import Agent, Browser, BrowserConfig, Controller
from dotenv import load_dotenv
import asyncio
from pydantic import BaseModel
from typing import List

load_dotenv()

class Post(BaseModel):
    caption: str
    url: str

class Posts(BaseModel):
    posts: List[Post]


controller = Controller(output_model=Posts)

# Configuring browser

browser = Browser(
    config=BrowserConfig(
        chrome_instance_path="C:\\Program Files (x86)\\BraveSoftware\\Brave-Browser\\Application\\brave.exe"

    )
)

llm = ChatOpenAI(model="gpt-4o")

async def main():

    initial_actions = [
        {'open_tab': {'url': 'https://www.instagram.com/cowboykentrollins/'}},
    ]
    sensitive_data = {'x_name': '', 'x_password': ''}

    agent = Agent(
        task="Open up instagram and navigate to cowboykentrollins's profile. Then look for a reel about making sloppy joes",
        llm=llm,
        browser=browser,
        controller=controller,
        initial_actions=initial_actions,
        sensitive_data=sensitive_data
    )
    result = await agent.run()
    data = result.final_result()
    parsed: Posts = Posts.model_validate_json(data)
    await browser.close()


if __name__ == "__main__":
    asyncio.run(main()) 