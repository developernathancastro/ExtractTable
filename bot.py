# Import for the Web Bot
from botcity.web import WebBot, Browser, By
from botcity.web.parsers import table_to_dict
from botcity.maestro import *
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
from datetime import datetime
BotMaestroSDK.RAISE_NOT_CONNECTED = False


def main():
    try:
        maestro = BotMaestroSDK.from_sys_args()
        execution = maestro.get_execution()
        print(f"Task ID is: {execution.task_id}")
        print(f"Task Parameters are: {execution.parameters}")

        bot = WebBot()

        bot.headless = False #Automação rodando em segundo plamo

        bot.browser = Browser.CHROME
        bot.driver_path = ChromeDriverManager().install()

        # Opens the BotCity website.
        bot.browse("https://www.w3schools.com/html/html_tables.asp")
        bot.maximize_window()
        elemento_tabela = bot.find_element('customers', By.ID)


        maestro.alert(

            task_id=execution.task_id,
            title='Elemento Coletado',
            message='Elemento adiconado a variável',
            alert_type=AlertType.INFO
        )

        dados_tabela = table_to_dict(elemento_tabela)
        bot.stop_browser()

        df = pd.DataFrame(dados_tabela)
        df.to_csv(r"C:\Users\natha\Processamento de arquivos PDF - BotCity\file\Customers.csv", index=False)

        maestro.alert(

            task_id=execution.task_id,
            title='Arquivo Salvo',
            message='Tabela coletada com sucesso',
            alert_type=AlertType.INFO
        )

        maestro.new_log_entry(
            activity_label='ExtractTable',
            values  =  {
                'robo':  'ExtractTable',
                'data_hora': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        )


        # Uncomment to mark this task as finished on BotMaestro
        maestro.finish_task(
            task_id=execution.task_id,
            status=AutomationTaskFinishStatus.SUCCESS,
            message="Tarefa finalizada com sucesso!"
            )

    except Exception as ex:

        bot.save_screenshot('erro.png')

        tags = {"RPA": "html_table"}

        maestro.error(
            task_id=execution.task_id,
            exception=ex,
            screenshot='erro.png',
            tags=tags
        )


def not_found(label):
    print(f"Element not found: {label}")

if __name__ == '__main__':
    main()


