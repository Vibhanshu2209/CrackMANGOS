import asyncio
import time


"""
this function can be called without async/await since it uses time.sleep 
"""
def a_function_with_time():
    print("I am time, I dont wait for anyone")
    time.sleep(3)
    print("But I like a beauty sleep")

"""
this function need to be run inside an event loop.

Event loop is the engine that runs and manages asynchronous functions.
asyncio.run creates that event loop inside which async functions can run.
"""

async def a_routine_to_follow():
    print("I also follow a oral hygiene co-routine")
    await asyncio.sleep(1)
    return "Before going to sleep"





# a_function_with_time()
# asyncio.run(a_routine_to_follow())
