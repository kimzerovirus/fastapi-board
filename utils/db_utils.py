from sqlalchemy import inspect

"""
sqlalchemy의 row 속성을 딕셔너리로 변환한다.
"""
def row_to_dict(row) -> dict:
    return {key: getattr(row, key) for key in row.keys()}