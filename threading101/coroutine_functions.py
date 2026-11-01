import asyncio
from asyncio_example import a_routine_to_follow



async def main():

    print("Calling the a_routine_to_follow without pausing")
    await a_routine_to_follow()


    coroutine_obj = a_routine_to_follow()
    print("Pausing the a_routine_to_follow")
    await asyncio.sleep(2)

    await coroutine_obj

    print("Finished the a_routine_to_follow")


asyncio.run(main())