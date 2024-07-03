from utils.browser_setup import get_edge_driver


def main():
    driver = get_edge_driver()

    try:
        driver.get('https://example.com')

        driver.add_cookie({'name': 'myCookie', 'value': 'cookieValue'})

        cookie = driver.get_cookie('myCookie')
        print(f"Value from Cookie: {cookie['value']}")

        driver.delete_cookie('myCookie')

        cookie_after_deletion = driver.get_cookie('myCookie')
        print(f"Value after deletion: {cookie_after_deletion}")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
