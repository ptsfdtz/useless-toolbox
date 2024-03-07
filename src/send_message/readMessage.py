import pandas as pd
def main():
    file_path = 'src/send_message/index.xlsx'

    data = pd.read_excel(file_path)

    result_dict = data.set_index('姓名')['邮箱'].to_dict()

    return result_dict

if __name__ == '__main__':
    main()
