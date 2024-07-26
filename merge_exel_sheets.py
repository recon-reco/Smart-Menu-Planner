def merge_excel_sheets(file_path):
    # 엑셀 파일의 모든 시트 이름 가져오기
    xls = pd.ExcelFile(file_path)
    sheet_names = xls.sheet_names
    
    # 모든 시트를 읽어서 하나의 데이터 프레임으로 합치기
    df_list = []
    for sheet in sheet_names:
        df = pd.read_excel(file_path, sheet_name=sheet)
        df_list.append(df)
    
    # 데이터 프레임 리스트를 하나로 합치기
    combined_df = pd.concat(df_list, ignore_index=True)
    
    return combined_df

# 엑셀 파일 경로
file_path = 'path_to_your_excel_file.xlsx'

# 함수 호출
combined_df = merge_excel_sheets(file_path)

# 결과 확인
combined_df.head()
