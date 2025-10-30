import openai
import httpx
import json
import asyncio
from dotenv import load_dotenv
import os

load_dotenv()

# OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
api_key = os.getenv("OPENWEATHER_API_KEY")

async def get_weather(city: str):
    async with httpx.AsyncClient() as httpx_client:
        res = await httpx_client.get( f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric")
        return res.json()

tools = {
    "getWeather": get_weather
}

async def main():
    completion = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "What's the weather in Accra?"}],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "getWeather",
                    "description": "Get current weather by city name",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "string"}
                        }
                    }
                }
            }
        ]
    )
    if completion.choices[0].message.tool_calls:
        tool_call = completion.choices[0].message.tool_calls[0]
        tool_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        result = await tools[tool_name](**args)

        final = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "is it going to rain in kasoa today?"},
                completion.choices[0].message,
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": tool_name,
                    "content": json.dumps(result)
                }
            ]
        )

        print(final.choices[0].message.content)

if __name__ == "__main__":
    asyncio.run(main())

