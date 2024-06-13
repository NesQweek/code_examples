from nifi_app import zoo_kafka_nifi_compose
from airflow_app import airflow_compose
from web_app import web_compose
from GUI.bin.main import GUI
from PyQt5.QtWidgets import QApplication
import sys

app = QApplication([])

confirm_1 = airflow_compose.main()
confirm_2 = zoo_kafka_nifi_compose.main()
confirm_3 = web_compose.main()

confirm_1 = True
confirm_2 = True
confirm_3 = True

if confirm_1 and confirm_2 and confirm_3:

    window = GUI()
    window.show()
    try:
        sys.exit(app.exec_())
    except SystemExit:
        print('Окно было закрыто')
