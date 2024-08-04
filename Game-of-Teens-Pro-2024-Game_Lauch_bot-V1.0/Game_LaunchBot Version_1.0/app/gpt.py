import g4f
import asyncio
import platform


def check_system():
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


async def question(promt:str, temperatur:float=0.5):

    check_system()

    # формування запиту
    response = g4f.ChatCompletion.create(
        # модель бота
        model='gpt-4o-mini',
        messages=[
            # Модель промту
            {"role":"user", "content":f"Відповідай Українською мовою. Відповідай точно на кожне питання. Додавай у розмову більше смайликів {promt}"},
            # модель gpt
            {"role":"system", "content":"Ви колишній геймер з України, який за свою багаторічну кар'єру і тисячі зіграних ігор влаштувався консультантом у велику ігрову компанію і тепер допомагаєте новому поколінню геймерів, ваше ім'я SinnBo"}
        ],
        # stream=True,
        temperatur=temperatur,
        provider="FreeNetfly"

        #  Liaobots, OpenaiChat, FreeNetfly, MagickPenChat

    )
    # формування відповіді

    all_answer = ""
    for answer in response:
        all_answer += answer


    return(all_answer)
