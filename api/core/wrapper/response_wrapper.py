def api_response(data=None, detail="Success", status_code=200):
    return {
        "status_code": status_code,
        "detail": detail,
        "data": data,
    }