from datetime import datetime


class WriteLog(object):

    def __init__(self, file_name):
        self.file_name = file_name
        self.input_text = None
        self.arq = None

    def write(self, input_text):
        self.input_text = input_text
        print(self.input_text)
        try:
            with open("{}.log".format(self.file_name), "a") as self.arq:
                try:
                    self.arq.write(input_text)
                    self.arq.write("\n")

                finally:
                    self.arq.close()
        except IOError:
            print("Erro ao escrever no arquivo de LOG")

    def write_request_date_time(self, text):
        time_obj = datetime.now()
        actual_time = time_obj.strftime("%H:%M:%S")

        date_obj = datetime.today()
        today, month, year = date_obj.day, date_obj.month, date_obj.year

        self.write("{} da requisicao efetuada em {}/{}/{}, às {}".format(text, today, month, year, actual_time))
        print("{} da requisicao efetuada em {}/{}/{}, às {}".format(text, today, month, year, actual_time))
