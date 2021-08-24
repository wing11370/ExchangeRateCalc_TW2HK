from TodayUnionPayRate_DBver import Flow_DBver
if __name__ == "__main__":

    newflow = Flow_DBver()


    # ======維護使用======
    # newflow.flow_delete_data()
    # newflow.flow_save() #每天執行一次
    # newflow.flow_check_data()

    # ======執行使用======
    newflow.flow_run()