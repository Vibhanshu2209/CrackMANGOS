import asyncio
import time

"""
function to study

asyncio.create_task
Usage: Used to detach execution immediately and run coroutines concurrently in the background (such as fire-and-forget operations in a FastAPI project).

"""

async def a_welcome_email_to_be_sent(message: str, reciever: str):
    print(f"Sending email {message = } to {reciever = }")
    await asyncio.sleep(1)
    print('email sent!')


async def a_popup_notification_to_be_sent(message: str, reciever: str):
    print(f"Sending popup with {message = } to {reciever = }")
    await asyncio.sleep(2)
    print('Notification sent!')
    time.sleep(4)
    print('4 seconds Nap done!')


async def main_for_email_task():
    email_sending_task = asyncio.create_task(a_welcome_email_to_be_sent("hello asyncio task", "python"), name="EMAIL_TASK")
    print("some other tasks")
    await email_sending_task

### BAD IMPLEMENTATION FOR PARALLELISM
async def main_for_email_coroutine():
    email_coroutine = a_welcome_email_to_be_sent("hello email coroutine", "python")
    notification_coroutine = a_popup_notification_to_be_sent("hello popup coroutine", "python")
    """ The above two line only Creates a coroutine object (for each), it does not schedule them on the event loop"""

    print("some routine tasks")
    await email_coroutine
    await notification_coroutine
    """
        The above two lines will be scheduled to be completed (one after the other) and suspend the main event loop
    """



### ACTUAL PARALLELISM
async def main_for_concurrent_routines():
    email_task = asyncio.create_task(a_welcome_email_to_be_sent("parellel email coroutine", "python"), name="EMAIL_TASK")
    popup_task = asyncio.create_task(a_popup_notification_to_be_sent("parallel popup coroutine", "python"), name="POPUP_TASK")

    email_result = await email_task
    print(f"Email task: {email_task.get_name()} completed")
    popup_result = await popup_task
    print(f"Popup task: {popup_task.get_name()} completed")


if __name__ == "__main__":

    # t1 = time.perf_counter()
    # asyncio.run(main_for_email_task())
    # asyncio.run(main_for_email_coroutine())
    # t2 = time.perf_counter()

    # print(f"Time taken: {t2 - t1:.2f} seconds")


    t3 = time.perf_counter()
    asyncio.run(main_for_concurrent_routines())
    t4 = time.perf_counter()
    print(f"Time taken: {t4 - t3:.2f} seconds")




